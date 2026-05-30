# External Release Go/No-Go Memo

- decision_date: YYYY-MM-DD
- methodology: `long-term-integrated-thesis`
- release_status: draft
- release_owner: replace
- decision: `go` | `no_go`

## Decision

State whether the workflow can be shared externally with institutional colleagues as final methodology.

Allowed values:

- `go`
- `no_go`

## Required Evidence

| gate | required evidence | status | evidence path |
| --- | --- | --- | --- |
| G04 true follow-through | completed qualifying later-event refresh | pending | replace |
| G06 external reviewer | completed scorecard, results memo and intake checklist | pending | replace |
| live case reproducibility | reviewer reproduces or caveats assigned live/fresh case action label | pending | replace |
| G01 method-source decision | reviewer accepts or caveats public method-source basis | pending | replace |
| theme selection freshness | reviewer accepts or caveats recent-theme freshness and refresh controls | pending | replace |
| practice falsification | reviewer accepts or caveats case-grounded methodology claims | pending | replace |
| methodology iteration traceability | reviewer accepts or caveats case-failure-to-patch traceability | pending | replace |
| ordinary-vs-workflow delta | reviewer accepts or caveats actionability delta versus ordinary memo | pending | replace |
| template completeness | reviewer accepts or caveats workflow template usability and completeness | pending | replace |
| G05 source challenge | reviewer accepts or caveats MarketScreener FY2 FCF source | pending | replace |
| public example source quality | reviewer accepts or caveats source quality for public examples | pending | replace |
| historical consensus exception | reviewer accepts or caveats TDOC/PTON unavailable-data exception | pending | replace |
| operational loop handoff | release owner confirms long-term-thesis loop is final external version | pending | replace |
| institutional colleague acceptance | completed checklist and dated acceptance memo pass return validator | pending | replace |
| release validator | `validate_long_term_release.py --require-external-ready` exits 0 | pending | replace |

## Remaining Caveats To Preserve

List caveats that should remain in the public methodology package even if release is approved:

- historical backtest consensus-exception caveats, unless fixed with evidence or reviewer acceptance;
- source-definition caveats for public market-data providers;
- no actionability claim without case-specific evidence;
- no use as model-portfolio policy without separate PM approval.

## Files Updated For Release

- `public-release-decision.md`
- `public-release-gate-tracker.csv`
- `public-readiness-audit.md`
- `public-workflow-pack/README.md`
- `release-qa-report-YYYY-MM-DD.md`
- `institutional-colleague-acceptance-YYYY-MM-DD.md`
- `memory/methodologies/review-log.csv`

## Validator Output

```text
paste final validator output here
```

## Final Signoff

- release_owner:
- date:
- decision:
- caveats:

## Refresh Conditions

- stale_after: YYYY-MM-DD
- must_refresh_if: any source caveat is later contradicted, reviewer changes recommendation, G04 follow-through evidence is revised, or users report reproducibility failures.
