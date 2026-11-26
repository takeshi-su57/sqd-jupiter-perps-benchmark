# Jupiter Perps × SQD — one-day benchmark: 2026-01-31

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 397,016,698 → 397,234,291 (217,594 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-31 00:00:00 UTC / 2026-01-31 23:59:59 UTC |
| Slot just before range | 397,016,697 @ 2026-01-30 23:59:59 UTC |
| Slot just after range | 397,234,292 @ 2026-02-01 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 397,234,291) |
| Blocks with Jupiter activity returned | 54,299 |
| HTTP batches | 539 |
| Raw data (decoded JSON) | 96.6487 MiB |
| Transferred on the wire (gzip) | 48.72 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 191.6 min |
| SQD overload retries | http529×770 |

## Trades (valid, executed size change)

**51,106 trades**, 9,510 distinct traders, total notional **$597,873,046.27**, fees $1,354,942.38, net realized PnL on closes $-13,247,586.59.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 14,122 | $203,428,583.00 |
| INCREASE | 29,213 | $278,264,028.95 |
| LIQUIDATE | 7,771 | $116,180,434.33 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 38,536 | $441,528,363.98 | $96.91 / $105.52 / $118.66 |
| BTC (Wormhole WBTC) | 7,547 | $104,502,199.31 | $75,655.98 / $78,920.59 / $84,130.54 |
| ETH (Wormhole WETH) | 5,023 | $51,842,482.98 | $2,259.97 / $2,478.48 / $2,710.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 35,432 | $399,098,065.67 |
| SHORT | 15,674 | $198,774,980.60 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 25,674 |
| InstantDecreasePositionEvent | 9,257 |
| LiquidateFullPositionEvent | 7,771 |
| DecreasePositionEvent | 4,865 |
| IncreasePositionEvent | 3,539 |

