#!/usr/bin/env bash
# One-month benchmark: bash scripts/run_month.sh 2026-01 [status]   (wrapper around run_range.sh)
set -uo pipefail
cd "$(dirname "$0")/.."
MONTH="${1:?usage: bash scripts/run_month.sh YYYY-MM [status]}"
read -r FIRST LAST < <(python3 -c "
import calendar,sys; y,m=map(int,sys.argv[1].split('-')); print(f'{y:04d}-{m:02d}-01', f'{y:04d}-{m:02d}-{calendar.monthrange(y,m)[1]:02d}')" "$MONTH") \
  || { echo "bad month: $MONTH (expected YYYY-MM)"; exit 2; }
exec bash scripts/run_range.sh "$FIRST" "$LAST" "${@:2}"
