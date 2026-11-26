# Jupiter Perps × SQD — one-day benchmark: 2026-01-15

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 393,549,073 → 393,767,430 (218,358 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-15 00:00:00 UTC / 2026-01-15 23:59:59 UTC |
| Slot just before range | 393,549,072 @ 2026-01-14 23:59:59 UTC |
| Slot just after range | 393,767,431 @ 2026-01-16 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 393,767,430) |
| Blocks with Jupiter activity returned | 39,728 |
| HTTP batches | 422 |
| Raw data (decoded JSON) | 51.4327 MiB |
| Transferred on the wire (gzip) | 26.68 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 220.9 min |
| SQD overload retries | http529×743 |

## Trades (valid, executed size change)

**25,974 trades**, 4,034 distinct traders, total notional **$384,903,723.18**, fees $345,449.57, net realized PnL on closes $143,035.51.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 8,313 | $168,196,749.13 |
| INCREASE | 16,779 | $201,144,864.62 |
| LIQUIDATE | 882 | $15,562,109.43 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 19,729 | $273,032,015.83 | $140.94 / $143.73 / $146.69 |
| BTC (Wormhole WBTC) | 3,781 | $63,124,374.26 | $95,098.22 / $96,235.58 / $97,155.00 |
| ETH (Wormhole WETH) | 2,464 | $48,747,333.08 | $3,273.92 / $3,318.79 / $3,383.09 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 18,376 | $260,326,114.22 |
| SHORT | 7,598 | $124,577,608.96 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 14,724 |
| InstantDecreasePositionEvent | 5,323 |
| DecreasePositionEvent | 2,990 |
| IncreasePositionEvent | 2,055 |
| LiquidateFullPositionEvent | 882 |

