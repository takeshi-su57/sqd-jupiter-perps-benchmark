# Jupiter Perps × SQD — one-day benchmark: 2026-01-13

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 393,109,961 → 393,329,102 (219,142 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-13 00:00:00 UTC / 2026-01-13 23:59:59 UTC |
| Slot just before range | 393,109,960 @ 2026-01-12 23:59:59 UTC |
| Slot just after range | 393,329,103 @ 2026-01-14 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 393,329,102) |
| Blocks with Jupiter activity returned | 42,827 |
| HTTP batches | 402 |
| Raw data (decoded JSON) | 60.4391 MiB |
| Transferred on the wire (gzip) | 31.28 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 149.6 min |
| SQD overload retries | http529×548 |

## Trades (valid, executed size change)

**30,638 trades**, 4,523 distinct traders, total notional **$465,383,469.84**, fees $441,621.10, net realized PnL on closes $830,733.79.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 11,624 | $213,964,260.02 |
| INCREASE | 17,879 | $230,558,033.30 |
| LIQUIDATE | 1,135 | $20,861,176.51 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 23,104 | $309,430,872.04 | $137.67 / $143.18 / $148.52 |
| BTC (Wormhole WBTC) | 5,031 | $107,872,840.44 | $90,933.99 / $93,524.25 / $96,432.70 |
| ETH (Wormhole WETH) | 2,503 | $48,079,757.35 | $3,088.27 / $3,189.18 / $3,360.95 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 16,919 | $259,393,637.89 |
| SHORT | 13,719 | $205,989,831.94 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 16,170 |
| InstantDecreasePositionEvent | 7,388 |
| DecreasePositionEvent | 4,236 |
| IncreasePositionEvent | 1,709 |
| LiquidateFullPositionEvent | 1,135 |

