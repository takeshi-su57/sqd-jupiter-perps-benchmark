# Jupiter Perps × SQD — one-day benchmark: 2026-01-27

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 396,153,765 → 396,368,724 (214,960 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-27 00:00:00 UTC / 2026-01-27 23:59:59 UTC |
| Slot just before range | 396,153,764 @ 2026-01-26 23:59:59 UTC |
| Slot just after range | 396,368,725 @ 2026-01-28 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 396,368,724) |
| Blocks with Jupiter activity returned | 35,074 |
| HTTP batches | 509 |
| Raw data (decoded JSON) | 38.6789 MiB |
| Transferred on the wire (gzip) | 20.19 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 204.6 min |
| SQD overload retries | http529×724 |

## Trades (valid, executed size change)

**17,138 trades**, 3,072 distinct traders, total notional **$229,847,513.06**, fees $202,163.99, net realized PnL on closes $205,218.46.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 6,811 | $102,021,139.42 |
| INCREASE | 9,793 | $116,751,039.62 |
| LIQUIDATE | 534 | $11,075,334.02 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 12,589 | $147,972,779.19 | $122.96 / $124.78 / $127.68 |
| BTC (Wormhole WBTC) | 2,770 | $63,958,958.76 | $87,189.78 / $88,351.56 / $89,419.30 |
| ETH (Wormhole WETH) | 1,779 | $17,915,775.11 | $2,897.00 / $2,957.26 / $3,030.81 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 9,514 | $127,752,271.17 |
| SHORT | 7,624 | $102,095,241.89 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 8,900 |
| InstantDecreasePositionEvent | 4,473 |
| DecreasePositionEvent | 2,338 |
| IncreasePositionEvent | 893 |
| LiquidateFullPositionEvent | 534 |

Also decoded: **721** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 17,138 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 9,793 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 534 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 6,811 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 7,321 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×8,481, PoolSwapEvent ×6,885, InstantCreateTpslEvent ×5,581, AddLiquidityEvent ×5,157, InstantCreateLimitOrderEvent ×1,496, CreatePositionRequestEvent ×1,456, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×231, IncreasePositionPreSwapEvent ×140, RepayToCustodyEvent ×99, RedeemStakeEvent ×86, WithdrawCollateralEvent ×82, BorrowFromCustodyEvent ×51, DepositCollateralEvent ×39

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-27 00:00:01 UTC | InstantIncreasePositionEvent | SOL | LONG | $879.66 | $124.10 | - | [23xUsspETp…](https://solscan.io/tx/23xUsspETp1VSi97m8ffUjTAjuRWDvzmrJ4bM2LNnADJTXKysXmCeyjduD7DwZgErAMvN9848yfcwaxMQNyuM56w) |
| 2026-01-27 00:00:25 UTC | LiquidateFullPositionEvent | ETH (Wormhole WETH) | LONG | $1,724.13 | $2,924.77 | $-9.24 | [4A1J8yewoW…](https://solscan.io/tx/4A1J8yewoWFkMLsY7sEhWcFUXAYssDAdijVpf86HFv6n5vDLeSejiyvFhagc4LHedZpeXcUoZs8KSnCykhmDcfZs) |
| 2026-01-27 00:00:26 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $996.87 | $88,200.00 | $-1.92 | [3ZkpqrW78x…](https://solscan.io/tx/3ZkpqrW78xm7manPrdSiNRsu43JBYD6tgW16y1CyH2Q8SL5i2exjm3HxtgsyEfh8idLyEkr2yQbJXnSAU4dpfNoC) |
| 2026-01-27 00:00:26 UTC | IncreasePositionEvent | SOL | LONG | $1,362.94 | $124.00 | - | [3bWJzDUaoU…](https://solscan.io/tx/3bWJzDUaoUQDg4V6SzS5KLendmVKnjAYqhYTtJYNUpi4pLsqmTLXChnLnDyu2GzZNYHhMcek2aEdG3L4M4bqCDjX) |
| 2026-01-27 00:00:28 UTC | InstantDecreasePositionEvent | SOL | LONG | $32,603.04 | $124.00 | $-44.91 | [3tELZBzoir…](https://solscan.io/tx/3tELZBzoirtTHy1kxnfNHnpcC8QKQBuRtfymw8KgF35azTbC2XTbkCZBiJidmEcJTMxeEAt6ZDaHcFugARzCNKBZ) |

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
