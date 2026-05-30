# Institutional Use Boundaries

- methodology: `long-term-integrated-thesis`
- status: candidate_internal_release
- external_release_status: not_ready_external_release
- objective_complete: false
- prepared_date: 2026-05-30
- stale_after: 2026-06-30
- must_refresh_if: G04 or G06 status changes, reviewer findings arrive, a live validation case has a material event, or source quality materially changes

## Boundary

This workflow can be used as an internal institutional research discipline. It should not be represented as final external-release methodology until G04 and G06 clear.

The method is designed for judgment under uncertainty, not for mechanical stock selection. It improves the odds that an analyst will expose weak assumptions, source gaps and valuation burden before making an actionability claim.

## Appropriate Use

Use the workflow when a long-term thesis depends on linked variables across:

- consumer or end-demand durability
- product reality and monetization
- macro and capital-cycle transmission
- industry structure and value migration
- company execution and capital allocation
- valuation expectations

Use it especially when a hot theme is being translated into a single public company, or when a strong product narrative needs to be bridged to revenue, margin, retention and valuation.

## Inappropriate Use

Do not use the workflow as:

- a same-day earnings reaction template
- a pure macro call
- a catalyst-only trade sheet
- a replacement for source work
- a way to force actionability on an attractive narrative
- a portfolio policy without reviewer sign-off

## Non-Negotiable Stop Rules

- No source trail means no durable conclusion.
- No expectation map means no actionability when valuation is material.
- Product usage without monetization bridge means watch-only.
- Clinical demand without payer/access and net-price evidence means watch-only.
- Shock-era demand without normalized demand evidence means watch-only.
- Hardware-linked subscription thesis without normalized hardware demand and hardware margin means watch-only.
- Acquired exposure without purchase price, integration and ROIC path means watch-only.
- Hot theme with unclear public-company value capture means `industry_map_first`.
- No ordinary-vs-workflow delta means methodology value is not proven.

## Required Evidence Standard

Facts, inferences and judgments must be separated.

Every durable conclusion needs:

- evidence-log row
- source date
- confidence level
- source-quality note
- explicit source gap if evidence is missing

Mira-derived calculations can support interpretation, but they cannot be the only evidence for a durable conclusion.

## Release Boundary

Current hard blockers:

- `G04`: true follow-through refresh is not complete.
- `G06`: external independent reviewer is not complete.

Until these are complete, permitted distribution is limited to:

- internal controlled use
- training with caveats
- external reviewer assignment
- case-by-case use with source gaps preserved

The workflow becomes eligible for institutional colleague release only when `public-release-decision.md` is updated to `release_status: ready_external_release` and `scripts/validate_long_term_release.py --require-external-ready` exits 0.

The workflow is not complete against the original project objective until `scripts/validate_objective_readiness.py` reports `objective_complete: true`. Current status is `objective_complete: false` because G04 follow-through evidence, G06 external review and final external release remain incomplete.
