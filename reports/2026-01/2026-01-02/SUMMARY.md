# Jupiter Perps × SQD — one-day benchmark: 2026-01-02

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 390,710,428 → 390,930,115 (219,688 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-02 00:00:00 UTC / 2026-01-02 23:59:59 UTC |
| Slot just before range | 390,710,427 @ 2026-01-01 23:59:59 UTC |
| Slot just after range | 390,930,116 @ 2026-01-03 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 390,930,115) |
| Blocks with Jupiter activity returned | 38,454 |
| Resumed | yes, from slot 390,821,143 (15,076 stored blocks re-verified) |
| HTTP batches | 325 |
| Raw data (decoded JSON) | 53.4806 MiB |
| Transferred on the wire (gzip) | 27.52 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 139.1 min total (67.7 + 71.4 min sessions) |
| SQD overload retries | http529×259 |

## Trades (valid, executed size change)

**27,032 trades**, 4,032 distinct traders, total notional **$337,767,573.82**, fees $301,637.31, net realized PnL on closes $439,829.12.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 10,105 | $152,634,840.43 |
| INCREASE | 15,893 | $170,483,295.79 |
| LIQUIDATE | 1,034 | $14,649,437.61 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 20,242 | $249,215,489.99 | $125.70 / $129.26 / $133.14 |
| BTC (Wormhole WBTC) | 4,115 | $58,673,491.50 | $88,273.75 / $89,597.68 / $90,904.57 |
| ETH (Wormhole WETH) | 2,675 | $29,878,592.33 | $2,990.00 / $3,085.10 / $3,147.54 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 13,675 | $145,712,294.67 |
| SHORT | 13,357 | $192,055,279.15 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 14,435 |
| InstantDecreasePositionEvent | 6,360 |
| DecreasePositionEvent | 3,745 |
| IncreasePositionEvent | 1,458 |
| LiquidateFullPositionEvent | 1,034 |

