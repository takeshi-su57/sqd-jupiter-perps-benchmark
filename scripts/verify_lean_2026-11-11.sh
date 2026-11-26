#!/usr/bin/env bash
# ONE-DAY verification of the v1.6 lean+gzip SQD query.
# Re-downloads 2026-11-11 (already verified with the v1.5 full query in ./data/results_2026-11-11)
# into a SEPARATE folder and requires identical decoded output.
#   bash scripts/verify_lean_2026-11-11.sh      (safe to re-run: resumes if interrupted)
set -uo pipefail
cd "$(dirname "$0")/.."
REF=./data/results_2026-11-11            # v1.5 full-query reference (never modified by this script)
OUT=./data/results_2026-11-11_lean
[ -f "$REF/candidates.ndjson" ] || { echo "missing reference $REF (v1.5 full-query run)"; exit 2; }
echo "Step 1/3: download 2026-11-11 with the lean+gzip query -> $OUT (log: $OUT.log)"
python3 benchmark.py --date-utc 2026-11-11 --out "$OUT" --resume --idl jupiter-perpetuals-idl.json \
  > "$OUT.report.stdout.json" 2> "$OUT.log"
echo "  benchmark exit code: $? (0 = PASS)"
echo "Step 2/3: offline replay + consistency + day-boundary checks"
python3 summarize.py "$OUT" --verify-boundaries > /dev/null && echo "  verified -> $OUT/SUMMARY.md" \
  || echo "  NOT verified -> see $OUT/SUMMARY.md"
echo "Step 3/3: compare with the v1.5 full-query reference"
python3 compare_runs.py "$REF" "$OUT"
