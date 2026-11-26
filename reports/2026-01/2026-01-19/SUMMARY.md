# Jupiter Perps × SQD — one-day benchmark: 2026-01-19

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 394,422,384 → 394,639,908 (217,525 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-19 00:00:00 UTC / 2026-01-19 23:59:59 UTC |
| Slot just before range | 394,422,383 @ 2026-01-18 23:59:59 UTC |
| Slot just after range | 394,639,909 @ 2026-01-20 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 394,639,908) |
| Blocks with Jupiter activity returned | 30,193 |
| HTTP batches | 422 |
| Raw data (decoded JSON) | 39.7715 MiB |
| Transferred on the wire (gzip) | 20.66 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 78.9 min |
| SQD overload retries | http529×360 |

## Trades (valid, executed size change)

**20,332 trades**, 4,671 distinct traders, total notional **$286,285,939.04**, fees $277,084.35, net realized PnL on closes $-1,161,119.35.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,121 | $105,421,051.70 |
| INCREASE | 12,582 | $139,804,453.62 |
| LIQUIDATE | 1,629 | $41,060,433.72 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 13,918 | $209,339,444.18 | $130.09 / $133.75 / $137.71 |
| ETH (Wormhole WETH) | 2,011 | $40,771,938.14 | $3,164.12 / $3,210.00 / $3,279.00 |
| BTC (Wormhole WBTC) | 4,403 | $36,174,556.72 | $91,910.28 / $92,726.32 / $93,583.64 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 14,563 | $216,909,314.17 |
| SHORT | 5,769 | $69,376,624.87 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 11,311 |
| InstantDecreasePositionEvent | 3,968 |
| DecreasePositionEvent | 2,153 |
| LiquidateFullPositionEvent | 1,629 |
| IncreasePositionEvent | 1,271 |

