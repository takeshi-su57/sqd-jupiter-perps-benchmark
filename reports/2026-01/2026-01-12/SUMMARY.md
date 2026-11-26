# Jupiter Perps × SQD — one-day benchmark: 2026-01-12

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 392,890,522 → 393,109,960 (219,439 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-12 00:00:00 UTC / 2026-01-12 23:59:59 UTC |
| Slot just before range | 392,890,521 @ 2026-01-11 23:59:59 UTC |
| Slot just after range | 393,109,961 @ 2026-01-13 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 393,109,960) |
| Blocks with Jupiter activity returned | 43,160 |
| HTTP batches | 397 |
| Raw data (decoded JSON) | 60.0878 MiB |
| Transferred on the wire (gzip) | 31.05 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 141.8 min |
| SQD overload retries | http529×547 |

## Trades (valid, executed size change)

**30,796 trades**, 3,842 distinct traders, total notional **$409,979,289.85**, fees $369,389.16, net realized PnL on closes $859,874.33.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 11,245 | $194,758,660.71 |
| INCREASE | 18,734 | $201,567,766.60 |
| LIQUIDATE | 817 | $13,652,862.54 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 24,821 | $319,769,703.21 | $138.23 / $141.16 / $144.16 |
| BTC (Wormhole WBTC) | 3,791 | $64,952,311.72 | $90,025.00 / $91,371.80 / $92,393.99 |
| ETH (Wormhole WETH) | 2,184 | $25,257,274.93 | $3,062.81 / $3,112.59 / $3,166.15 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 19,275 | $249,878,596.88 |
| SHORT | 11,521 | $160,100,692.97 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 16,814 |
| InstantDecreasePositionEvent | 7,187 |
| DecreasePositionEvent | 4,058 |
| IncreasePositionEvent | 1,920 |
| LiquidateFullPositionEvent | 817 |

Also decoded: **1,382** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 30,796 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 18,734 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 817 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 11,245 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 12,055 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×13,701, PoolSwapEvent ×13,102, InstantCreateTpslEvent ×8,931, CreatePositionRequestEvent ×2,504, InstantCreateLimitOrderEvent ×2,346, RemoveLiquidityEvent ×522, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×189, BorrowFromCustodyEvent ×133, AddLiquidityEvent ×127, RepayToCustodyEvent ×107, DepositCollateralEvent ×95, WithdrawCollateralEvent ×80

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-12 00:00:02 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $81,691.12 | $90,876.12 | - | [3SUVMEGPTP…](https://solscan.io/tx/3SUVMEGPTPRJMSRhJuNGKWjrYbKeE1zR1SmWpvz4mwWELjw136AabYnKMqFy1BtLWz5YQUPqNbaFLv61YNjs3uFa) |
| 2026-01-12 00:00:10 UTC | DecreasePositionEvent | SOL | LONG | $3,997.66 | $139.40 | $21.10 | [5nbSfEUCqz…](https://solscan.io/tx/5nbSfEUCqz2NFb2HG58tfSxmnK2x5sEtEznoBb8At5F4dJgKxuJZyM2KU4ZomLpXJmx6zu8YNpGjLWwy7yjFMeaY) |
| 2026-01-12 00:00:11 UTC | InstantDecreasePositionEvent | SOL | SHORT | $33,116.34 | $139.40 | $50.03 | [Sr4ncv4ELx…](https://solscan.io/tx/Sr4ncv4ELx8wsiKwmfhXConyZ5DjpAQq3RgdyRdUXdqRMLrucbYEKuDfvMUHh21VfbgVZmk84N4GBhejFTGEFnf) |
| 2026-01-12 00:02:38 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $203.22 | $90,888.67 | - | [4AXLEhaVnR…](https://solscan.io/tx/4AXLEhaVnRNTJB51q1TxrgH8XJmkviKsAv1FMW5Wxxq48gyMkLcekBBoYXh8MS5CK2A6QaMEut7KAuJLnSnPngAu) |
| 2026-01-12 00:05:31 UTC | LiquidateFullPositionEvent | BTC (Wormhole WBTC) | LONG | $5,648.20 | $90,688.22 | $-8.43 | [4KPDFxZmoL…](https://solscan.io/tx/4KPDFxZmoLrNchLH7z6kh7BMeq2ud2yrQPovMNhQ7chqLHxKkW1WRiLAtNFPrXvhvZTsZAPprN9hzi2VszJTxHay) |

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
