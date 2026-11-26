# Jupiter Perps × SQD — one-day benchmark: 2026-01-17

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 393,985,855 → 394,204,205 (218,351 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-17 00:00:00 UTC / 2026-01-17 23:59:59 UTC |
| Slot just before range | 393,985,854 @ 2026-01-16 23:59:59 UTC |
| Slot just after range | 394,204,206 @ 2026-01-18 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 394,204,205) |
| Blocks with Jupiter activity returned | 19,788 |
| HTTP batches | 412 |
| Raw data (decoded JSON) | 16.6817 MiB |
| Transferred on the wire (gzip) | 9.24 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 84.4 min |
| SQD overload retries | http529×373 |

## Trades (valid, executed size change)

**7,572 trades**, 1,972 distinct traders, total notional **$85,701,968.08**, fees $89,478.04, net realized PnL on closes $76,946.98.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 2,708 | $41,957,925.58 |
| INCREASE | 4,737 | $41,377,874.29 |
| LIQUIDATE | 127 | $2,366,168.21 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 5,717 | $66,704,596.03 | $143.26 / $144.07 / $144.89 |
| BTC (Wormhole WBTC) | 1,058 | $9,923,877.72 | $95,000.00 / $95,261.98 / $95,600.00 |
| ETH (Wormhole WETH) | 797 | $9,073,494.33 | $3,282.92 / $3,307.11 / $3,328.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 4,882 | $48,284,570.77 |
| SHORT | 2,690 | $37,417,397.30 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 4,432 |
| InstantDecreasePositionEvent | 1,887 |
| DecreasePositionEvent | 821 |
| IncreasePositionEvent | 305 |
| LiquidateFullPositionEvent | 127 |

Also decoded: **380** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 7,572 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 4,737 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 126 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 2,708 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 2,822 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [xvoZiUCrr7…](https://solscan.io/tx/xvoZiUCrr7ryZYHYG8wfhsdQYd1D5gzRqBi7G8TscfZ2z4cT7SPDaW9qaGh6UdeCqEypeoun49UxqtNNCuj7RwW)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×3,443, ClosePositionRequestEvent ×3,428, InstantCreateTpslEvent ×2,365, InstantCreateLimitOrderEvent ×712, CreatePositionRequestEvent ×572, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×363, AddLiquidityEvent ×83, RepayToCustodyEvent ×74, WithdrawCollateralEvent ×64, IncreasePositionPreSwapEvent ×51, RedeemStakeEvent ×43, BorrowFromCustodyEvent ×29, DepositCollateralEvent ×21

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-17 00:00:06 UTC | DecreasePositionEvent | SOL | LONG | $21.53 | $144.86 | $0.32 | [4JNgJsxM2x…](https://solscan.io/tx/4JNgJsxM2xtmohb635nomzkq3Va7QQgWHt6LWsCt767ADZEmSMUxy2fduKDdQUDj4MHgd4gvpoF6VuLfU7iwi6uh) |
| 2026-01-17 00:00:19 UTC | InstantIncreasePositionEvent | SOL | SHORT | $713.12 | $144.89 | - | [3g5mHHLvyQ…](https://solscan.io/tx/3g5mHHLvyQAxMi3fyEWXQaCFo6Qa7o389ZcAckRPsJmbJVLvQJ7WVEktxas4U6AkqtVreSutTdW7uE7unzRocsgN) |
| 2026-01-17 00:00:21 UTC | InstantDecreasePositionEvent | SOL | SHORT | $15,340.66 | $144.89 | $-272.78 | [3NM3YBjsGm…](https://solscan.io/tx/3NM3YBjsGmDXoQBj5dY7XEMmj71BPFpJjxY5dcAuLcNuekmgLVdxaGtSjX58d3A4fYd2jMpSazqG9V8rmQBjNKeo) |
| 2026-01-17 00:04:50 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $3,416.34 | $95,495.27 | - | [Phyj3S1puy…](https://solscan.io/tx/Phyj3S1puyi1f48oQT8Xrs6jVMo5qCdiUNWEoJXwnHUPQ4mqEvtKh7vqsxuiwzL1mkrqbhfhDDEiJ29xYj6bPu7) |
| 2026-01-17 00:07:55 UTC | LiquidateFullPositionEvent | SOL | LONG | $3,468.54 | $144.66 | $-5.02 | [4jzu7bjdSc…](https://solscan.io/tx/4jzu7bjdScEe8R3fdH68bejdxGtQzWY4kPdUqJro1H2aPoKwytdMrqUB2ZYtKvxkMxYx1neexCmUjHL3mn4PE4YF) |

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
