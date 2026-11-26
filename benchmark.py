#!/usr/bin/env python3
"""Read-only Jupiter Perps / SQD Portal historical *accuracy* probe.

No RPC, Dune, Trawl, database writes, or changes to any Lucky Plans repository.
Python >=3.9, standard library only. Does NOT certify full-history coverage by itself.
"""
import argparse
import collections
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import gzip
import hashlib
import http.client
import zlib
import json
import os
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROGRAM = 'PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu'
SQD_URL = 'https://portal.sqd.dev/datasets/solana-mainnet/finalized-stream'
# Community-maintained IDL; fetched once, persisted with digest, not an official guarantee.
IDL_URL = ('https://raw.githubusercontent.com/monakki/jup-perps-client/main/'
           'generator/idl/jupiter-perpetuals.json')
CPI_TAG = bytes.fromhex('e445a52e51cb9a1d')  # Anchor emit_cpi! tag
BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
RETRY_STATS = collections.Counter()  # per-process count of retried SQD stream responses
WIRE_STATS = collections.Counter()   # bytes actually transferred (compressed) vs decoded
ACTION_TYPES = {
    'IncreasePositionEvent': 'INCREASE',
    'InstantIncreasePositionEvent': 'INCREASE',
    'DecreasePositionEvent': 'DECREASE',
    'InstantDecreasePositionEvent': 'DECREASE',
    'LiquidateFullPositionEvent': 'LIQUIDATE',
    'LiquidatePositionEvent': 'LIQUIDATE',
}

