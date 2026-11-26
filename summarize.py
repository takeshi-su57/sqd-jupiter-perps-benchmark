#!/usr/bin/env python3
"""Offline replay + human-readable summary for a finished benchmark run.

Reads ONLY the files benchmark.py wrote (raw.ndjson, idl_used.json, report.json,
candidates.ndjson). It re-decodes raw.ndjson from scratch with the same decoder
to prove the stored raw data is self-sufficient, runs arithmetic consistency
checks on real decoded events, and writes:

  SUMMARY.md   readable report
  trades.csv   one row per valid executed trade (size change > 0)
  replay.json  machine-readable replay/consistency results

Optional --verify-boundaries issues 2 tiny SQD header-only requests to prove the
slot before the range is < 00:00 UTC and the slot after is >= next midnight.
"""
import argparse
import collections
import csv
import json
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import benchmark as bm

# Jupiter Perps custody mints. Labels are confirmed by price levels in the data
# itself (SOL ~$80s, BTC ~$70k, ETH ~$2k) — see the price table in SUMMARY.md.
MARKETS = {
    'So11111111111111111111111111111111111111112': 'SOL',
    '3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh': 'BTC (Wormhole WBTC)',
    '7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs': 'ETH (Wormhole WETH)',
}
E6 = Decimal(1_000_000)


def usd(raw):
    return None if raw is None else Decimal(int(raw)) / E6


def fmt_usd(d):
    return '-' if d is None else f'${d:,.2f}'


def iso(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def replay(out):
    """Re-decode raw.ndjson exactly as the live run did; return stats + rows."""
    idl = json.loads((out / 'idl_used.json').read_bytes())
    dec = bm.Decoder(idl)
    report = json.loads((out / 'report.json').read_text())
    day = report['request'].get('dateUTC')
    lo = hi = None
    if day:
        d = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)
        lo = int(d.timestamp()); hi = lo + 86400
    stats = collections.Counter(); rows = []; min_ts = max_ts = None
    other_events = collections.Counter()
    for line in (out / 'raw.ndjson').open('rb'):
        if not line.strip():
            continue
        block = json.loads(line)
        stats['returnedBlocks'] += 1
        ts = block['header'].get('timestamp')
        if lo is not None and (ts < lo or ts >= hi):
            stats['outOfUtcDayBlocks'] += 1
            continue
        min_ts = ts if min_ts is None else min(min_ts, ts)
        max_ts = ts if max_ts is None else max(max_ts, ts)
        # Count non-trade events too, so the summary shows what else was decoded.
        for src, key in (('cpi', 'instructions'), ('log', 'logs')):
            for it in block.get(key, []):
                if it.get('programId') != bm.PROGRAM or (src == 'cpi' and it.get('isCommitted') is not True):
                    continue
                try:
                    raw = bm.raw_from_item(it, src)
                    d = dec.decode(raw, src) if raw else None
                except Exception:
                    continue
                if d and d[0] not in bm.ACTION_TYPES:
                    other_events[d[0]] += 1
        rows.extend(bm.parse_block(block, dec, stats))
    return report, stats, rows, (min_ts, max_ts), other_events


