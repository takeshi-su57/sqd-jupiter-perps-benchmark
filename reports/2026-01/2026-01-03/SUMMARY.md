# Jupiter Perps × SQD — one-day benchmark: 2026-01-03

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 390,930,116 → 391,149,215 (219,100 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-03 00:00:00 UTC / 2026-01-03 23:59:59 UTC |
| Slot just before range | 390,930,115 @ 2026-01-02 23:59:59 UTC |
| Slot just after range | 391,149,216 @ 2026-01-04 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 391,149,215) |
| Blocks with Jupiter activity returned | 27,207 |
| HTTP batches | 327 |
| Raw data (decoded JSON) | 30.6804 MiB |
| Transferred on the wire (gzip) | 16.09 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 139.9 min |
| SQD overload retries | http529×487 |

## Trades (valid, executed size change)

**14,658 trades**, 2,893 distinct traders, total notional **$170,955,167.45**, fees $160,351.81, net realized PnL on closes $202,047.47.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 5,745 | $81,462,824.32 |
| INCREASE | 8,534 | $84,393,392.81 |
| LIQUIDATE | 379 | $5,098,950.32 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 11,749 | $140,387,366.99 | $129.56 / $131.89 / $133.88 |
| ETH (Wormhole WETH) | 1,192 | $15,397,721.60 | $3,075.60 / $3,108.18 / $3,134.81 |
| BTC (Wormhole WBTC) | 1,717 | $15,170,078.85 | $89,284.12 / $90,064.93 / $90,686.87 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 8,501 | $76,413,228.70 |
| SHORT | 6,157 | $94,541,938.75 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 7,905 |
| InstantDecreasePositionEvent | 3,935 |
| DecreasePositionEvent | 1,810 |
| IncreasePositionEvent | 629 |
| LiquidateFullPositionEvent | 379 |

Also decoded: **749** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 14,658 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 8,534 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 379 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 5,745 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 6,116 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×6,827, PoolSwapEvent ×6,428, InstantCreateTpslEvent ×4,785, CreatePositionRequestEvent ×1,158, InstantCreateLimitOrderEvent ×1,045, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×457, AddLiquidityEvent ×231, BorrowFromCustodyEvent ×150, DepositCollateralEvent ×138, IncreasePositionPreSwapEvent ×101, RepayToCustodyEvent ×88, WithdrawCollateralEvent ×58, RedeemStakeEvent ×46

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-03 00:00:15 UTC | DecreasePositionEvent | SOL | LONG | $4,370.62 | $132.25 | $47.85 | [4C6XmVpkd4…](https://solscan.io/tx/4C6XmVpkd4vHuGKxaDcGDtgUxizN9JhaKAezCKtAdrjKXmkSYvExkyBTbMaRkxVsTpAYa8fqagD2xm9jc7vjYtFK) |
| 2026-01-03 00:00:32 UTC | InstantIncreasePositionEvent | SOL | LONG | $2,637.65 | $132.26 | - | [wu2uxGYK1N…](https://solscan.io/tx/wu2uxGYK1N51tCFDvRCBYwjDY6xZ17TmUFtyedDjGTqu3vYk1aiZJkkFSeGRCDtNi3qVwyJZbEupNUQvxLcvPZW) |
| 2026-01-03 00:01:02 UTC | InstantDecreasePositionEvent | SOL | SHORT | $10,440.33 | $132.32 | $4.29 | [zTv6TreYVm…](https://solscan.io/tx/zTv6TreYVmqhk9BJmjanpGmBaWMNKF9ShhzoyZ5jqa5NA9zqpndprYW7DSogqrjs921k4RAEHixvCKv5A3keXyd) |
| 2026-01-03 00:01:21 UTC | IncreasePositionEvent | SOL | SHORT | $2,755.83 | $132.32 | - | [2J6CJ1PZqc…](https://solscan.io/tx/2J6CJ1PZqcA2TG1212o6zsK3eEoFrjani32jKWM3LuJwcZQLkgzPyngwoyEmnLcZRj73LzViKBMBtF6XxJtLNqUK) |
| 2026-01-03 00:02:16 UTC | LiquidateFullPositionEvent | SOL | SHORT | $9,045.39 | $132.33 | $-13.50 | [5DfPzV9thJ…](https://solscan.io/tx/5DfPzV9thJeb6UeFvUEropQrW3xKRtB1ekUQ5e3UzSkrahfv1qaLrst7vdG8fPKGKYS8nhkQFAi9S5Fm1UWtK25U) |

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