Also decoded: **1,153** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 30,638 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 17,879 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 926 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 209 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 11,624 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 12,750 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [5jQWGXLmZu…](https://solscan.io/tx/5jQWGXLmZu8JEsx1R9RrFw5Pzj1VSn5xzqPXamr4zTUnhQDDsSimSW7EVMJacY9mffjQgUr7HMEBo9U7vmBpK1aA), [zJh7cVS6Ny…](https://solscan.io/tx/zJh7cVS6NyABBXAyTpFhdcDv8hgPgLf1qamevq1AxzwndUURdFk9amV6Yeg1PP3zyLDSqQafNnYGv6ia4SJQExr), [5hjAefUwPD…](https://solscan.io/tx/5hjAefUwPDGCfnNA4avp3NSzJ3nMQMKzNKMHzfFLKGSmHdNcVagzZ8E3zRoTWHPNmor9RKF7RSunCACMtd2V2sTJ), [N2qVFJWGyt…](https://solscan.io/tx/N2qVFJWGytK6CVjtLwtqxwraTNMsLqEK6A91FUn9qvrCwuYFRRWdUhgdoGZ1un1KFfhGCxF3YWdNrtxATfA34zH), [3BUf6guF1s…](https://solscan.io/tx/3BUf6guF1s11JcHFdR6pTyHyWfsXvunXz6AiFoEHSTdh8zevGUKp2xnXR2c2JX3FpEAMstNRXTBW3GGE3Enr1pcM), [3aWXuMKAuc…](https://solscan.io/tx/3aWXuMKAuckrBnaNXBHEeU65QNsZEKsBsUa4dLQxthqyVTwLTN9Tdq1A9tdNYRhrgFi6y787BEhKVGVhBA52BdMM), [5RLRnV6ip5…](https://solscan.io/tx/5RLRnV6ip5h4abJn3TGP388sMAYZGdZW395t7vQWr3fF6yVEBphszQnBjZEAA6pZteWVbrcNugFv2EtvewNKwkrk), [5zSqmM7PPa…](https://solscan.io/tx/5zSqmM7PPashLPwVbU5HovLY5rKVn7cdEnaccA7v74Sd1QKomgptM1GBJTeUQ39JTdYVeivowgrEe3rxgViA33tz), [5Ayp1rtFxz…](https://solscan.io/tx/5Ayp1rtFxztGZpkKcEs2s6XUZk636UhVqGxXSVmLe9Pmx11xXww6Y2a1ZEL8jiTCKQFm6kb1gN3AffBYmioiQR3L), [5W2kTQ2R3s…](https://solscan.io/tx/5W2kTQ2R3swT5PSVSU2yHngYcgoHxfpgqf4S76amti7nEEPpbR7jcs8CHb5dS9KVbVaF2Kqite6YUTW6rb5bHAou), [2KNHNvdMK5…](https://solscan.io/tx/2KNHNvdMK5FMyVsUG1mkZkv6n6mNXzWkVwuZUsPvzQZCHTqMdfdS5YBfVqPvMcfjLgcKXz6CDFkvSZTrVJGBYEP), [48tntxuHxT…](https://solscan.io/tx/48tntxuHxT8PfLF5vg6UpQ3kdC8Sgvdo2Pxuvob3JyHHwuLgZnxvcNNEkE7nwQSdhSdr7Ugv6uAgcyDdLhbMDfkS), [2S4vtC6Hjs…](https://solscan.io/tx/2S4vtC6Hjsa3Qx6nN6qqtLZBusaBs62tWKU9agT83bpGkEW886saF6AX9sPwDAkegDsT8WDu4RBuCqVRzhWPv5k), [4tPQEQZpBZ…](https://solscan.io/tx/4tPQEQZpBZBkuK5QiGUt6xVVarTJCA1xCxuqGig8eebtgHyvaXPYxdwEUfUd7tRDHx84ra1LfooLeDHSzuP7NKop), [wkNGeqs9ox…](https://solscan.io/tx/wkNGeqs9oxnLX6HfpwMxF3gxMqaC9M1jQ5ACoFMwPESLyTnYpPundEnt2mZEjfSJhT733Az2S3MvVg1y1Z9QUhL), [38U78gWjBV…](https://solscan.io/tx/38U78gWjBV2hUzgRbN6pkEpZVdXxudjABnUqAA5pJX6WEXvzwEmfKfHAQdjdGyaNbh5k9aKUAV2zS2D8SU9dabeq), [5yKW1xiCpW…](https://solscan.io/tx/5yKW1xiCpWht9x8dceuqBu4MJpAu5R1uou6VPymZGXhgutiR8jx8av3mws6RvMKifMTS3yNqmXid8pSv3Cxm7a3V), [3yNT4XPP3H…](https://solscan.io/tx/3yNT4XPP3HaV1gHrXKuzNRXaD4gGb5BnHBDnr2kFUJt9avsJCYN48KfijpsVpPyMcGQeg1Z3DmKBV58woyA2njBc), [5FjieJUvTU…](https://solscan.io/tx/5FjieJUvTU2Xb3dUW93eaMYj92Su2vzxpJ3P91eMLXQVFEyLPwSoHEjdJoYHFPYk47bPUhjEwoSzyzkoGZLVfqdJ), [3GHpx1M9Zi…](https://solscan.io/tx/3GHpx1M9ZijAYTo3MyAATkBXqUXpigXERnJiKgu8fXmXpWyUZt1THFAAvJWb8kXFqCrhrdxo6TNWes3VsqBndfqR)

Non-trade Jupiter events decoded (not converted to trades): ClosePositionRequestEvent ×14,634, PoolSwapEvent ×12,430, InstantCreateTpslEvent ×9,351, InstantCreateLimitOrderEvent ×2,589, CreatePositionRequestEvent ×2,494, WithdrawFeesEvent ×480, RemoveLiquidityEvent ×466, AddLiquidityEvent ×281, IncreasePositionPreSwapEvent ×266, BorrowFromCustodyEvent ×118, RepayToCustodyEvent ×89, WithdrawCollateralEvent ×67, DepositCollateralEvent ×65, RedeemStakeEvent ×46

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-13 00:00:04 UTC | DecreasePositionEvent | SOL | LONG | $13,738.95 | $139.00 | $27.00 | [4arFBMPvH6…](https://solscan.io/tx/4arFBMPvH6D7abK1Xsf3HwZwgV2C16V6wfVDoU943UUn5ekrVyddxGaZMepXnpDGmh27mM9pH744EPkRgbQZX2J1) |
| 2026-01-13 00:00:04 UTC | IncreasePositionEvent | SOL | LONG | $2,856.19 | $139.00 | - | [5UQzRXbHUK…](https://solscan.io/tx/5UQzRXbHUKGgWwW1aDrdHL6PW8oJnwmsFeeaCVQPa44nJhDGUNDwydakxaMgGbbsqJ95KCqqU7NV1yxvrjqvni9b) |
| 2026-01-13 00:00:06 UTC | InstantIncreasePositionEvent | SOL | SHORT | $21,752.17 | $138.98 | - | [5EeMMetLp1…](https://solscan.io/tx/5EeMMetLp1UHoPqy9NHXX2KqnDgSB9m7JMm9qB1jy6tU4HStgPsSJfxTUmJAqyBXRN97LP4ktboEfQeoyxsx6R7U) |
| 2026-01-13 00:00:53 UTC | InstantDecreasePositionEvent | SOL | SHORT | $9,867.60 | $138.99 | $316.32 | [2vqqbMMFKy…](https://solscan.io/tx/2vqqbMMFKy5c5UYyDi78q7d4CvRp6c5vjSFCuX4gQMUDzaPozvDM55eqiVVcLXDWvMtiXv4oPnqTgroUVwJEn8Ed) |
| 2026-01-13 00:01:43 UTC | LiquidateFullPositionEvent | BTC (Wormhole WBTC) | SHORT | $2,061.89 | $91,221.65 | $-3.04 | [4y59UYBw93…](https://solscan.io/tx/4y59UYBw93c8MGmiPiWDAoj82rLDoi2ceFwZ7P9iKwpSm4mZZxhTG5xVVeXKjsrcS8FXdsY23RfFxo5LYwX5J7so) |

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