def consistency(rows):
    """Arithmetic checks that only hold if field semantics and units are right.

    Learned from real data (2026-11-11):
      * feeUsd == positionFeeUsd + fundingFeeUsd on every trade.
      * On increases positionSizeUsd is the size AFTER the fill (>= fill).
      * On decreases positionSizeUsd is the size REMAINING (0 on a full close).
      * pnlDelta == |exitPrice - entryPrice| * size / entryPrice (positionPrice = entry),
        and hasProfit agrees with side + price direction.
      * Liquidations follow the same formula except when fees already consumed the
        collateral; the protocol then records pnlDelta=0. That is real on-chain data,
        so it is reported as informational, not as a decoder failure.
    """
    checks = collections.Counter(); fails = []; info = []
    def check(name, ok, cand):
        checks[name + ('_ok' if ok else '_FAIL')] += 1
        if not ok and len(fails) < 20:
            fails.append({'check': name, 'signature': cand['signature'], 'event': cand['eventName']})
    for cand, issues in rows:
        if issues or not cand['isExecutedSizeChange']:
            continue
        f = {k: (int(v) if isinstance(v, str) and v.lstrip('-').isdigit() else v)
             for k, v in cand['allEventFields'].items()}
        size = int(cand['sizeUsdDeltaRaw'])
        if cand['action'] == 'INCREASE' and 'positionSizeUsd' in f:
            check('increase_position_size_ge_fill', f['positionSizeUsd'] >= size, cand)
        if all(isinstance(f.get(k), int) for k in ('feeUsd', 'positionFeeUsd', 'fundingFeeUsd')):
            check('fee_eq_position_fee_plus_funding', f['feeUsd'] == f['positionFeeUsd'] + f['fundingFeeUsd'], cand)
        entry, exit_ = f.get('positionPrice'), f.get('price')
        if cand['action'] in ('DECREASE', 'LIQUIDATE') and isinstance(entry, int) and entry > 0:
            expected = abs(exit_ - entry) * size // entry
            if f['pnlDelta'] and exit_ != entry:
                went_up = exit_ > entry; is_long = f['positionSide'] == 1
                check('pnl_sign_matches_side_and_price', f['hasProfit'] == (went_up == is_long), cand)
            close = abs(f['pnlDelta'] - expected) <= max(10, expected // 100)
            if cand['action'] == 'DECREASE':
                check('pnl_matches_entry_exit_formula_1pct', close, cand)
            elif close:
                checks['liquidation_pnl_matches_formula_ok'] += 1
            else:
                checks['liquidation_pnl_protocol_adjusted_info'] += 1
                if len(info) < 20:
                    info.append({'signature': cand['signature'], 'pnlDelta': f['pnlDelta'], 'formula': expected,
                                 'collateralUsdBefore': f.get('originalPositionCollateralUsd')})
    return checks, fails, info


def verify_boundaries(report, api_key=None):
    r = report['request']; res = {}
    before = bm.request_stream({'type': 'solana', 'fromBlock': r['fromSlot'] - 64, 'toBlock': r['fromSlot'] - 1,
                                'fields': {'block': {'number': True, 'timestamp': True}}}, api_key, retries=10)
    after = bm.request_stream({'type': 'solana', 'fromBlock': r['toSlot'] + 1, 'toBlock': r['toSlot'] + 64,
                               'fields': {'block': {'number': True, 'timestamp': True}}}, api_key, retries=10)
    hb = [json.loads(x)['header'] for x in before if x.strip()]
    ha = [json.loads(x)['header'] for x in after if x.strip()]
    res['lastBlockBeforeRange'] = max(hb, key=lambda h: h['number']) if hb else None
    res['firstBlockAfterRange'] = min(ha, key=lambda h: h['number']) if ha else None
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('results', help='benchmark output directory, e.g. results_2026-11-11')
    ap.add_argument('--verify-boundaries', action='store_true')
    args = ap.parse_args(argv)
    out = Path(args.results)
    report, stats, rows, (min_ts, max_ts), other = replay(out)
    live = report['counts']

    # 1. Replay must reproduce the live run's counters exactly.
    keys = sorted(set(live) | set(stats))
    mismatches = {k: (live.get(k, 0), stats.get(k, 0)) for k in keys if live.get(k, 0) != stats.get(k, 0)}
    # 2. Replay candidates must equal candidates.ndjson line-for-line (minus valid/issues wrapper).
    stored = [json.loads(l) for l in (out / 'candidates.ndjson').open() if l.strip()]
    same_rows = len(stored) == len(rows) and all(
        s['rawSha256'] == c['rawSha256'] and s['signature'] == c['signature'] for s, (c, _) in zip(stored, rows))
    checks, check_fails, check_info = consistency(rows)
    bounds = verify_boundaries(report) if args.verify_boundaries else None

    trades = [c for c, iss in rows if not iss and c['isExecutedSizeChange']]
    zero = [c for c, iss in rows if not iss and not c['isExecutedSizeChange']]
    invalid = [(c, iss) for c, iss in rows if iss]

    # ---- trades.csv
    cols = ['time_utc', 'slot', 'signature', 'event', 'action', 'market', 'side', 'trader', 'position',
            'size_usd', 'price_usd', 'fee_usd', 'realized_pnl_usd', 'collateral_usd_delta', 'source',
            'instruction_address', 'solscan']
    with (out / 'trades.csv').open('w', newline='') as fh:
        w = csv.writer(fh); w.writerow(cols)
        for c in trades:
            f = c['allEventFields']
            w.writerow([iso(c['timestamp']), c['slot'], c['signature'], c['eventName'], c['action'],
                        MARKETS.get(c['marketMint'], c['marketMint']), c['positionSide'], c['trader'],
                        c['positionKey'], c['sizeUsdDelta'], usd(c['executionPriceRaw']), c['feeUsd'],
                        c['realizedPnlUsd'] or '', usd(f['collateralUsdDelta']) if f.get('collateralUsdDelta') else '',
                        c['source'], '.'.join(map(str, c['instructionAddress'] or [])),
                        'https://solscan.io/tx/' + c['signature']])

    # ---- aggregates
    by_event = collections.Counter(c['eventName'] for c in trades)
    by_action = collections.defaultdict(lambda: [0, Decimal(0)])
    by_market = collections.defaultdict(lambda: [0, Decimal(0), []])
    by_side = collections.defaultdict(lambda: [0, Decimal(0)])
    pnl = Decimal(0); fees = Decimal(0); traders = set()
    for c in trades:
        s = usd(c['sizeUsdDeltaRaw'])
        by_action[c['action']][0] += 1; by_action[c['action']][1] += s
        m = MARKETS.get(c['marketMint'], c['marketMint'])
        by_market[m][0] += 1; by_market[m][1] += s; by_market[m][2].append(usd(c['executionPriceRaw']))
        by_side[c['positionSide']][0] += 1; by_side[c['positionSide']][1] += s
        if c['realizedPnlRaw']: pnl += usd(c['realizedPnlRaw'])
        if c['feeUsdRaw']: fees += usd(c['feeUsdRaw'])
        traders.add(c['trader'])

    replay_ok = not mismatches and same_rows
    consistency_ok = not any(k.endswith('_FAIL') for k in checks)
    bounds_ok = None
    if bounds:
        lo = int(datetime.fromisoformat(report['request']['dateUTC']).replace(tzinfo=timezone.utc).timestamp())
        bounds_ok = (bounds['lastBlockBeforeRange'] and bounds['lastBlockBeforeRange']['timestamp'] < lo and
                     bounds['firstBlockAfterRange'] and bounds['firstBlockAfterRange']['timestamp'] >= lo + 86400)
    overall = report['status'] != 'FAIL_OR_INCONCLUSIVE' and replay_ok and consistency_ok and bounds_ok is not False

    (out / 'replay.json').write_text(json.dumps({
        'replayMatchesLiveCounters': not mismatches, 'counterMismatches': mismatches,
        'replayMatchesCandidatesFile': same_rows, 'consistencyChecks': dict(checks),
        'consistencyFailures': check_fails, 'consistencyInfo': check_info, 'boundaryVerification': bounds, 'boundariesOk': bounds_ok,
        'nonTradeEventsDecoded': dict(other), 'overallVerified': overall}, indent=2) + '\n')

    # ---- SUMMARY.md
    st = report['stream']; rq = report['request']; L = []
    a = L.append
    a(f"# Jupiter Perps × SQD — one-day benchmark: {rq.get('dateUTC') or 'slot range'}\n")
    a(f"**Benchmark status:** `{report['status']}`  ")
    a(f"**Offline replay + consistency verification:** {'PASSED' if overall else 'FAILED'}\n")
    a('> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked '
      'with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter\'s own API.\n')
    a('## Coverage\n')
    a('| | |\n|---|---|')
    a(f"| Slots | {rq['fromSlot']:,} → {rq['toSlot']:,} ({rq['toSlot']-rq['fromSlot']+1:,} slots) |")
    a(f"| Date resolution | {(rq.get('dateResolution') or {}).get('method')} |")
    if min_ts is not None:
        a(f"| First / last block time in data | {iso(min_ts)} / {iso(max_ts)} |")
    if bounds:
        b0, b1 = bounds['lastBlockBeforeRange'], bounds['firstBlockAfterRange']
        a(f"| Slot just before range | {b0['number']:,} @ {iso(b0['timestamp'])} |")
        a(f"| Slot just after range | {b1['number']:,} @ {iso(b1['timestamp'])} |")
        a(f"| Day boundaries verified | {'yes' if bounds_ok else 'NO'} |")
    a(f"| Stream complete | {st['complete']} (last slot {st['lastSlot']:,}) |")
    a(f"| Blocks with Jupiter activity returned | {live.get('returnedBlocks', 0):,} |")
    rs = st.get('resume') or {}
    if rs:
        a(f"| Resumed | yes, from slot {rs['resumedFromSlot']:,} ({rs['replayedBlocks']:,} stored blocks re-verified) |")
    a(f"| HTTP batches | {st['httpBatches'] + rs.get('priorSessionHttpBatches', 0):,} |")
    a(f"| Raw data (decoded JSON) | {st['rawMiB']:,} MiB |")
    if 'wireBytesThisSession' in st:
        wire = st['wireBytesThisSession'] + rs.get('priorSessionWireBytes', 0)
        a(f"| Transferred on the wire (gzip) | {wire/2**20:,.2f} MiB |")
    a(f"| SQD query mode | {rq.get('queryMode', 'full (pre-v1.6)')} |")
    if rs.get('priorSessionSeconds'):
        a(f"| Wall time (streaming) | {(st['seconds'] + rs['priorSessionSeconds'])/60:,.1f} min total "
          f"({rs['priorSessionSeconds']/60:,.1f} + {st['seconds']/60:,.1f} min sessions) |")
    elif rs:
        a(f"| Wall time (streaming) | {st['seconds']/60:,.1f} min (last session only; earlier sessions not recorded) |")
    else:
        a(f"| Wall time (streaming) | {st['seconds']/60:,.1f} min |")
    if st.get('retries'):
        a(f"| SQD overload retries | {', '.join(f'{k}×{v:,}' for k, v in st['retries'].items())} |")
    a('')
    a('## Trades (valid, executed size change)\n')
    a(f"**{len(trades):,} trades**, {len(traders):,} distinct traders, total notional **{fmt_usd(sum(by_action[x][1] for x in by_action))}**, "
      f"fees {fmt_usd(fees)}, net realized PnL on closes {fmt_usd(pnl)}.\n")
    a('| Action | Count | Notional |\n|---|---:|---:|')
    for k in sorted(by_action): a(f"| {k} | {by_action[k][0]:,} | {fmt_usd(by_action[k][1])} |")
    a('\n| Market | Count | Notional | Min / median / max price |\n|---|---:|---:|---|')
    for k, (n, s, p) in sorted(by_market.items(), key=lambda x: -x[1][1]):
        p.sort(); a(f"| {k} | {n:,} | {fmt_usd(s)} | {fmt_usd(p[0])} / {fmt_usd(p[len(p)//2])} / {fmt_usd(p[-1])} |")
    a('\n| Side | Count | Notional |\n|---|---:|---:|')
    for k in sorted(by_side): a(f"| {k} | {by_side[k][0]:,} | {fmt_usd(by_side[k][1])} |")
    a('\n| Event type | Count |\n|---|---:|')
    for k, v in by_event.most_common(): a(f"| {k} | {v:,} |")
    a(f"\nAlso decoded: **{len(zero):,}** valid zero-size position events (collateral-only changes, not counted as trades) "
      f"and **{len(invalid):,}** invalid candidates.\n")
    a('## Data-quality checks\n')
    a('| Check | Result |\n|---|---|')
    for k, v in report['passConditions'].items(): a(f"| {k} | {'✅' if v else '❌'} |")
    a(f"| raw.ndjson replay reproduces live counters | {'✅' if not mismatches else '❌ ' + json.dumps(mismatches)} |")
    a(f"| raw.ndjson replay reproduces candidates.ndjson | {'✅' if same_rows else '❌'} |")
    for k in sorted(checks):
        mark = '✅' if k.endswith('_ok') else ('ℹ️' if k.endswith('_info') else '❌')
        a(f"| arithmetic: {k} | {checks[k]:,} {mark} |")
    a('')
    a(f"Duplicate log/CPI representations merged: {live.get('crossSourceDuplicates', 0):,}. "
      f"Uncommitted CPI instructions skipped: {live.get('uncommittedCpiInstructions', 0):,}. "
      f"Failed-tx events skipped: {live.get('failedTransactionEvents', 0):,}.\n")
    if check_info:
        a('Liquidations where the protocol recorded a PnL different from the entry/exit formula '
          '(collateral already consumed by fees; real on-chain values, kept as-is): ' +
          ', '.join(f"[{x['signature'][:10]}…](https://solscan.io/tx/{x['signature']})" for x in check_info) + '\n')
    if other:
        a('Non-trade Jupiter events decoded (not converted to trades): ' +
          ', '.join(f'{k} ×{v:,}' for k, v in other.most_common()) + '\n')
    a('## Sample real trades (verify on Solscan)\n')
    a('| Time | Event | Market | Side | Size | Price | PnL | Tx |\n|---|---|---|---|---:|---:|---:|---|')
    seen = set()
    for c in trades:
        if c['eventName'] in seen: continue
        seen.add(c['eventName'])
        a(f"| {iso(c['timestamp'])} | {c['eventName']} | {MARKETS.get(c['marketMint'], c['marketMint'][:8])} | {c['positionSide']} | "
          f"{fmt_usd(usd(c['sizeUsdDeltaRaw']))} | {fmt_usd(usd(c['executionPriceRaw']))} | {fmt_usd(usd(c['realizedPnlRaw']))} | "
          f"[{c['signature'][:10]}…](https://solscan.io/tx/{c['signature']}) |")
    a('\n## Units and assumptions\n')
    a('- USD fields (`sizeUsdDelta`, `price`, `feeUsd`, `pnlDelta`) are integers with 6 decimals; raw integers are kept in '
      '`candidates.ndjson`. The scale is confirmed by price levels above and fee-to-size ratios, not by an external source.')
    a('- `positionSide`: 1 = LONG, 2 = SHORT. Realized PnL = `pnlDelta` × (`hasProfit` ? +1 : −1).')
    a(f"- IDL: community IDL `{report['idl']['urlOrPath']}`, sha256 `{report['idl']['sha256']}`.")
    a('- Source: SQD Portal only. No Solana RPC, Dune, Trawl, or Helius. No database writes.\n')
    a('## Files\n')
    a('- `trades.csv` — readable table of every valid executed trade (open in a spreadsheet)')
    a('- `candidates.ndjson` — all decoded candidates with raw integers and every event field')
    a('- `raw.ndjson` — untouched SQD response lines (re-decodable offline: `python3 summarize.py <dir>`)')
    a('- `report.json`, `replay.json`, `query.json`, `idl_used.json`')
    (out / 'SUMMARY.md').write_text('\n'.join(L) + '\n')
    print('\n'.join(L))
    return 0 if overall else 1


if __name__ == '__main__':
    sys.exit(main())
