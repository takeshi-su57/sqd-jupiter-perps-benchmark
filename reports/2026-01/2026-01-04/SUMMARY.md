# Jupiter Perps × SQD — one-day benchmark: 2026-01-04

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 391,149,216 → 391,365,654 (216,439 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-04 00:00:00 UTC / 2026-01-04 23:59:59 UTC |
| Slot just before range | 391,149,215 @ 2026-01-03 23:59:59 UTC |
| Slot just after range | 391,365,655 @ 2026-01-05 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 391,365,654) |
| Blocks with Jupiter activity returned | 28,831 |
| HTTP batches | 325 |
| Raw data (decoded JSON) | 34.4065 MiB |
| Transferred on the wire (gzip) | 18.00 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 103.6 min |
| SQD overload retries | http529×427 |

## Trades (valid, executed size change)

**16,727 trades**, 3,296 distinct traders, total notional **$222,365,049.24**, fees $213,859.67, net realized PnL on closes $61,594.20.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,391 | $99,553,970.78 |
| INCREASE | 9,840 | $115,613,547.88 |
| LIQUIDATE | 496 | $7,197,530.59 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 13,081 | $174,575,166.34 | $133.07 / $134.22 / $135.48 |
| BTC (Wormhole WBTC) | 2,360 | $31,892,354.11 | $90,590.77 / $91,248.00 / $91,748.15 |
| ETH (Wormhole WETH) | 1,286 | $15,897,528.79 | $3,117.69 / $3,140.63 / $3,165.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 9,643 | $123,485,415.04 |
| SHORT | 7,084 | $98,879,634.20 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 9,055 |
| InstantDecreasePositionEvent | 4,217 |
| DecreasePositionEvent | 2,174 |
| IncreasePositionEvent | 785 |
| LiquidateFullPositionEvent | 496 |

Also decoded: **733** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 16,727 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 9,840 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 496 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,391 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 6,879 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×8,051, PoolSwapEvent ×6,962, InstantCreateTpslEvent ×5,526, InstantCreateLimitOrderEvent ×1,320, CreatePositionRequestEvent ×1,290, RemoveLiquidityEvent ×522, WithdrawFeesEvent ×480, AddLiquidityEvent ×129, IncreasePositionPreSwapEvent ×122, RepayToCustodyEvent ×80, BorrowFromCustodyEvent ×72, WithdrawCollateralEvent ×66, DepositCollateralEvent ×52

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-04 00:00:03 UTC | InstantIncreasePositionEvent | SOL | SHORT | $1,412.74 | $133.28 | - | [2WaeT4SeUz…](https://solscan.io/tx/2WaeT4SeUzviuRYs1goHzc2T8uWxX9KRvH4kQNJjGPSpz3AsVMsXR6eeST25uh59vDVfJrs8c9Xxa8HHNHvftnMv) |
| 2026-01-04 00:00:08 UTC | InstantDecreasePositionEvent | SOL | LONG | $113.36 | $133.28 | $1.97 | [31dZhK637c…](https://solscan.io/tx/31dZhK637cUfFGo39ZQXUW4gNPwBb86KcHJ42TxF97pLGMGJGmQXo6u4k5pDu9XMFajgwq1ouRmc8GiE7aVmPZRg) |
| 2026-01-04 00:00:58 UTC | DecreasePositionEvent | SOL | SHORT | $7,305.78 | $133.36 | $9.52 | [4VaZkrX3pa…](https://solscan.io/tx/4VaZkrX3panvdRUTwAdUsUXBAwzMwVWb5iYQifCPHnYU25zKayYDLcuG4drjvvxFf1AQ3siQuPCVj8oRNx7RKT1H) |
| 2026-01-04 00:01:40 UTC | IncreasePositionEvent | SOL | LONG | $21.41 | $133.26 | - | [3wx5gQ5aXr…](https://solscan.io/tx/3wx5gQ5aXrEedDV6mTFiRbvicSXyx1H4tQn1hDYz3n1yhG9Qy8uMbMo3RTfQUofGH6AJv8TGKJFsiDUEBgjryGPV) |
| 2026-01-04 00:02:33 UTC | LiquidateFullPositionEvent | BTC (Wormhole WBTC) | SHORT | $1,227.17 | $90,739.67 | $-9.22 | [M8yriem2oQ…](https://solscan.io/tx/M8yriem2oQ1FhGebA3R8NRRqjyADEtbUvLnx9DqhXc7c1gvqyYzHziSQLRJy1fTLq3cvEVAzMMcvumewm5buzKk) |

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
