#!/usr/bin/env bash
# =============================================================================
#  Jupiter Perps x SQD Portal benchmark: @DESC@
#  UTC days @FROM@ .. @TO@ (@NDAYS@ days). Single self-contained file. Just run it:
#
#      bash @FILE@            start (or resume) in background
#      bash @FILE@ status     per-day progress table
#      bash @FILE@ log        follow live progress (Ctrl+C to quit watching)
#      bash @FILE@ stop       stop the background run
#
#  It unpacks next to itself into ./jupiter_sqd_benchmark/ (shared by all launchers,
#  so days verified by one launcher are skipped by the next), self-tests, then runs
#  every day in the background (survives closing the terminal / SSH), retrying SQD
#  overload errors and resuming interrupted days automatically. It re-starts itself
#  after a server reboot until all days are verified (tagged @reboot crontab line,
#  removed when done; NO_AUTOSTART=1 disables). Lean gzip SQD queries (v1.6).
#  Read-only: SQD Portal only, no RPC, no database writes, no Lucky Plans repos.
#  Optional: SQD_API_KEY=... bash @FILE@   (sent as Authorization: Bearer)
# =============================================================================
set -uo pipefail
FROM="@FROM@"
TO="@TO@"
LABEL="@LABEL@"
ANCHOR="@ANCHOR@"             # known SQD slot inside the range (date-fallback hint)
MIN_FREE_GB=@MINGB@
SELF="$(readlink -f "$0")"
WORK="$(dirname "$SELF")/jupiter_sqd_benchmark"
PIDFILE="$WORK/runner.pid"            # one runner per folder, whichever launcher started it
LOG="$WORK/data/runner_logs/runner_${LABEL}.log"
CRON_TAG="# jupiter-sqd-benchmark-${LABEL}"

