#!/usr/bin/env bash
# Build a single-file launcher for a UTC day range:
#   bash scripts/build_launcher.sh FROM TO LABEL ANCHOR_SLOT "description" "ETA text" MIN_FREE_GB
set -euo pipefail
cd "$(dirname "$0")/.."
FROM=$1 TO=$2 LABEL=$3 ANCHOR=$4 DESC=$5 ETA=$6 MINGB=${7:-3}
NDAYS=$(python3 -c "import sys;from datetime import date as d;print((d.fromisoformat(sys.argv[2])-d.fromisoformat(sys.argv[1])).days+1)" "$FROM" "$TO")
mkdir -p dist
OUT="dist/run_jupiter_benchmark_${LABEL}.sh"
FILES=(benchmark.py summarize.py compare_runs.py jupiter-perpetuals-idl.json README.md
       scripts/run_one_day.sh scripts/run_range.sh scripts/run_month.sh tests/test_*.py)
{ sed -e "s|@FROM@|$FROM|g" -e "s|@TO@|$TO|g" -e "s|@LABEL@|$LABEL|g" -e "s|@ANCHOR@|$ANCHOR|g" \
      -e "s|@DESC@|$DESC|g" -e "s|@ETA@|$ETA|g" -e "s|@MINGB@|$MINGB|g" -e "s|@NDAYS@|$NDAYS|g" \
      -e "s|@FILE@|$(basename "$OUT")|g" scripts/launcher_header.sh
  tar czf - "${FILES[@]}" | base64 -w 76; } > "$OUT"
chmod +x "$OUT"; bash -n "$OUT"
grep -q '@[A-Z]*@' <(sed '/^__PAYLOAD_BELOW__$/q' "$OUT") && { echo "unfilled placeholder in $OUT"; exit 1; }
echo "built $OUT ($(du -h "$OUT" | cut -f1), $NDAYS days)"
