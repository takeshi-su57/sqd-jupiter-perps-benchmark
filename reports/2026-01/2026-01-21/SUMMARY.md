# Jupiter Perps × SQD — one-day benchmark: 2026-01-21

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 394,856,966 → 395,074,218 (217,253 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-21 00:00:00 UTC / 2026-01-21 23:59:59 UTC |
| Slot just before range | 394,856,965 @ 2026-01-20 23:59:59 UTC |
| Slot just after range | 395,074,219 @ 2026-01-22 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 395,074,218) |
| Blocks with Jupiter activity returned | 40,264 |
| HTTP batches | 453 |
| Raw data (decoded JSON) | 53.7342 MiB |
| Transferred on the wire (gzip) | 27.89 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 72.8 min |
| SQD overload retries | http529×342 |

## Trades (valid, executed size change)

**26,545 trades**, 4,041 distinct traders, total notional **$383,331,594.97**, fees $319,070.77, net realized PnL on closes $-332,825.72.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 9,683 | $169,825,849.48 |
| INCREASE | 15,664 | $191,678,223.28 |
| LIQUIDATE | 1,198 | $21,827,522.20 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 17,285 | $244,887,621.40 | $125.16 / $128.33 / $132.01 |
| BTC (Wormhole WBTC) | 5,429 | $72,261,343.02 | $87,179.33 / $89,279.27 / $90,437.20 |
| ETH (Wormhole WETH) | 3,831 | $66,182,630.55 | $2,864.02 / $2,965.02 / $3,066.44 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 17,488 | $248,175,465.04 |
| SHORT | 9,057 | $135,156,129.93 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 14,368 |
| InstantDecreasePositionEvent | 6,151 |
| DecreasePositionEvent | 3,532 |
| IncreasePositionEvent | 1,296 |
| LiquidateFullPositionEvent | 1,198 |

Also decoded: **1,262** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 26,545 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 15,664 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,197 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 9,683 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 10,873 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [22HV6G39m8…](https://solscan.io/tx/22HV6G39m8BickPbUho2j6dnUzFkbe6yAjENPwqwo6vqGcjfsNAMEswjgcniXtrahAcCNXE9Kbspv3MGmhFmXVqG)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×11,919, ClosePositionRequestEvent ×11,826, InstantCreateTpslEvent ×7,746, CreatePositionRequestEvent ×2,292, AddLiquidityEvent ×1,965, InstantCreateLimitOrderEvent ×1,901, RemoveLiquidityEvent ×517, WithdrawFeesEvent ×480, BorrowFromCustodyEvent ×247, IncreasePositionPreSwapEvent ×209, DepositCollateralEvent ×194, RepayToCustodyEvent ×112, RedeemStakeEvent ×86, WithdrawCollateralEvent ×61

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-21 00:00:07 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $1,621.68 | $88,302.83 | - | [PMge5ryMnB…](https://solscan.io/tx/PMge5ryMnBFJnF8uFFMrPCQmkrm5iWrQSpujsCz4B99VGKqmK3kB3NNKHQsjQr1vp6XMAZ9sZ7k8YoHv7KmNykY) |
| 2026-01-21 00:00:23 UTC | InstantDecreasePositionEvent | SOL | SHORT | $124.01 | $125.66 | $0.46 | [4LVv7ZeW7W…](https://solscan.io/tx/4LVv7ZeW7Wbby4mTp1p4P2S3JWRYchMD4kFZyLJEzNXeQjTHBfKCNRz1o7PMapdyB7nKhohX6TEPg6TbDzriUbxh) |
| 2026-01-21 00:00:33 UTC | DecreasePositionEvent | SOL | SHORT | $2,628.73 | $125.81 | $-4.65 | [3QtpQdtt17…](https://solscan.io/tx/3QtpQdtt1736b399FdoHmXkuYMLBKxCjvxHP9ujwXUvRZCMDXqUyy7c4HSRvM3bb3MPCNKbL2YYTa8NbFyp3RMzL) |
| 2026-01-21 00:01:10 UTC | IncreasePositionEvent | SOL | LONG | $30.00 | $125.90 | - | [V2G9MpFGgb…](https://solscan.io/tx/V2G9MpFGgbHos39TchoxwnuDVhNa7LJohwDzwTCRaj1Trc3BwpeTpwXK4cymzd2b5UAbWKJUHHXKRv7v5RqFAmS) |
| 2026-01-21 00:04:05 UTC | LiquidateFullPositionEvent | BTC (Wormhole WBTC) | SHORT | $5,482.94 | $88,474.20 | $-8.21 | [5QKenHz3gL…](https://solscan.io/tx/5QKenHz3gLWhC1WzzGpUrDekdcS9GXQykpMVgEw95jPB2SEGYT8kqrZkBzn1y3pKZ57QWqyJ5rfny9bqjhQomUqx) |

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
