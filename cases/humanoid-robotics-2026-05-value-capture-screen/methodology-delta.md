# Methodology Delta: Humanoid Robotics Value-Capture Screen

- case: humanoid robotics / physical AI
- review_date: 2026-05-30
- linked_methodology: `long-term-integrated-thesis`
- result: positive_partial

## What Worked

The workflow correctly blocked premature single-equity actionability.

The critical distinction was not whether humanoid robotics is an interesting theme. It was whether public-company value capture is direct, material and measurable.

## Patch Confirmed

`theme_to_company_handoff` should include a hard `public_company_value_capture` gate.

If public-company expressions are mostly:

- private companies
- pre-revenue options
- enabling layers without revenue separation
- adjacent automation businesses

then the default decision should be:

`industry_map_first`

## New Patch

Add `theme_value_capture_screen` as a lightweight pre-case workflow:

- value-chain node
- public expression
- theme purity
- value-capture evidence
- evidence maturity
- valuation risk
- workflow decision

This should be used before a full single-company memo when a theme has high market heat but weak public-equity purity.

## What Failed / Remains Weak

- The screen does not prove which robotics stock is best.
- Tesla Optimus evidence still needs a stable archived PDF and transcript support.
- ABB / component supplier evidence is underdeveloped.
- The screen lacks valuation maps because no single stock should be selected yet.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: a public company discloses material humanoid revenue, backlog, production volume, customer deployment or unit economics.
