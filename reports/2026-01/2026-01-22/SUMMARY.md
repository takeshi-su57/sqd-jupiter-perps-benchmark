# Jupiter Perps × SQD — one-day benchmark: 2026-01-22

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 395,074,219 → 395,290,656 (216,438 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-22 00:00:00 UTC / 2026-01-22 23:59:59 UTC |
| Slot just before range | 395,074,218 @ 2026-01-21 23:59:59 UTC |
| Slot just after range | 395,290,657 @ 2026-01-23 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 395,290,656) |
| Blocks with Jupiter activity returned | 32,937 |
| HTTP batches | 459 |
| Raw data (decoded JSON) | 36.1499 MiB |
| Transferred on the wire (gzip) | 18.47 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 78.8 min |
| SQD overload retries | http529×352 |

## Trades (valid, executed size change)

**15,215 trades**, 2,807 distinct traders, total notional **$209,230,291.82**, fees $170,477.82, net realized PnL on closes $-122,078.18.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 5,174 | $91,498,238.07 |
| INCREASE | 9,466 | $106,620,396.69 |
| LIQUIDATE | 575 | $11,111,657.07 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 10,993 | $136,429,913.98 | $126.63 / $128.71 / $130.81 |
| BTC (Wormhole WBTC) | 2,233 | $49,071,020.90 | $88,432.64 / $89,474.00 / $90,264.16 |
| ETH (Wormhole WETH) | 1,989 | $23,729,356.94 | $2,904.90 / $2,962.27 / $3,033.31 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 10,430 | $136,398,568.41 |
| SHORT | 4,785 | $72,831,723.41 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 8,828 |
| InstantDecreasePositionEvent | 3,451 |
| DecreasePositionEvent | 1,723 |
| IncreasePositionEvent | 638 |
| LiquidateFullPositionEvent | 575 |

Also decoded: **695** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 15,215 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 9,466 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 575 ✅ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 5,174 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 5,743 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Non-trade Jupiter events decoded (not converted to trades): AddLiquidityEvent ×7,789, PoolSwapEvent ×6,995, ClosePositionRequestEvent ×6,741, InstantCreateTpslEvent ×4,997, InstantCreateLimitOrderEvent ×1,220, CreatePositionRequestEvent ×1,045, WithdrawFeesEvent ×480, BorrowFromCustodyEvent ×136, DepositCollateralEvent ×136, RemoveLiquidityEvent ×119, IncreasePositionPreSwapEvent ×117, RepayToCustodyEvent ×54, WithdrawCollateralEvent ×24

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-22 00:00:02 UTC | InstantDecreasePositionEvent | SOL | LONG | $1,400.14 | $129.42 | $2.18 | [24nvYnkTLD…](https://solscan.io/tx/24nvYnkTLDf6uTPCq9ce73seTwHiMkLDgSid6DvBqGwMJRJSKQGt6GLPuP2nWyuZ3Nd6Cz1Ej5iz7yCpey5eP2AP) |
| 2026-01-22 00:00:04 UTC | InstantIncreasePositionEvent | ETH (Wormhole WETH) | LONG | $1,771.54 | $2,979.17 | - | [5EootGtcEr…](https://solscan.io/tx/5EootGtcErrDqhefhwxvE35fJE2PgmzV2tfUapZ52q8cCa1s2cPuK7WzXw7grCdWrTdqjduw51FtuoUjh7Ydmhwo) |
| 2026-01-22 00:00:04 UTC | LiquidateFullPositionEvent | SOL | SHORT | $992.21 | $129.48 | $-1.65 | [2YcK81PpjN…](https://solscan.io/tx/2YcK81PpjNL8RupodmtG85DWXrW87Q6aTpYyXdVkfvakTwvV7WHmfhcZPeDpqEGfTa9WbAAFcK8eksr18Wn4TivX) |
| 2026-01-22 00:00:04 UTC | DecreasePositionEvent | SOL | SHORT | $1,741.45 | $129.45 | $14.80 | [41Db2WC1X8…](https://solscan.io/tx/41Db2WC1X8LsxcvQYKQwoZhdRf2eRyqcs3DkY3NASpqDEZsh4bVSctVqcYWw1fddTd7NEQj5gQwnT5TKjTo9UKj5) |
| 2026-01-22 00:01:01 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $17,397.81 | $89,431.44 | - | [Z647tzTqXP…](https://solscan.io/tx/Z647tzTqXPX9U7U9XGNdJp4BJUSeEEUeBh4AcVs2pLH6sR55BKWtmkiXnKbchQmmJtYXGjWJiGoru7ZgxzVZDpN) |

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
