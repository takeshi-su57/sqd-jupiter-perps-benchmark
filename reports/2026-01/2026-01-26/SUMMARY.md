# Jupiter Perps × SQD — one-day benchmark: 2026-01-26

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 395,938,480 → 396,153,764 (215,285 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-26 00:00:00 UTC / 2026-01-26 23:59:59 UTC |
| Slot just before range | 395,938,479 @ 2026-01-25 23:59:59 UTC |
| Slot just after range | 396,153,765 @ 2026-01-27 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 396,153,764) |
| Blocks with Jupiter activity returned | 34,694 |
| HTTP batches | 497 |
| Raw data (decoded JSON) | 39.5051 MiB |
| Transferred on the wire (gzip) | 21.10 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 159.9 min |
| SQD overload retries | http529×607 |

## Trades (valid, executed size change)

**18,694 trades**, 3,461 distinct traders, total notional **$241,820,441.21**, fees $195,662.69, net realized PnL on closes $533,890.34.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 7,811 | $113,611,872.58 |
| INCREASE | 10,351 | $119,452,717.90 |
| LIQUIDATE | 532 | $8,755,850.74 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 13,456 | $153,019,833.59 | $118.42 / $123.07 / $125.47 |
| BTC (Wormhole WBTC) | 3,001 | $55,870,317.10 | $86,411.70 / $87,709.75 / $88,765.66 |
| ETH (Wormhole WETH) | 2,237 | $32,930,290.53 | $2,810.76 / $2,895.81 / $2,947.63 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 11,077 | $140,485,689.04 |
| SHORT | 7,617 | $101,334,752.17 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 9,506 |
| InstantDecreasePositionEvent | 5,213 |
| DecreasePositionEvent | 2,598 |
| IncreasePositionEvent | 845 |
| LiquidateFullPositionEvent | 532 |

Also decoded: **1,087** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 18,694 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 10,351 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 531 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 7,811 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 8,322 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [53S6necRyr…](https://solscan.io/tx/53S6necRyrRKbC3Jb6xeuX8ycpLtuqiRd9HDhQLWPtjyhWfKM3rL8Ysrhnem9AnJMecBY7sid6x5ysTFZaYPLTLU)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×9,151, PoolSwapEvent ×7,894, InstantCreateTpslEvent ×6,450, CreatePositionRequestEvent ×1,606, InstantCreateLimitOrderEvent ×1,487, WithdrawFeesEvent ×480, AddLiquidityEvent ×474, RemoveLiquidityEvent ×246, IncreasePositionPreSwapEvent ×165, BorrowFromCustodyEvent ×120, RepayToCustodyEvent ×97, DepositCollateralEvent ×81, WithdrawCollateralEvent ×57

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-26 00:00:01 UTC | InstantIncreasePositionEvent | SOL | LONG | $1,458.28 | $118.72 | - | [2FSaFcHT2u…](https://solscan.io/tx/2FSaFcHT2uh3i9L9EZz1mDqvMeGoZ7D6i1ZhSEVTRijzDPhNzVju2woi46WeKBaQi12jo9qGCYpoQCtXZDJvVYFx) |
| 2026-01-26 00:00:15 UTC | DecreasePositionEvent | SOL | LONG | $4,428.10 | $118.62 | $-23.29 | [3WSe6Cd7ar…](https://solscan.io/tx/3WSe6Cd7arx9wLxv6qdeAEcHFkpyfW5vDr2qmVTWCiEXsUyUHW7Le5qmDvcqKm8wvV1eQB9gVxMrLM4wkAiEFVaz) |
| 2026-01-26 00:00:20 UTC | IncreasePositionEvent | SOL | LONG | $298.74 | $118.60 | - | [2fLpULFe65…](https://solscan.io/tx/2fLpULFe65BxR6khZbtibuBawCFSrNyVhrtmXCPKTiNeRtib3ayVaCW6dqZJwmfG3HHDG2gNbzz1LsT7q6qiRYK6) |
| 2026-01-26 00:00:53 UTC | LiquidateFullPositionEvent | SOL | LONG | $2,059.23 | $118.52 | $-3.04 | [39CMLaBEdU…](https://solscan.io/tx/39CMLaBEdUzkXPLGUUVpQBA98bqpaUzRLZPpJtks2vM6fK697hPTfKakAUyhVUg319QKpPEARyQ5TXsmNcBABR9z) |
| 2026-01-26 00:01:06 UTC | InstantDecreasePositionEvent | SOL | SHORT | $3,120.67 | $118.48 | $85.54 | [4x32TbhDvr…](https://solscan.io/tx/4x32TbhDvrdz7q9prtq48LHyYrNYnSWgzMdVfy3vowSU7fcB9RHZLmvKubZGQuQ9efihJVNtcvoEEPpaRUsrYd5k) |

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
