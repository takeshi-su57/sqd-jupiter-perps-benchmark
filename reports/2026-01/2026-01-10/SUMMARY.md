# Jupiter Perps × SQD — one-day benchmark: 2026-01-10

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 392,452,782 → 392,671,258 (218,477 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-10 00:00:00 UTC / 2026-01-10 23:59:59 UTC |
| Slot just before range | 392,452,781 @ 2026-01-09 23:59:59 UTC |
| Slot just after range | 392,671,259 @ 2026-01-11 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 392,671,258) |
| Blocks with Jupiter activity returned | 17,519 |
| HTTP batches | 317 |
| Raw data (decoded JSON) | 15.874 MiB |
| Transferred on the wire (gzip) | 8.68 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 107.2 min |
| SQD overload retries | http529×412 |

## Trades (valid, executed size change)

**7,177 trades**, 1,753 distinct traders, total notional **$75,564,271.90**, fees $83,859.56, net realized PnL on closes $-183,112.95.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 2,491 | $35,490,422.62 |
| INCREASE | 4,570 | $38,941,767.79 |
| LIQUIDATE | 116 | $1,132,081.50 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 5,709 | $61,158,234.65 | $135.21 / $135.98 / $136.86 |
| BTC (Wormhole WBTC) | 827 | $9,340,190.67 | $90,281.51 / $90,502.64 / $90,703.12 |
| ETH (Wormhole WETH) | 641 | $5,065,846.59 | $3,075.00 / $3,087.70 / $3,098.99 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 5,171 | $56,808,537.16 |
| SHORT | 2,006 | $18,755,734.74 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 4,310 |
| InstantDecreasePositionEvent | 1,734 |
| DecreasePositionEvent | 757 |
| IncreasePositionEvent | 260 |
| LiquidateFullPositionEvent | 116 |

Also decoded: **472** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 7,177 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 4,570 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 116 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 2,491 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 2,597 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×3,312, ClosePositionRequestEvent ×3,286, InstantCreateTpslEvent ×2,473, InstantCreateLimitOrderEvent ×684, CreatePositionRequestEvent ×531, WithdrawFeesEvent ×480, AddLiquidityEvent ×162, BorrowFromCustodyEvent ×43, IncreasePositionPreSwapEvent ×36, RepayToCustodyEvent ×34, DepositCollateralEvent ×30, WithdrawCollateralEvent ×14, RemoveLiquidityEvent ×10

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-10 00:00:06 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $975.23 | $90,516.53 | - | [5EmhV8YcNg…](https://solscan.io/tx/5EmhV8YcNg7op1gQszFwAgYVscHyHnY6VXfkhQFdL3tbBhWLrtF8omBk7GJAZR3prUwZf8sCFhCRr1kqCZnPvu7H) |
| 2026-01-10 00:00:16 UTC | InstantDecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $2,008.44 | $90,506.56 | $6.47 | [3XocwCemMi…](https://solscan.io/tx/3XocwCemMixPUd2jC46xdjbN6mRgDPaVj817LcoBuyp8Y2CP6RoXBJaRCgzFSziCBWRBADAsULT6HYXEbmJbLEZw) |
| 2026-01-10 00:01:22 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $21,637.55 | $90,513.70 | $57.18 | [2L7JTinmAt…](https://solscan.io/tx/2L7JTinmAtdSefmmpkEeGdpJLawNyP6nvpiGkGVHCNYzr2dauLhwqhUtJAAGjB3Z2WHCFFdMfLGqNTwnFY1rEBMz) |
| 2026-01-10 00:04:22 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $575.50 | $90,531.41 | - | [mjfTeXsYV7…](https://solscan.io/tx/mjfTeXsYV7ZN1nGq1Zb3rgFhHQiozrdzJETuqz9rhu4qAD1JNGyx475LQWdmDkgGEnBoAN28BxHbrcrR9UVWG8m) |
| 2026-01-10 00:15:07 UTC | LiquidateFullPositionEvent | SOL | LONG | $5,500.77 | $135.54 | $-22.43 | [2rGkVEmTmx…](https://solscan.io/tx/2rGkVEmTmxNgko7zYPxDkUL64x1v3mgZWJzMneoTbwa5wFUhpeMuyYmHumXvSNMbKayi8S1DRGeUiYE3Qoas9ErK) |

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
