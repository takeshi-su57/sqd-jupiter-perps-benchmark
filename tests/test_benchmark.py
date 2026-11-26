"""Offline synthetic unit tests; NOT a substitute for testing real SQD data."""
import hashlib
import struct
import unittest
import json
import tempfile
from pathlib import Path
from argparse import Namespace
from unittest.mock import patch
import benchmark as b

PUBKEY1=b.b58_encode(bytes([3])*32)
PUBKEY2=b.b58_encode(bytes([5])*32)
PUBKEY3=b.b58_encode(bytes([7])*32)
EVENT_NAME='InstantIncreasePositionEvent'
FIELDS=[
  {'name':'positionKey','type':'publicKey'},
  {'name':'positionSide','type':'u8'},
  {'name':'positionMint','type':'publicKey'},
  {'name':'owner','type':'publicKey'},
  {'name':'sizeUsdDelta','type':'u64'},
  {'name':'price','type':'u64'},
  {'name':'feeUsd','type':'u64'},
  {'name':'referral','type':{'option':'publicKey'}},
]
IDL={'address':b.PROGRAM,'events':[{'name':EVENT_NAME,'fields':FIELDS}]}
DISCRIMINATOR=hashlib.sha256(('event:'+EVENT_NAME).encode()).digest()[:8]
PAYLOAD=(DISCRIMINATOR+bytes([3])*32+b'\x01'+bytes([7])*32+bytes([5])*32+
        struct.pack('<QQQ',12_000_000,48_000_000_000,35_000)+b'\x00')

class AccuracyTests(unittest.TestCase):
    def test_sqd_relation_syntax_matches_current_schema(self):
        query=b.build_query(468300000,468300999)
        self.assertTrue(query['instructions'][0]['transaction'])
        self.assertTrue(query['logs'][0]['transaction'])
        self.assertNotIn('include',query['instructions'][0])
        self.assertNotIn('include',query['logs'][0])
        self.assertTrue(query['fields']['transaction']['transactionIndex'])
        self.assertEqual(query['instructions'][0]['programId'],[b.PROGRAM])

    def test_no_positional_guess_for_sparse_transactions(self):
        # A filtered transaction array might have only one tx, originally at block index 3.
        transactions=[{'signatures':['5'*88], 'err':None}]
        self.assertIsNone(b.get_tx(transactions,0))
        self.assertIsNone(b.get_tx(transactions,3))

    def test_base58_roundtrip(self):
        for data in (b'\x00\x00'+bytes([255])*8, b'', bytes([4])*32):
            self.assertEqual(b.b58_decode(b.b58_encode(data)),data)
    def test_decodes_real_anchor_envelopes_synthetically(self):
        d=b.Decoder(IDL)
        name,values=d.decode(PAYLOAD,'log')
        self.assertEqual(name,EVENT_NAME)
        self.assertEqual(values['owner'],PUBKEY2)
        self.assertEqual(values['sizeUsdDelta'],12_000_000)
        self.assertIsNone(values['referral'])
        name2,values2=d.decode(b.CPI_TAG+PAYLOAD,'cpi')
        self.assertEqual((name2,values2),(name,values))
        self.assertIsNone(d.decode(PAYLOAD,'cpi'))
    def test_raw_log_base64(self):
        # SQD Portal returns kind=data log messages as bare base64 (observed live, v1.5).
        self.assertEqual(b.raw_from_item({'kind':'data','message':__import__('base64').b64encode(PAYLOAD).decode()},'log'),PAYLOAD)
        with self.assertRaises(ValueError):
            b.raw_from_item({'kind':'data','message':'not base64!!'},'log')
        self.assertEqual(b.raw_from_item({'kind':'data','message':'Program data: '+__import__('base64').b64encode(PAYLOAD).decode()},'log'),PAYLOAD)
    def _block(self,commit=True,failed=False,include_tx=True,include_log=True):
        inst={'programId':b.PROGRAM,'data':b.b58_encode(b.CPI_TAG+PAYLOAD),
              'transactionIndex':0,'instructionAddress':[2,0],'isCommitted':commit}
        logs=[]
        if include_log:
            logs=[{'programId':b.PROGRAM,'kind':'data','message':__import__('base64').b64encode(PAYLOAD).decode(),
                   'transactionIndex':0,'instructionAddress':[2,0]}]
        return {'header':{'number':468300000,'timestamp':1794370000},
          'transactions':[{'transactionIndex':0,'signatures':['5'*88],'err':{'fail':True} if failed else None}] if include_tx else [],
          'instructions':[inst],'logs':logs}
    def test_dedupe_cpi_log_and_scale(self):
        stats=__import__('collections').Counter()
        out=b.parse_block(self._block(),b.Decoder(IDL),stats)
        self.assertEqual(len(out),1)
        self.assertFalse(out[0][1])
        self.assertEqual(out[0][0]['sizeUsdDelta'],'12')
        self.assertEqual(out[0][0]['feeUsd'],'0.035')
        self.assertEqual(stats['crossSourceDuplicates'],1)
        self.assertEqual(stats['validCandidates'],1)
    def test_failed_transaction_rejected(self):
        stats=__import__('collections').Counter()
        rows=b.parse_block(self._block(failed=True),b.Decoder(IDL),stats)
        self.assertEqual(rows,[])
        self.assertEqual(stats['failedTransactionEvents'],2)
    def test_missing_transaction_is_invalid(self):
        stats=__import__('collections').Counter()
        rows=b.parse_block(self._block(include_tx=False),b.Decoder(IDL),stats)
        self.assertEqual(len(rows),1)
        self.assertIn('missing_signature',rows[0][1])
        self.assertEqual(stats['missingTransactionLink'],2)
    def test_invalid_borsh_truncation(self):
        with self.assertRaises(ValueError):b.Decoder(IDL).decode(PAYLOAD[:-1],'log')
    def test_full_synthetic_two_page_stream_and_report(self):
        with tempfile.TemporaryDirectory() as temp:
            idl=Path(temp)/'idl.json'
            idl.write_text(json.dumps(IDL))
            source=self._block()
            next_block={'header':{'number':468300001,'timestamp':1794370001},
                        'transactions':[],'instructions':[],'logs':[]}
            batches=[[json.dumps(source).encode()+b'\n'],
                     [json.dumps(next_block).encode()+b'\n']]
            args=Namespace(out=str(Path(temp)/'out'),idl=str(idl),from_slot=468300000,
                to_slot=468300001,no_include=False,api_key=None,timeout=5,reference=None)
            with patch.object(b,'request_stream',side_effect=batches) as fake:
                self.assertEqual(b.benchmark(args),0)
                self.assertEqual(fake.call_count,2)
            report=json.loads((Path(args.out)/'report.json').read_text())
            self.assertEqual(report['status'],'PASS_STRUCTURAL_ONLY')
            self.assertEqual(report['stream']['httpBatches'],2)
            self.assertEqual(report['counts']['validCandidates'],1)
            self.assertEqual(len((Path(args.out)/'raw.ndjson').read_text().splitlines()),2)

    def test_complete_stream_requires_final_slot(self):
        with tempfile.TemporaryDirectory() as temp:
            idl=Path(temp)/'idl.json';idl.write_text(json.dumps(IDL))
            args=Namespace(out=str(Path(temp)/'out'),idl=str(idl),from_slot=468300000,
                to_slot=468300001,no_include=False,api_key=None,timeout=5,reference=None)
            with patch.object(b,'request_stream',side_effect=[
                [json.dumps(self._block()).encode()+b'\n'],[]]):
                self.assertEqual(b.benchmark(args),2)
            report=json.loads((Path(args.out)/'report.json').read_text())
            self.assertEqual(report['status'],'FAIL_OR_INCONCLUSIVE')
            self.assertFalse(report['stream']['complete'])

    def test_no_fake_exactly_valid_price(self):
        stats=__import__('collections').Counter()
        rows=b.parse_block(self._block(),b.Decoder(IDL),stats)
        self.assertEqual(rows[0][0]['executionPriceRaw'],str(48_000_000_000))
        self.assertNotIn('executionPriceUsd',rows[0][0])

