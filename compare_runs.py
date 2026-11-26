#!/usr/bin/env python3
"""Compare two benchmark result folders for the same slot range.

Used to prove the v1.6 lean+gzip query returns exactly the same decoded Jupiter
events as the v1.5 full query:

    python3 compare_runs.py results_2026-11-11 results_2026-11-11_lean

Exit 0 only if both runs completed the same range and candidates.ndjson is
identical row-for-row (same events, same order, same fields and raw integers).
"""
import json
import sys
from pathlib import Path


def load(folder):
    folder = Path(folder)
    report = json.loads((folder / 'report.json').read_text())
    rows = [json.loads(line) for line in (folder / 'candidates.ndjson').open() if line.strip()]
    return report, rows


def wire_mib(report):
    s = report['stream']
    if 'wireBytesThisSession' not in s:
        return None
    return (s['wireBytesThisSession'] + (s.get('resume') or {}).get('priorSessionWireBytes', 0)) / 2**20


def main(argv):
    if len(argv) != 2:
        print(__doc__); return 2
    (ra, a), (rb, b) = load(argv[0]), load(argv[1])
    ok = True
    print(f"{'':34}{'A: ' + Path(argv[0]).name:>30}{'B: ' + Path(argv[1]).name:>34}")
    for label, fa, fb in [
        ('status', ra['status'], rb['status']),
        ('query mode', ra['request'].get('queryMode', 'full (pre-v1.6)'), rb['request'].get('queryMode', 'full (pre-v1.6)')),
        ('slot range', f"{ra['request']['fromSlot']}..{ra['request']['toSlot']}", f"{rb['request']['fromSlot']}..{rb['request']['toSlot']}"),
        ('stream complete', ra['stream']['complete'], rb['stream']['complete']),
        ('raw MiB (decoded JSON)', ra['stream']['rawMiB'], rb['stream']['rawMiB']),
        ('MiB on the wire', wire_mib(ra), wire_mib(rb)),
        ('candidates', len(a), len(b)),
        ('valid executed trades', ra['counts'].get('validExecutedTrades'), rb['counts'].get('validExecutedTrades')),
        ('invalid candidates', ra['counts'].get('invalidCandidates', 0), rb['counts'].get('invalidCandidates', 0)),
    ]:
        fmt = lambda v: 'n/a' if v is None else (f'{v:,.2f}' if isinstance(v, float) else str(v))
        print(f'{label:34}{fmt(fa):>30}{fmt(fb):>34}')

    if (ra['request']['fromSlot'], ra['request']['toSlot']) != (rb['request']['fromSlot'], rb['request']['toSlot']):
        print('\nFAIL: runs cover different slot ranges; nothing to compare.'); return 1
    if not (ra['stream']['complete'] and rb['stream']['complete']):
        print('\nFAIL: at least one run did not stream its full range.'); ok = False
    if a == b:
        print(f'\nIDENTICAL: all {len(a):,} decoded candidates match row-for-row (fields, raw integers, order).')
    else:
        ok = False
        key = lambda r: (r['slot'], r['transactionIndex'], r['source'], str(r['instructionAddress']), r['rawSha256'])
        ka, kb = {key(r): r for r in a}, {key(r): r for r in b}
        only_a, only_b = sorted(set(ka) - set(kb)), sorted(set(kb) - set(ka))
        changed = [k for k in set(ka) & set(kb) if ka[k] != kb[k]]
        print(f'\nDIFFERENT: {len(only_a)} only in A, {len(only_b)} only in B, {len(changed)} changed.')
        for title, keys, src in (('only in A', only_a, ka), ('only in B', only_b, kb)):
            for k in keys[:5]:
                r = src[k]
                print(f"  {title}: slot {r['slot']} {r['eventName']} https://solscan.io/tx/{r['signature']}")
        for k in changed[:5]:
            diff = sorted(f for f in set(ka[k]) | set(kb[k]) if ka[k].get(f) != kb[k].get(f))
            print(f"  changed: slot {k[0]} fields {diff}")
    wa, wb = wire_mib(ra), wire_mib(rb)
    base = wa if wa is not None else ra['stream']['rawMiB']
    if wb:
        print(f"Transfer: B moved {wb:,.2f} MiB vs A {base:,.2f} MiB ({base / wb:,.1f}x less).")
    print('RESULT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
