# Jupiter Perps × SQD — one-day benchmark: 2026-01-06

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 391,583,703 → 391,800,703 (217,001 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-06 00:00:00 UTC / 2026-01-06 23:59:59 UTC |
| Slot just before range | 391,583,702 @ 2026-01-05 23:59:59 UTC |
| Slot just after range | 391,800,704 @ 2026-01-07 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 391,800,703) |
| Blocks with Jupiter activity returned | 42,875 |
| HTTP batches | 399 |
| Raw data (decoded JSON) | 61.4337 MiB |
| Transferred on the wire (gzip) | 31.73 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 108.8 min |
| SQD overload retries | http529×443 |

## Trades (valid, executed size change)

**31,104 trades**, 4,257 distinct traders, total notional **$627,361,223.17**, fees $693,926.32, net realized PnL on closes $646,339.10.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 11,618 | $296,704,930.26 |
| INCREASE | 18,304 | $301,420,815.32 |
| LIQUIDATE | 1,182 | $29,235,477.58 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 24,308 | $361,213,092.38 | $136.12 / $139.04 / $143.42 |
| BTC (Wormhole WBTC) | 4,535 | $230,976,123.62 | $91,222.08 / $93,368.38 / $94,416.33 |
| ETH (Wormhole WETH) | 2,261 | $35,172,007.17 | $3,181.67 / $3,240.15 / $3,306.23 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 19,488 | $355,472,285.77 |
| SHORT | 11,616 | $271,888,937.40 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 16,803 |
| InstantDecreasePositionEvent | 7,367 |
| DecreasePositionEvent | 4,251 |
| IncreasePositionEvent | 1,501 |
| LiquidateFullPositionEvent | 1,182 |