Also decoded: **1,221** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 27,032 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 15,893 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,020 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 14 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 10,105 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 11,133 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [2zRHzyzhXb…](https://solscan.io/tx/2zRHzyzhXbnPo3rTuWQxz5XLUzeWSG6iMxjhZ8iL5peDPKaYSZzXNGJz4MjbA2udRDND4A6DtT6yuViqdiRUG6Jj), [k1vL9jpXNW…](https://solscan.io/tx/k1vL9jpXNWUWKLiDSJPMLShsvWv4QchqQcwVapDdL2JxxVBnHQ8Jr8PLrvhpwzMRGphVPY5mNgVNqKJroGgonfQ), [3jauT8evrf…](https://solscan.io/tx/3jauT8evrfdePsb7d3Czhy56VfatHJTds9ajrFF6zGC7vuAFZTVUZmqij3XwuD8CB2YjQSfmPea4pbCULecrb4W8), [48eyoxFZmh…](https://solscan.io/tx/48eyoxFZmh7NJXosurYF6MnAHgRLJvpmnGWtCrSn4TvktVb3q9iX2JSKzDpr38SvA1o6AkTaZMXRTBmQ3dJByErT), [53VFjbNq2D…](https://solscan.io/tx/53VFjbNq2DKWrpm2EBxu2j7tuZ6Ri2xu5vUVSYymxyo7XroB5GFv7xuwCcXXwvt1ozt9qCEgrhrWGVTmEn9XTBNj), [3zi8Uf5RK8…](https://solscan.io/tx/3zi8Uf5RK8E8ArqhWvvW2g44gcbsNFU6s7fWDHfv4ELSPva4s6qwVGUZZnxbjefgNwRP88qbHtB8mQm8rutbqx2L), [23MG1gN1SK…](https://solscan.io/tx/23MG1gN1SK4uYwBwyFGP43AEceYPafDMxJiYKP6ummLVgxk37zL9pfVf5NvrBRuETahoVMJsDV3fQ8fcRsq2DHZP), [39kTN9wwva…](https://solscan.io/tx/39kTN9wwvahDuhz4Ngk4ggRwTi7ykdhEGgy65HJ1MzjFHA2gAuYAyXRcF4h9cwmontpFyCDcomFJPWNZj6xd885o), [3CaCB2C3Wk…](https://solscan.io/tx/3CaCB2C3WkiNHFURQzzn6jNmGLyDNms5nLmv8fuCjejb6DQaeFzjsJHfS51uopYRQ53LZCMEJKRqyqwxF8iyJ5qN), [4ahXGGaH5V…](https://solscan.io/tx/4ahXGGaH5VixF3BrGBKaWPY2bX7Ym4b7rLUhYnsdPTxdKsEyYVenA8Vvavf3D1239XVwasHBJWUWbmM46PeAHuRX), [3onJebKv8q…](https://solscan.io/tx/3onJebKv8qjh6DunUP5nHiNqDK8zXGsAc545yM4V2JJY7oXK1rE5UDbyviCFGw4Djomp1pKPFEmz3xSGim9mazRd), [2N2dLyJy4F…](https://solscan.io/tx/2N2dLyJy4FeTWmDEvk57Rbjept7VZv6jsK8jLMhaQFhNXwYAc585XSDKbAD7iDSKcNjwmm3ze6fR7hSR13s8hYQD), [2pFB5GWC7h…](https://solscan.io/tx/2pFB5GWC7h4XRNtTCna4a8CuQCcyRUDnTJWUN1JMPnZsT9Q6kB9275MMysSsMqSrXzD54PnnFKxVUkQR5eoY1YfT), [3TVRik8o1q…](https://solscan.io/tx/3TVRik8o1qpDw835HCRvQ1Mi18sLJWQRbX3dbBXgY19haX9ZgG833ZgZaGybyrdtBbwULAw1SvyvnY432iUPhorr)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×12,384, PoolSwapEvent ×11,589, InstantCreateTpslEvent ×8,156, InstantCreateLimitOrderEvent ×2,113, CreatePositionRequestEvent ×2,000, RemoveLiquidityEvent ×915, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×241, AddLiquidityEvent ×192, BorrowFromCustodyEvent ×118, DepositCollateralEvent ×108, RepayToCustodyEvent ×74, WithdrawCollateralEvent ×67

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-02 00:00:03 UTC | InstantIncreasePositionEvent | SOL | SHORT | $610.74 | $126.77 | - | [4S8nBFev1x…](https://solscan.io/tx/4S8nBFev1xzjZno1bXUfczzHo3CqqGoQAsfzdzo3xRpVrhSFtTZWYdBky7MCUbWMA62wkTHC95s7A5YLrp48X8Sb) |
| 2026-01-02 00:00:04 UTC | IncreasePositionEvent | SOL | SHORT | $1,133.99 | $126.80 | - | [CXKZoP2KRz…](https://solscan.io/tx/CXKZoP2KRz7t1W86DZ5SreuwKr5KUpC5GCChfFqTVhmeT1JQc9kByt4798qEMY9ihxn6WagibwAhGFqYJSNGVPD) |
| 2026-01-02 00:00:28 UTC | InstantDecreasePositionEvent | ETH (Wormhole WETH) | LONG | $15,705.24 | $2,998.93 | $103.60 | [2hLhGdKpSC…](https://solscan.io/tx/2hLhGdKpSCbGq2BQcQr56seJCD4xr1nBSp6bA1ZFHoeLtx1qVbXESE9G7Q4769u4c59e6rM352z73dKKAMCAb7qC) |
| 2026-01-02 00:00:52 UTC | DecreasePositionEvent | SOL | LONG | $4,867.85 | $126.86 | $66.32 | [3sS8ofz2VS…](https://solscan.io/tx/3sS8ofz2VSFEnu64nuv3tU6BzJLm58QTFCkM96qRbR2C8TpEjT2hxUEDBcqVG2jWPKHCzL5ZR6HnhUf5ZDtDVfxv) |
| 2026-01-02 00:01:16 UTC | LiquidateFullPositionEvent | SOL | SHORT | $18,236.48 | $126.92 | $-26.53 | [3xPTpNx18J…](https://solscan.io/tx/3xPTpNx18JVPFW8UHmEh5WQweB1YxdgdZ6FUNE7FkG2ktQKNPACxD4grWbPn17fHsZDW2WZZUeAfepei3Fer1H5n) |

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
