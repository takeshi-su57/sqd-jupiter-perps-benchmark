# Jupiter Perps × SQD — one-day benchmark: 2026-01-30

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 396,800,384 → 397,016,697 (216,314 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-30 00:00:00 UTC / 2026-01-30 23:59:59 UTC |
| Slot just before range | 396,800,383 @ 2026-01-29 23:59:59 UTC |
| Slot just after range | 397,016,698 @ 2026-01-31 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 397,016,697) |
| Blocks with Jupiter activity returned | 46,134 |
| HTTP batches | 568 |
| Raw data (decoded JSON) | 62.0719 MiB |
| Transferred on the wire (gzip) | 32.44 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 176.3 min |
| SQD overload retries | http529×696 |

## Trades (valid, executed size change)

**32,011 trades**, 5,346 distinct traders, total notional **$491,683,676.21**, fees $698,360.32, net realized PnL on closes $-2,696,502.03.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 11,046 | $207,166,247.75 |
| INCREASE | 18,216 | $240,101,666.74 |
| LIQUIDATE | 2,749 | $44,415,761.72 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 22,473 | $299,501,455.67 | $112.18 / $115.68 / $118.92 |
| BTC (Wormhole WBTC) | 5,955 | $112,900,303.93 | $81,028.40 / $82,726.81 / $84,587.63 |
| ETH (Wormhole WETH) | 3,583 | $79,281,916.61 | $2,633.23 / $2,723.39 / $2,824.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 20,594 | $308,247,391.82 |
| SHORT | 11,417 | $183,436,284.40 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 16,582 |
| InstantDecreasePositionEvent | 7,371 |
| DecreasePositionEvent | 3,675 |
| LiquidateFullPositionEvent | 2,749 |
| IncreasePositionEvent | 1,634 |

