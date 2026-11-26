# Jupiter Perps × SQD — one-day benchmark: 2026-01-29

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 396,584,441 → 396,800,383 (215,943 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-29 00:00:00 UTC / 2026-01-29 23:59:59 UTC |
| Slot just before range | 396,584,440 @ 2026-01-28 23:59:59 UTC |
| Slot just after range | 396,800,384 @ 2026-01-30 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 396,800,383) |
| Blocks with Jupiter activity returned | 43,742 |
| HTTP batches | 497 |
| Raw data (decoded JSON) | 64.2488 MiB |
| Transferred on the wire (gzip) | 32.74 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 149.2 min |
| SQD overload retries | http529×624 |

## Trades (valid, executed size change)

**32,312 trades**, 5,865 distinct traders, total notional **$461,359,658.66**, fees $654,543.23, net realized PnL on closes $-1,682,555.85.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 9,769 | $174,567,631.05 |
| INCREASE | 19,838 | $233,217,216.46 |
| LIQUIDATE | 2,705 | $53,574,811.15 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 22,698 | $294,296,623.37 | $115.24 / $118.12 / $125.29 |
| BTC (Wormhole WBTC) | 6,265 | $101,681,618.42 | $83,236.21 / $84,900.98 / $89,195.33 |
| ETH (Wormhole WETH) | 3,349 | $65,381,416.87 | $2,750.68 / $2,821.63 / $3,007.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 23,360 | $345,613,629.14 |
| SHORT | 8,952 | $115,746,029.52 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 17,823 |
| InstantDecreasePositionEvent | 6,520 |
| DecreasePositionEvent | 3,249 |
| LiquidateFullPositionEvent | 2,705 |
| IncreasePositionEvent | 2,015 |

