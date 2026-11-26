# Jupiter Perps × SQD — one-day benchmark: 2026-01-20

**Benchmark status:** `PASS_STRUCTURAL_ONLY`  
**Offline replay + consistency verification:** PASSED

> `PASS_STRUCTURAL_ONLY` = the full day streamed from SQD and every Jupiter trade event decoded and linked with zero structural failures. It is **not** an independent reconciliation of PnL against Jupiter's own API.

## Coverage

| | |
|---|---|
| Slots | 394,639,909 → 394,856,965 (217,057 slots) |
| Date resolution | sqd-timestamp-api |
| First / last block time in data | 2026-01-20 00:00:00 UTC / 2026-01-20 23:59:59 UTC |
| Slot just before range | 394,639,908 @ 2026-01-19 23:59:59 UTC |
| Slot just after range | 394,856,966 @ 2026-01-21 00:00:00 UTC |
| Day boundaries verified | yes |
| Stream complete | True (last slot 394,856,965) |
| Blocks with Jupiter activity returned | 37,565 |
| HTTP batches | 455 |
| Raw data (decoded JSON) | 49.7209 MiB |
| Transferred on the wire (gzip) | 25.88 MiB |
| SQD query mode | lean |
| Wall time (streaming) | 64.1 min |
| SQD overload retries | http529×313 |

## Trades (valid, executed size change)

**26,115 trades**, 4,957 distinct traders, total notional **$437,885,247.23**, fees $473,484.71, net realized PnL on closes $-2,648,765.88.

| Action | Count | Notional |
|---|---:|---:|
| DECREASE | 7,699 | $150,549,257.15 |
| INCREASE | 16,039 | $213,468,304.22 |
| LIQUIDATE | 2,377 | $73,867,685.86 |

| Market | Count | Notional | Min / median / max price |
|---|---:|---:|---|
| SOL | 17,283 | $254,950,232.12 | $124.54 / $128.27 / $134.51 |
| BTC (Wormhole WBTC) | 5,692 | $102,209,717.50 | $87,783.03 / $90,433.64 / $92,800.00 |
| ETH (Wormhole WETH) | 3,140 | $80,725,297.60 | $2,929.04 / $3,030.80 / $3,196.17 |

| Side | Count | Notional |
|---|---:|---:|
| LONG | 18,196 | $331,291,648.65 |
| SHORT | 7,919 | $106,593,598.58 |

| Event type | Count |
|---|---:|
| InstantIncreasePositionEvent | 14,150 |
| InstantDecreasePositionEvent | 4,909 |
| DecreasePositionEvent | 2,790 |
| LiquidateFullPositionEvent | 2,377 |
| IncreasePositionEvent | 1,889 |

Also decoded: **1,391** valid zero-size position events (collateral-only changes, not counted as trades) and **0** invalid candidates.

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
| arithmetic: fee_eq_position_fee_plus_funding_ok | 26,115 ✅ |
| arithmetic: increase_position_size_ge_fill_ok | 16,039 ✅ |
| arithmetic: liquidation_pnl_matches_formula_ok | 2,073 ✅ |
| arithmetic: liquidation_pnl_protocol_adjusted_info | 304 ℹ️ |
| arithmetic: pnl_matches_entry_exit_formula_1pct_ok | 7,699 ✅ |
| arithmetic: pnl_sign_matches_side_and_price_ok | 10,069 ✅ |

Duplicate log/CPI representations merged: 0. Uncommitted CPI instructions skipped: 0. Failed-tx events skipped: 0.