Also decoded: **1,616** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 32,011 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 18,216 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 2,380 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 369 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 11,046 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 13,756 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [2fJUb9eC4f…](https://solscan.io/tx/2fJUb9eC4fubApbp2ZDeNSiCy1XRDY8ungzHnzwBQfQxA943yk8qWybsGvgey8p3Ath3SS2mqLYyPKmgMofrnvAk), [2Hk97i3Pbw…](https://solscan.io/tx/2Hk97i3PbwtCaZscqeMsBaQyKQRbAennk3D2XGWmd7VJ7xZizz7WTSvAZYfzMKvrWeCDCKMj8pHTMKpRbAk3LLYS), [5WsZHwxXqE…](https://solscan.io/tx/5WsZHwxXqEEFPauYKevtoiSa7g5dCv4HPGWNKt4wKhC6XsatEscQNkRPQLFjQnUFB825j2y29DyrPqCAkfAELs88), [47fcdWWT6G…](https://solscan.io/tx/47fcdWWT6Gij8CqkhkssQHskmfn9UEYH96kY7j7G9j6W186R1WJgyDi67UVeZ7Ux8HqdU82h71v3udYGbPh98QpD), [5cUuLnTvJe…](https://solscan.io/tx/5cUuLnTvJehJ154X3nhbKuBEhNBLBYwDU2vwRSZqnXkV6cpBxCTi24suqonSRNbBygHw65BPWhcQiLwUnaGTDVoE), [2MwTLBCLdM…](https://solscan.io/tx/2MwTLBCLdM7fs1xBhSJWAtY4R48CC86HuBLZ7xWP7DnmNJrs6xxxHRn9LWFEahDEuqW2XEkeWXAUA9gXfLT5FoYY), [53wJ7DwPow…](https://solscan.io/tx/53wJ7DwPow8oeRpppWBxcNMtox5bzwvT6cJRHAyemUu1MmqojABUmtr1XoRwqD8PDvMYyJHY8ss1AvDPnfb5qbw9), [3bUKmsCFJU…](https://solscan.io/tx/3bUKmsCFJUaGbqrHUjKQebWA8zRCN81wMhThUGvvDocnqbeCzT1V5w4Tadenk28V58W7n87bcXXG7Z6LW3u93qm8), [62mbFtvkPP…](https://solscan.io/tx/62mbFtvkPP8uh64VBWAnW18WuygWyc8hXty1i6GqpY4D1CBU731i2Pty4JmjgUXLyqrL484xutAcATwoYg6F84Au), [ACkHSbQfbv…](https://solscan.io/tx/ACkHSbQfbv36iHe9DnB9aCEViTBVTmBxG7qWRDikAGn3aAJuKpMzyUHcmnBpYh5f4YfJeY3nG9LhugQEeDjDZHc), [48VhDmDDH4…](https://solscan.io/tx/48VhDmDDH4W5wuvQAXAtT5JfHdpGVTKJtPXKRB4tbA5n33xDVJ6dqKMSjgRDfr9dQkohYNGVCzQnJVrFuQTessNZ), [4aqVe6PMfm…](https://solscan.io/tx/4aqVe6PMfmwbRhXvv3Z33Dr8AztAn9fApTmyxLdjAFzUXNaw5cWHd3tbtmSyChGMHDz2GCxd6jjjYsjgfreKvWrQ), [5osQqzvr9X…](https://solscan.io/tx/5osQqzvr9Xi3y5CPQZBy8AqCUBKoBSXZ7XQLYSWFJsbvXTGMJx8m9SSP8HT1E7VStAhrLMQJRmMdCT4VTaFACg27), [G6sXDqC8Wc…](https://solscan.io/tx/G6sXDqC8WciE7NRkzJ8Wkbm9Vm7nXJQ9X2K1sXX9n9YrXqbzJxvQLRVudcW5Do9Dp3DRvS7NeTnMQW5Xn5WoTtK), [2DNyPBcEsn…](https://solscan.io/tx/2DNyPBcEsn1y2VRpbDxv8C6yq7RHH6Fidt6DffRNiW8b1FSegcYX47jtuDpV6LJwcBDBmiDjoN2cKabfuYfJMjG9), [3wHepx5Uat…](https://solscan.io/tx/3wHepx5Uat5DMR6A3B51aJrCFNqjVamqwAmVMHMCbJMuogmmGfir3nWikkT6Sn21iQBNHot8WzBqxaGxUsYe5EXJ), [5WpV4FvpDV…](https://solscan.io/tx/5WpV4FvpDVaYwUDoHddMUsJgoJmgEZbc3323m4JxsbHnKc31xq6mRxAZAni29Erz5h42XzWVVHo8gaVNiTAu5NjG), [4phq8vo1Bb…](https://solscan.io/tx/4phq8vo1Bb2BiQsP3mvGXz9uHi4AjFCbLttpDmNjsJRuiMijbaEgqaWJCPcDDYzZpKzDpzNjmGxScL9sGF3YJpxP), [DRQGuYbWXk…](https://solscan.io/tx/DRQGuYbWXk9LqWWqd7gNxfgjvnZtHFjuhMP9C6Gv77H7a2w72buFw59XZJeat8awRANGmZHmL1rHAumSb17m3si), [5genqGFtwg…](https://solscan.io/tx/5genqGFtwgNbqSzRgGeBXs3dVtk7q9QqNLdU92Q5r7WRHxvc941D8nx45e8iDybsxopsqzL7ofm529hhLryGyrMo)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×14,112, ClosePositionRequestEvent ×12,762, InstantCreateTpslEvent ×8,279, InstantCreateLimitOrderEvent ×2,335, AddLiquidityEvent ×2,050, CreatePositionRequestEvent ×1,953, RemoveLiquidityEvent ×736, WithdrawFeesEvent ×480, RepayToCustodyEvent ×242, BorrowFromCustodyEvent ×138, WithdrawCollateralEvent ×121, DepositCollateralEvent ×109, RedeemStakeEvent ×43, LiquidateBorrowPositionEvent ×40, IncreasePositionPreSwapEvent ×23, DelegateStakeEvent ×7

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-30 00:00:12 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $70.49 | $84,526.31 | - | [3xM9LU8Zou…](https://solscan.io/tx/3xM9LU8ZouguT9qB4p8J5Zrs2hDisCM2bBKVD8LMPi8Ri65wRFVizuZ7CRaSSWx6p38dn7ZrEZXzX6xXrPXE6wr5) |
| 2026-01-30 00:00:26 UTC | InstantDecreasePositionEvent | SOL | LONG | $21,537.57 | $117.70 | $40.93 | [2Scxu3PYa2…](https://solscan.io/tx/2Scxu3PYa2BP9iep6xSDPyw99FvDSxgVULRqvELWCga3Ugmgp9NBvdToyByaJJhceTxLDgLFnZcM7T5MjcL2QfG9) |
| 2026-01-30 00:00:34 UTC | LiquidateFullPositionEvent | SOL | SHORT | $478.65 | $117.73 | $-9.89 | [6jG9W71Cz5…](https://solscan.io/tx/6jG9W71Cz5smBLEM7Az5nuALYcGrsyzVnHv6sNri62DdLzRobg8i6wfKbksTvcb43NCoif7Cn3pWeSqtvtq2AJi) |
| 2026-01-30 00:02:54 UTC | DecreasePositionEvent | SOL | SHORT | $13,673.09 | $117.79 | $-30.08 | [4hgAGemwNc…](https://solscan.io/tx/4hgAGemwNcczihFW3jYcN21UeiPNYBheEg1WJXn7ETVafpZvhc7zxBdErNYgmojKJyT8DUr6RzhNhmod2su767Gd) |
| 2026-01-30 00:03:38 UTC | IncreasePositionEvent | SOL | SHORT | $903.68 | $117.82 | - | [4K47dFu6mo…](https://solscan.io/tx/4K47dFu6moJvhoYhXnosUgMzY8txifpw4615MpGtYqHzU8hRpZCTPE7CZJofm9ekvdDu4A6P8oLZM6J5BhjS2M26) |

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
