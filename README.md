# SQD × Jupiter Perps benchmark

This tool backfills Jupiter Perpetuals trade events (program `PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu`) from the
**SQD Portal** (`solana-mainnet/finalized-stream`). It decodes them with a pinned Anchor IDL and proves the decoding
is right, one UTC day at a time.

- **Read-only.** It uses only the SQD Portal: no Solana RPC, Dune, Trawl or Helius, and it makes no database writes.
- It does not touch the Lucky Plans repositories.

## Results

| Run | Days | Valid trades | Notional | Wire | Streaming |
|---|---:|---:|---:|---:|---:|
| 2026-11-11, full query (v1.5) | 1 | 10,660 | $198M | 121.7 MiB (raw) | 128 min |
| 2026-11-11, lean + gzip (v1.6) | 1 | 10,660, **identical** | $198M | 13.5 MiB | 182 min |
| January 2026 (v1.6) | **31/31 verified** | **688,772** | **$9.72B** | 722 MiB | 65 h |

- Every day ended `PASS_STRUCTURAL_ONLY` with `overallVerified: true`. That means the offline replay reproduced the
  live output exactly, every arithmetic check passed, and both day boundaries were proven by real block timestamps.
- The per-day reports are in [`reports/`](reports/). Start with
  [`reports/2026-01/RANGE_SUMMARY_2026-01-01_2026-01-31.txt`](reports/2026-01/RANGE_SUMMARY_2026-01-01_2026-01-31.txt).
- `PASS_STRUCTURAL_ONLY` means the day streamed completely, decoded with no structural or decoder failures under the
  pinned IDL, and contained executed trades.
- It does **not** prove independent PnL accuracy, coverage of every historical program version, or production
  readiness. That needs a `--reference` comparison against an independent source.

## Layout

```
benchmark.py              stream one slot range / UTC day from SQD, decode, write results
summarize.py              offline replay + consistency checks -> SUMMARY.md, trades.csv, replay.json
compare_runs.py           compare two runs of the same range (exit 0 only if decoded rows are identical)
jupiter-perpetuals-idl.json  pinned community IDL (sha256 f2d7ff50...)
scripts/                  run_one_day.sh, run_range.sh, run_month.sh, verify_lean_2026-11-11.sh,
                          build_launcher.sh + launcher_header.sh (single-file launchers)
tests/                    offline unit tests
reports/                  committed small results: SUMMARY.md / report.json / replay.json per day
data/      (gitignored)   fetched data: results_YYYY-MM-DD/, logs/, RANGE_SUMMARY_*.txt (~3 GB for January)
dist/      (gitignored)   built launchers
```

## Usage

Run everything from the repository root. Python 3.9 or later is needed, with no third-party packages.

```bash
python3 -m unittest discover -s tests            # offline tests (31)
bash scripts/run_one_day.sh 2026-11-11           # one day -> data/results_2026-11-11/ (+ summarize, verified)
bash scripts/run_range.sh 2026-01-01 2026-01-07  # day range; verified days are skipped, others resume
bash scripts/run_range.sh 2026-01-01 2026-01-31 status   # per-day status table only
bash scripts/run_month.sh 2026-02                # whole month (wrapper around run_range.sh)
bash scripts/verify_lean_2026-11-11.sh           # re-download 2026-11-11 lean and compare to the full-query run
```

- For dates far from known anchors, pass `ANCHOR=<slot near the range>` to `run_range.sh`, or `--anchor-slot` to
  `run_one_day.sh`. Known anchors:
  - 2026-01-01: `390490507`
  - 2026-01-15: `393549073`
  - 2026-02-01: `397234292`
  - 2026-11-11: `468300000`
- Every run uses `--resume`, so it is safe to stop and start again. The stored `raw.ndjson` is replayed, and a torn
  last line is dropped, before streaming continues.
- If a day's stored data came from a different query shape, it is moved aside to `results_DAY.superseded-*` rather
  than deleted.
- With an API key, run `SQD_API_KEY=... bash scripts/run_range.sh ...`. The key is sent as `Authorization: Bearer`.
  SQD lists a free "Testing" plan with more throughput.

### Single-file launchers (for a server)

```bash
bash scripts/build_launcher.sh 2026-01-01 2026-01-31 2026-01 393549073 \
  "ONE-MONTH benchmark, January 2026" "roughly 50-70 hours total, ~3 GB disk" 4
# -> dist/run_jupiter_benchmark_2026-01.sh
```

