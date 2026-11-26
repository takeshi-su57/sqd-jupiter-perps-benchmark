# Jupiter Perps × SQD — one-day benchmark: 2026-01-05

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 391,365,655 → 391,583,702 (218,048 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-05 00:00:00 UTC / 2026-01-05 23:59:59 UTC |
| Slot just before range | 391,365,654 @ 2026-01-04 23:59:59 UTC |
| Slot just after range | 391,583,703 @ 2026-01-06 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 391,583,702) |
| Blocks with Jupiter activity returned | 43,084 |
| HTTP batches | 365 |
| Raw data (decoded JSON) | 60.7915 MiB |
| Transferred on the wire (gzip) | 31.32 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 120.2 min |
| SQD overload retries | http529×467 |

## Trades (valid, executed size change)

**31,005 trades**, 4,410 distinct traders, total notional **$511,146,986.87**, fees $580,369.03, net realized PnL on closes $544,402.55.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 12,633 | $235,265,546.08 |
| INCREASE | 17,296 | $262,550,887.41 |
| LIQUIDATE | 1,076 | $13,330,553.38 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 23,035 | $315,603,762.58 | $133.15 / $136.19 / $139.81 |
| BTC (Wormhole WBTC) | 5,321 | $159,105,323.32 | $91,479.31 / $93,285.58 / $94,781.00 |
| ETH (Wormhole WETH) | 2,649 | $36,437,900.97 | $3,134.00 / $3,186.79 / $3,262.27 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 18,292 | $256,954,626.26 |
| SHORT | 12,713 | $254,192,360.61 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 15,839 |
| InstantDecreasePositionEvent | 7,788 |
| DecreasePositionEvent | 4,845 |
| IncreasePositionEvent | 1,457 |
| LiquidateFullPositionEvent | 1,076 |

Also decoded: **1,496** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 31,005 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 17,296 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 1,071 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 5 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 12,633 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 13,703 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [5QGeYHSEeM…](https://solscan.io/tx/5QGeYHSEeMLo8wDWctWYeVyqLqdQixeiGm8TB7fBpA1E9zyy5s4kRn7zNZgycZhCroCNCFhSuNFDPZT1xJDtHUrm), [KtFU3sUneL…](https://solscan.io/tx/KtFU3sUneLEPZhNsXQaEJT825U2jFENUD6SzjrzMNCG3as5G4rEYtCKrmWbYspAjbaZ4HuuW7j1Fo8HizJBtLsJ), [G5svrY4jtv…](https://solscan.io/tx/G5svrY4jtvCLuTGpiyjkRsagNy9twiEYgS5u2kFTe9SG7dQr9pT2EjG5wud8Se8a5YhqCwFxEUEKsWg4ooxtZFs), [21gpArc3ye…](https://solscan.io/tx/21gpArc3yeHair5D2uXYpvF6SB15AN4nkwQ332jgBUBG8dpbZspb3jqKAVHPhcrNk6UEFNTAU74RA6Q9dhoGVqUK), [5zQisrzaWj…](https://solscan.io/tx/5zQisrzaWjPkRNs5mZsKdBsLCxursxzUNXN9uYYBaKHBTnyx7yGVTYztksZFUZ1bT4Cdb6a1gkFJnKx2KtbDgWPU)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×14,401, PoolSwapEvent ×12,662, InstantCreateTpslEvent ×8,908, CreatePositionRequestEvent ×2,988, InstantCreateLimitOrderEvent ×2,173, RemoveLiquidityEvent ×637, WithdrawFeesEvent ×480, AddLiquidityEvent ×299, IncreasePositionPreSwapEvent ×212, BorrowFromCustodyEvent ×125, RepayToCustodyEvent ×75, DepositCollateralEvent ×69, WithdrawCollateralEvent ×63, RedeemStakeEvent ×46

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-05 00:00:00 UTC | InstantDecreasePositionEvent | SOL | LONG | $8,245.87 | $134.04 | $83.81 | [GwwAcrZxmP…](https://solscan.io/tx/GwwAcrZxmP6ikK2jxNB2VyfzGwfaV9vhnqVdueBxJch5qLwsMdV7Fh4muMbD7GadVbJTN5GvPUKk39eQKJjeCGM) |
| 2026-01-05 00:00:00 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $9,647.73 | $91,494.00 | - | [5z5JDq5Nzy…](https://solscan.io/tx/5z5JDq5Nzyso2AuDehENkTmZmNShxHsqb8j5A3Bg3gakGVT9DaJKVVgNmuE1Yg83ER63u9Rosf6mekUpsvFQ1CXz) |
| 2026-01-05 00:01:03 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $5,365.95 | $91,600.00 | $-20.43 | [5PWtpuKvpe…](https://solscan.io/tx/5PWtpuKvpebYF2XqdJfJT3Qph5BZCfffTMP5ecAt985HBYQL3qJtrekmreDJ9TXzxeXUrHCzj9a5ecJVK4KFzZfY) |
| 2026-01-05 00:01:03 UTC | LiquidateFullPositionEvent | SOL | SHORT | $3,460.07 | $134.33 | $-9.59 | [2TY48aBqBo…](https://solscan.io/tx/2TY48aBqBox6yqMtCoTKvcZa3AEQJi1GdcarnRYviKacSkkfGHAHZ6LEY27Br57TE9Nsa6kjcCzPN5TY2DzmbU1A) |
| 2026-01-05 00:01:04 UTC | IncreasePositionEvent | SOL | SHORT | $1,203.51 | $134.30 | - | [3LzZZpBaCn…](https://solscan.io/tx/3LzZZpBaCnXnwej9zUjCB6PrH4u3teTZzSaHwJBsYw5TUCHuSf7u8LK3fxXRAjSATic7mHnLf5kmXmfbixWzPNS7) |

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
