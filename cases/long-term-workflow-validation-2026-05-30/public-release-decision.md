# Public Release Decision

- decision_date: 2026-05-30
- methodology: `long-term-integrated-thesis`
- release_status: not_ready_external_release
- internal_status: candidate_internal_release

## Decision

Do not release externally to institutional colleagues as final methodology yet.

The workflow is strong enough for internal candidate use and external reviewer assignment. It is not yet strong enough for final external sharing because two hard gates are still incomplete:

1. no true post-memo follow-through refresh has been completed;
2. no external independent reviewer has completed the blind review.

## What Is Ready

- Public workflow pack.
- Formal operating loop: `../../loops/long-term-thesis-loop.md`.
- Fill guide.
- Analyst checklist.
- Template inventory.
- Source appendix.
- External reviewer brief and scorecard.
- External review return template and intake checklist.
- External review return validation standard and script.
- CRM G05 source package.
- External reviewer bundle manifest.
- Follow-through refresh playbook and trigger tracker.
- Follow-through refresh validation standard and script.
- Institutional colleague release notes template, use-boundaries memo, adoption FAQ and release bundle manifest.
- Cross-case validation matrix, overlay coverage audit and cross-case validation summary.
- Historical backtest archive audit and publication standard.
- Ordinary-vs-workflow comparison.
- Multiple live and historical validation cases.
- Release QA validator: `../../scripts/validate_long_term_release.py`.
- Release QA runner: `../../scripts/run_long_term_release_checks.py`.
- Validator regression test: `../../scripts/test_long_term_release_validators.py`.

## What Is Not Ready

- True follow-through refresh evidence.
- Completed external reviewer scorecard, results memo and intake checklist.
- External reviewer scorecard challenging the CRM G05 source package, especially MarketScreener FY2 FCF methodology.
- External reviewer decision accepting or rejecting the TDOC/PTON historical consensus unavailable-data exception.
- Historical backtest transcript / consensus archive package.

## Release Gates

See:

- `public-release-gate-tracker.csv`
- `release-qa-report-2026-05-30.md`
- `final-release-cutover-checklist.csv`
- `institutional-colleague-acceptance-checklist.csv`
- `public-workflow-pack/institutional-colleague-acceptance-memo-template.md`
- `external-release-go-no-go-template.md`

Current blocking gates:

- `G04`: true follow-through refresh
- `G06`: external independent reviewer scorecard and results memo

## Allowed Use

Allowed:

- internal research trial
- analyst training with caveats
- external reviewer dry run
- case-by-case use when source gaps are explicit

Not allowed:

- final external publication
- method adoption label
- use as a model portfolio policy without reviewer sign-off
- actionability claims without completed G04/G06 gates

## Next Release Action

Assign the external reviewer packet.

In parallel, wait for the next material event in `follow-through-trigger-tracker.csv`; preferred first refresh is `CRM_2026`.

Run `../../scripts/run_long_term_release_checks.py` after any gate-status, public-pack or release-decision change.

Before changing `release_status` to `ready_external_release`, complete `final-release-cutover-checklist.csv`, complete `institutional-colleague-acceptance-checklist.csv`, validate a dated colleague acceptance memo with `../../scripts/validate_institutional_colleague_acceptance_return.py`, write a go/no-go memo from `external-release-go-no-go-template.md`, and run `../../scripts/validate_long_term_release.py --require-external-ready`.

Also complete the institutional colleague release notes from `public-workflow-pack/institutional-colleague-release-notes-template.md`, run `../../scripts/validate_institutional_colleague_acceptance.py`, and verify `institutional-release-bundle-manifest.csv` before distribution.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: external reviewer returns findings, CRM/ETN/VRT/LLY publish a material follow-through event, or a public-grade valuation data source becomes available.