def b58_decode(value):
    if not isinstance(value, str):
        raise ValueError('base58 input must be a string')
    n = 0
    for c in value:
        if c not in BASE58:
            raise ValueError('invalid base58 character')
        n = n * 58 + BASE58.index(c)
    return b'\x00' * (len(value) - len(value.lstrip('1'))) + (n.to_bytes((n.bit_length()+7)//8,'big') if n else b'')

def b58_encode(raw):
    n = int.from_bytes(raw, 'big')
    chars = ''
    while n:
        n, r = divmod(n, 58)
        chars = BASE58[r] + chars
    return '1' * (len(raw)-len(raw.lstrip(b'\x00'))) + chars

def pubkey_ok(x):
    if not isinstance(x, str): return False
    try: return len(b58_decode(x)) == 32
    except ValueError: return False

def serializable(obj):
    if isinstance(obj, dict): return {k:serializable(v) for k,v in obj.items()}
    if isinstance(obj, list): return [serializable(v) for v in obj]
    if isinstance(obj, int) and not isinstance(obj, bool): return str(obj)
    return obj

class Reader:
    def __init__(self, raw): self.raw, self.offset = raw, 0
    def take(self, length):
        if length < 0 or self.offset+length > len(self.raw): raise ValueError('truncated Borsh payload')
        out = self.raw[self.offset:self.offset+length]
        self.offset += length
        return out
    def read(self, typ, definitions, depth=0):
        if depth > 30: raise ValueError('Borsh recursive type limit exceeded')
        if isinstance(typ, dict):
            if 'option' in typ or 'coption' in typ:
                target = typ.get('option',typ.get('coption'))
                tag = self.read('u8' if 'option' in typ else 'u32',definitions,depth+1)
                if tag not in (0,1): raise ValueError('invalid option tag')
                return None if tag == 0 else self.read(target,definitions,depth+1)
            if 'vec' in typ:
                length = self.read('u32',definitions,depth+1)
                if length > 100000: raise ValueError('vector length too large')
                return [self.read(typ['vec'],definitions,depth+1) for _ in range(length)]
            if 'array' in typ:
                subtyp,count = typ['array']
                if count > 100000: raise ValueError('array length too large')
                return [self.read(subtyp,definitions,depth+1) for _ in range(count)]
            if 'defined' in typ:
                desc = typ['defined']
                key = desc if isinstance(desc,str) else desc['name']
                return self.read(definitions[key],definitions,depth+1)
            if 'kind' in typ:
                if typ['kind'] == 'struct':
                    fields=typ.get('fields',[])
                    if all(isinstance(f,dict) for f in fields):
                        return {f['name']:self.read(f['type'],definitions,depth+1) for f in fields}
                    return [self.read(f,definitions,depth+1) for f in fields]
                if typ['kind'] == 'enum':
                    idx=self.read('u8',definitions,depth+1)
                    if idx>=len(typ['variants']):raise ValueError('invalid enum tag')
                    variant=typ['variants'][idx]
                    fields=variant.get('fields') or []
                    if fields and isinstance(fields[0],dict):
                        val={f['name']:self.read(f['type'],definitions,depth+1) for f in fields}
                    else: val=[self.read(f,definitions,depth+1) for f in fields]
                    return {'variant':variant['name'],'value':val}
            raise ValueError('unsupported Borsh type: '+str(typ))
        if typ in ('publicKey','pubkey'):return b58_encode(self.take(32))
        if typ == 'bool':
            b=self.take(1)[0]
            if b not in (0,1):raise ValueError('invalid bool')
            return bool(b)
        if typ in ('u8','u16','u32','u64','u128','i8','i16','i32','i64','i128'):
            return int.from_bytes(self.take(int(typ[1:])//8),'little',signed=typ.startswith('i'))
        if typ in ('string','bytes'):
            length=self.read('u32',definitions,depth+1)
            if length>1_000_000: raise ValueError('string/bytes too long')
            b=self.take(length)
            return b.decode('utf-8') if typ=='string' else b.hex()
        if typ in ('f32','f64'):
            import struct
            return struct.unpack('<f' if typ=='f32' else '<d',self.take(4 if typ=='f32' else 8))[0]
        raise ValueError('unsupported Borsh primitive: '+str(typ))

class Decoder:
    def __init__(self,idl):
        self.definitions={d['name']:d['type'] for d in idl.get('types',[]) if 'type' in d}
        self.events={}
        for ev in idl.get('events',[]):
            fields=ev.get('fields')
            if fields is None:
                fields=self.definitions.get(ev['name'],{}).get('fields')
            if fields is None:continue
            disc=bytes(ev['discriminator']) if 'discriminator' in ev else hashlib.sha256(('event:'+ev['name']).encode()).digest()[:8]
            self.events[disc]=(ev['name'],fields)
        if not self.events:raise ValueError('IDL missing usable event definitions')
    def decode(self,data,source):
        if source=='cpi':
            if not data.startswith(CPI_TAG):return None
            data=data[8:]
        if len(data)<8 or data[:8] not in self.events:return None
        name,fields=self.events[data[:8]]
        reader=Reader(data[8:])
        values={f['name']:reader.read(f['type'],self.definitions) for f in fields}
        if reader.offset!=len(reader.raw):raise ValueError(f'{name} trailing {len(reader.raw)-reader.offset} bytes; check IDL version')
        return name,values

def raw_from_item(item,source):
    text=(item.get('data') if source=='cpi' else item.get('message'))
    if not isinstance(text,str) or not text:return None
    if source=='cpi':return b58_decode(text)
    if item.get('kind') != 'data':return None
    # SQD log.kind=data carries the base64 payload of a native `Program data:` line
    # (prefix stripped). Verified live: messages contain '+'/'/' and decode to IDL events.
    import base64
    if text.startswith('Program data:'):
        text=text.partition(':')[2].strip()
    return base64.b64decode(text,validate=True)

def numeric_raw(v):
    return str(v) if isinstance(v,int) and not isinstance(v,bool) else None

def event_to_candidate(name, vals, slot, timestamp, txi, signature, ix, source):
    action=ACTION_TYPES.get(name)
    if action is None:return None,[]
    owner=vals.get('owner')
    position=vals.get('positionKey')
    mint=vals.get('positionMint')
    side=vals.get('positionSide')
    # A full liquidation has positionSizeUsd, not sizeUsdDelta, in the pinned IDL.
    size=vals.get('sizeUsdDelta')
    if name=='LiquidateFullPositionEvent':
        size=vals.get('positionSizeUsd')
    size_changed=isinstance(size,int) and not isinstance(size,bool) and size>0
    price=vals.get('price')
    errors=[]
    for label,value in [('owner',owner),('positionKey',position),('positionMint',mint)]:
        if not pubkey_ok(value):errors.append('invalid_'+label)
    # On Jupiter Perps: 1=LONG, 2=SHORT (0=None).
    if side not in (1,2): errors.append('missing_or_unknown_side')
    # sizeUsdDelta==0 is possible for collateral-only changes, not necessarily corrupt.
    if not isinstance(size,int) or isinstance(size,bool) or size<0: errors.append('invalid_sizeUsdDelta')
    if size_changed and (not isinstance(price,int) or price<=0):errors.append('invalid_price')
    if not isinstance(signature,str) or len(signature)<64:errors.append('missing_signature')
    if not isinstance(txi,int):errors.append('missing_transaction_index')
    if not isinstance(ix,list):errors.append('missing_instruction_address')
    pnl=None
    if size_changed and action in ('DECREASE','LIQUIDATE'):
        if not isinstance(vals.get('pnlDelta'),int) or not isinstance(vals.get('hasProfit'),bool):
            errors.append('missing_realized_pnl_fields')
        else:pnl=vals['pnlDelta'] * (1 if vals['hasProfit'] else -1)
    usd=lambda raw: str(Decimal(raw)/Decimal(1_000_000)) if isinstance(raw,int) else None
    candidate={
        'platform':'JUPITER_PERPS','chain':'solana','slot':slot,'timestamp':timestamp,
        'signature':signature,'transactionIndex':txi,'instructionAddress':ix,
        'source':source,'eventName':name,'action':action,'trader':owner,'positionKey':position,
        'marketMint':mint,'positionSideCode':side,
        'positionSide':{1:'LONG',2:'SHORT'}.get(side),
        'isExecutedSizeChange':size_changed,
        'eventClassification':'EXECUTED_SIZE_CHANGE' if size_changed else 'ZERO_SIZE_POSITION_EVENT',
        'sizeUsdDeltaRaw':numeric_raw(size),'sizeUsdDelta':usd(size),
        'executionPriceRaw':numeric_raw(price),
        'feeUsdRaw':numeric_raw(vals.get('feeUsd')),'feeUsd':usd(vals.get('feeUsd')),
        'realizedPnlRaw':numeric_raw(pnl),'realizedPnlUsd':usd(pnl),
        'allEventFields':serializable(vals),
        'note':'Not a drop-in Prisma PerpTradingEventLog; requires Jupiter event adapter + price/side mapping verification'
    }
    return candidate,errors

def build_query(start,end,include_transaction=True,mode='lean'):
    # SQD Portal's *Solana* relationship selector is a direct `transaction` boolean,
    # NOT the nested `include: {transaction:true}` used by the old benchmark.
    # Both filters remain narrowly scoped to Jupiter's Perps program.
    #
    # mode='lean' (default) asks SQD server-side for ONLY committed Anchor emit_cpi!
    # event instructions (first 8 data bytes == CPI_TAG, isCommitted=true). On the
    # 2026-11-11 full query, ~74% of bytes were non-event instructions + their accounts
    # and uncommitted instructions that the parser discards anyway. Fewer bytes => fewer
    # SQD batches => fewer rate-limited requests. mode='full' keeps every Jupiter instruction.
    if mode not in ('lean','full'):raise ValueError('query mode must be lean or full')
    instruction_filter={'programId':[PROGRAM]}
    if mode=='lean':
        instruction_filter['d8']=['0x'+CPI_TAG.hex()]
        instruction_filter['isCommitted']=True
    log_filter={'programId':[PROGRAM],'kind':['data']}
    if include_transaction:
        instruction_filter['transaction']=True
        log_filter['transaction']=True
    return {
        'type':'solana','fromBlock':start,'toBlock':end,
        'fields':{
            'block':{'number':True,'timestamp':True,'hash':True},
            'transaction':{'transactionIndex':True,'signatures':True,'err':True},
            'instruction':{'programId':True,'accounts':True,'data':True,
                'transactionIndex':True,'instructionAddress':True,'isCommitted':True,'error':True},
            'log':{'programId':True,'kind':True,'message':True,
                'transactionIndex':True,'instructionAddress':True}},
        'instructions':[instruction_filter],'logs':[log_filter]
    }

def get_tx(txs,txi):
    if not isinstance(txi,int):return None
    # Distinguish an explicit block index from a position in a sparse filtered array.
    explicit=[t for t in txs if t.get('transactionIndex',t.get('index')) == txi]
    if len(explicit)==1:return explicit[0]
    if len(explicit)>1:raise ValueError('ambiguous transaction index')
    # Never infer a transaction from its position in a possibly sparse Portal array.
    # Request transactionIndex explicitly and fail closed if SQD omits it.
    return None

def parse_block(block,decoder,stats):
    if 'header' not in block or not isinstance(block['header'].get('number'),int):
        raise ValueError('SQD response missing header.number')
    slot=block['header']['number']; timestamp=block['header'].get('timestamp')
    txs=block.get('transactions',[])
    if not isinstance(txs,list):raise ValueError('transactions must be list')
    emissions=[]
    sources=[('cpi',i) for i in block.get('instructions',[]) if i.get('programId')==PROGRAM]
    sources += [('log',i) for i in block.get('logs',[]) if i.get('programId')==PROGRAM]
    stats['rawSources']+=len(sources)
    for idx,(source,item) in enumerate(sources):
        if source=='cpi' and item.get('isCommitted') is False:
            stats['uncommittedCpiInstructions']+=1
            continue
        if source=='cpi' and item.get('isCommitted') is not True:
            stats['missingInstructionCommitStatus']+=1
            continue
        try: raw=raw_from_item(item,source)
        except Exception:
            stats['badRawEncoding']+=1;continue
        if not raw:continue
        try:decoded=decoder.decode(raw,source)
        except Exception:
            stats['decodeErrors']+=1;continue
        if decoded is None:
            if source=='cpi' and raw.startswith(CPI_TAG):stats['unknownCpiEvents']+=1
            elif source=='log':stats['unknownDataLogs']+=1
            continue
        name,vals=decoded
        stats['decodedEmissions']+=1
        if name not in ACTION_TYPES:continue
        txi=item.get('transactionIndex')
        tx=get_tx(txs,txi)
        if tx is None:
            stats['missingTransactionLink']+=1
            signature=None
        elif 'err' not in tx:
            stats['missingTransactionStatus']+=1
            signature=None
        elif tx['err'] is not None:
            stats['failedTransactionEvents']+=1
            continue
        else:
            signature=(tx.get('signatures') or [None])[0]
        ix=item.get('instructionAddress')
        if source=='log' and not isinstance(ix,list):
            stats['missingInstructionAddress']+=1
        canonical=hashlib.sha256(raw[8:] if source=='cpi' else raw).hexdigest()
        candidate,errors=event_to_candidate(name,vals,slot,timestamp,txi,signature,ix,source)
        if candidate is None:continue
        candidate['rawSha256']=canonical
        emissions.append((candidate,errors))
    # Deduplicate log + CPI representations only, preserving repeated identical
    # emissions within the same source (two fills can have identical values).
    groups=collections.defaultdict(lambda:{'cpi':[],'log':[]})
    for cand,errors in emissions:
        key=(cand['transactionIndex'],cand['eventName'],cand['rawSha256'])
        groups[key][cand['source']].append((cand,errors))
    output=[]
    for group in groups.values():
        cp=group['cpi'];lg=group['log']
        stats['crossSourceDuplicates']+=min(len(cp),len(lg))
        output.extend(cp if len(cp)>=len(lg) else lg)
        if len(cp) and len(lg) and len(cp)!=len(lg):stats['unequalEmissionMultiplicity']+=1
    for candidate,errors in output:
        if errors:stats['invalidCandidates']+=1
        else:
            stats['validCandidates']+=1
            if candidate['isExecutedSizeChange']:stats['validExecutedTrades']+=1
            else:stats['zeroSizePositionEvents']+=1
        stats['action_'+candidate['action']]+=1
    return output

def request_stream(query,api_key=None,timeout=90,retries=10):
    headers={
        'Content-Type':'application/json',
        'Accept':'application/jsonl',
        # Identify the benchmark explicitly instead of urllib's generic default.
        'User-Agent':'LuckyPlans-SQD-AccuracyBenchmark/1.4',
        # Public Portal is limited by data volume (~0.1 MB/s, small monthly quota), so ask
        # for gzip: ~45% fewer wire bytes on lean Jupiter batches (measured 2026-11-23).
        'Accept-Encoding':'gzip',
    }
    if api_key:headers['Authorization']='Bearer '+api_key  # SQD docs: preferred over x-api-key
    body=json.dumps(query,separators=(',',':')).encode()
    for attempt in range(retries+1):
        req=Request(SQD_URL,data=body,headers=headers,method='POST')
        try:
            with urlopen(req,timeout=timeout) as response:
                status=response.status
                if status==204:return []
                # A single HTTP response is only one SQD batch; caller continues.
                payload=response.read()
                WIRE_STATS['wireBytes']+=len(payload)
                if (response.headers.get('Content-Encoding') or '').lower()=='gzip':
                    payload=gzip.decompress(payload)  # truncated body -> EOFError/BadGzipFile -> retry
                WIRE_STATS['decodedBytes']+=len(payload)
                return payload.splitlines(keepends=True)
        except HTTPError as e:
            if e.code in (429,502,503,504,529) and attempt < retries:
                hint=e.headers.get('Retry-After')
                backoff=min(60.,2.**(attempt+1))
                # Retry-After is a minimum; keep growing backoff while the shared Portal stays overloaded.
                try: wait=max(backoff,min(120.,float(hint))) if hint else backoff
                except (ValueError,TypeError):wait=backoff
                RETRY_STATS[f'http{e.code}']+=1
                print(f'SQD stream HTTP {e.code} at fromBlock {query.get("fromBlock")}, retry {attempt+1}/{retries} after {wait:g}s',file=sys.stderr)
                time.sleep(wait);continue
            details=e.read(1000).decode('utf-8','replace')
            ray=e.headers.get('cf-ray','unknown')
            reqid=e.headers.get('x-request-id','unknown')
            kind=e.headers.get('content-type','unknown')
            raise RuntimeError(
                f'SQD HTTP {e.code} (content-type={kind}, cf-ray={ray}, x-request-id={reqid}): {details}'
            ) from e
        except (URLError,TimeoutError,ConnectionError,http.client.HTTPException,
                EOFError,gzip.BadGzipFile,zlib.error) as e:
            # Includes resets / truncated (possibly gzip) bodies mid-stream, not just connect failures.
            if attempt<retries:
                RETRY_STATS["network"]+=1
                time.sleep(min(60.,2.**(attempt+1)));continue
            raise RuntimeError(f'SQD network error: {e}') from e

def _timestamp_block(ts, timeout=30, api_key=None, attempts=7):
    """GET the first indexed Solana slot >= timestamp, respecting SQD backoff."""
    url=f'https://portal.sqd.dev/datasets/solana-mainnet/timestamps/{ts}/block'
    headers={'User-Agent':'LuckyPlans-SQD-AccuracyBenchmark/1.4','Accept':'application/json'}
    if api_key:
        headers['Authorization']='Bearer '+api_key
    for attempt in range(attempts):
        try:
            with urlopen(Request(url,headers=headers),timeout=timeout) as response:
                result=json.load(response)
            block=result.get('block_number')
            if not isinstance(block,int) or isinstance(block,bool) or block<0:
                raise ValueError('unexpected SQD timestamp response: '+repr(result))
            return block
        except HTTPError as e:
            try:
                details=e.read(300).decode('utf-8','replace')
            except Exception:
                details=''
            if e.code in (429,502,503,504,529) and attempt+1 < attempts:
                hint=e.headers.get('Retry-After')
                try:
                    pause=max(1.,min(120.,float(hint))) if hint else min(30.,2.**attempt)
                except (ValueError,TypeError):
                    pause=min(30.,2.**attempt)
                print(f'SQD timestamp lookup HTTP {e.code}, retry {attempt+1}/{attempts-1} after {pause:g}s',file=sys.stderr)
                time.sleep(pause)
                continue
            raise RuntimeError(f'SQD timestamp HTTP {e.code}; x-request-id={e.headers.get("x-request-id","unknown")}; {details}') from e
        except (URLError,TimeoutError) as e:
            if attempt+1 >= attempts:
                raise RuntimeError(f'SQD timestamp transport failed: {e}') from e
            pause=min(30.,2.**attempt)
            print(f'SQD timestamp network failure, retry after {pause:g}s: {e}',file=sys.stderr)
            time.sleep(pause)


def _block_at_or_after(slot, timeout=30, api_key=None):
    """Fetch indexed Solana block headers (not transaction bodies) around one slot."""
    if slot<0:slot=0
    query={'type':'solana','fromBlock':int(slot),'toBlock':int(slot)+127,
           'fields':{'block':{'number':True,'timestamp':True}}}
    lines=request_stream(query,api_key,timeout=timeout,retries=6)
    result=[]
    for line in lines:
        if not line.strip():continue
        data=json.loads(line)
        header=data.get('header',{})
        slot_number=header.get('number')
        ts=header.get('timestamp')
        if isinstance(slot_number,int) and isinstance(ts,int) and ts>0 and slot_number>=slot:
            result.append((slot_number,ts))
    if not result:
        raise RuntimeError(f'SQD block-only probe returned no timestamped blocks at/after slot {slot}')
    return min(result)


def _fallback_date_slots(start_ts, end_ts, timeout=30, api_key=None, anchor_slot=468300000):
    """Resolve UTC boundaries with SQD block-header probes if timestamp API is overloaded.

    Does not issue raw Solana RPC or fetch full transactions. Uses a conservative
    superset plus a timestamp filter during parsing, and verifies both edges.
    """
    known={}
    def probe(slot):
        slot=max(0,int(slot))
        if slot not in known:
            known[slot]=_block_at_or_after(slot,timeout,api_key)
        return known[slot]

    anchor_n,anchor_ts=probe(anchor_slot)
    def first_at_or_after(target):
        step=max(1024,int(abs(target-anchor_ts)*3.0))
        if anchor_ts < target:
            low=anchor_n
            high=anchor_n+step
            while probe(high)[1] < target:
                low=high;step*=2;high+=step
                if step>10_000_000:raise RuntimeError('cannot bracket future timestamp with SQD headers')
        else:
            high=anchor_n
            low=max(0,anchor_n-step)
            while probe(low)[1]>=target:
                if low==0:return 0
                high=low;step*=2;low=max(0,low-step)
                if step>10_000_000:raise RuntimeError('cannot bracket historical timestamp with SQD headers')
        while high-low>1:
            middle=(low+high)//2
            if probe(middle)[1]>=target:high=middle
            else:low=middle
        return high

    start_boundary=first_at_or_after(start_ts)
    next_boundary=first_at_or_after(end_ts)
    # The binary search targets the earliest next available block. Include enough
    # padding to tolerate missing slots / minor clock inconsistencies, then check
    # both edges using real block timestamps. Only date-matching events are parsed.
    pad=4096
    for _ in range(6):
        first=max(0,start_boundary-pad)
        last=next_boundary+pad
        if probe(first)[1]<start_ts and probe(last)[1]>=end_ts:
            return first,last,{'method':'sqd-header-fallback','startBoundaryEstimate':start_boundary,
                               'nextMidnightBoundaryEstimate':next_boundary,
                               'edgeSamples':{'from':probe(first),'to':probe(last)},
                               'headerProbes':len(known)}
        pad*=2
    raise RuntimeError('SQD header fallback could not verify UTC day boundaries')


def resolve_utc_day(day, timeout=30, api_key=None, anchor_slot=468300000, return_details=False):
    """Return an inclusive slot range for a UTC day, with a stream-header fallback."""
    parsed=date.fromisoformat(day)
    beginning=datetime(parsed.year,parsed.month,parsed.day,tzinfo=timezone.utc)
    start_ts=int(beginning.timestamp())
    end_ts=int((beginning+timedelta(days=1)).timestamp())
    try:
        first=_timestamp_block(start_ts,timeout,api_key)
        after=_timestamp_block(end_ts,timeout,api_key)
        if after<=first:raise ValueError('SQD timestamp resolver returned invalid bounds')
        lo,hi=first,after-1
        details={'method':'sqd-timestamp-api','firstSlot':first,'nextMidnightFirstSlot':after}
    except (RuntimeError,ValueError,HTTPError,URLError,TimeoutError) as e:
        print(f'SQD timestamp lookup unavailable ({e}); falling back to SQD block HEADER sampling',file=sys.stderr)
        lo,hi,details=_fallback_date_slots(start_ts,end_ts,timeout,api_key,anchor_slot)
    return (lo,hi,details) if return_details else (lo,hi)

def load_idl(args,target):
    if args.idl:
        data=Path(args.idl).read_bytes();origin=str(Path(args.idl).resolve())
    else:
        origin=IDL_URL
        with urlopen(origin,timeout=30) as res:data=res.read()
    idl=json.loads(data)
    if idl.get('address') not in (None,PROGRAM):raise ValueError('IDL program address mismatch')
    checksum=hashlib.sha256(data).hexdigest()
    (target/'idl_used.json').write_bytes(data)
    return idl,origin,checksum

def benchmark(args):
    target=Path(args.out);target.mkdir(parents=True,exist_ok=True)
    idl,origin,checksum=load_idl(args,target)
    decoder=Decoder(idl)
    stats=collections.Counter()
    from_slot=args.from_slot;to_slot=args.to_slot
    query=build_query(from_slot,to_slot,include_transaction=not args.no_include,
                      mode=getattr(args,'query_mode','lean'))
    prior=target/'query.json'
    if getattr(args,'resume',False) and prior.exists() and (target/'raw.ndjson').exists():
        old=json.loads(prior.read_text())
        if (old.get('fromBlock'),old.get('toBlock'))!=(from_slot,to_slot):
            raise ValueError(f'--resume range {from_slot}..{to_slot} differs from existing run '
                             f'{old.get("fromBlock")}..{old.get("toBlock")}; use a new --out')
        if {k:v for k,v in old.items() if k!='fromBlock'}!={k:v for k,v in query.items() if k!='fromBlock'}:
            # Never mix query shapes in one raw.ndjson. Move the old partial run aside
            # (nothing is deleted) and start this day fresh with the current query.
            aside=target.with_name(target.name+'.superseded-'+time.strftime('%Y%m%dT%H%M%S'))
            target.rename(aside);target.mkdir(parents=True)
            (target/'idl_used.json').write_bytes((aside/'idl_used.json').read_bytes())
            print(f'Stored query differs (older query shape); moved old partial run to {aside}, starting fresh',file=sys.stderr)
    (target/'query.json').write_text(json.dumps(query,indent=2))
    start=time.monotonic();next_slot=from_slot;last_slot=from_slot-1
    date_start=date_end=None
    if getattr(args,'date_utc',None):
        parsed=date.fromisoformat(args.date_utc)
        date_start=int(datetime(parsed.year,parsed.month,parsed.day,tzinfo=timezone.utc).timestamp())
        date_end=date_start+86400
    pages=0;raw_bytes=0;unique=set();errors_examples=[]
    completed=False;failure=None
    valid_results=[]
    raw_path=target/'raw.ndjson';out_path=target/'candidates.ndjson'
    resume_info=None

    def handle(line,outfile):
        """Validate ordering, then decode one SQD block line (shared by live + resume)."""
        nonlocal last_slot,raw_bytes
        block=json.loads(line)
        slot=block['header']['number']
        if slot < next_slot or slot > to_slot or slot <= last_slot:
            raise RuntimeError(f'non-monotonic/out-of-range slot {slot}')
        last_slot=slot
        raw_bytes+=len(line.rstrip(b'\n'));stats['returnedBlocks']+=1
        if date_start is not None:
            ts=block.get('header',{}).get('timestamp')
            if not isinstance(ts,int):
                raise RuntimeError('missing UTC timestamp at slot '+str(slot))
            if ts<date_start or ts>=date_end:
                stats['outOfUtcDayBlocks']+=1
                return
        rows=parse_block(block,decoder,stats)
        for candidate,issues in rows:
            # Event occurrence ID includes source location and sequence; raw hash
            # alone cannot distinguish multiple identical fills in one tx.
            dedupkey=(slot,candidate['transactionIndex'],candidate['source'],
                      str(candidate['instructionAddress']),candidate['rawSha256'])
            if dedupkey in unique:
                stats['repeatedSourceIdentity']+=1;issues=list(issues)+['repeated_source_identity']
            unique.add(dedupkey)
            output={'valid':not issues,'issues':issues,**candidate}
            outfile.write(json.dumps(output,separators=(',',':'))+'\n')
            if not issues: valid_results.append(candidate)
            if issues and len(errors_examples)<10:
                errors_examples.append({'slot':slot,'name':candidate['eventName'],'issues':issues})

    try:
        resuming=getattr(args,'resume',False) and raw_path.exists() and raw_path.stat().st_size>0
        if resuming:
            # Drop a torn final line (process killed mid-write), then replay stored raw data
            # through the exact same validation/decoding path before continuing the stream.
            data=raw_path.read_bytes()
            keep=data.rfind(b'\n')+1
            if keep!=len(data):
                with raw_path.open('r+b') as fh:fh.truncate(keep)
            with raw_path.open('rb') as rawfile,out_path.open('w') as outfile:
                for line in rawfile:
                    if line.strip():handle(line,outfile)
            resume_info={'resumedFromSlot':last_slot+1,'replayedBlocks':stats['returnedBlocks'],
                         'replayedBytes':raw_bytes,'tornBytesDropped':len(data)-keep,
                         'priorSessionSeconds':0.0,'priorSessionHttpBatches':0}
            try:  # carry earlier sessions' wall time / request counts forward
                prev=json.loads((target/'report.json').read_text()).get('stream',{})
                pr=prev.get('resume') or {}
                resume_info['priorSessionSeconds']=round(pr.get('priorSessionSeconds',0)+prev.get('seconds',0),3)
                resume_info['priorSessionHttpBatches']=pr.get('priorSessionHttpBatches',0)+prev.get('httpBatches',0)
                resume_info['priorSessionWireBytes']=pr.get('priorSessionWireBytes',0)+prev.get('wireBytesThisSession',0)
            except (OSError,ValueError,AttributeError):
                pass
            next_slot=last_slot+1
            print(f'Resuming: replayed {stats["returnedBlocks"]} stored blocks, continuing at slot {next_slot}',file=sys.stderr)
        with raw_path.open('ab' if resuming else 'wb') as rawfile,out_path.open('a' if resuming else 'w') as outfile:
            while next_slot<=to_slot:
                page_query={**query,'fromBlock':next_slot}
                lines=request_stream(page_query,args.api_key,timeout=args.timeout,
                                     retries=getattr(args,'retries',60))
                pages+=1
                if not lines:raise RuntimeError(f'empty/204 SQD batch at slot {next_slot}; cannot certify coverage')
                before=next_slot
                for line in lines:
                    if not line.strip():continue
                    line=line if line.endswith(b'\n') else line+b'\n'
                    handle(line,outfile)
                    rawfile.write(line)
                rawfile.flush();outfile.flush()
                next_slot=last_slot+1
                if next_slot<=before:raise RuntimeError('SQD response made no forward progress')
        completed=next_slot>to_slot
    except Exception as e:
        failure=str(e)
    duration=time.monotonic()-start
    conditions={
        'full_requested_range_streamed':completed,
        'at_least_one_executed_trade':stats['validExecutedTrades']>0,
        'zero_decoding_failures':stats['decodeErrors']==0,
        'zero_raw_encoding_failures':stats['badRawEncoding']==0,
        'zero_unknown_anchor_cpi':stats['unknownCpiEvents']==0,
        'zero_unrecognized_data_logs':stats['unknownDataLogs']==0,
        'zero_invalid_candidates':stats['invalidCandidates']==0,
        'zero_missing_transaction_links':stats['missingTransactionLink']==0,
        'zero_missing_instruction_addresses':stats['missingInstructionAddress']==0,
        'zero_missing_transaction_status':stats['missingTransactionStatus']==0,
        'zero_missing_commit_status':stats['missingInstructionCommitStatus']==0,
        'zero_duplicate_source_ids':stats['repeatedSourceIdentity']==0,
        'zero_event_multiplicity_mismatch':stats['unequalEmissionMultiplicity']==0,
    }
    reference_comparison=None
    if args.reference:
        try:
            expected=json.loads(Path(args.reference).read_text())
            if not isinstance(expected,list) or not expected:
                raise ValueError('reference JSON must contain a nonempty array')
            checked=[]
            for ref in expected:
                if not isinstance(ref,dict) or not ref.get('signature') or not ref.get('eventName'):
                    raise ValueError('each reference needs signature and eventName')
                matches=[cand for cand in valid_results if all(cand.get(k)==v for k,v in ref.items())]
                checked.append({'reference':ref,'matched':bool(matches),'matchCount':len(matches)})
            reference_comparison={'expected':len(expected),'matched':sum(x['matched'] for x in checked),
                                  'results':checked}
            conditions['all_reference_events_matched']=all(x['matched'] for x in checked)
        except Exception as e:
            conditions['all_reference_events_matched']=False
            reference_comparison={'error':str(e)}
    passed=all(conditions.values()) and not failure
    status=('PASS_WITH_REFERENCE_CHECKS' if args.reference else 'PASS_STRUCTURAL_ONLY') if passed else 'FAIL_OR_INCONCLUSIVE'
    report={
      'status':status,
      'IMPORTANT':'Passing tests proves only local decode and validity in the requested SQD range, NOT complete Jupiter history or equality to independent source.',
      'request':{'source':'SQD Portal ONLY','fromSlot':from_slot,'toSlot':to_slot,'endpoint':SQD_URL,
                 'queryMode':getattr(args,'query_mode','lean'),
                 'dateUTC':getattr(args,'date_utc',None),
                 'dateResolution':getattr(args,'date_resolution',None)},
      'idl':{'urlOrPath':origin,'sha256':checksum,'eventsAvailable':len(decoder.events)},
      'stream':{'lastSlot':last_slot,'complete':completed,'httpBatches':pages,'resume':resume_info,'rawBytes':raw_bytes,
        'rawMiB':round(raw_bytes/(1024*1024),4),'seconds':round(duration,3),
        'rawMiBPerSecond':round((raw_bytes-(resume_info or {}).get('replayedBytes',0))/(1024*1024)/duration,4) if duration else None,
        'retries':dict(RETRY_STATS),'wireBytesThisSession':WIRE_STATS['wireBytes'],
        'decodedBytesThisSession':WIRE_STATS['decodedBytes']},
      'counts':dict(stats),'passConditions':conditions,'referenceComparison':reference_comparison,'errors':errors_examples,'exception':failure,
      'files':['raw.ndjson','candidates.ndjson','idl_used.json','query.json','report.json']}
    (target/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return 0 if passed else 2

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--from-slot',type=int,default=468300000)
    parser.add_argument('--to-slot',type=int,default=468300999)
    parser.add_argument('--date-utc',help='Select a full UTC calendar day YYYY-MM-DD; SQD header fallback if timestamp lookup fails')
    parser.add_argument('--anchor-slot',type=int,default=468300000,help='Known historical Solana slot for date header fallback; default is verified Nov 11 2026 slot')
    parser.add_argument('--out',default='results')
    parser.add_argument('--idl',help='Local Anchor IDL JSON; otherwise download community IDL from GitHub (not Trawl)')
    parser.add_argument('--api-key',default=os.environ.get('SQD_API_KEY'),help='SQD Portal API key (sent as Authorization: Bearer)')
    parser.add_argument('--timeout',type=int,default=120)
    parser.add_argument('--reference',help='Optional JSON array of independently verified expected trade fields (signature, eventName, etc.)')
    parser.add_argument('--query-mode',choices=['lean','full'],default='lean',help='lean (default): only committed Anchor event CPIs server-side; full: every Jupiter instruction')
    parser.add_argument('--resume',action='store_true',help='Continue an interrupted run: replay existing raw.ndjson in --out, then stream from the next slot')
    parser.add_argument('--retries',type=int,default=60,help='Retries per SQD batch on 429/5xx/529 (default 60, ~15 min of backoff)')
    parser.add_argument('--no-include',action='store_true',help='Do not request parent transaction relations; decoding may work but identities will fail validation')
    args=parser.parse_args(argv)
    args.date_resolution=None
    if args.date_utc:
        resolution_started=time.monotonic()
        try:
            args.from_slot,args.to_slot,args.date_resolution=resolve_utc_day(
                args.date_utc,args.timeout,args.api_key,args.anchor_slot,return_details=True)
        except Exception as e:
            # Leave a durable diagnostic artifact instead of only an argparse message.
            target=Path(args.out);target.mkdir(parents=True,exist_ok=True)
            (target/'report.json').write_text(json.dumps({
                'status':'FAIL_OR_INCONCLUSIVE','stage':'utc_date_resolution',
                'request':{'source':'SQD Portal ONLY','dateUTC':args.date_utc,'anchorSlot':args.anchor_slot},
                'exception':str(e),'seconds':round(time.monotonic()-resolution_started,3)},indent=2)+'\n')
            parser.error('failed to resolve UTC date via SQD timestamp API and header fallback: '+str(e))
        args.date_resolution['seconds']=round(time.monotonic()-resolution_started,3)
    if args.from_slot<0 or args.to_slot<args.from_slot:parser.error('invalid slot range')
    # A UTC day is ~402k slots at late-2026 slot times (~215ms); cap with headroom.
    if args.to_slot-args.from_slot > (600000 if args.date_utc else 100000):
        parser.error('slot range exceeds benchmark safety cap')
    try:return benchmark(args)
    except Exception as e:
        print('ERROR:',e,file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