Also decoded: **764** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 20,332 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 12,582 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,291 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 338 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,121 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 7,741 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [H4EBg6HSHD…](https://solscan.io/tx/H4EBg6HSHDF8cMVvC2nW6aJRGNWRXuomrL74GHxioMGNM6hus4JpzEHXEUGKsFSDLo1iQV3r5Wnfiawrot4DP5J), [2eu6FRwWKU…](https://solscan.io/tx/2eu6FRwWKUB4RvzaSdkZ3sgV4LZyUQuEe6wp8UzEUxwVfHonEy2GaLoYX3v6DnhxBF58xSdcmhUDQVSvQkNfqpms), [2cMpWxS1H9…](https://solscan.io/tx/2cMpWxS1H9k7QefnEs1zd7kt6zUfj9tdSi6A6DX9Fe2MgsZkp2qXcc9chdpXbuzteFwGagoH31QiV2oNzACVEuFZ), [34DdfW9NhY…](https://solscan.io/tx/34DdfW9NhYeahpHBEdu71qJSu5cd985V8ihtMoW3fdqo3y6RUY1h5jrZo6DtixuTCc9ZdXk8Xqa8XFGBcrcmbouN), [3vzEqQegum…](https://solscan.io/tx/3vzEqQegumyRMDbUC1pLejnkhxcEuQmYQFYRPosTh1mWWo3zvShWXMXXdgUdWgwNjMqNzg45EXh9jKX4mk4jCwx5), [3eKhFAwmow…](https://solscan.io/tx/3eKhFAwmowiHyYEuZXsurf5U7amngV5dGuHQ3RsKDKKCFAea4iVuoGEy938uBAUntpKd5msFSs5kBdJwYvKZhFkD), [5nw4bC1pjB…](https://solscan.io/tx/5nw4bC1pjBNTGSFB2WTDceKYJTA4pfxQZAhZKvYjcD9cgC1Poc1it1Vf7TCvtCc7jBnhZDfd6Wp58ex6UpYFm7Sm), [55dZ7htCmn…](https://solscan.io/tx/55dZ7htCmnCV7HuxZyrHvx5LQUQiTaVs4bSd3efCxuMDgVzFMbK45bJSmP2Eqw7y3Wf9fNnF3N2C59oUtpKJ93qL), [Qp4yDzgJcn…](https://solscan.io/tx/Qp4yDzgJcnzuVK8eNSYUCmQVzw76b11ecAfWgtCH5BCyxDq8z2LGuaDwHg7V9Ty11z8HhnfY62H1hgfttXwzLPT), [UFxKFnN9nJ…](https://solscan.io/tx/UFxKFnN9nJMgcdikHL3NZmtt6bzRTXP26qvLdkkSJD5sxwSpMHgBiDHsxFsavtxoywiqCmxyTYqsCuSKAioxn2X), [ViU3uiuop2…](https://solscan.io/tx/ViU3uiuop2S6F2QsjH5iUz4rJbs7TpXWnzjTeaMjvWRngbwxud6AVJjh4KAjndqLkDUKtTXpJ657jZRHQzT8gVM), [49pxbFCmb6…](https://solscan.io/tx/49pxbFCmb6UstW3vZQ6RUGTzXhNinNrtsQfR8buBCuymn7QP4PGh4nxjk5aFC5N3DaTmXEdXrUbp1TpVM6u4J8GC), [32mynEdk4D…](https://solscan.io/tx/32mynEdk4DHWDocjuwpuDRHdHVZQA1vHdisLMr4G2qnGyHnYUCHHJFLt7kTrc5pHJE7YfLNvAAuswXJRiG7dz9fd), [tMwaz9DV7a…](https://solscan.io/tx/tMwaz9DV7agiFLhMY4SbcXsyM1WMnpVS9z2h9uAoDbTSFqSmQzYH73dtKaAE25Y8qkY8J4RSEt8mZLMVf7Zr7w6), [5dXZFm6mfZ…](https://solscan.io/tx/5dXZFm6mfZz5z1JWKLZaJ2obDYx8TWL9kBQj1QssFcY6sXXLvr6CsrD4WxMM5oDD8ZDzU9X8b85JsDS11rqdMSSu), [44cV6rJj8x…](https://solscan.io/tx/44cV6rJj8xEWKHJBXx8nujBiS8RJbCzG1Rxp2V1QVhtGrfwjKqqrAHK6B112KZGKp4ACwS6zm5V6id6mvLKpy6mh), [4f2cd15k3j…](https://solscan.io/tx/4f2cd15k3jByYnEkgu197vpNFZPrcveL5BBbvBusoLdKqkP4ywuQPLv17sq4NhzudMbwfuQ17hhA7CoeZJqEdGYy), [3j4iWm8fsU…](https://solscan.io/tx/3j4iWm8fsUJpP6ZHNsbPyVye3RRfiMGwSUjCzEk4APX29GknxUyEXyubZEBdHVTWQ2o56oudr2vBYaKeNnjMXnk4), [2SnCp2r33o…](https://solscan.io/tx/2SnCp2r33oY7PuKWNRBHGQkeC4u9msc4nCux5G76oLG5KRqe5C6RyoLXw4QHXeM1D9HutSjv3C1Pz3A3VYuSViPV), [3mbd4oufkD…](https://solscan.io/tx/3mbd4oufkDFCcKzZUhKDsc7AzGoXXkNx21s6yrVUMSYGqdWkDjs5x6oaAsC1W5azh21BGzehkqmRgEVBJ792yxx3)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×9,497, ClosePositionRequestEvent ×8,023, InstantCreateTpslEvent ×5,010, CreatePositionRequestEvent ×1,656, InstantCreateLimitOrderEvent ×1,570, RemoveLiquidityEvent ×1,236, AddLiquidityEvent ×1,143, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×113, RepayToCustodyEvent ×75, DepositCollateralEvent ×52, BorrowFromCustodyEvent ×46, RedeemStakeEvent ×43, WithdrawCollateralEvent ×37, LiquidateBorrowPositionEvent ×1

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-19 00:00:05 UTC | IncreasePositionEvent | SOL | LONG | $8,146.23 | $137.70 | - | [3GQzwrXmd4…](https://solscan.io/tx/3GQzwrXmd44N51eQSDz7McEMF782SrnqXqSW67Cj4yw7cHA91nofAa3WhtTX8T1dqvijXG7s8pdGB6pKJDGcyXJn) |
| 2026-01-19 00:00:05 UTC | DecreasePositionEvent | SOL | LONG | $8,510.93 | $137.60 | $-267.80 | [2xGKgwZt8U…](https://solscan.io/tx/2xGKgwZt8Ume3UtjCAkpg49udhUD3cuTVuYMq9KyuBxMztENXDrZAxvc3yCu71aPskUYoydtovArhyTBka9AG6Md) |
| 2026-01-19 00:00:05 UTC | LiquidateFullPositionEvent | SOL | LONG | $13,291.87 | $137.58 | $-833.43 | [47QMWaCeu8…](https://solscan.io/tx/47QMWaCeu8ntYMzF4HN12jDnS4Wjr86NSov3Q6eHTgcsLoTRy6YEKQimhnanyf3xP4s9SyWrsgmLBV1AtKRLzLUb) |
| 2026-01-19 00:00:05 UTC | InstantIncreasePositionEvent | SOL | LONG | $148.69 | $137.58 | - | [2aV7fb3RJm…](https://solscan.io/tx/2aV7fb3RJmXiwnccSebBpd3gV2ACdNXDisUP8rW5v7ft1tfS161EdT17Ap1h5NMNyKdKex3XCfx7VmWvWZ5D7N7E) |
| 2026-01-19 00:00:11 UTC | InstantDecreasePositionEvent | SOL | SHORT | $1,000.00 | $137.55 | $39.07 | [2dzydPztC2…](https://solscan.io/tx/2dzydPztC2Yjyen77ejrsnH6f7hzPr8XCSyQVmP8jii9dXZhVoV9F2Wv6PBaJpCfFb8Dw2oBJcFo6A41FEcZEGMw) |

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