Copy only that file to the server and run `bash run_jupiter_benchmark_2026-01.sh`. It has `status`, `log` and `stop`
subcommands.

- **What it does:** it unpacks itself into `./jupiter_sqd_benchmark/` next to itself, runs a self-test, then runs in
  the background with `nohup` and `setsid`.
- **Shared folder:** every launcher uses that same folder, so days already verified by one launcher are skipped by
  the next.
- **Reboots:** it re-starts after a reboot through a tagged `@reboot` crontab line, which is removed once every day
  is verified. Set `NO_AUTOSTART=1` to disable this.

### Output per day (`data/results_YYYY-MM-DD/`)

| File | Contents |
|---|---|
| `SUMMARY.md` | human-readable result; start here |
| `trades.csv` | one row per valid executed trade |
| `candidates.ndjson` | decoded candidate events inside the UTC day |
| `raw.ndjson` | unmodified SQD JSON Lines, including boundary padding |
| `query.json` / `idl_used.json` | exact SQD request and IDL used (provenance) |
| `report.json` | stream statistics, validation and date resolution |
| `replay.json` | offline replay and consistency results (`overallVerified`) |

## How correctness is checked

### During streaming

- SQD returned the requested final slot and the stream completed.
- Anchor data decoded with no unexpected logs and no missing transaction links.
- Signatures and instruction addresses are valid.
- Zero-size position events are kept but not counted as trades.

### Offline (`summarize.py`)

It re-decodes `raw.ndjson` from scratch, and must reproduce the live counters and `candidates.ndjson` exactly. Then
it runs checks that only pass if the field meanings and units are right:

- `feeUsd == positionFeeUsd + fundingFeeUsd`
- On increases, `positionSizeUsd >= sizeUsdDelta`, because the field holds the size after the fill.
- On decreases, `pnlDelta == |price - positionPrice| * size / positionPrice` within ±1%, and `hasProfit` agrees
  with the side and the price direction.
- Liquidations where fees had already consumed the collateral record `pnlDelta = 0` on chain. These are reported as
  informational, not counted as failures.

### Boundaries (`--verify-boundaries`)

Two small header requests prove that the slot before the range is before 00:00 UTC, and that the slot after it is
at or after the next midnight.

## Verified facts about the data

- SQD `kind=data` log messages are **base64**, not base58.
- Jupiter events are Anchor `emit_cpi!` events: CPI tag `e445a52e51cb9a1d`, Borsh-encoded payloads.
- USD and price fields use a 1e6 scale.
- `positionSide`: 1 = LONG, 2 = SHORT.
- On decreases, `positionSizeUsd` is the remaining size.
- Markets: `So111…` = SOL, `3NZ9JMVB…` = BTC, `7vfCXTUX…` = ETH.
- Slot time is about 215 ms in late 2026 (a UTC day is about 402k slots) and about 395 ms in January 2026 (about
  218k slots).

## SQD Portal usage notes

- **Public Portal throttling:** it rate-limits by data volume, returning HTTP 529 "overloaded" with `Retry-After`
  of about 10 s. Retries use backoff (`--retries`, default 60). At 1–3 hours per day, throttling, not bandwidth,
  sets the run time.
- **Response size:** each response ends after a server-side scan budget, so the client cannot choose a bigger
  batch.
- **Lean query (v1.6 default):** a server-side `d8 = 0xe445a52e51cb9a1d` filter plus `isCommitted: true` on the
  Jupiter instruction filter, with gzip on top. That is 9× less transfer than v1.5, with byte-identical decoded
  output. `--query-mode full` restores the v1.5 behaviour.

## History

| Version | Change |
|---|---|
| v1.6 | Lean query + gzip, 31-day January run, single-file launchers, restructured into this repo. |
| v1.5 | Fixes from the first live day: day cap raised from 350k to 600k slots, base64 logs, stream retries with backoff, `--resume`, durable failure report, `summarize.py`, `compare_runs.py`. |
| v1.4 | Timestamp lookup retries, and a header-only fallback for UTC date resolution. |

## Sources

- SQD Solana Portal API: https://docs.sqd.dev/en/portal/solana/api, error handling: https://docs.sqd.dev/en/portal/introduction/error-handling
- Jupiter Perps IDL: https://github.com/monakki/jup-perps-client/blob/main/generator/idl/jupiter-perpetuals.json
- Position-side PDA semantics: https://deepwiki.com/julianfssen/jupiter-perps-anchor-idl-parsing/4.4-position-pdas
