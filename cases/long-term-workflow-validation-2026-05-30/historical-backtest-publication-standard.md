# Historical Backtest Publication Standard

- standard_date: 2026-05-30
- scope: TDOC 2020-2022 and PTON 2020-2022 failure backtests
- status: internal_candidate_standard
- stale_after: 2026-06-30
- must_refresh_if: exact peak-date EV, consensus expectations, official transcripts or filing backups are obtained

## Purpose

Historical failure backtests are useful because they test whether the workflow would have downgraded a real failed thesis before the visible collapse.

They are also easy to overstate. A postmortem can look more certain than it was at the time if the source trail does not prove what was knowable then.

This standard defines when a historical backtest can be used as an external example.

## Public-Grade Requirements

Each historical failure case needs:

1. peak price source with date and stable URL;
2. peak-date or defensible quarter-end share count;
3. cash and debt source sufficient to reconstruct enterprise value;
4. contemporaneous consensus expectations or an unavailable-data exception;
5. archived earnings-call transcript or official Q&A support for the downgrade trigger;
6. SEC filing backup for the core operating metrics;
7. false-precision warning when exact historical data is unavailable;
8. explicit statement of what the workflow could have known at the time.

## Current Decision

TDOC and PTON remain valid internal methodology evidence.

They should not be used as fully public-grade external examples until the archive audit no longer has `blocks_external_example` rows.

See:

- `historical-backtest-source-archive-audit.csv`
- `historical-source-cleanup-2026-05-30.md`
- `../tdoc-2020-2022-failure-backtest/`
- `../pton-2020-2022-failure-backtest/`

## Reviewer Instruction

An external reviewer should challenge:

- whether the downgrade trigger uses only information available before the collapse;
- whether valuation reconstruction has false precision;
- whether transcript support or consensus gaps change the claimed downgrade timing;
- whether the case is being used as internal evidence or external proof.

## Release Rule

If any row in `historical-backtest-source-archive-audit.csv` has:

- `current_status = incomplete`
- or `release_decision_impact = blocks_external_example`

then the historical case can support internal method development but cannot be presented as a public-grade external example.