say()  { printf '%s\n' "$*"; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
running() { [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; }

unpack() {
  mkdir -p "$WORK/data/runner_logs" || die "cannot create $WORK"
  # Code files are refreshed every start; data/ (results, logs) is never touched.
  sed -n '/^__PAYLOAD_BELOW__$/,$p' "$SELF" | tail -n +2 | base64 -d | tar xzf - -C "$WORK" \
    || die "embedded package is corrupt (re-download this file)"
}

preflight() {
  command -v python3 >/dev/null || die "python3 not found (sudo apt install python3)"
  python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' || die "python3 >= 3.9 required"
  local free_gb; free_gb=$(df -Pk "$WORK" | awk 'NR==2{print int($4/1048576)}')
  [ "${free_gb:-0}" -ge "$MIN_FREE_GB" ] || die "need ${MIN_FREE_GB} GB free disk, have ${free_gb} GB"
  (cd "$WORK" && python3 -m unittest discover -s tests >/dev/null 2>"$WORK/data/runner_logs/selftest.log") \
    || die "self-test failed, see $WORK/data/runner_logs/selftest.log"
  python3 - <<'EOF' || say "WARNING: SQD Portal not reachable right now; the runner will keep retrying."
import urllib.request, sys
req = urllib.request.Request('https://portal.sqd.dev/datasets/solana-mainnet/metadata',
                             headers={'User-Agent': 'LuckyPlans-SQD-AccuracyBenchmark/1.4'})
try: urllib.request.urlopen(req, timeout=20).read(); sys.exit(0)
except urllib.error.HTTPError as e: sys.exit(0 if e.code in (429, 529) else 1)   # overloaded = reachable
except Exception: sys.exit(1)
EOF
}

cron_add() {   # auto-restart after reboot; removed automatically when all days are verified
  [ -n "${NO_AUTOSTART:-}" ] && return 0          # NO_AUTOSTART=1 bash <file>  -> skip
  command -v crontab >/dev/null || return 0
  (crontab -l 2>/dev/null | grep -vF "$CRON_TAG"; echo "@reboot bash '$SELF' >/dev/null 2>&1 $CRON_TAG") | crontab - 2>/dev/null || true
}
cron_remove() {
  [ -n "${NO_AUTOSTART:-}" ] && return 0
  command -v crontab >/dev/null || return 0
  crontab -l 2>/dev/null | grep -qF "$CRON_TAG" || return 0
  crontab -l 2>/dev/null | grep -vF "$CRON_TAG" | crontab - 2>/dev/null || true
}

start() {
  if running; then
    say "A benchmark is already running in $WORK (pid $(cat "$PIDFILE")). Progress:"; status; return 0
  fi
  say "Unpacking to $WORK ..."; unpack
  say "Checking python, disk space, self-tests, SQD reachability ..."; preflight
  cron_add
  cd "$WORK"
  # setsid + nohup: keeps running after the terminal/SSH session closes.
  CRON_TAG="$CRON_TAG" ANCHOR="$ANCHOR" nohup setsid bash -c '
    echo "$(date -u +%FT%TZ) runner started for '"$FROM"' .. '"$TO"'"
    bash scripts/run_range.sh '"$FROM"' '"$TO"'; rc=$?
    if [ "$rc" = 0 ]; then
      echo "$(date -u +%FT%TZ) RANGE COMPLETE: all days verified. See data/RANGE_SUMMARY_'"$FROM"'_'"$TO"'.txt"
      if [ -z "${NO_AUTOSTART:-}" ] && command -v crontab >/dev/null; then crontab -l 2>/dev/null | grep -vF "$CRON_TAG" | crontab - 2>/dev/null; fi
    else
      echo "$(date -u +%FT%TZ) runner finished with unverified days (exit $rc). Run this file again to retry them."
    fi
    rm -f runner.pid' >>"$LOG" 2>&1 < /dev/null &
  echo $! > "$PIDFILE"
  say ""
  say "Started in background (pid $(cat "$PIDFILE")). You can close this window."
  say "Expected: @ETA@"
  say ""
  say "  Progress:   bash $(basename "$SELF") status"
  say "  Live log:   bash $(basename "$SELF") log"
  say "  Stop:       bash $(basename "$SELF") stop"
  say "  Results:    $WORK/data/results_YYYY-MM-DD/SUMMARY.md and $WORK/data/RANGE_SUMMARY_${FROM}_${TO}.txt"
}

status() {
  [ -d "$WORK" ] || { say "Not started yet. Run: bash $(basename "$SELF")"; return 0; }
  if running; then say "State: RUNNING (pid $(cat "$PIDFILE"))"
  elif grep -q "RANGE COMPLETE" "$LOG" 2>/dev/null; then say "State: COMPLETE"
  else say "State: NOT RUNNING (run this file again to continue)"; fi
  say ""
  [ -f "$WORK/scripts/run_range.sh" ] && { (cd "$WORK" && bash scripts/run_range.sh "$FROM" "$TO" status) || true; }
  say ""; say "Recent activity:"; tail -n 5 "$LOG" 2>/dev/null | sed 's/^/  /'
  local cur; cur=$(ls -t "$WORK"/data/logs/*.log 2>/dev/null | head -1)
  [ -n "$cur" ] && say "  current day: $(tail -n 1 "$cur" | cut -c1-140)"
  return 0
}

stop() {
  cron_remove
  if running; then kill -- -"$(cat "$PIDFILE")" 2>/dev/null || kill "$(cat "$PIDFILE")"; rm -f "$PIDFILE"
    say "Stopped. Run this file again any time to resume where it left off."
  else say "Not running."; fi
}

case "${1:-start}" in
  start)  start ;;
  status) status ;;
  log)    [ -f "$LOG" ] || die "not started yet"; tail -n 20 -F "$LOG" "$WORK"/data/logs/*.log ;;
  stop)   stop ;;
  *)      say "usage: bash $(basename "$SELF") [start|status|log|stop]"; exit 2 ;;
esac
exit $?

__PAYLOAD_BELOW__
