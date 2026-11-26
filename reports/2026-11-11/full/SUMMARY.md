# Jupiter Perps × SQD — one-day benchmark: 2026-11-11

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 467,914,168 → 468,316,356 (402,189 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-11-11 00:00:00 UTC / 2026-11-11 23:59:59 UTC |
| Slot just before range | 467,914,167 @ 2026-11-10 23:59:59 UTC |
| Slot just after range | 468,316,357 @ 2026-11-12 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 468,316,356) |
| Blocks with Jupiter activity returned | 52,394 |
| Resumed | yes, from slot 468,214,255 (35,829 stored blocks re-verified) |
| HTTP batches | 578 |
| Raw data downloaded | 121.7163 MiB |
| Wall time (streaming) | 128.4 min total (78.5 + 49.8 min sessions) |
| SQD overload retries | http529×222 |

## Trades (valid, executed size change)

**10,660 trades**, 1,797 distinct traders, total notional **$198,341,738.42**, fees $181,093.25, net realized PnL on closes $136,179.07.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 3,838 | $91,881,207.79 |
| INCREASE | 6,452 | $101,412,242.44 |
| LIQUIDATE | 370 | $5,048,288.19 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 7,126 | $146,608,001.86 | $82.12 / $83.77 / $85.74 |
| BTC (Wormhole WBTC) | 2,689 | $35,142,614.74 | $73,127.70 / $73,975.28 / $74,700.00 |
| ETH (Wormhole WETH) | 845 | $16,591,121.82 | $2,035.00 / $2,060.27 / $2,100.45 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 6,279 | $90,845,042.24 |
| SHORT | 4,381 | $107,496,696.18 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 5,582 |
| InstantDecreasePositionEvent | 2,844 |
| DecreasePositionEvent | 994 |
| IncreasePositionEvent | 870 |
| LiquidateFullPositionEvent | 370 |

Also decoded: **1,436** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 10,660 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 6,452 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 369 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 1 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 3,838 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 4,198 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 53,102. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [3e6BSTycDH…](https://solscan.io/tx/3e6BSTycDH1sPjDBEMmpttxPkL9PHGxw5qyoHpz5MrGjDgr3M9Wtbvcfrmg12SUw56Pp1sA1873dugJxRPZ3ximP)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×5,209, ClosePositionRequestEvent ×4,700, InstantCreateTpslEvent ×2,758, CreatePositionRequestEvent ×1,333, AddLiquidityEvent ×978, InstantCreateLimitOrderEvent ×676, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×260, DepositCollateralEvent ×187, BorrowFromCustodyEvent ×63, RepayToCustodyEvent ×53, WithdrawCollateralEvent ×31, IncreasePositionPreSwapEvent ×4, RedeemStakeEvent ×1

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-11-11 00:00:08 UTC | InstantDecreasePositionEvent | SOL | LONG | $157,605.96 | $83.25 | $563.73 | [5c2aCpSK9g…](https://solscan.io/tx/5c2aCpSK9gHbpLpUvpe9PHe7qDirPTKCbcMkQRUxLSLKSisbeGAnjghemFawkZGPztkfgv7qLvNuufw5RNZZHMRG) |
| 2026-11-11 00:00:28 UTC | InstantIncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $0.32 | $73,689.62 | - | [Yupq2xFkvb…](https://solscan.io/tx/Yupq2xFkvbT4zs3BvbY8toUv29Yconu7559kyabjePb7C5t1yyCG5kKUQZP7szgqW4sUHh287r32iMTEpuMEi6N) |
| 2026-11-11 00:00:30 UTC | DecreasePositionEvent | SOL | SHORT | $299.30 | $83.24 | $-1.74 | [4PqhwUT9U5…](https://solscan.io/tx/4PqhwUT9U5Zn2jvUgo5h8T2JWwQYem5reJxRT3vMzWxUGjNn2p8oYJCu5XgiMwoTUxjwyvmkmUFCMEb6kfKDByf4) |
| 2026-11-11 00:01:53 UTC | IncreasePositionEvent | BTC (Wormhole WBTC) | LONG | $0.32 | $73,669.18 | - | [3YFVbtwCAL…](https://solscan.io/tx/3YFVbtwCALoVyXx8MFywGpwEmrmkpHAmJ7Bij8oWiD9Mk8r1TCSDH53MD75JaNSAmYFsq5kKD95ZZeSkcRPDPkoa) |
| 2026-11-11 00:37:04 UTC | LiquidateFullPositionEvent | SOL | SHORT | $10,010.00 | $83.46 | $-24.08 | [22PdkbsZjp…](https://solscan.io/tx/22PdkbsZjpgU1s36jSEiHrWYLr8aXueJEY8eegRK2xgTFDGKwhWedLGkxBmxZWrVFwCHJn46qsH7bfdwBd4CAQHs) |

## Units and assumptions

- USD fields (`sizeUsdDelta`, `price`, `feeUsd`, `pnlDelta`) are integers with 6 decimals; raw integers are kept in `candidates.ndjson`. The scale is confirmed by price levels above and fee-to-size ratios, not by an external source.
- `positionSide`: 1 = LONG, 2 = SHORT. Realized PnL = `pnlDelta` × (`hasProfit` ? +1 : −1).
- IDL: community IDL `https://raw.githubusercontent.com/monakki/jup-perps-client/main/generator/idl/jupiter-perpetuals.json`, sha256 `f2d7ff5009e7696939cb2e888368967744131e6aa51dc5ea7c966cc9f29ed16c`.
- Source: SQD Portal only. No Solana RPC, Dune, Trawl, or Helius. No database writes.

## Files

- `trades.csv` — readable table of every valid executed trade (open in a spreadsheet)
- `candidates.ndjson` — all decoded candidates with raw integers and every event field
- `raw.ndjson` — untouched SQD response lines (re-decodable offline: `python3 summarize.py <dir>`)
- `report.json`, `replay.json`, `query.json`, `idl_used.json`
