# Jupiter Perps × SQD — one-day benchmark: 2026-01-14

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 393,329,103 → 393,549,072 (219,970 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-14 00:00:00 UTC / 2026-01-14 23:59:59 UTC |
| Slot just before range | 393,329,102 @ 2026-01-13 23:59:59 UTC |
| Slot just after range | 393,549,073 @ 2026-01-15 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 393,549,072) |
| Blocks with Jupiter activity returned | 41,946 |
| HTTP batches | 414 |
| Raw data (decoded JSON) | 54.6705 MiB |
| Transferred on the wire (gzip) | 28.49 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 176.1 min |
| SQD overload retries | http529×651 |

## Trades (valid, executed size change)

**27,051 trades**, 4,233 distinct traders, total notional **$390,537,727.33**, fees $361,828.14, net realized PnL on closes $310,645.88.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 9,810 | $174,904,509.60 |
| INCREASE | 16,478 | $200,196,805.96 |
| LIQUIDATE | 763 | $15,436,411.77 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 19,574 | $255,149,434.44 | $143.32 / $146.11 / $148.39 |
| BTC (Wormhole WBTC) | 4,851 | $70,143,933.49 | $94,529.35 / $96,753.17 / $97,925.25 |
| ETH (Wormhole WETH) | 2,626 | $65,244,359.41 | $3,279.20 / $3,339.65 / $3,400.00 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 15,887 | $219,670,845.13 |
| SHORT | 11,164 | $170,866,882.20 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 15,069 |
| InstantDecreasePositionEvent | 6,177 |
| DecreasePositionEvent | 3,633 |
| IncreasePositionEvent | 1,409 |
| LiquidateFullPositionEvent | 763 |

Also decoded: **1,106** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 27,051 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 16,478 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 759 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 4 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 9,810 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 10,558 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [562XDDX6gD…](https://solscan.io/tx/562XDDX6gDFTJnq282gaWopPN6PyvRLEtfa6UGzAAASxJZiSVQ3tm7sncHVe46NAZ6SYVKNrdN22vKvkLpgTAx3u), [4dN2Vzk8rb…](https://solscan.io/tx/4dN2Vzk8rbq9omHKLUg5kfhuWtWHyGv6aQQwaSfXYbko22S6bB7onH8U5op6a8iSq7qEZbF4Q54q79FWbnR93JCJ), [5UMZMnxWb9…](https://solscan.io/tx/5UMZMnxWb9GPQQwRsdDiuMG2LtToneetjTbHpHq1s4F9843U5f2LSWCpxG6zZjttUzhP6Hm9UtgWxDAPg6Wbak94), [5eD5VmFHgE…](https://solscan.io/tx/5eD5VmFHgE1V9uvpfxDmRFcs5123Hex8wM6RGCn26D4mVDQmvgEJe69UtQTrxUiDzbDxAzpxcjgw77hFphTrn4yE)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×13,036, PoolSwapEvent ×10,806, InstantCreateTpslEvent ×8,907, CreatePositionRequestEvent ×2,319, InstantCreateLimitOrderEvent ×2,243, AddLiquidityEvent ×548, WithdrawFeesEvent ×480, IncreasePositionPreSwapEvent ×255, RemoveLiquidityEvent ×216, BorrowFromCustodyEvent ×150, RepayToCustodyEvent ×97, DepositCollateralEvent ×96, WithdrawCollateralEvent ×42

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-14 00:00:02 UTC | InstantDecreasePositionEvent | SOL | LONG | $1,093.16 | $145.45 | $-7.82 | [5Fv3QuGEQG…](https://solscan.io/tx/5Fv3QuGEQGjCPDQxn3PfM6hwwZHqyGPyNNLVVE1xJFoA8LdwMSn1F9tCohaeoQ7DpRnoSqq3mKyhPTUz2r2EAcCC) |
| 2026-01-14 00:00:09 UTC | InstantIncreasePositionEvent | SOL | LONG | $6,318.62 | $145.48 | - | [4Aa1cSZHBk…](https://solscan.io/tx/4Aa1cSZHBk1bAUCMRugDxBtTVzWqRLH99VA9cNu4bDoySCyY5MpTSrVDeVCn9jKeKwi7wcKt6KFbX5qXt7uVXzPW) |
| 2026-01-14 00:00:11 UTC | DecreasePositionEvent | SOL | SHORT | $39,427.77 | $145.50 | $-101.01 | [4FsZ7323SY…](https://solscan.io/tx/4FsZ7323SYqv2BBUXZtJCNCsCTxP1t4zt2y6htvVEv8m7y2yqsXPtkq6QqN9ZvBk7EDkP6AxLziT4Qq7Gsi4ZJNB) |
| 2026-01-14 00:00:11 UTC | IncreasePositionEvent | SOL | SHORT | $566.26 | $145.50 | - | [446rztnfAd…](https://solscan.io/tx/446rztnfAdKiLSZ37Zgm7crDJjaYpjjiAUDkE79X8PobDUNsKLaztMUgynfP9BfpRjcAL8EYanrcdJMrf1u5W9WC) |
| 2026-01-14 00:01:31 UTC | LiquidateFullPositionEvent | SOL | SHORT | $1,342.88 | $145.71 | $-9.89 | [35mbEPyWct…](https://solscan.io/tx/35mbEPyWctxu6Uq57Gxz5wPLzQ2utR7h9GfM4LfjV6UXqJbcYPuEJW1J5FARyqqJWgUgUz8sDj7qukdQrA5pyxwe) |

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
