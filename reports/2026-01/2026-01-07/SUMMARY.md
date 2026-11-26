# Jupiter Perps × SQD — one-day benchmark: 2026-01-07

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 391,800,704 → 392,017,795 (217,092 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-07 00:00:00 UTC / 2026-01-07 23:59:59 UTC |
| Slot just before range | 391,800,703 @ 2026-01-06 23:59:59 UTC |
| Slot just after range | 392,017,796 @ 2026-01-08 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 392,017,795) |
| Blocks with Jupiter activity returned | 35,859 |
| HTTP batches | 356 |
| Raw data (decoded JSON) | 46.8589 MiB |
| Transferred on the wire (gzip) | 24.15 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 103.3 min |
| SQD overload retries | http529×423, network×1 |

## Trades (valid, executed size change)

**23,553 trades**, 3,641 distinct traders, total notional **$317,407,084.70**, fees $301,520.91, net realized PnL on closes $-333,484.47.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 7,716 | $134,046,412.23 |
| INCREASE | 14,955 | $167,571,129.58 |
| LIQUIDATE | 882 | $15,789,542.89 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 17,134 | $216,302,832.07 | $134.29 / $136.93 / $141.30 |
| BTC (Wormhole WBTC) | 3,800 | $60,778,298.79 | $90,579.63 / $91,534.65 / $93,677.96 |
| ETH (Wormhole WETH) | 2,619 | $40,325,953.84 | $3,123.28 / $3,172.17 / $3,295.05 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 16,762 | $236,619,239.33 |
| SHORT | 6,791 | $80,787,845.37 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 13,442 |
| InstantDecreasePositionEvent | 4,808 |
| DecreasePositionEvent | 2,908 |
| IncreasePositionEvent | 1,513 |
| LiquidateFullPositionEvent | 882 |

Also decoded: **1,024** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 23,553 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 14,955 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 876 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 6 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 7,716 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 8,587 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [5PCvGUvjcT…](https://solscan.io/tx/5PCvGUvjcT4XDZdM2MAVNz7oU9jmR4w54dHvBXUCH6FbVYswvBh7T2oDthEuZVwnZfpQeaoPSEVXHM8ehiy3ETuo), [28bGBnfh1Z…](https://solscan.io/tx/28bGBnfh1ZiadiPaZ3hMju7nQzNTsusEp5jaqVZiuqYV8UeqhPCR6iEqWUK3EFFezggzjjSKeH3hgSKXFtnyY1bc), [27XeE2pnLf…](https://solscan.io/tx/27XeE2pnLfjTz5W1rnJxwvdq5cJDhLe9LsnVgA3qJ6y4QBsd79HTaGqcW9D6VjSPUoxwGiiqXhH6vxsMvXJE6ENt), [wjWazxkDxM…](https://solscan.io/tx/wjWazxkDxMFyM4BjE8TCGtQgXcnhvS63X8pevws1Zsw3RbK3LfidLsqN1zhemrct1nxfDA8A8AqnXioMvLeD8HS), [2LLZnx4jYH…](https://solscan.io/tx/2LLZnx4jYH5xnGBcrVACg9ZUrSxjuAqKjbbgESRy8XgpsyJMwGeq1dnuEG9PfsewibTxTrLNeGW44BzqPx8vUJ5P), [411u8SURcc…](https://solscan.io/tx/411u8SURcckAuptLx8T7noeYDpaAYdkLnc1QMkwMkhr6LxcjHpnrBYwV9Pz3D94BGGaQkzvnECP5nKrZg8LE9yJb)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×10,690, ClosePositionRequestEvent ×10,193, InstantCreateTpslEvent ×6,582, InstantCreateLimitOrderEvent ×1,925, AddLiquidityEvent ×1,861, CreatePositionRequestEvent ×1,689, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×163, RemoveLiquidityEvent ×67, BorrowFromCustodyEvent ×52, RepayToCustodyEvent ×46, RedeemStakeEvent ×46, DepositCollateralEvent ×32, WithdrawCollateralEvent ×31

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-07 00:00:04 UTC | InstantIncreasePositionEvent | SOL | LONG | $2,798.02 | $140.99 | - | [3NNRhryjFM…](https://solscan.io/tx/3NNRhryjFMA4T3VdkkmT8iJtSscJUJ7obuCZyMrC5mAEDPav6vZfZivgRtdR53Ky6brPHS3jLJ2mhf2vFHWbdADn) |
| 2026-01-07 00:00:16 UTC | InstantDecreasePositionEvent | SOL | LONG | $877.47 | $140.93 | $-0.13 | [3fRk9ToS1c…](https://solscan.io/tx/3fRk9ToS1czT5DtMzCQpBH1qUviqK1eerjHDzmoRL2Qard5J4oB2gGQ1537SK2vEocUvmaatfxf8eDqXtcKeJm71) |
| 2026-01-07 00:00:19 UTC | DecreasePositionEvent | SOL | LONG | $3,308.98 | $140.92 | $6.41 | [3R9H2bN5Jp…](https://solscan.io/tx/3R9H2bN5Jp4wxBmEndu31AGvWf5J93iHUcPgnHvEb3VF3nDVyp2SgSgh46dcZ8nsYMBPXnmaervnCxfbvSkpChYZ) |
| 2026-01-07 00:00:27 UTC | LiquidateFullPositionEvent | SOL | LONG | $84,785.67 | $140.86 | $-204.89 | [3GXJtfkT1g…](https://solscan.io/tx/3GXJtfkT1gHqB66MRWrBGoiyUZvFTdqh76fizPASfz18Z87GoNgUGxa3MASh9Z8mXtz6wdg3u1VvSNtiamKfkoSF) |
| 2026-01-07 00:00:52 UTC | IncreasePositionEvent | SOL | LONG | $986.00 | $140.80 | - | [56afUZWz6D…](https://solscan.io/tx/56afUZWz6D91Zm4mAYyGing4ro1fjcr48fuwNP2iokqWJQP1D9KzaruZ7AD8N1Et52cubpfidhWsxTQfZAywWb5w) |

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