Also decoded: **2,465** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 51,106 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 29,213 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 5,959 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1,812 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 14,122 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 21,641 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [PJafv9KasV…](https://solscan.io/tx/PJafv9KasVUYKQjYKGmenZ7XJRAGjtgQj4gQgMvGHPE6d5ZDV2TDQ32fxgmAtU3Fq9Enpk3b5NWoUQuGPZZPgKG), [3Zaigdmx3s…](https://solscan.io/tx/3Zaigdmx3sE7ZPfHbnzbhQWRbt7p5qvwKkELWtmPEoMvehaq3qUimjb61Gxtqxg5BxrA5kx6dZu1P36Wae443eS8), [2U8M1VkNcf…](https://solscan.io/tx/2U8M1VkNcf2pBYYvzGhUovzRjkFtn2ULShiXPTAGe34N9bFy33dBPJzM1DGbhrBJerRbxkD59UNydsAgBjtidRU1), [4MhJFc1SHu…](https://solscan.io/tx/4MhJFc1SHuvcg32unAnFyEyz9TWvHyZyErfUp6cYJj7AHV31T3SfwzXCdj38JUUeQwVZFDoynBG9C8vnNJ7nWJu2), [5Y3SmAFAGs…](https://solscan.io/tx/5Y3SmAFAGsXXJp6YjNDsmgJVdueghfmCQjh12bq9umaGYbhvke5jKVtruefhesuFk2vqYPUoyZEhp1FX7sZNhT2S), [5DzfHZj1B5…](https://solscan.io/tx/5DzfHZj1B5qXzmVQVtPAeaTYSSvNYtwpJZfVpXQsScHCfie33XyX82kxrKR9bRGZTKXJvKAE3uXUnYEza5vFeaTr), [57FMKX4rtC…](https://solscan.io/tx/57FMKX4rtCxYbPwUqkEBD5VgZ1gM39i1rxJxDaEUfN8ftC4gvjjtcZvCCRRJFqrGXr63SkHw62ciJufif1wbfATE), [5La48DxKpT…](https://solscan.io/tx/5La48DxKpTE2zmXVo1vAyAwbx4SQjbW793H43ZdLr6PhuSo2nT6WFewWLBDsLounU71zRyXNqdHzga3pKsAPJ7Jn), [3KQRa9YHui…](https://solscan.io/tx/3KQRa9YHui73WTL1qoErQFS74N43RcmiPESvqk2SEDsWCJbvi2YFUysXteJWoupd1269QTH7f47An3NTZCDi7AcN), [FhtdvUwynj…](https://solscan.io/tx/FhtdvUwynjGpoGepFN5EbgL5xGB3GpYED3wZsVuLsrNu3MwnUTsZ2ABWnFrYmwoudyL4YuHqXvXqExb4gRJGq8J), [5P2fPu1D4V…](https://solscan.io/tx/5P2fPu1D4V7M4PMEjJgErBNHHxH6E7uKUUX9ptBNNzi1W6eXjq5njMVunho1vwGUnW9Q2sFGFX8isxE7iewGFzLL), [fQPwhyKY9Y…](https://solscan.io/tx/fQPwhyKY9YsYCUSYYwVsieHQmh8iaug3WK6Udfryti7JjhHqwyfwKe54V8WXptq8DeiM2vb5ByC6dVamuwgQw8G), [3KzUgnumuU…](https://solscan.io/tx/3KzUgnumuUnc9yiSRHAcigcyT4zUgwp3oxg1g6fuKupGKqWZyAu5BWMiv1dkNmqw73gPHzXAedaEfZYWwuQKMhbD), [5M3Kt6B4YZ…](https://solscan.io/tx/5M3Kt6B4YZ6Tn7g5xd6u1rJ5h8NynxBfPYTnwJiqgSikwy5oEYCuyJbPpcKUYUnD3FNFwNqHJHQ44ESzeCuDHxnU), [1zKSnCEkvE…](https://solscan.io/tx/1zKSnCEkvEeWVJuTc6MAvqdbbueSmyDJSqTMKZ1cWNykwbWeMHytGwJKYAxm5BL7NLxXDDjMw9nhdXiS9v5zQTY), [4iVxN8sr4C…](https://solscan.io/tx/4iVxN8sr4CvipHvxB8F8ciWraAomdBsCtg8FRdaaMXgz5wukTZaJgijBdpicEZ3AwYcJTZMQNVPXQR1kx8QvkEM9), [StCYWrrjb4…](https://solscan.io/tx/StCYWrrjb4voDtLomNhnT5pwLJo5fsgFUQLS25c81qJQoJQN1FGEGBKyybc1Djod4d8yk7NH36WGeFcKw6h81SZ), [2FgQAc6nXW…](https://solscan.io/tx/2FgQAc6nXWGeovyE87THvu47Dfi3kej2DSf5G91ru1wroKB9Rx8JNEcE83EVCWnyN4aXq1oz6wv8jLj1VDyN2G38), [5xBYiM1GDe…](https://solscan.io/tx/5xBYiM1GDeu2W18z1YViyR2V2qgscMDUYKAkeNa86m5ESKjRjf9z5h6YPyFYL7cHwLQ3GRajvAZbF2NdYS4WTtQf), [26SUbQ3Uer…](https://solscan.io/tx/26SUbQ3UerBZEUFr588d5hFyj2VGAcNf72UaPGxnvwJZjBujw4UeXb6VTnBYJraetH3qWvrhF4ZoKh78bZD2vzmm)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×23,711, ClosePositionRequestEvent ×18,508, InstantCreateTpslEvent ×10,607, AddLiquidityEvent ×6,124, InstantCreateLimitOrderEvent ×4,332, CreatePositionRequestEvent ×2,796, RemoveLiquidityEvent ×2,790, RepayToCustodyEvent ×500, WithdrawFeesEvent ×480, WithdrawCollateralEvent ×273, LiquidateBorrowPositionEvent ×203, DepositCollateralEvent ×183, BorrowFromCustodyEvent ×141, RedeemStakeEvent ×100, IncreasePositionPreSwapEvent ×28

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-31 00:00:11 UTC | InstantIncreasePositionEvent | SOL | SHORT | $350.49 | $117.43 | - | [vKraJhaqrk…](https://solscan.io/tx/vKraJhaqrkawmaSmDUw3jjNDGmkGbyV8ppUV3wcjLPa43cndrnZedBf5VzZ474nm2ey8jg62EAcbGijHKpWFotT) |
| 2026-01-31 00:01:23 UTC | IncreasePositionEvent | SOL | LONG | $492.26 | $117.40 | - | [31ALv9ngeG…](https://solscan.io/tx/31ALv9ngeG2eKZoEnZ4VRZiwPGBNTY9fpakmyAacwAYZc8pkXJ6JBpc4ZzkuXZs8czt356RBJzsicKyQf3K9d2zY) |
| 2026-01-31 00:01:51 UTC | InstantDecreasePositionEvent | SOL | LONG | $265.50 | $117.38 | $1.26 | [4DguC1cGir…](https://solscan.io/tx/4DguC1cGirMp6qEurttoCZrv3U9D7xUW5MptUJz27uMocYrbaByMgj4Avw8H6iRy1FX23bZpFfD6AVBQT68PDoap) |
| 2026-01-31 00:01:53 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $60.00 | $84,026.91 | $0.08 | [48SEguHapG…](https://solscan.io/tx/48SEguHapGvFmSwXrnkHyFu9igbkg8TvKDL4fs8KuwMbUwUWiYY2QrCkXSqrXqcjKf6R7DzTCuTCkEVrmPLwuFEw) |
| 2026-01-31 00:20:01 UTC | LiquidateFullPositionEvent | SOL | SHORT | $23,492.23 | $117.61 | $-130.85 | [32UD8xCDDu…](https://solscan.io/tx/32UD8xCDDufekMgxeEfRcikQ855Weax6TExb6fpU4ZHrKVZNpS6jjwNGK3p24ebwbQBAk4zvX2KBsAtg47DDrqZW) |

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