Liquidations where the protocol recorded a PnL different from the entry/exit formula (collateral already consumed by fees; real on-chain values, kept as-is): [2xZVUSTMLi…](https://solscan.io/tx/2xZVUSTMLiP6EM6oSnrZ7roKMiWWDBmrzAYHdcZZ9rZzhfESTfMdrVQX2MPwdcWQX9cnuwVgnZay3maoi5Qt5i1), [72zo1bmYFt…](https://solscan.io/tx/72zo1bmYFtkvDYwmDm9oH36x3MNagS2gezyTXwE8kUH8k9CbHuHypChgbtA91rDhy3Jz1WMbhe3JACt7vmpRBdG), [4RtxM1FpYT…](https://solscan.io/tx/4RtxM1FpYTS1dS5zJhRboitM9k12rdGE1MzQWZPY9m7z9tPvfH75QzSXkdeVw4sEEtJmmULpvoWDupZkvyaXQJ9w), [4TmCbYthyt…](https://solscan.io/tx/4TmCbYthytGKWAd6bsVi5GDHKKQ7PZSAMXZmkf7hQy5sFRzymSVUzNyF4YFgcz1FuBhyC3e6wVUTYB4SSdREA9q), [2vD8vwqu2y…](https://solscan.io/tx/2vD8vwqu2yJETEcuNmGMMPAWXbBsAoTzWfgztHcvhMQBymfVBmZgRMGcNGx8sN94BQiHsM1Na1qwQTFN7VuQToW2), [JBzpYhVYBn…](https://solscan.io/tx/JBzpYhVYBn7udD11s5XjSXqrXQvg9EeNWigc2MvydrGfDG4aZPbNLjSxFPpnoDHjauqom4fMWzFU3Hve6UgySWh), [5BgM1W7FrC…](https://solscan.io/tx/5BgM1W7FrCSA1ciwMUtj5bj9oAqtF5jEnMu5McDCqXQX6xddv7pjg9EE35TourssB3azyY4oDGqAac6ESBEPcoVy), [LzMBSrcJDe…](https://solscan.io/tx/LzMBSrcJDe4QDeyyNoz1MipfFeQxj6RJQskbFsin79nm1dAkDMbbegXHAYKzZdMDHjsZqjEKA2Ei6nqFKUzxdBt), [27rpQt6JU9…](https://solscan.io/tx/27rpQt6JU9hYFxZ3KqLTV4JcNV8C72FwRXyxR5Q9gWX4PudpMXydRvM6LrAc9M3gni3jRZCqx2M18kvhHcQmh4a9), [4HQ9aVZaYH…](https://solscan.io/tx/4HQ9aVZaYHTHXqVdbt7fxCRTJkm21tDPGY2xqHwhZ24YiakZMCwYE2qp5GQwQfDs6S17qoqJ1qThkZFVw3Hk14Bj), [3eKgz66xda…](https://solscan.io/tx/3eKgz66xdaZFyJaGgFmoDWE6PA8pMesYxe1365TzHyv3omB5S5mmkKFZrhntgEwkY86baB2GyaQiXS53YHaVHALL), [4XkmySqtjN…](https://solscan.io/tx/4XkmySqtjNCbkLEkvCJXTnsXKGh7VwmiyCZ5UUbDrafFgL8DQ6AH6LbyVgm8UwyRCCTXRZwS7U5Yt1f7uSyW1XyC), [56f1ccHuJ5…](https://solscan.io/tx/56f1ccHuJ5BWt4v7nsTsaEBcogLAZGQajKQd5Fk7zjRWongeFD8N3RyYDgPUAmRPymG3LkSFMH23UTedi1h3NRSH), [asg9q9FnJP…](https://solscan.io/tx/asg9q9FnJPMJS71EFfxvdfAXt2mCD8Tkmpum2RoDyiexJCM9aYoAr9GbJCrqESEhf7uiLgzrpJv23A4LD2WpGap), [2kQdDeMtM5…](https://solscan.io/tx/2kQdDeMtM5Fssfrng5fokcFJVJ4jUHScY7Czep8Sfmn2F2w2QAAcvozi7Zhz2qDtzNDh7mb68vHk66vXWPrPzasa), [4NsMBdVoF7…](https://solscan.io/tx/4NsMBdVoF73XnhyvgWi9FoMiGPtVJVDihGPSJkUjdUmXgMmkWr5iHmc7Wf6tkCXSUfDhQH7tXVB3BdcqyRZ96Pxo), [4dyMgEnB2Q…](https://solscan.io/tx/4dyMgEnB2QoZhAU3kCJH2F39abBYWhwTyaNkdTXs5CL22PTAEw4HkXdbXhfJqbei9R85in91g4CpurTHxz19PP6X), [5rYfye2A9J…](https://solscan.io/tx/5rYfye2A9JVmEi8J94HZkapZbUCvQp238XCsphVbA11X5FBt1y4QJTVo5FSZcGsYL2jKPirG4ZFsyhu9ZeQKdw5f), [65jQg7wfnc…](https://solscan.io/tx/65jQg7wfncaAFnqgPpUfNnKceB3gXCQwAsHEcovcL7jnvaGYF7TEKJtXyLLiniGrTPVWP6sV2mF1Jc2sp2yKL8J), [4LeXohoykx…](https://solscan.io/tx/4LeXohoykxi2aqm5jA2PzKeRjBZwMRvdsAjxauLi6TZn54sKq9fwD2ZTyMMQ9LdSfn7Zi3f44sBjtSXdCYyG7Wg5)

Non-trade Jupiter events decoded (not converted to trades): PoolSwapEvent ×11,819, ClosePositionRequestEvent ×10,528, InstantCreateTpslEvent ×6,027, InstantCreateLimitOrderEvent ×2,179, CreatePositionRequestEvent ×1,601, AddLiquidityEvent ×622, RemoveLiquidityEvent ×589, WithdrawFeesEvent ×480, RepayToCustodyEvent ×167, IncreasePositionPreSwapEvent ×154, DepositCollateralEvent ×140, BorrowFromCustodyEvent ×128, WithdrawCollateralEvent ×98, RedeemStakeEvent ×43, LiquidateBorrowPositionEvent ×12

## Sample real trades (verify on Solscan)

| Time | Event | Market | Side | Size | Price | PnL | Tx |
|---|---|---|---|---:|---:|---:|---|
| 2026-01-20 00:00:10 UTC | InstantIncreasePositionEvent | SOL | LONG | $23,417.24 | $133.37 | - | [D7rA3uWWAR…](https://solscan.io/tx/D7rA3uWWARmPngmCE8uyN3CAu3tDeevzkre2LeJXaw9AUhw2JBGcvQ16H9gn8UerVp4EX9ispBiby785ZzoYKAe) |
| 2026-01-20 00:00:58 UTC | InstantDecreasePositionEvent | BTC (Wormhole WBTC) | SHORT | $371.74 | $92,535.18 | $2.63 | [SpdaB1X3i5…](https://solscan.io/tx/SpdaB1X3i5YJ5wyQRTX8cadgUmEqZDLmgz5tfStxYBxPzHLBTkexfTDfRzevg1bZAds4bVA3xihLBNqzCTEkXbJ) |
| 2026-01-20 00:01:21 UTC | DecreasePositionEvent | SOL | LONG | $445.58 | $133.36 | $-2.80 | [s16jKHVdai…](https://solscan.io/tx/s16jKHVdaif1yNABLrm3mqXhGWo8WrAGsXoiTmoG2PzXgDvmziXpfCU8ohAQoyQfQHAsYUcu5uiiHg8CiJiReYb) |
| 2026-01-20 00:04:40 UTC | LiquidateFullPositionEvent | SOL | SHORT | $2,747.82 | $133.56 | $-4.00 | [5eLNVBJgdC…](https://solscan.io/tx/5eLNVBJgdCEM6rNxWEj64DL7KBmhqLhSgaNVvgXs1d9KMKn7Sd6xyWJcgfMCk1XwHbYRr2omrdFLkUV1mVewoAAH) |
| 2026-01-20 00:05:02 UTC | IncreasePositionEvent | ETH (Wormhole WETH) | SHORT | $1,440.62 | $3,195.00 | - | [3hRVjJUiEq…](https://solscan.io/tx/3hRVjJUiEqzuehEpxUZE7NghBtsU6nb8XCSBr8xMTB51qrLgVpVrj9aASCwtZcpk1GSQKVZnSpi1mLKRSscDk55w) |

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
