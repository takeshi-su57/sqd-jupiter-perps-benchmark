# Jupiter Perps × SQD — one-day benchmark: 2026-01-25

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 395,723,262 → 395,938,479 (215,218 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-25 00:00:00 UTC / 2026-01-25 23:59:59 UTC |
| Slot just before range | 395,723,261 @ 2026-01-24 23:59:59 UTC |
| Slot just after range | 395,938,480 @ 2026-01-26 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 395,938,479) |
| Blocks with Jupiter activity returned | 34,311 |
| HTTP batches | 492 |
| Raw data (decoded JSON) | 46.988 MiB |
| Transferred on the wire (gzip) | 24.44 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 117.2 min |
| SQD overload retries | http529×497 |

## Trades (valid, executed size change)

**24,579 trades**, 5,282 distinct traders, total notional **$291,131,047.47**, fees $482,353.77, net realized PnL on closes $-2,707,449.36.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,437 | $98,214,705.25 |
| INCREASE | 15,434 | $141,205,144.22 |
| LIQUIDATE | 2,708 | $51,711,198.00 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 18,433 | $212,456,339.27 | $117.20 / $121.48 / $127.26 |
| BTC (Wormhole WBTC) | 3,817 | $54,057,515.30 | $85,985.87 / $87,324.50 / $89,177.48 |
| ETH (Wormhole WETH) | 2,329 | $24,617,192.90 | $2,784.00 / $2,844.53 / $2,953.90 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 18,661 | $216,283,585.29 |
| SHORT | 5,918 | $74,847,462.17 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 13,374 |
| InstantDecreasePositionEvent | 4,013 |
| LiquidateFullPositionEvent | 2,708 |
| DecreasePositionEvent | 2,424 |
| IncreasePositionEvent | 2,060 |

