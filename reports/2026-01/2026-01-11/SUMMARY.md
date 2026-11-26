# Jupiter Perps × SQD — one-day benchmark: 2026-01-11

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 392,671,259 → 392,890,521 (219,263 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-11 00:00:00 UTC / 2026-01-11 23:59:59 UTC |
| Slot just before range | 392,671,258 @ 2026-01-10 23:59:59 UTC |
| Slot just after range | 392,890,522 @ 2026-01-12 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 392,890,521) |
| Blocks with Jupiter activity returned | 25,788 |
| HTTP batches | 338 |
| Raw data (decoded JSON) | 30.8396 MiB |
| Transferred on the wire (gzip) | 16.15 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 115.2 min |
| SQD overload retries | http529×467 |

## Trades (valid, executed size change)

**15,094 trades**, 2,653 distinct traders, total notional **$218,739,461.51**, fees $190,153.54, net realized PnL on closes $313,768.12.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 5,699 | $106,344,185.39 |
| INCREASE | 9,038 | $104,588,317.49 |
| LIQUIDATE | 357 | $7,806,958.62 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 12,674 | $171,483,883.54 | $135.57 / $138.36 / $141.35 |
| BTC (Wormhole WBTC) | 1,413 | $24,248,045.50 | $90,110.28 / $90,656.63 / $91,148.01 |
| ETH (Wormhole WETH) | 1,007 | $23,007,532.46 | $3,081.20 / $3,109.47 / $3,141.72 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 9,657 | $141,192,897.59 |
| SHORT | 5,437 | $77,546,563.91 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 8,172 |
| InstantDecreasePositionEvent | 3,613 |
| DecreasePositionEvent | 2,086 |
| IncreasePositionEvent | 866 |
| LiquidateFullPositionEvent | 357 |

Also decoded: **610** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 15,094 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 9,038 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 355 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 2 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 5,699 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 6,053 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [3C44oVAC1z…](https://solscan.io/tx/3C44oVAC1zkswGdjR5w4ixgpioFdtZUaYT8qAsBdYJdSU5T2q7Ty7JHJGpGj7VdPXARPW6ig3AbdEg3fxaSVkY4e), [4mVkiN6e1s…](https://solscan.io/tx/4mVkiN6e1sohVW31Xc88FX5eoHujSy969aKVVG6V9Z52L3gcN8acgKsKPHjKVeyJ7cJj7aqS3oswaKuC8Fhb34mn)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×7,441, PoolSwapEvent ×6,333, InstantCreateTpslEvent ×4,873, CreatePositionRequestEvent ×1,188, InstantCreateLimitOrderEvent ×1,148, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×295, AddLiquidityEvent ×167, IncreasePositionPreSwapEvent ×76, RepayToCustodyEvent ×71, BorrowFromCustodyEvent ×68, WithdrawCollateralEvent ×55, DepositCollateralEvent ×49, RedeemStakeEvent ×46

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-11 00:00:30 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $6,848.00 | $90,382.48 | - | [24CyCZsTJC…](https://solscan.io/tx/24CyCZsTJCZ8YPbxxhZHcthpt7Zbqyj7Hp66hpAssWE7zJyp3LLZLdmpvMbzGXSSv5JSm9u9ujMLofUVCSUNm6aE) |
| 2026-01-11 00:01:36 UTC | InstantDecreasePositionEvent | SOL | LONG | $262.98 | $135.63 | $0.05 | [3L2Ld3CHhw…](https://solscan.io/tx/3L2Ld3CHhwoyPUp8iatXm7wBvsZrbkTAz8fyWhoXugSQ5fW2dJsUEkYyw2kGPnz76yzgYeszRuEvDJ4MRE9oB5fe) |
| 2026-01-11 00:07:52 UTC | IncreasePositionEvent | SOL | LONG | $10,978.76 | $135.57 | - | [2ebWfwwdE7…](https://solscan.io/tx/2ebWfwwdE7AGxsBTiiHQAAPARkgeRw1ehbb5kcJgDNg7Fdb6wUN3Gmv1TnR4vb7tYf5dGFkBrpKqvgZjN4LBgnJ9) |
| 2026-01-11 00:13:43 UTC | DecreasePositionEvent | SOL | SHORT | $42,228.23 | $135.84 | $51.80 | [2H9f4pHtDr…](https://solscan.io/tx/2H9f4pHtDridpvWqvUBqaK9kNk6XoyddJ7hA5fXg7Jtp6Th6fNFgk9hoq5gyGDwbgoEmtHWW35Kb4kQ3d7MSuDH5) |
| 2026-01-11 00:13:45 UTC | LiquidateFullPositionEvent | SOL | SHORT | $11,660.82 | $135.92 | $-29.63 | [3fHz1buwYa…](https://solscan.io/tx/3fHz1buwYaS646WkKkqNeMkUAJcdfg5pdJa5cBjRoo61L8VUWbrM7jk69iuc3osLXUZ98A4QnNaHzV6rqTzFB2dj) |

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