if __name__=='__main__':unittest.main()

# v1.3 regression tests target real-world validation failure modes from
# the live SQD 1,000-slot report, rather than only synthetic encoding behavior.
class JupiterSemanticsTests(unittest.TestCase):
    def _core_values(self, side=2, size=5000000):
        return {'owner':PUBKEY2,'positionKey':b.b58_encode(bytes([7])*32),
                'positionMint':b.b58_encode(bytes([5])*32),
                'positionSide':side,'sizeUsdDelta':size,'price':30_000_000,
                'feeUsd':1000,'hasProfit':False,'pnlDelta':5_000_000}

    def _normalized(self,name,vals):
        return b.event_to_candidate(name,vals,468300096,1794438076,
                                    1,'5'*88,[2,0],'log')

    def test_side_1_is_long_and_2_is_short(self):
        for side, label in ((1,'LONG'),(2,'SHORT')):
            with self.subTest(side=side):
                cand, problems=self._normalized('InstantIncreasePositionEvent', self._core_values(side=side))
                self.assertEqual(problems,[])
                self.assertEqual(cand['positionSide'],label)
                self.assertTrue(cand['isExecutedSizeChange'])

    def test_zero_size_not_mislabeled_as_corruption_or_trade(self):
        cand,problems=self._normalized('InstantDecreasePositionEvent',self._core_values(size=0))
        self.assertEqual(problems,[])
        self.assertFalse(cand['isExecutedSizeChange'])
        self.assertEqual(cand['eventClassification'],'ZERO_SIZE_POSITION_EVENT')

    def test_unknown_side_still_rejected(self):
        cand,problems=self._normalized('InstantIncreasePositionEvent',self._core_values(side=0))
        self.assertIn('missing_or_unknown_side',problems)
        self.assertIsNone(cand['positionSide'])

    def test_full_liquidation_uses_position_size_field(self):
        vals=self._core_values()
        vals.pop('sizeUsdDelta')
        vals['positionSizeUsd']=7_000_000
        cand,problems=self._normalized('LiquidateFullPositionEvent',vals)
        self.assertEqual(problems,[])
        self.assertEqual(cand['sizeUsdDeltaRaw'],'7000000')
        self.assertEqual(cand['realizedPnlUsd'],'-5')

    def test_resolve_utc_day_uses_next_midnight_exclusive(self):
        from unittest.mock import patch
        from io import BytesIO
        class MockResult:
            def __init__(self,body):self.body=BytesIO(body)
            def __enter__(self):return self.body
            def __exit__(self,*args):return False
        responses=[MockResult(b'{"block_number":468000000}'),MockResult(b'{"block_number":468210000}')]
        with patch.object(b,'urlopen',side_effect=responses) as opening:
            start,end=b.resolve_utc_day('2026-11-11')
            self.assertEqual((start,end),(468000000,468209999))
            self.assertIn('1794355200',opening.call_args_list[0].args[0].full_url)
            self.assertIn('1794441600',opening.call_args_list[1].args[0].full_url)


