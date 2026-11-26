# Jupiter Perps × SQD — one-day benchmark: 2026-01-24

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 395,507,026 → 395,723,261 (216,236 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-24 00:00:00 UTC / 2026-01-24 23:59:59 UTC |
| Slot just before range | 395,507,025 @ 2026-01-23 23:59:59 UTC |
| Slot just after range | 395,723,262 @ 2026-01-25 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 395,723,261) |
| Blocks with Jupiter activity returned | 17,521 |
| HTTP batches | 433 |
| Raw data (decoded JSON) | 12.8019 MiB |
| Transferred on the wire (gzip) | 7.29 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 111.4 min |
| SQD overload retries | http529×462 |

## Trades (valid, executed size change)

**5,524 trades**, 1,605 distinct traders, total notional **$58,565,643.05**, fees $52,001.64, net realized PnL on closes $-69,916.70.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 2,009 | $28,308,130.92 |
| INCREASE | 3,417 | $28,172,211.92 |
| LIQUIDATE | 98 | $2,085,300.21 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 4,161 | $41,438,748.00 | $126.45 / $127.09 / $127.91 |
| BTC (Wormhole WBTC) | 875 | $12,876,225.40 | $89,023.00 / $89,325.52 / $89,795.50 |
| ETH (Wormhole WETH) | 488 | $4,250,669.65 | $2,939.60 / $2,954.94 / $2,965.64 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 3,583 | $36,022,977.51 |
| SHORT | 1,941 | $22,542,665.54 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 3,196 |
| InstantDecreasePositionEvent | 1,418 |
| DecreasePositionEvent | 591 |
| IncreasePositionEvent | 221 |
| LiquidateFullPositionEvent | 98 |

Also decoded: **356** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 5,524 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 3,417 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 98 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 2,009 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 2,099 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×2,566, PoolSwapEvent ×2,462, InstantCreateTpslEvent ×1,832, CreatePositionRequestEvent ×505, InstantCreateLimitOrderEvent ×486, WithdrawFeesEvent ×480, AddLiquidityEvent ×342, IncreasePositionPreSwapEvent ×67, RepayToCustodyEvent ×48, WithdrawCollateralEvent ×36, DepositCollateralEvent ×30, BorrowFromCustodyEvent ×29, RemoveLiquidityEvent ×5

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-24 00:00:33 UTC | InstantDecreasePositionEvent | SOL | SHORT | $104.97 | $127.28 | $0.58 | [24kLrzrkeR…](https://solscan.io/tx/24kLrzrkeRM3WBpGofKM7Nu4BH44sm9cMgEbnVa83Uz95BZJpencYbFcSEbuJBZzotCQbTpSXoogFLrpL5wdBpiQ) |
| 2026-01-24 00:00:45 UTC | InstantIncreasePositionEvent | SOL | LONG | $2,988.19 | $127.27 | - | [5jywsBqAEL…](https://solscan.io/tx/5jywsBqAELwKP5rJPhGsH6UQrPohhyjaAmUBVnkBGe2hHfgyiNbaBFfB152xtKdkYZ4Hv7Auov33bsvGLyqnrDf) |
| 2026-01-24 00:02:54 UTC | LiquidateFullPositionEvent | SOL | SHORT | $2,061.81 | $127.49 | $-3.73 | [2B9PULy5mQ…](https://solscan.io/tx/2B9PULy5mQES5MuZim891roP22qRohrFcW3HM3iBn5En3X5sP2AyuDpRPUAvi3Va7RiWCuLd7zjNKZnKxugVfXZ2) |
| 2026-01-24 00:02:55 UTC | DecreasePositionEvent | SOL | SHORT | $10,987.72 | $127.50 | $-30.23 | [4aqmNdSnJt…](https://solscan.io/tx/4aqmNdSnJtHYcJr9Squi5ZEKx17TbcHbibkTwSZfXaUCsuPZHUNqyFehzpH1zBGgTW1dRgTixvWCVyLnxnJi5vA1) |
| 2026-01-24 00:12:51 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $70,882.22 | $89,407.13 | - | [5nrLoFafJa…](https://solscan.io/tx/5nrLoFafJac8a4AY58tCEN5BqD68yGiSqGAoMiXzy65thdEqHvC5UcJiaW14vnA8BnKMsqGDDD5mddcuviqV19nt) |

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