Also decoded: **1,720** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 32,312 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 19,838 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 2,581 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 124 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 9,769 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 12,433 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [2D8gfwnF83…](https://solscan.io/tx/2D8gfwnF83Np29fUX3YYGLgTiWmHKZuPRrqrFteTHuXvjr11Y6jB2i6736PeXzfWffY7qtPNx6CbgBYfrwmtT7ws), [3AgcNu2sB5…](https://solscan.io/tx/3AgcNu2sB5go9XBFFJfRJ73bz5qBA8cfQaVuEcq4RGUmZiJgAf99xyw4D45KwN4vHFNy7ZKkQS3MaXDPJBzw9C1z), [3zPAPgup1H…](https://solscan.io/tx/3zPAPgup1HFU8RzqH6Ayrv1XY6j8Bcws2YMYsQeK5b2SvW86DxURJ3eoDPGp6myJaJVjbrYNf8DbVX9zC7Q9Pc4e), [5Fu2zRuAyu…](https://solscan.io/tx/5Fu2zRuAyuzUhh5xHvjyCsmuL9HwSRycWuQnqSQYGHWNZMDkE1nQSKePBVueXUaimAM2LLZv4MSwtYGoVT1ywyMo), [2zGVo8gfrd…](https://solscan.io/tx/2zGVo8gfrdpxAsKK2E4N8DdP1pqUYPV3wQS2PUVXYMygPXEMSP5DNC181BDQMSMrLriks5n11EsHsuyauUGHwGdo), [48eFSHXpiV…](https://solscan.io/tx/48eFSHXpiV9Msdi2TUXNmnBzKjU1kwRULkP5nx8sxUEYkePz3RExAttGgrpGzrR9d6V6s3QmKZLsh1Mo43yqUxPW), [3Qm7SFyeF9…](https://solscan.io/tx/3Qm7SFyeF9KST9spN6XLXTiDPDq98tV7Fz6rgANzcc3TtpUTJRN39iGB8HStr6D5QLWuWLrhrZ4ycDX2aP7AGTaz), [5LvP24HLif…](https://solscan.io/tx/5LvP24HLifQmwzTLmPPYLvVUhx2mvuiLh9Qy5hHWeXtzbrh7XNSec9Lwgk8AMqqcd375LN224T1375N4LCwjkrpd), [5v8XE7Vqbr…](https://solscan.io/tx/5v8XE7VqbrE66SMG8JAuz3cCbWqXwwLgzoh9bVXaqKsUDTkUcDJSsThq8UutpTUDtGyk6gdQreXA3ouRLFLU8joL), [xkxZkRPBNr…](https://solscan.io/tx/xkxZkRPBNrDsgugz4jVdnMzoRUvW7W5GogQkqNWeipXXavK4iB24jLpKQA6Fidrf17n3XENAf5nRMVvbSfn1EZf), [Ab7Yzn2h3E…](https://solscan.io/tx/Ab7Yzn2h3EvGoJcMLjiqroQbxZgKf6Pb1QyJmDYaNdU81tfcSWSUxqfUKtAaQs9ABLbt28TLjWgzQRiH639mcw8), [3QJc9A1uHW…](https://solscan.io/tx/3QJc9A1uHWpPoUwyZe6XLUSKACSXu8h29tPEwXkwN1ANPRZ6gRRKZ3PhocDLt5nNRXLrPRwKHctYD45FFzig2kaE), [5e5PNy5QWF…](https://solscan.io/tx/5e5PNy5QWFHNbJPzpqfxqpATsTNg6K2ZcXsQZFKwmZF9VkPqH5yDj7TfLMJmCDEiY7txsaYS8RhgJd1nCEUHVRMS), [5CHht3wVLe…](https://solscan.io/tx/5CHht3wVLeRPtug6HajdtGW6hpCc3qBZd8JNu7zJtG3vc4wnsCbaN4tqEYjjH9w1H5qLsDFfXS5LVeLaZBqxCds2), [21cNyTns35…](https://solscan.io/tx/21cNyTns35oLtWiDobC8wzKgyvjR7a93cxuhcmydRpq2JDmMC3PXfQaHp7uiAoK3YfuC3WGEDXkNB9RzWdG3ihcN), [4Fh98hSyN1…](https://solscan.io/tx/4Fh98hSyN15L4TouqjispihP4ecQrvrAx1qDR6mTTEf4iAaBto8pxUrYCFfsfUGyJn32jcqevpLGg42EDNGoaJgm), [4kkag6WQ2k…](https://solscan.io/tx/4kkag6WQ2kyymWMFNfmv895Z8SThkt5iovyzULnsokaNTx2AQKzGARwdJnUvwUZvVbjSE45Akd6MCZQueMUaAYfq), [4gvJ238757…](https://solscan.io/tx/4gvJ238757y5Q7o3sMYiKhovEcTrJ26KhzkihvRWcuYTFaR64VS1zg1KEyTiDkLQ9i4Mv5KxuMqQhekRwE4k8wxR), [3zy5cbRm2t…](https://solscan.io/tx/3zy5cbRm2tDrJv91wFve2YVobCMBnEmt2DZdLfuTf487J6MNWkkcD3KvvNcc6LfDeavam3s1mvmbi9bNa8hWN5hG), [7iMV7ePkPG…](https://solscan.io/tx/7iMV7ePkPGya9D5Upe9hSB5KMar5rZjpGrEEhmwivoNMFhbfeCLA3W6hvs7hawx1HFgAtRQXnjyLvT4BLSmrg4M)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×15,596, ClosePositionRequestEvent ×12,577, InstantCreateTpslEvent ×7,932, AddLiquidityEvent ×5,112, InstantCreateLimitOrderEvent ×2,719, CreatePositionRequestEvent ×1,582, RemoveLiquidityEvent ×928, WithdrawFeesEvent ×480, RepayToCustodyEvent ×219, DepositCollateralEvent ×101, WithdrawCollateralEvent ×95, BorrowFromCustodyEvent ×93, RedeemStakeEvent ×83, IncreasePositionPreSwapEvent ×33, LiquidateBorrowPositionEvent ×7

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-29 00:00:15 UTC | InstantDecreasePositionEvent | SOL | SHORT | $4,955.06 | $125.16 | $-5.20 | [jwWFbDtpV9…](https://solscan.io/tx/jwWFbDtpV9G2S4uWhQ5dapM9c2cQ3RrEXnk2db8JGNQT7btMVf1qHgp8rjw1BwFAEHM9n7zjUFfuTHgSPDwfEBS) |
| 2026-01-29 00:00:34 UTC | InstantIncreasePositionEvent | SOL | LONG | $141.26 | $125.17 | - | [4aPfMS6FVn…](https://solscan.io/tx/4aPfMS6FVnRhX7gy89YE3816G5J8s3k8rze2JyHfUwHtTvu415EwnyocWHquP8iRMF6YNqpTmw3T8QKS9eYiXiFu) |
| 2026-01-29 00:00:45 UTC | DecreasePositionEvent | SOL | SHORT | $1,849.00 | $125.25 | $3.25 | [3XhRm6fdq5…](https://solscan.io/tx/3XhRm6fdq5bpxFfM49nkYnwuTN3y5PCvK7n3sL65g4RrxXxXzdiLvb8ixGgKp5KSeFKwhsWu53zWMd1r5x95U7ku) |
| 2026-01-29 00:04:34 UTC | IncreasePositionEvent | SOL | LONG | $3,988.80 | $124.95 | - | [5tn3vWyjpV…](https://solscan.io/tx/5tn3vWyjpVVgzrBR9m9T2djRdgjKuxtN4ELLSsrXKvxpYzTSLeaMjWGRkynBfetZE6fBszDr2WwMkKfvTBRiuSBL) |
| 2026-01-29 00:04:37 UTC | LiquidateFullPositionEvent | BTC (Wormhole WBTC) | LONG | $1,716.30 | $89,030.35 | $-4.13 | [2ZGxKg6FBo…](https://solscan.io/tx/2ZGxKg6FBonFUxcL6Lj7EUzAyQKjQrQQc9zTskBwb2MZKc9o43zjFTJkbkPmSRfFi5hxrxZ3kXr6GbooxCfaoizL) |

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
