# Jupiter Perps × SQD — one-day benchmark: 2026-01-09

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 392,234,925 → 392,452,781 (217,857 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-09 00:00:00 UTC / 2026-01-09 23:59:59 UTC |
| Slot just before range | 392,234,924 @ 2026-01-08 23:59:59 UTC |
| Slot just after range | 392,452,782 @ 2026-01-10 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 392,452,781) |
| Blocks with Jupiter activity returned | 38,237 |
| HTTP batches | 370 |
| Raw data (decoded JSON) | 51.6579 MiB |
| Transferred on the wire (gzip) | 26.56 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 167.9 min |
| SQD overload retries | http529×565 |

## Trades (valid, executed size change)

**26,070 trades**, 3,313 distinct traders, total notional **$379,713,230.33**, fees $315,640.82, net realized PnL on closes $200,212.98.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 8,818 | $166,381,261.90 |
| INCREASE | 16,460 | $192,140,859.76 |
| LIQUIDATE | 792 | $21,191,108.66 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 20,614 | $263,591,067.71 | $134.83 / $138.18 / $140.94 |
| BTC (Wormhole WBTC) | 3,339 | $71,330,876.69 | $89,592.57 / $90,687.39 / $91,924.88 |
| ETH (Wormhole WETH) | 2,117 | $44,791,285.92 | $3,056.32 / $3,095.14 / $3,144.67 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 17,619 | $212,050,085.16 |
| SHORT | 8,451 | $167,663,145.16 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 14,826 |
| InstantDecreasePositionEvent | 5,581 |
| DecreasePositionEvent | 3,237 |
| IncreasePositionEvent | 1,634 |
| LiquidateFullPositionEvent | 792 |

Also decoded: **1,157** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 26,070 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 16,460 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 792 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 8,818 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 9,599 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×11,571, ClosePositionRequestEvent ×11,143, InstantCreateTpslEvent ×7,110, CreatePositionRequestEvent ×2,140, AddLiquidityEvent ×2,107, InstantCreateLimitOrderEvent ×2,003, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×219, IncreasePositionPreSwapEvent ×144, BorrowFromCustodyEvent ×74, RepayToCustodyEvent ×70, DepositCollateralEvent ×54, RedeemStakeEvent ×46, WithdrawCollateralEvent ×44

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-09 00:00:07 UTC | InstantIncreasePositionEvent | SOL | LONG | $3,954.73 | $138.24 | - | [5h6dLaTPUX…](https://solscan.io/tx/5h6dLaTPUX4iA4YpifxGAwYEa163jqy42Rd2SbfL353ydRVMdN6HNtTLXTcsEUR7v1rQeu6BtsyQhwAztu5fYTmj) |
| 2026-01-09 00:00:48 UTC | InstantDecreasePositionEvent | SOL | LONG | $1,934.98 | $138.32 | $22.43 | [4JNzapKsKn…](https://solscan.io/tx/4JNzapKsKnNgzxEgerd56xJNvA6WU9S8ik6DZw5j5micgV63GM7MR4kScz6j6LLmLqsH3yxG7mYPbWGiqXYgE4FT) |
| 2026-01-09 00:01:49 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $4,714.09 | $90,986.20 | $35.33 | [2tEECb2846…](https://solscan.io/tx/2tEECb2846KPez67ZHK3UHsWY7H9FVVcSLb4ikva1jUVE9dZhBadCeaAV8YYcjCm9wtwUrpMeMwmHuWbKgNuA17e) |
| 2026-01-09 00:04:27 UTC | IncreasePositionEvent | SOL | SHORT | $1,046.78 | $138.40 | - | [4LYWAFfjKf…](https://solscan.io/tx/4LYWAFfjKfrtFvouaGJQbCE1SWCU4PJJyGHJgArymQcV6iJrLQu8UpbLW5GHXfywKWgzcBpZYFh8MKd6y8RJTie8) |
| 2026-01-09 00:46:10 UTC | LiquidateFullPositionEvent | SOL | SHORT | $9,287.88 | $139.12 | $-37.81 | [kG7UNrVvRf…](https://solscan.io/tx/kG7UNrVvRfzjLM59ibdd6YUDDomwk5YAY2bF5ckV74NtvMX5TaJprLi77FeEANqioyrAaGHgCsBntryvUPmwQxk) |

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
