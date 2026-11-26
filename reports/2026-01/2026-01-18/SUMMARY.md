# Jupiter Perps × SQD — one-day benchmark: 2026-01-18

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 394,204,206 → 394,422,383 (218,178 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-18 00:00:00 UTC / 2026-01-18 23:59:59 UTC |
| Slot just before range | 394,204,205 @ 2026-01-17 23:59:59 UTC |
| Slot just after range | 394,422,384 @ 2026-01-19 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 394,422,383) |
| Blocks with Jupiter activity returned | 26,308 |
| HTTP batches | 422 |
| Raw data (decoded JSON) | 30.9081 MiB |
| Transferred on the wire (gzip) | 16.24 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 92.5 min |
| SQD overload retries | http529×395 |

## Trades (valid, executed size change)

**15,809 trades**, 3,244 distinct traders, total notional **$202,938,008.84**, fees $193,957.76, net realized PnL on closes $-132,238.98.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 4,754 | $79,800,261.06 |
| INCREASE | 10,065 | $106,428,246.18 |
| LIQUIDATE | 990 | $16,709,501.61 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 11,280 | $140,110,849.99 | $137.71 / $142.10 / $143.92 |
| BTC (Wormhole WBTC) | 2,916 | $39,776,767.81 | $93,574.45 / $95,090.63 / $95,482.88 |
| ETH (Wormhole WETH) | 1,613 | $23,050,391.05 | $3,278.01 / $3,324.90 / $3,367.50 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 11,456 | $147,596,221.45 |
| SHORT | 4,353 | $55,341,787.39 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 8,506 |
| InstantDecreasePositionEvent | 2,940 |
| DecreasePositionEvent | 1,814 |
| IncreasePositionEvent | 1,559 |
| LiquidateFullPositionEvent | 990 |

Also decoded: **678** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 15,809 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 10,065 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 982 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 8 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 4,754 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 5,701 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [WTqk6WqUAS…](https://solscan.io/tx/WTqk6WqUASwuk8Pmv4vG8qf7yXuNVegP4tEEsJqwonTSiJv69ZP5XPG9JDMdp3nQeAn3GujGua8W3x2DcKtg5FA), [4H8r7gzUZy…](https://solscan.io/tx/4H8r7gzUZyC2HcvQ3VeYX7jR1E9AjvXtQujsQh69ixmXPfUjr1FQSRExmhTmequxjs9X1tRR9zA9VgaRG8W2cRWt), [5HPhjyLSrk…](https://solscan.io/tx/5HPhjyLSrkbsHUcEc4CzrjkzYLC5g5oT9WBG1A3DNcREUhxKWM5ah88K4it2CfymvFFPu4APgqCvHpE5Sh27CPpR), [5avCzjCTyy…](https://solscan.io/tx/5avCzjCTyyz5y8Urdviefzf2rmHDGjAAu3gk73tSZh5UXveQPAKS4JprAUm5CaLipRDyv8Sz48yseWjLMRnLU2ZV), [3o4K4b5LPH…](https://solscan.io/tx/3o4K4b5LPHFDBkiH1qn3etPSJ2zUH1QrQsm8zBUme499Jkt54S2Bn7gP9Nwy7F4gAfqbQUP3CiKjUCjnFXPV4BPp), [4w1WpBYh4m…](https://solscan.io/tx/4w1WpBYh4mtD4Rk6BwzA3V5js2qKFRJaKb1QggddPG73kqnyRdSapL4XagWxz2rvUCGsKcGqux7R8my3TiDMa2p), [N3kgqATb3t…](https://solscan.io/tx/N3kgqATb3tboRrvFci6WSqJyt6HfT9qXy3BBFyrSPysqcnmvmL7kkRLhdX9CRBZNHYpQzsWhgxP7bGSFM54PkDh), [55oHfkkRct…](https://solscan.io/tx/55oHfkkRctVEfzF777qnVaSMxHzbKqhw9WQwfDocYScnLrds16SS26z1wFBwatUMHxrbD8UT1yiZuihozjMNBs8B)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×6,995, ClosePositionRequestEvent ×6,954, InstantCreateTpslEvent ×3,317, CreatePositionRequestEvent ×1,496, InstantCreateLimitOrderEvent ×1,120, AddLiquidityEvent ×1,107, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×211, BorrowFromCustodyEvent ×171, DepositCollateralEvent ×152, IncreasePositionPreSwapEvent ×94, RedeemStakeEvent ×86, RepayToCustodyEvent ×38, WithdrawCollateralEvent ×25

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-18 00:00:15 UTC | InstantIncreasePositionEvent | SOL | LONG | $18.39 | $143.63 | - | [axrinRRmfy…](https://solscan.io/tx/axrinRRmfyzSoA2jYn6DkVwGrCyDw7fJ7tzZnkV663VFAcC1BbRsHnRRigT3SHbQdSGR83qPnSqcdufmEiDng9S) |
| 2026-01-18 00:00:27 UTC | InstantDecreasePositionEvent | ETH (Wormhole WETH) | LONG | $18,468.95 | $3,307.77 | $46.51 | [3zrPdciEH7…](https://solscan.io/tx/3zrPdciEH7EPG6eXGNyBX4p5TVEKTyL5stMpfxTzvXCBGK1BmKaW8G2ZPvgrizsTzwaRSFgfYVdVDq6zkasm7sL5) |
| 2026-01-18 00:00:42 UTC | IncreasePositionEvent | ETH (Wormhole WETH) | LONG | $482.00 | $3,307.56 | - | [ZFMUr1TFSH…](https://solscan.io/tx/ZFMUr1TFSHH6wTfkp8jrPXTxqckwtqgQvz99wkqFN2J1tCmPTFNnJ5SKsz5Ep4Fth1LbPnY5tswDPfUdHiKwACK) |
| 2026-01-18 00:00:57 UTC | DecreasePositionEvent | BTC (Wormhole WBTC) | LONG | $1,452.70 | $95,090.00 | $5.34 | [2QboBtkE11…](https://solscan.io/tx/2QboBtkE111JXuibqLScihm1iSy4P3KhfBnDN2guGYY3sBAybZza1ZFKc4RSF2ypPC7PHQhCu8GaH5KsiHy478nt) |
| 2026-01-18 00:40:58 UTC | LiquidateFullPositionEvent | SOL | LONG | $4,574.18 | $143.52 | $-6.65 | [d9qwML54oc…](https://solscan.io/tx/d9qwML54ocuxcBcFyCXdCUKjix14Fa3EC1rC8aTzNjc9o2EavGivxWCfWcQFVSTxqrdUh8W5nfPPpqUNwZFvYso) |

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
