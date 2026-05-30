# Historical Consensus Unavailable-Data Exception

- exception_date: 2026-05-30
- scope: TDOC 2020-2022 and PTON 2020-2022 historical failure backtests
- status: prepared_pending_reviewer_acceptance
- stale_after: 2026-06-30
- must_refresh_if: licensed FactSet/CapIQ/Visible Alpha export, broker estimate archive or public company-consensus archive becomes available

## Purpose

The historical failure backtests need contemporaneous consensus expectations to prove what valuation and growth expectations were priced before the thesis broke.

This pass tests whether public sources can recover that consensus cleanly.

Result: public sources provide useful point-in-time snippets, but not a complete, dated revenue / EBITDA / EPS consensus package for both TDOC and PTON. The correct release behavior is to document the source attempts and keep the external-example caveat until a reviewer accepts the exception or a licensed export is added.

## Source Attempts

See `historical-consensus-source-attempts.csv`.

TDOC:

- BusinessQuant provides a current historical estimates table, but the current crawl does not prove the estimates were visible with the same values at the 2021/2022 decision dates.
- Investing.com and Healthcare Dive provide point-in-time consensus / guidance context around the Q1 2022 and JPM 2022 windows.
- These sources help explain market expectations, but they do not reconstruct a complete contemporaneous revenue / EBITDA / EPS expectation map.

PTON:

- Benzinga provides useful point-in-time Q1 FY2022 EPS/revenue consensus snippets and Q2 revenue analyst-estimate comparison.
- Motley Fool and CNBC provide management guidance / outlook-reset context.
- These sources support the downgrade-timing story, but they do not reconstruct a complete FY2022/FY2023 consensus package.

## Exception Rule

The historical backtests may remain internal validation evidence if:

1. consensus fields are explicitly labeled partial or source_gap;
2. no modeled value is labeled consensus;
3. the memo says downgrade timing is supported by company filings, transcript/guidance evidence and observed revisions, not by a complete consensus table;
4. external reviewer accepts that the historical case is illustrative, not public-grade proof;
5. the case is refreshed if a licensed export or broker archive becomes available.

## Release Impact

This exception does not clear the historical public-example gate by itself.

It converts the remaining gap from vague missing data to a reviewer-decision item:

- accept caveated use as internal / reviewer-facing evidence; or
- require licensed consensus export before external institutional distribution.

## Decision

Current decision:

- `historical_consensus_exception_prepared`
- `external_public_grade_example: no`
- `requires_external_reviewer_acceptance: yes`

