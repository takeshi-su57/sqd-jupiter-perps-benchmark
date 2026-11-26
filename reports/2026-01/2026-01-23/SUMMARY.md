# Jupiter Perps × SQD — one-day benchmark: 2026-01-23

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 395,290,657 → 395,507,025 (216,369 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-23 00:00:00 UTC / 2026-01-23 23:59:59 UTC |
| Slot just before range | 395,290,656 @ 2026-01-22 23:59:59 UTC |
| Slot just after range | 395,507,026 @ 2026-01-24 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 395,507,025) |
| Blocks with Jupiter activity returned | 34,662 |
| HTTP batches | 432 |
| Raw data (decoded JSON) | 41.1118 MiB |
| Transferred on the wire (gzip) | 20.94 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 65.6 min |
| SQD overload retries | http529×340 |

## Trades (valid, executed size change)

**18,229 trades**, 2,930 distinct traders, total notional **$231,683,757.51**, fees $206,580.49, net realized PnL on closes $-26,776.11.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,352 | $102,159,547.85 |
| INCREASE | 11,142 | $119,157,928.99 |
| LIQUIDATE | 735 | $10,366,280.68 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 13,072 | $161,323,145.18 | $125.15 / $127.65 / $130.03 |
| BTC (Wormhole WBTC) | 3,016 | $50,015,521.46 | $88,471.25 / $89,598.39 / $91,111.19 |
| ETH (Wormhole WETH) | 2,141 | $20,345,090.88 | $2,889.00 / $2,947.68 / $3,015.07 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 11,984 | $144,657,061.03 |
| SHORT | 6,245 | $87,026,696.49 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 10,180 |
| InstantDecreasePositionEvent | 4,084 |
| DecreasePositionEvent | 2,268 |
| IncreasePositionEvent | 962 |
| LiquidateFullPositionEvent | 735 |

Also decoded: **1,155** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 18,229 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 11,142 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 735 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,352 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 7,077 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×8,143, ClosePositionRequestEvent ×8,019, AddLiquidityEvent ×7,546, InstantCreateTpslEvent ×5,108, CreatePositionRequestEvent ×1,514, InstantCreateLimitOrderEvent ×1,264, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×153, RemoveLiquidityEvent ×137, DepositCollateralEvent ×120, BorrowFromCustodyEvent ×100, RedeemStakeEvent ×86, RepayToCustodyEvent ×67, WithdrawCollateralEvent ×65

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-23 00:00:05 UTC | InstantDecreasePositionEvent | SOL | LONG | $10.00 | $128.36 | $0.06 | [3yCyEQMSEj…](https://solscan.io/tx/3yCyEQMSEjHBBsqCzJTMxXfFSFMNeSwZrpKPx7rRcrZyWaCowbHjxhZ3mMa4tfE4HfPDFCnqyahpYMgH5GmKum2S) |
| 2026-01-23 00:00:22 UTC | DecreasePositionEvent | SOL | SHORT | $757.36 | $128.27 | $-0.62 | [4tbaSRnYAQ…](https://solscan.io/tx/4tbaSRnYAQwQBWchzoBgEaZUqvxhnBrUSW4pc8Y5craRB6H13qffY9vH2z8ht9sd4qdib8UvzRFqhpcdPxopL6gW) |
| 2026-01-23 00:00:28 UTC | InstantIncreasePositionEvent | SOL | SHORT | $313.58 | $128.27 | - | [3brS2XLTQy…](https://solscan.io/tx/3brS2XLTQySmELAbH5JAJyZmENhgaPsfdY5BZ6T7wVeBCBTe8VRtXnpvBD74jNFfScaH1a5qqxR67yXKy3MhDdjU) |
| 2026-01-23 00:06:02 UTC | IncreasePositionEvent | SOL | LONG | $738.98 | $128.18 | - | [2VqL6FzLTy…](https://solscan.io/tx/2VqL6FzLTyJW64NtZKCGuPXHhoXnzU19ieZD1vfcn4RKEhzCY1qEohfn5oxiSuguXfBxkqWX5ESxDd4mLLp5KfEB) |
| 2026-01-23 00:30:17 UTC | LiquidateFullPositionEvent | SOL | LONG | $13,227.80 | $128.07 | $-20.47 | [5Vjt4rrVuB…](https://solscan.io/tx/5Vjt4rrVuBUsejSHjeuBeko9sjMSbaR4BMSMkgQYYRhp5fxfhZ2CMhNDfo9YjGQL5uyJouC3fEK18pz4CJkB2PVs) |

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