class ResumeTests(unittest.TestCase):
    """An interrupted run must resume without losing or double-counting events."""
    def _args(self,temp,resume):
        idl=Path(temp)/'idl.json';idl.write_text(json.dumps(IDL))
        return Namespace(out=str(Path(temp)/'out'),idl=str(idl),from_slot=468300000,to_slot=468300002,
                         no_include=False,api_key=None,timeout=5,reference=None,resume=resume,retries=0)
    def _blocks(self):
        first=AccuracyTests()._block()
        second={'header':{'number':468300001,'timestamp':1794370001},'transactions':[],'instructions':[],'logs':[]}
        third={'header':{'number':468300002,'timestamp':1794370002},'transactions':[],'instructions':[],'logs':[]}
        return [json.dumps(x).encode()+b'\n' for x in (first,second,third)]
    def test_resume_after_overload_completes_without_duplicates(self):
        b1,b2,b3=self._blocks()
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(b,'request_stream',side_effect=[[b1,b2],RuntimeError('SQD HTTP 529')]), patch('sys.stdout'):
                self.assertEqual(b.benchmark(self._args(temp,False)),2)
            with patch.object(b,'request_stream',side_effect=[[b3]]) as fake, patch('sys.stdout'), patch('sys.stderr'):
                self.assertEqual(b.benchmark(self._args(temp,True)),0)
            self.assertEqual(fake.call_args.args[0]['fromBlock'],468300002)
            out=Path(temp)/'out'
            report=json.loads((out/'report.json').read_text())
            self.assertEqual(report['status'],'PASS_STRUCTURAL_ONLY')
            self.assertEqual(report['stream']['resume']['resumedFromSlot'],468300002)
            self.assertEqual(report['counts']['validCandidates'],1)
            self.assertEqual((out/'raw.ndjson').read_bytes(),b1+b2+b3)
            self.assertEqual(len((out/'candidates.ndjson').read_text().splitlines()),1)
    def test_resume_drops_torn_last_line(self):
        b1,b2,b3=self._blocks()
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'out';out.mkdir()
            (out/'raw.ndjson').write_bytes(b1+b2[:20])  # killed mid-write
            with patch.object(b,'request_stream',side_effect=[[b2,b3]]) as fake, patch('sys.stdout'), patch('sys.stderr'):
                self.assertEqual(b.benchmark(self._args(temp,True)),0)
            self.assertEqual(fake.call_args.args[0]['fromBlock'],468300001)
            self.assertEqual((out/'raw.ndjson').read_bytes(),b1+b2+b3)


class QueryShapeChangeTests(unittest.TestCase):
    def test_resume_with_different_query_moves_old_run_aside(self):
        rt=ResumeTests(); b1,b2,b3=rt._blocks()
        with tempfile.TemporaryDirectory() as temp:
            args=rt._args(temp,False); args.query_mode='full'
            with patch.object(b,'request_stream',side_effect=[[b1],RuntimeError('SQD HTTP 529')]), patch('sys.stdout'):
                self.assertEqual(b.benchmark(args),2)
            args=rt._args(temp,True); args.query_mode='lean'
            with patch.object(b,'request_stream',side_effect=[[b1,b2,b3]]) as fake, patch('sys.stdout'), patch('sys.stderr'):
                self.assertEqual(b.benchmark(args),0)
            self.assertEqual(fake.call_args.args[0]['fromBlock'],468300000)   # fresh start, not resumed
            aside=[p for p in Path(temp).iterdir() if '.superseded-' in p.name]
            self.assertEqual(len(aside),1)
            self.assertEqual((aside[0]/'raw.ndjson').read_bytes(),b1)        # old data kept, not deleted
            self.assertEqual(json.loads((Path(temp)/'out'/'query.json').read_text())['instructions'][0].get('isCommitted'),True)