Also decoded: **1,589** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 24,579 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 15,434 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 2,085 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 623 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,437 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 9,126 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [P8Z1pksxxT…](https://solscan.io/tx/P8Z1pksxxTXi5KLHW6sa8aEMATMBQ9JrSe2YGLCrVRjNr3yrGgJWVE8mN2c4c5yrMYD7R9pRHFDfjdAQiX53eff), [5nEWq32dEv…](https://solscan.io/tx/5nEWq32dEvRo9p5MEdCGo1JsYVKB97EZMGgrHwsQXLUr6sFQsb4Wkit23CsdUZFFRiuuTNuBDDQMDN9cwJP1vtGi), [2SScYPaCdf…](https://solscan.io/tx/2SScYPaCdfeijzHrrVWpoYzzurg5fQ4H3WjixCYviMQeZKbQVCdHZ61KgWHR8bUm7uE8R3yrLZ88FXyW2aJbP2Du), [3KfJy6ZtUr…](https://solscan.io/tx/3KfJy6ZtUrEaMZgDNjTjQ4hFBV7RS3ErcEBeGCqR9hUGiKCrQvxbqbiRyhdoawyfNwDQbsfVozzomtWTw1S1P7YR), [5piotxpEfe…](https://solscan.io/tx/5piotxpEfeQRh1GAFPXBCTrtwuL3JX9GwjmYkR3DeJwiy62wsMAUd85PL1XKGV59vPZ42mJJKEJe6dq3itnhi93m), [5p7aFGDTh6…](https://solscan.io/tx/5p7aFGDTh6ZCnCcDjmXpF6k5FfZt4xMAkDhEMNDRMo2uszew7AXNvRf5JV4Hs3eD4229g6wxaxRw7gvzGWo9LqnQ), [5WVQeJfsPn…](https://solscan.io/tx/5WVQeJfsPnyVWVeAJEoLzZp7WYGtjWnj2ZH3AdDi1MWyCUxAMqcNoeuucbGh6rgEPKJJc6oo8Cxj9t5FtzBJFFbY), [4ous9KyWhJ…](https://solscan.io/tx/4ous9KyWhJbTFtGwghYU6ZXWG9BjS6hjsZsHztWYKQAM1HzsrZkwsuD4BhHwtCHdxzaDET23xmyEWQmwJk7RyvBH), [3hHAEX2nNE…](https://solscan.io/tx/3hHAEX2nNEcLmYZYJcYWm4rAR5em4QXrT3TJC4f7XKJHyn7kuWM6QBANX2y8B5tMCqGYKGJjY3mM4mjeXALcgPM6), [3mtVQg6MVW…](https://solscan.io/tx/3mtVQg6MVWqTX8A17tJNTsHeNcFMeMhAgZXFwGMRmwFQTspQtP9Dn8ZrGzCnp7wN4CvwLggYCS7L7w9siktFFTn3), [2ebYbX4mU1…](https://solscan.io/tx/2ebYbX4mU1twsbyiwAk1FhkDWYZVLSw2P7QL33ASHVrHXgS5NgigqegSmdt1Sumifho3j83QsVsBRbq97odMCASV), [31skRh863h…](https://solscan.io/tx/31skRh863hDu4QXGJT97EU9aJrQBg8BsBuzorTHJ9Bru3naizB9AQk3Qk3RtTaNWbsQA8kY5LTVZ4avqvs5N84HH), [2QF7NZNBpb…](https://solscan.io/tx/2QF7NZNBpbvpmzszmhcnUPGeumtvmPhgyRNwUGi4WN9n3SeS1D2M3Gq5faqNcyTPAM6CvwiPVM6QJEJDyk5Aeitd), [2h2YHTAWpq…](https://solscan.io/tx/2h2YHTAWpqHHNTRv13ESAgJnMNo6dAW3SYc2Z13P3ySCUPBSVdyFXu6h56UDL9ZkwSU6neZVFhv3S1W3TAFZJUGf), [3E7Jv9RJj9…](https://solscan.io/tx/3E7Jv9RJj9ucT7FiWeGtdRGPA5J9UtpjnUFRewDXfFzRqeNpzGTWUNNXB55gMeife73NdiQG32CVDajp82zG73C8), [imEGtUpsvQ…](https://solscan.io/tx/imEGtUpsvQdRuJWUJeHjzv9x2dmuvUW3vWCp62YT4M7TFhwP6qM6DwzUebfDuNsMfJQCdCAwGta1CWqZVmSika9), [xxF4vWU8xD…](https://solscan.io/tx/xxF4vWU8xDEW7LJr9uNdjc9xqJdQR4KdTR6eirVfBNQ2BehkNa3NVYq4zd4P44K3CXCuSZx7AfB3ZD38WpYEnW8), [2DVp3wQv7R…](https://solscan.io/tx/2DVp3wQv7R9hNtKj1oKoApf7yAjJfE8ZF1y5vGkUerw8P16ERVzXQQSK6p71WRmdpagYnjzrj1LyM5tM3cNyrTQW), [3CKhf8KBqi…](https://solscan.io/tx/3CKhf8KBqiUTZr8Py4nMzJw4fdLLrixu2cBUPHT4TwkonenoC5bdfw2SAedUkSafJxx8U3U8Vbi6UQekhZgYcbeT), [4cu4L52Fzb…](https://solscan.io/tx/4cu4L52FzbuVd8JV9QfbfoPCT8CkcDRBTeZuF7DctREcgCjTmidq2DkpPL4imEfym2FrVAtBv2CstK5CEDYpCj3i)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×10,723, ClosePositionRequestEvent ×9,834, InstantCreateTpslEvent ×5,315, InstantCreateLimitOrderEvent ×2,068, CreatePositionRequestEvent ×1,716, AddLiquidityEvent ×1,338, RemoveLiquidityEvent ×823, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×177, RepayToCustodyEvent ×172, WithdrawCollateralEvent ×106, RedeemStakeEvent ×86, DepositCollateralEvent ×74, BorrowFromCustodyEvent ×69, LiquidateBorrowPositionEvent ×14

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-25 00:00:05 UTC | InstantIncreasePositionEvent | SOL | LONG | $2,123.86 | $127.01 | - | [3qimRnTiqH…](https://solscan.io/tx/3qimRnTiqH4YSZt5hgehj2uzvoWNA92nNPgTT4i7RC5zBEfmM4k3FqLVWukCmRhBTBXh1MgniDr6QCBKQTgfmKym) |
| 2026-01-25 00:00:10 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $6,781.63 | $89,086.32 | - | [2cHi2YHfHx…](https://solscan.io/tx/2cHi2YHfHx1Jm47P8Rb26nLV4X9MJd2sQkyXxj3jcm7zHPbercubg58SE5NBMkBNCWCfW1wkdMgfNFbgzFoD6mt7) |
| 2026-01-25 00:00:12 UTC | InstantDecreasePositionEvent | SOL | SHORT | $4,131.56 | $126.99 | $10.27 | [5SWAjiLpxb…](https://solscan.io/tx/5SWAjiLpxbq21ziHZbxAEwdHPHsAWfthHTCeSdV7Dye1JyLVvUYDnGE1FPDMAmJGuVwQmdRaLoCHkZ9yRJa5vFK) |
| 2026-01-25 00:14:26 UTC | DecreasePositionEvent | SOL | LONG | $2,422.01 | $127.16 | $1.99 | [4PxPgSA4Ha…](https://solscan.io/tx/4PxPgSA4HaYC2iswjLT7haLrAJisfWZLvxzgsbMwKPqaSWAJpgSzArGePQUmfoznxTcnXS7FqVMAfkXB4sy7gsee) |
| 2026-01-25 00:28:19 UTC | LiquidateFullPositionEvent | SOL | LONG | $1,865.37 | $126.84 | $-5.02 | [66hWgW9o9f…](https://solscan.io/tx/66hWgW9o9fkLRAfGwmZye2fcKG54gnvZfS4t9EToH74B5vmhRyBCFhFs6uPwcmS17HYuHxiSYpsReduG7zSfCN62) |

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
