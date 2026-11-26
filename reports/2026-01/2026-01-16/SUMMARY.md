# Jupiter Perps × SQD — one-day benchmark: 2026-01-16

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 393,767,431 → 393,985,854 (218,424 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-16 00:00:00 UTC / 2026-01-16 23:59:59 UTC |
| Slot just before range | 393,767,430 @ 2026-01-15 23:59:59 UTC |
| Slot just after range | 393,985,855 @ 2026-01-17 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 393,985,854) |
| Blocks with Jupiter activity returned | 30,696 |
| HTTP batches | 422 |
| Raw data (decoded JSON) | 35.8778 MiB |
| Transferred on the wire (gzip) | 18.96 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 190.3 min |
| SQD overload retries | http529×696 |

## Trades (valid, executed size change)

**17,502 trades**, 3,245 distinct traders, total notional **$226,366,497.02**, fees $202,072.29, net realized PnL on closes $161,705.61.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,448 | $106,190,240.80 |
| INCREASE | 10,548 | $109,776,051.35 |
| LIQUIDATE | 506 | $10,400,204.86 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 13,519 | $180,377,218.60 | $140.21 / $142.94 / $145.48 |
| BTC (Wormhole WBTC) | 2,427 | $25,350,358.10 | $94,259.74 / $95,210.00 / $95,803.43 |
| ETH (Wormhole WETH) | 1,556 | $20,638,920.32 | $3,251.59 / $3,289.81 / $3,325.43 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 11,166 | $146,935,148.70 |
| SHORT | 6,336 | $79,431,348.32 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 9,669 |
| InstantDecreasePositionEvent | 4,312 |
| DecreasePositionEvent | 2,136 |
| IncreasePositionEvent | 879 |
| LiquidateFullPositionEvent | 506 |

Also decoded: **798** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 17,502 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 10,548 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 505 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,448 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 6,946 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [4KEBgEoHHW…](https://solscan.io/tx/4KEBgEoHHW3eJHDCNc6N64S2VjoLy7uSDTN5JPAVoJRWXuz2MTtksyiStVWmfcZqtZQo1pm6xgN6wVU741BuKL7s)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×8,245, PoolSwapEvent ×8,020, InstantCreateTpslEvent ×5,539, InstantCreateLimitOrderEvent ×1,484, CreatePositionRequestEvent ×1,271, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×155, AddLiquidityEvent ×112, IncreasePositionPreSwapEvent ×89, BorrowFromCustodyEvent ×85, DepositCollateralEvent ×61, RepayToCustodyEvent ×58, WithdrawCollateralEvent ×49

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-16 00:00:04 UTC | InstantIncreasePositionEvent | ETH (Wormhole WETH) | LONG | $596.74 | $3,317.73 | - | [5gk94GUo84…](https://solscan.io/tx/5gk94GUo84Eg6SHNQrohAvv6sMLSa2z5vR5HR8gmNTehWdGz5xzzXrxkReWtQV3e4rMWteWe3Lw9CgtCDBUvwTw2) |
| 2026-01-16 00:00:10 UTC | InstantDecreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $26,206.01 | $95,579.05 | $54.07 | [2Dk6LcuFnV…](https://solscan.io/tx/2Dk6LcuFnVSXnYGDnerVxeUhhVEJWvjVoojzbtMv28jUK7V34YUVNRVGWxRVXBeVYC38LmY2S4jJxZ6XqLtCymWp) |
| 2026-01-16 00:01:33 UTC | DecreasePositionEvent | SOL | LONG | $246,146.49 | $142.33 | $1,515.01 | [2kvVEfPQeM…](https://solscan.io/tx/2kvVEfPQeM73z4DZaLyp2tZwHyHrCXk8wK5rHMhXG3XBeWHhTpco8k16khUsxV6B5fdu55ksQgSDRJ7Azj1tDbYb) |
| 2026-01-16 00:06:34 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $95,863.01 | $95,700.00 | - | [2dh7yfN31q…](https://solscan.io/tx/2dh7yfN31qeZy1FTP38M4SX9phJGxVY8uTPXqFkiVRxeYVhgWChw8WcTzUvrWMMKFya3brcmhF2BQpmHo4HXe5Y5) |
| 2026-01-16 00:35:50 UTC | LiquidateFullPositionEvent | SOL | SHORT | $1,562.88 | $142.74 | $-6.34 | [35kiQgHLu1…](https://solscan.io/tx/35kiQgHLu1SFuvP9oCsvquwnhk2w7wL91CQacZ5GiMvDamTMStDjRQBLs8sjxxn51XproyfpDrMLJrNiw3XPBg2e) |

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
