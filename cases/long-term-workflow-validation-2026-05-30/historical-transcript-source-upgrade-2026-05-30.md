# Historical Transcript Source Upgrade

- upgrade_date: 2026-05-30
- scope: TDOC 2020-2022 and PTON 2020-2022 historical failure backtests
- status: improved_not_final_public_grade
- stale_after: 2026-06-30
- must_refresh_if: official transcript archives, licensed transcript exports or contemporaneous consensus estimates are obtained

## Purpose

The historical failure backtests need transcript support because downgrade timing should rely on what a disciplined analyst could have heard or read at the time, not only later 10-K hindsight.

This pass adds public transcript paths for the key post-peak downgrade windows while preserving the remaining consensus gap.

## TDOC Transcript Support

Added to `../tdoc-2020-2022-failure-backtest/evidence-log.csv`:

- Q4 2021 public transcript path: `tdoc_q4_2021_call_transcript`
- Q2 2022 public transcript path: `tdoc_q2_2022_call_transcript`

Methodology impact:

- The Q4 2021 transcript supports the idea that the thesis had shifted from 2020 demand shock growth toward a more complex revenue-per-member, visit-growth and product-mix thesis.
- The Q2 2022 transcript supports the post-break evidence trail around guidance pressure and execution risk.
- These transcript sources improve downgrade-timing support, but they do not replace contemporaneous consensus expectations.

## PTON Transcript Support

Added to `../pton-2020-2022-failure-backtest/evidence-log.csv`:

- Q2 FY2022 company IR-hosted Refinitiv transcript path: `pton_q2_fy2022_call_transcript`

Methodology impact:

- The transcript supports the downgrade trigger around hardware-demand normalization, guidance reset, adjusted EBITDA loss and connected-fitness gross-margin pressure.
- It strengthens the claim that the workflow would have forced `watch_only_pending_normalized_hardware_demand` before the full FY2022 postmortem.
- It does not replace contemporaneous FY2022/FY2023 consensus estimates.

## Remaining Blocker

The historical cases still should not be used as fully public-grade external examples while consensus expectations remain missing or undocumented as unavailable-data exceptions.

The current public-release impact is:

- transcript archive rows: improved
- consensus rows: still blocking external-example use
- G04/G06: still hard blockers for methodology release

