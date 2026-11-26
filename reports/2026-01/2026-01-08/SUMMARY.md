# Jupiter Perps × SQD — one-day benchmark: 2026-01-08

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 392,017,796 → 392,234,924 (217,129 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-08 00:00:00 UTC / 2026-01-08 23:59:59 UTC |
| Slot just before range | 392,017,795 @ 2026-01-07 23:59:59 UTC |
| Slot just after range | 392,234,925 @ 2026-01-09 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 392,234,924) |
| Blocks with Jupiter activity returned | 42,401 |
| HTTP batches | 387 |
| Raw data (decoded JSON) | 57.6896 MiB |
| Transferred on the wire (gzip) | 29.57 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 109.9 min |
| SQD overload retries | http529×470 |

## Trades (valid, executed size change)

**28,562 trades**, 3,790 distinct traders, total notional **$453,579,555.27**, fees $416,257.89, net realized PnL on closes $-2,235,159.81.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 10,205 | $211,779,933.17 |
| INCREASE | 17,299 | $215,431,658.97 |
| LIQUIDATE | 1,058 | $26,367,963.12 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 21,430 | $326,288,293.23 | $132.58 / $136.71 / $139.90 |
| BTC (Wormhole WBTC) | 4,150 | $86,761,066.55 | $89,226.01 / $90,381.78 / $91,568.25 |
| ETH (Wormhole WETH) | 2,982 | $40,530,195.49 | $3,051.00 / $3,108.89 / $3,180.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 19,034 | $289,072,239.92 |
| SHORT | 9,528 | $164,507,315.35 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 15,555 |
| InstantDecreasePositionEvent | 6,310 |
| DecreasePositionEvent | 3,895 |
| IncreasePositionEvent | 1,744 |
| LiquidateFullPositionEvent | 1,058 |

Also decoded: **1,284** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

## Data-quality checks

| Check | Result |
|---|---|
| full_requested_range_streamed | ✅ |
| at_least_one_executed_trade | ✅ |
| zero_decoding_failures | ✅ |
| zero_raw_encoding_failures | ✅ |
| zero_unknown_anchor_cpi | ✅ |
| zero_unrecognized_data_logs | ✅ |
| zero_invalid_candidates | ✅ |
| zero_missing_transaction_links | ✅ |
| zero_missing_instruction_addresses | ✅ |
| zero_missing_transaction_status | ✅ |
| zero_missing_commit_status | ✅ |
| zero_duplicate_source_ids | ✅ |
| zero_event_multiplicity_mismatch | ✅ |
| raw.ndjson replay reproduces live counters | ✅ |
| raw.ndjson replay reproduces candidates.ndjson | ✅ |
| arithmetic: fee_eq_position_fee_plus_funding_ok | 28,562 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 17,299 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,057 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 10,205 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 11,254 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [4RDMqGUAb2…](https://solscan.io/tx/4RDMqGUAb2bvsakZHBQUb4yyRpuY6fymHsAXQwmyfyVkLrFXmzoshYQMBhWC9NyMmuheKhSxpDs7KRVyCqrVkNVj)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×12,984, PoolSwapEvent ×12,933, InstantCreateTpslEvent ×8,116, AddLiquidityEvent ×2,735, CreatePositionRequestEvent ×2,425, InstantCreateLimitOrderEvent ×2,272, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×234, RemoveLiquidityEvent ×143, RepayToCustodyEvent ×70, BorrowFromCustodyEvent ×67, DepositCollateralEvent ×55, WithdrawCollateralEvent ×40

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-08 00:00:03 UTC | InstantIncreasePositionEvent | SOL | LONG | $9.73 | $136.23 | - | [5wUuxZbgmM…](https://solscan.io/tx/5wUuxZbgmMNKgNBsX2BpzMWxFjb997kqqHLerLDrFrf5uGAsXSxkqFDpLTyP3Vu8DtZ7ALyD2EyW1zFT5F7MABSF) |
| 2026-01-08 00:00:18 UTC | InstantDecreasePositionEvent | SOL | LONG | $951.28 | $136.23 | $-0.03 | [2tuoDvtg5s…](https://solscan.io/tx/2tuoDvtg5ssLNx6ZrWcPFLUQ8tMCQSTm3tcjEuevyQ3CVgApciZjjaaxb8FaTfFfwDDbEwX9H5PkGHoxKUmGb8j5) |
| 2026-01-08 00:00:24 UTC | DecreasePositionEvent | SOL | LONG | $57,357.34 | $136.18 | $2.11 | [23d4iTkprN…](https://solscan.io/tx/23d4iTkprNkZM3XM6zd7grcq1dj91KcqXYd4CCXBAjUv2Fsc7DWVncLRDGAzUsTk8Mdhm9YngDpPoufKAwb5HffH) |
| 2026-01-08 00:01:14 UTC | LiquidateFullPositionEvent | SOL | LONG | $1,759.55 | $136.13 | $-7.06 | [2UYyb8HgaB…](https://solscan.io/tx/2UYyb8HgaBEXoUer7QMgA92m9GAbwKDfWCgqdj3jtxKYHkw1EbKgc2Gz4b4Dwoo61rYmJ6e5FEyro25cjHYHR38J) |
| 2026-01-08 00:03:55 UTC | IncreasePositionEvent | SOL | LONG | $2,084.56 | $136.22 | - | [27sSbnu8ru…](https://solscan.io/tx/27sSbnu8ruZD3K4RrhtdRc1qZ2h2vbgR58TPB3VtQYS8Cr6napGHU74BdJ5x7fDfMZ6cvLWRnjJuLRKddaYaptbZ) |

## Units and assumptions

- USD fields (`sizeUsdDelta`, `price`, `feeUsd`, `pnlDelta`) are integers with 6 decimals; raw integers are kept in `candidates.ndjson`. The scale is confirmed by price levels above and fee-to-size ratios, not by an external source.
- `positionSide`: 1 = LONG, 2 = SHORT. Realized PnL = `pnlDelta` × (`hasProfit` ? +1 : −1).
- IDL: community IDL `/home/work/Documents/luckyplans/SQD_Jupiter_Accuracy_Benchmark_v1.4/jupiter_sqd_benchmark/jupiter-perpetuals-idl.json`, sha256 `f2d7ff5009e7696939cb2e888368967744131e6aa51dc5ea7c966cc9f29ed16c`.
- Source: SQD Portal only. No Solana RPC, Dune, Trawl, or Helius. No database writes.

## Files

- `trades.csv` — readable table of every valid executed trade (open in a spreadsheet)
- `candidates.ndjson` — all decoded candidates with raw integers and every event field
- `raw.ndjson` — untouched SQD response lines (re-decodable offline: `python3 summarize.py <dir>`)
- `report.json`, `replay.json`, `query.json`, `idl_used.json`
