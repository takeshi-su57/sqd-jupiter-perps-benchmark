#!/usr/bin/env bash
# Benchmark a range of UTC days = one independently resumable/verifiable run per day.
#   bash scripts/run_range.sh 2026-01-01 2026-01-07          # run (or continue) those days
#   bash scripts/run_range.sh 2026-01-01 2026-01-07 status   # only print the per-day status table
# Safe to stop (Ctrl+C) and start again: verified days are skipped, others resume.
set -uo pipefail
cd "$(dirname "$0")/.."
FROM="${1:?usage: bash run_range.sh YYYY-MM-DD YYYY-MM-DD [status]}"
TO="${2:?usage: bash run_range.sh YYYY-MM-DD YYYY-MM-DD [status]}"
MODE="${3:-run}"
ATTEMPTS="${ATTEMPTS:-5}"          # tries per day per pass
PASSES="${PASSES:-3}"              # full passes over not-yet-verified days
ANCHOR="${ANCHOR:-}"               # optional known slot near the range (date-fallback hint)
DAYLIST=$(python3 -c "
import sys; from datetime import date, timedelta
a, b = date.fromisoformat(sys.argv[1]), date.fromisoformat(sys.argv[2])
assert a <= b and (b - a).days < 400
print(' '.join(str(a + timedelta(i)) for i in range((b - a).days + 1)))" "$FROM" "$TO") \
  || { echo "bad range: $FROM .. $TO (expected YYYY-MM-DD YYYY-MM-DD, from <= to)"; exit 2; }
SUMMARY="data/RANGE_SUMMARY_${FROM}_${TO}.txt"

verified() { python3 -c "import json,sys;sys.exit(0 if json.load(open(sys.argv[1])).get('overallVerified') else 1)" \
  "data/results_$1/replay.json" 2>/dev/null; }

status_table() {
  python3 - $DAYLIST <<'PYEOF'
import csv, json, sys
from pathlib import Path
days = sys.argv[1:]
tot = dict(trades=0, notional=0.0, mib=0.0, wire=0.0, minutes=0.0); ok = 0
print(f"{'day':<12}{'status':<24}{'verified':<10}{'trades':>8}{'notional $':>16}{'raw MiB':>9}{'wire MiB':>9}{'min':>7}")
for day in days:
    out = Path(f"data/results_{day}")
    try: r = json.loads((out / 'report.json').read_text())
    except Exception: print(f"{day:<12}{'not run':<24}"); continue
    try: v = json.loads((out / 'replay.json').read_text()).get('overallVerified')
    except Exception: v = None
    s = r.get('stream') or {}; c = r.get('counts') or {}; rs = s.get('resume') or {}
    mins = (s.get('seconds', 0) + rs.get('priorSessionSeconds', 0)) / 60
    known = 'wireBytesThisSession' in s
    wire = (s.get('wireBytesThisSession', 0) + rs.get('priorSessionWireBytes', 0)) / 2**20
    notional = 0.0
    try:
        with (out / 'trades.csv').open() as fh:
            notional = sum(float(row['size_usd']) for row in csv.DictReader(fh))
    except Exception: pass
    t = c.get('validExecutedTrades', 0)
    print(f"{day:<12}{r.get('status','?'):<24}{str(bool(v)):<10}{t:>8,}{notional:>16,.0f}{s.get('rawMiB',0):>9.1f}{(f'{wire:.1f}' if known else 'n/a'):>9}{mins:>7.0f}")
    if v:
        ok += 1; tot['trades'] += t; tot['notional'] += notional; tot['mib'] += s.get('rawMiB', 0)
        tot['wire'] += wire; tot['minutes'] += mins
print(f"\n{ok}/{len(days)} days verified | verified totals: {tot['trades']:,} trades, ${tot['notional']:,.0f} notional, "
      f"{tot['mib']:,.1f} MiB raw, {tot['wire']:,.1f} MiB on the wire, {tot['minutes']/60:,.1f} h streaming")
sys.exit(0 if ok == len(days) else 1)
PYEOF
}

if [ "$MODE" = status ]; then status_table; exit $?; fi

mkdir -p data/logs
EXTRA=(); [ -n "$ANCHOR" ] && EXTRA=(--anchor-slot "$ANCHOR")
for pass in $(seq 1 "$PASSES"); do
  pending=0
  for day in $DAYLIST; do
    if verified "$day"; then [ "$pass" = 1 ] && echo "$day: already verified, skipping"; continue; fi
    for a in $(seq 1 "$ATTEMPTS"); do
      echo "$(date -u +%FT%TZ) $day: pass $pass, attempt $a/$ATTEMPTS (log: data/logs/$day.log)"
      bash scripts/run_one_day.sh "$day" "${EXTRA[@]}" >>"data/logs/$day.log" 2>&1
      if verified "$day"; then echo "$(date -u +%FT%TZ) $day: VERIFIED"; break; fi
      echo "$(date -u +%FT%TZ) $day: not verified yet; resuming in 60s"; sleep 60
    done
    verified "$day" || pending=$((pending+1))
  done
  [ "$pending" = 0 ] && break
  echo "$(date -u +%FT%TZ) pass $pass done, $pending day(s) still unverified; waiting 10 min before next pass"; sleep 600
done
echo; status_table | tee "$SUMMARY"; exit "${PIPESTATUS[0]}"