Also decoded: **1,678** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 31,104 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 18,304 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,167 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 15 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 11,618 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 12,795 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [3iqY8nBMQc…](https://solscan.io/tx/3iqY8nBMQcskWmMe9tBhGNijHdvEW2FrNXKaXjPAaRhbb7YkMAzGdbVwRGTZu4QdvVGKRKXENVXVxa29k4nZBegN), [5cf1CWSdZb…](https://solscan.io/tx/5cf1CWSdZbEsxogQoqxfUHtvFTvWrZVRj3m9xbEXvjGDCj6Te7yh8xDd5n83qcpJUi6YDWtVtbPhn6YpkYkdBSxX), [sN2xx1ZTdC…](https://solscan.io/tx/sN2xx1ZTdCLR5Xp1uV3wqTFKTyZXLHH6gpBJ5W3C5pe25f4PbBSD9qF25A7qZttSW3EvEUDrt8RPKyVSntTRkgd), [2S3GVD5xNd…](https://solscan.io/tx/2S3GVD5xNdrBCazj96LRubuuNyq9RoSU2f8RkGyqBXga1byXZVGtASBnbwvMDwphX3ZJ7GnQPA1BcuHbhLw2Xnp), [TJX39TzmUD…](https://solscan.io/tx/TJX39TzmUDQXzoA6jmwhQBpwKbbVQzDbkN4E8jXvgcPo81davXcmzPU5NciA2v3y1UmVZfvXpmRXDRCMqEpUdxw), [4rd7rhqeMx…](https://solscan.io/tx/4rd7rhqeMxnDGto5pEeaA44jqB9ustnA3BoF4GSfNZoHxGwJ7LH3GQLKihVPzqpQdbZis99qMZiL6PCg1jLe4gsM), [4TS7wAwE3h…](https://solscan.io/tx/4TS7wAwE3hg2WMWVrRAnRcPhx4MN7QLX7JtSgz4Mr4Hwc1GtgQDmt6dhuCx7E76izpz3RLtmgWt6TCFqoLe6Q8dX), [52tpHVa5UN…](https://solscan.io/tx/52tpHVa5UNdSYGE35NVkPP59YJsmCRzT1SgKwyqKxUToLqfu86pR4bAEhQZnLgv5nquLoVUkZqtqNsiaYKwKsaCo), [3kT3vskL2y…](https://solscan.io/tx/3kT3vskL2ySvCwGaQUj4LU2WA6QtkVG8mEMx65jF1dnzZ7BHFCN1cDqA2AtWRivqKpjNSKovdmDsCenvbNAcpJ1u), [5M1rMimeRX…](https://solscan.io/tx/5M1rMimeRXYyKByx2AjZkwiwXEj1TPYQbooLGZ3qyg13AnmjWsLXeNSL9tmH1QMoZAAydx5KrJJeMwsUDkGXtCsx), [2VCkNQerN2…](https://solscan.io/tx/2VCkNQerN226MCdVRpGvznv3w6vHtpcA7X8vpYQscdQuhw5JoAHjzmo19E8vJZ8QCu61LrXtC6UCnZGAytMctjfa), [3Ud8Nb2viE…](https://solscan.io/tx/3Ud8Nb2viEmBW9aWuCvrvDB6tWBbtkQ3EokMzvZo1yXG9mH1M31GyFjmRK1EvndLgR7wBKs4bH8YeqWvL12yBU5d), [4xMh1NEnop…](https://solscan.io/tx/4xMh1NEnoppU7SLuBavA9P6qdGFvGuJ3VRHXecotAXJDNfpDBkdjMym7WTA7Ze4Wb8R7Zn7Ss3uUnQ7b7FQxE1H9), [5AkHEP8L9c…](https://solscan.io/tx/5AkHEP8L9cLJL38tRCGJ6AQgHBhEL1xAcqc7gmULvP711Fn1SyRekBBBtYPN9ENGaJCasf4pSrsjeueuRVRiqZZz), [2woTMiGjTW…](https://solscan.io/tx/2woTMiGjTWZCsq5MTLrJ6qTahmbK2DKpsrNGyaCYzFYN1pw61fP32yFojg7oMuWKk4x3fYtC1sSxZtBaPH1SruBz)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×14,356, PoolSwapEvent ×13,445, InstantCreateTpslEvent ×9,484, InstantCreateLimitOrderEvent ×2,336, CreatePositionRequestEvent ×2,254, AddLiquidityEvent ×610, RemoveLiquidityEvent ×489, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×167, BorrowFromCustodyEvent ×91, RepayToCustodyEvent ×79, WithdrawCollateralEvent ×41, DepositCollateralEvent ×34

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-06 00:00:03 UTC | InstantIncreasePositionEvent | SOL | LONG | $4,257.12 | $137.93 | - | [DLfN8vSxXy…](https://solscan.io/tx/DLfN8vSxXyFrUTqfGdwwY62iCpKgvqUepahr4oFifiYSzNLsz8iJoZEaq3h3wcZ7RxVigkfMffv6Myh36Bfa2Hw) |
| 2026-01-06 00:00:04 UTC | InstantDecreasePositionEvent | SOL | LONG | $7,702.41 | $137.93 | $173.79 | [3b5bfWM6pG…](https://solscan.io/tx/3b5bfWM6pG7Upm9tAne7vi1nAqam3e3hr3tkDM42PRXgD1LBbcKeCzD8y8FpYzNLyuyznkTXbrMcMFc2UnUhKD79) |
| 2026-01-06 00:00:43 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $22,351.61 | $93,865.00 | $-72.71 | [3VwcThmxWR…](https://solscan.io/tx/3VwcThmxWRSTbW19PAoehZ9iFrALUNFrD2jVAbbFsJvsZcsNgYTw4TTc935JEhqg7bnpnJaN5ZkuhtX87kdtsEJM) |
| 2026-01-06 00:02:11 UTC | IncreasePositionEvent | SOL | LONG | $18.25 | $138.06 | - | [3hv8atPgfn…](https://solscan.io/tx/3hv8atPgfny28UJ6svs7Ypnjt3ZzpoBj9s7gP2vAk4sftCeq5PpejXQkvPdPVCjqmCwjwXJwTMC7sX9DMz5jYS6f) |
| 2026-01-06 00:06:18 UTC | LiquidateFullPositionEvent | SOL | LONG | $7,045.43 | $137.82 | $-10.51 | [5QJ18ezcYv…](https://solscan.io/tx/5QJ18ezcYvYeT6xGpTe2M9j5z1TShvj5sJh86ks8xJ3sdEQe9MQBNMC3nqq6xQG3PuczEaFsdU2y1pZbLy2SnMsp) |

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
