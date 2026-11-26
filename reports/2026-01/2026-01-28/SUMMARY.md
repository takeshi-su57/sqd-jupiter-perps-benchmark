# Jupiter Perps × SQD — one-day benchmark: 2026-01-28

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 396,368,725 → 396,584,440 (215,716 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-28 00:00:00 UTC / 2026-01-28 23:59:59 UTC |
| Slot just before range | 396,368,724 @ 2026-01-27 23:59:59 UTC |
| Slot just after range | 396,584,441 @ 2026-01-29 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 396,584,440) |
| Blocks with Jupiter activity returned | 35,135 |
| HTTP batches | 475 |
| Raw data (decoded JSON) | 36.7968 MiB |
| Transferred on the wire (gzip) | 18.59 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 96.0 min |
| SQD overload retries | http529×431 |

## Trades (valid, executed size change)

**14,659 trades**, 2,728 distinct traders, total notional **$206,030,020.49**, fees $241,813.12, net realized PnL on closes $-160,644.21.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 5,502 | $96,260,089.34 |
| INCREASE | 8,640 | $103,156,299.11 |
| LIQUIDATE | 517 | $6,613,632.04 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 10,284 | $132,712,951.07 | $124.62 / $126.30 / $128.15 |
| BTC (Wormhole WBTC) | 2,862 | $51,036,226.24 | $88,713.00 / $89,357.80 / $90,476.33 |
| ETH (Wormhole WETH) | 1,513 | $22,280,843.18 | $2,980.00 / $3,009.27 / $3,041.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 9,178 | $125,357,866.33 |
| SHORT | 5,481 | $80,672,154.16 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 7,910 |
| InstantDecreasePositionEvent | 3,507 |
| DecreasePositionEvent | 1,995 |
| IncreasePositionEvent | 730 |
| LiquidateFullPositionEvent | 517 |

Also decoded: **522** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 14,659 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 8,640 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 517 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 5,502 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 6,004 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): AddLiquidityEvent ×10,869, ClosePositionRequestEvent ×6,964, PoolSwapEvent ×6,182, InstantCreateTpslEvent ×4,566, CreatePositionRequestEvent ×1,235, InstantCreateLimitOrderEvent ×1,122, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×123, RepayToCustodyEvent ×90, BorrowFromCustodyEvent ×85, WithdrawCollateralEvent ×69, DepositCollateralEvent ×50, RemoveLiquidityEvent ×25

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-28 00:00:18 UTC | InstantIncreasePositionEvent | SOL | SHORT | $230.09 | $127.09 | - | [2Kt7mYGJ2n…](https://solscan.io/tx/2Kt7mYGJ2nqAKPAN3Sa1vHHv14vTz1hSbDcPGTUcjGuBnRSKdqL7nCQhqV2vKa18WruftgX3baAZiGXozJk3qCQ3) |
| 2026-01-28 00:00:37 UTC | InstantDecreasePositionEvent | ETH (Wormhole WETH) | LONG | $755.88 | $3,024.12 | $2.65 | [5KnBmSA6hv…](https://solscan.io/tx/5KnBmSA6hvppBv5uRfNAZS7QNgEeLKQewQTgiguZiNuZ6UbesmNewD2cYA8pj8q26mm5GbHTnonNoUcawgpjQ88a) |
| 2026-01-28 00:01:49 UTC | DecreasePositionEvent | ETH (Wormhole WETH) | LONG | $9,875.74 | $3,018.00 | $-40.62 | [4hGuKZZSMy…](https://solscan.io/tx/4hGuKZZSMyssRtYSPZ8iCK2GnRkEH6kqcgkNhse58vvtjqE9CnEbTd81ghQUN2tCN8Lk1U1zwkaUfFF53C3WtSpL) |
| 2026-01-28 00:03:40 UTC | IncreasePositionEvent | SOL | LONG | $3,683.77 | $126.87 | - | [4e5TAgPAyr…](https://solscan.io/tx/4e5TAgPAyrLHDraSwoQ8xN4auj4XkWWBBGhPaRQHJR87C3NpMinrRpcVnHBtfcTuz9PyFQ3dnqj2SUp2M2jCvyy7) |
| 2026-01-28 00:04:03 UTC | LiquidateFullPositionEvent | SOL | LONG | $4,447.31 | $126.82 | $-23.17 | [dbxHPYTNQ4…](https://solscan.io/tx/dbxHPYTNQ4thQVWaXpB8QK9RkgTFt1pgwfWtcvmogXn2wKRhfQokPXA6P6MbFYfJZAPXFMAL4KrVZJA7Mg94c8i) |

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
