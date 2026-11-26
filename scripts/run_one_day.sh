#!/usr/bin/env bash
# Real SQD one-day run (no offline fixtures). Safe to re-run: --resume continues an
# interrupted download from raw.ndjson instead of starting over.
#   bash scripts/run_one_day.sh 2026-11-11 [extra benchmark.py args, e.g. --anchor-slot N]
set -uo pipefail
cd "$(dirname "$0")/.."
DAY="${1:-2026-11-11}"; shift || true
OUT="./data/results_${DAY}"
mkdir -p data
IDL_ARGS=()
# Pinned IDL (sha256 f2d7ff50...) so every day of a month decodes with the same schema.
[ -f jupiter-perpetuals-idl.json ] && IDL_ARGS=(--idl jupiter-perpetuals-idl.json)
rc=0
python3 benchmark.py --date-utc "$DAY" --out "$OUT" --resume "${IDL_ARGS[@]}" "$@" > "$OUT.report.stdout.json" || rc=$?
echo "benchmark exit code: $rc (0 = PASS)" >&2
python3 summarize.py "$OUT" --verify-boundaries > /dev/null && echo "summary: verified -> $OUT/SUMMARY.md" >&2 \
  || echo "summary: NOT verified -> see $OUT/SUMMARY.md and $OUT/replay.json" >&2
exit $rc