Also decoded: **1,130** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 25,974 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 16,779 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 849 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 33 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 8,313 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 9,187 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [48uGpRxavm…](https://solscan.io/tx/48uGpRxavmKrpxnMWyEjSevXfEQvY4Ec66oVV1R4qxZffQWk3vt3fnVCDxVVPoxaKSeL41t7sqg3woo6kmyRLgjB), [3TFumtNmjn…](https://solscan.io/tx/3TFumtNmjneFKYzkj4sdoUQm6ohYxHjQMJ365UELdLm9KkhJkRftt36uAQHoqWdnubGEd2zLvuCpAabNAFWNvpWh), [3GwSnYbLj6…](https://solscan.io/tx/3GwSnYbLj6pMd5DZ8gjxSfzw3QShXVvt26KWcQF8GGJ3o8h9ZW2w5rbYfBQ7E7U9VcUS4Lk49o5trKsnBkk5C1im), [4jue1QLhYK…](https://solscan.io/tx/4jue1QLhYKemqVMEJLGabSGg89DcC1PXgKHFwdNVxXbx48z6sB5r68A9f1kTtodjrc9EH3jvsK3nFXRNgMFqWpxk), [2EyPNoNjxi…](https://solscan.io/tx/2EyPNoNjxi3MMHPp2xJaqiug47r2GxEA1bGURhcqzpLAaWKEbUqSCXaHMS8izM7G8e1kWhtDDgbk3m2PXnwXfQTN), [28WbMTkUsz…](https://solscan.io/tx/28WbMTkUszzSYZHj9xGAQn7wYCttyVTWQzrt2AfrGYE6m2NigG69NibdLy2oy9g3HHfAZeP7Nm54cNjYLZVLhDkh), [2rmL7N8LaZ…](https://solscan.io/tx/2rmL7N8LaZMDKV6XpUginJ3YgLpG7UzZQLa5mR1YhBCin2Xr6uFid9AuE4XDVg1xqgBko87fKvQxkrijkrBmJxDt), [2QddAbUHD7…](https://solscan.io/tx/2QddAbUHD77KFbK3SpFvnE4N2PWH2ju44C6sd8Ma3762nxfptaumtEtyhv8CcxW2AZHwovdMd4wt4kM8AcUkYwyK), [4ZXDJSouNy…](https://solscan.io/tx/4ZXDJSouNywF7VCXnpeXrFqXgJEtaohrY32UUBCHttsTtczCtbV1TWxKYTxUFb2cDUEfcErp79Vtcp86aW7WRbvi), [5baQb65zkt…](https://solscan.io/tx/5baQb65zkt4DEvBQ5aJ8SC7yxdUb7CLskHMQzXQPFvDwJeL4zHD75iVUH5Si1oNaYftT2kNvNqTeMTyV3HwGdShh), [5R5dP9Mqgw…](https://solscan.io/tx/5R5dP9MqgwLS6qbujXHk9Cr3hapbXMR2VT5a7HTNBHziVcmM8CKm6Bj9D5sQe3VDq3JNi8mob8YNeThK5LAhoTwD), [2ws8iyMFH3…](https://solscan.io/tx/2ws8iyMFH3sPGZ4UeNJRbyBQnJAn7xUPYQ3naCSBDhnviYRG9K7YABfL3xVs4HvZSdG4Fv7m8nH89ikBuozsTkjj), [2DkDqFyNG6…](https://solscan.io/tx/2DkDqFyNG6JrfZju1dGJPoavrsxi1L7rdzjepJ45G6MJsp1o6JBGx3uUTZjmeNHuMf74HF5Avbwni64A8gne1cLT), [5sHxMHvDp6…](https://solscan.io/tx/5sHxMHvDp6yDzC1oBoUhPJrsaa4CgKzSKZVEhpYTtaFSBLNA7N5DwgMyztzPtoAAE16uBLo6ZRYXWPBo58EUKTgm), [4VTpPnM3zK…](https://solscan.io/tx/4VTpPnM3zKaNMMiSmhFTBUef3urosSdcA9dDJ3p6banUheeDT17h91Ceyg8s6iK2Tyebv93miLY8bhdr4iyWGjAi), [36AeJhe3Ug…](https://solscan.io/tx/36AeJhe3UgHjspa4wYEd8juFL916HngC8zYtm7LuDXnq27yNZVC4JzgYNv9xfzGC7pGgvQzwPMDsp29NxpNBKkUK), [5g3678H2Hy…](https://solscan.io/tx/5g3678H2HyaThNMVogfX5XT7KqFzcAGtpqdeFC7AfuEHQh9zH4N8H68bPstnbUADfgaL4U8gxktcy3ioBWzuMvwK), [22M59BEwfx…](https://solscan.io/tx/22M59BEwfxb3M3JS2fde4xprVF8jcGdxNHvRXE7mPqijcMkjjEr6czS2MUxWqwxh8NDRmDbfSPHk4DvdeWVefDbg), [obtC3Z7XqE…](https://solscan.io/tx/obtC3Z7XqEq8kr8meegpTs6bcxSwFhm6v6FLT2rUWhoBDiNxdqZ8SYoUMSbbLPnAC3no6YV1pm3VXYGzeJ3kphX), [DocbkecftS…](https://solscan.io/tx/DocbkecftSQYy3vHVXF7nftRLAHeiLbdXD3HoDu7ohH7YQeFn2zwYxVt21ePE4ZoQ76MBVrybfE4gbcaRgJG1N2)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×11,817, PoolSwapEvent ×10,802, InstantCreateTpslEvent ×7,448, CreatePositionRequestEvent ×2,252, InstantCreateLimitOrderEvent ×2,109, AddLiquidityEvent ×837, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×213, BorrowFromCustodyEvent ×171, RemoveLiquidityEvent ×131, DepositCollateralEvent ×123, RepayToCustodyEvent ×119, WithdrawCollateralEvent ×61, RedeemStakeEvent ×43, WithdrawStakeEvent ×3

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-15 00:00:05 UTC | InstantIncreasePositionEvent | ETH (Wormhole WETH) | SHORT | $117.82 | $3,354.72 | - | [2kRfrq6JjB…](https://solscan.io/tx/2kRfrq6JjByTodVbsdFR9SbVmU1TH7ewEJEYb4VQZS6satK6odAfh41vLMaK54i9wtj5jY45Y5bifkbAtg2TBFqa) |
| 2026-01-15 00:00:21 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $13,938.80 | $96,938.95 | $817.68 | [3RjV27Co7s…](https://solscan.io/tx/3RjV27Co7sicRUrvxZq6wptFkvkCPu6hQvM5KAoqQg7B3Z5NPBifUnj3tEnDQFts24n4QQAFERH7WB9haMcNQn7Q) |
| 2026-01-15 00:00:46 UTC | InstantDecreasePositionEvent | SOL | LONG | $1,300.00 | $146.59 | $4.56 | [sqQCDoW1Fv…](https://solscan.io/tx/sqQCDoW1Fvxg5k7R3hhkWyD32pjJjZoGMdSstgZRFuTgL3kP5hPuCr9oyZQzfBbyN4jQ7BxftTP1g8d7WX4Xgte) |
| 2026-01-15 00:02:51 UTC | LiquidateFullPositionEvent | ETH (Wormhole WETH) | LONG | $13,103.63 | $3,348.09 | $-22.98 | [3qEii5e8Y7…](https://solscan.io/tx/3qEii5e8Y7P98wdJ4rKREZSNSPcJ7iriXTZVrzDHbnUp4A2LgR4kVXY2k8q3cFw2LK8iYyd9RgJH3RMx5dJJ9Vmi) |
| 2026-01-15 00:03:29 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $440,400.21 | $96,793.71 | - | [2TosHP6D72…](https://solscan.io/tx/2TosHP6D72YihxGv9e1q6VPMHePU1aW9gkBKy9WN8jZ7wWpZFeigYCLxeXofUTuwoGzX61PZruKumkd9RMBHEDv9) |

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
