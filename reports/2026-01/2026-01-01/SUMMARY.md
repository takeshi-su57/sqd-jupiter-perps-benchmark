# Jupiter Perps × SQD — one-day benchmark: 2026-01-01

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 390,490,507 → 390,710,427 (219,921 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-01 00:00:00 UTC / 2026-01-01 23:59:59 UTC |
| Slot just before range | 390,490,506 @ 2025-12-31 23:59:59 UTC |
| Slot just after range | 390,710,428 @ 2026-01-02 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 390,710,427) |
| Blocks with Jupiter activity returned | 19,688 |
| HTTP batches | 267 |
| Raw data (decoded JSON) | 21.1874 MiB |
| Transferred on the wire (gzip) | 11.22 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 60.3 min |
| SQD overload retries | http529×271 |

## Trades (valid, executed size change)

**9,989 trades**, 1,995 distinct traders, total notional **$111,095,881.58**, fees $93,536.00, net realized PnL on closes $95,409.18.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 3,758 | $48,276,620.90 |
| INCREASE | 6,054 | $59,367,884.82 |
| LIQUIDATE | 177 | $3,451,375.85 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 7,759 | $88,373,785.51 | $123.94 / $125.11 / $127.07 |
| BTC (Wormhole WBTC) | 1,434 | $15,123,874.48 | $87,400.00 / $88,006.02 / $88,797.02 |
| ETH (Wormhole WETH) | 796 | $7,598,221.60 | $2,967.99 / $2,983.72 / $3,005.52 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 6,366 | $65,533,101.49 |
| SHORT | 3,623 | $45,562,780.09 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 5,546 |
| InstantDecreasePositionEvent | 2,436 |
| DecreasePositionEvent | 1,322 |
| IncreasePositionEvent | 508 |
| LiquidateFullPositionEvent | 177 |

Also decoded: **440** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 9,989 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 6,054 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 177 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 3,758 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 3,921 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×4,950, PoolSwapEvent ×4,388, InstantCreateTpslEvent ×3,408, InstantCreateLimitOrderEvent ×875, CreatePositionRequestEvent ×814, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×122, IncreasePositionPreSwapEvent ×69, AddLiquidityEvent ×59, RedeemStakeEvent ×46, BorrowFromCustodyEvent ×35, RepayToCustodyEvent ×35, DepositCollateralEvent ×32, WithdrawCollateralEvent ×23

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-01 00:00:02 UTC | InstantIncreasePositionEvent | SOL | LONG | $370.26 | $124.45 | - | [5seHByCGVd…](https://solscan.io/tx/5seHByCGVdW5yXKdTg67S7UENRCUkMs499yXiRVjzgwL4hW6HdktUFY6TZgGxCt7sPBcKKYUFt9U5R1mC7zrJeoP) |
| 2026-01-01 00:00:25 UTC | IncreasePositionEvent | SOL | LONG | $10,143.06 | $124.41 | - | [5hZTvvSYi9…](https://solscan.io/tx/5hZTvvSYi9z3U2dbkADNUcpHL8SXGhgczAYXw9kEvfvMBiVfPqJ55jcrwRdzGij9jc6h45ZrN11KZX1tVD6MQ7my) |
| 2026-01-01 00:00:25 UTC | LiquidateFullPositionEvent | SOL | LONG | $62,161.10 | $124.40 | $-90.16 | [5W7pLM7dKz…](https://solscan.io/tx/5W7pLM7dKzkBvfWe7uybKzKkAizTFTe8Yp9YdQ3e1i9AgXpQarV92CBa8bW8eR7DyBtKufRsAhmnNyEqXjRWTXVN) |
| 2026-01-01 00:01:27 UTC | InstantDecreasePositionEvent | ETH (Wormhole WETH) | LONG | $3,332.72 | $2,967.99 | $-5.75 | [96PPbr4w2v…](https://solscan.io/tx/96PPbr4w2v2btvGeNEezNrK4K78n1NtyvGqL6dCRbF489npk5ax2HnE3CEtNHRp7yQyW7L6UJACt5SuBQ1jemaw) |
| 2026-01-01 00:01:41 UTC | DecreasePositionEvent | ETH (Wormhole WETH) | SHORT | $4,967.11 | $2,968.40 | $5.98 | [VJcTFBGn48…](https://solscan.io/tx/VJcTFBGn48irwMYrY7mreSAxC6BMSbAm4eMDhU9tg6is4EiZRxdpfA4QPW3a7uW9krkrfQjXxBNXeG62H6xuJ7M) |

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
