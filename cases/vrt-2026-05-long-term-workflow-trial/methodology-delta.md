# Methodology Delta From VRT Trial

- case: VRT long-term workflow trial
- date: 2026-05-30
- status: iteration_delta
- linked_methodology: `cases/long-term-methodology-2026-05-30/methodology-card.md`
- contrast_case: `cases/etn-2026-05-long-term-workflow-trial/`

## What The Workflow Improved

The VRT trial proved a second useful discipline:

> Higher theme purity does not automatically mean better investment conclusion.

VRT has cleaner AI infrastructure exposure than ETN and stronger reported growth, but its valuation burden is much higher. The workflow correctly moved from "VRT is a purer AI power winner" to:

> VRT has higher purity and stronger current growth, but also higher market heat and a larger expectation burden. Keep watch-only pending full expectation map.

## New Defects Exposed

### P0: Need Purity-Vs-Expectation Burden Scoring

The ETN/VRT pair shows that `theme_to_company_handoff` should not stop at `investable_purity`.

Add a pair of fields:

- `theme_purity_score`: 1-5
- `expectation_burden_score`: 1-5

Interpretation:

- high purity + low burden: best research candidate
- high purity + high burden: watchlist / expectation-map priority
- low purity + low burden: possible ignored derivative beneficiary
- low purity + high burden: reject or avoid

### P1: Order/Backlog Disclosure Quality Must Be Scored

VRT discloses strong sales, organic growth and guidance, but the trial did not capture a robust order/backlog table comparable to ETN. The workflow needs to score whether order/backlog evidence is direct, partial or unavailable.

Add:

- `order_backlog_disclosure_quality`: `direct`, `partial`, `qualitative`, `source_gap`

### P1: Cash Flow Quality Needs Working-Capital Decomposition

VRT's Q1 adjusted FCF was very strong, but Q1 cash flow benefited from working-capital movement, including deferred revenue. The workflow should not treat strong FCF as automatically recurring.

Add:

- `fcf_quality`
- `working_capital_tailwind`
- `deferred_revenue_change`
- `capex_intensity`
- `repeatability_of_cash_conversion`

## Proposed Workflow Patch

For hot-theme single-equity research, add a `purity_vs_expectation_burden` block:

| field | description |
| --- | --- |
| `theme_purity_score` | how directly company economics map to the theme |
| `expectation_burden_score` | how much future success current price appears to require |
| `evidence_maturity_score` | how much evidence has moved from narrative to realized financials |
| `valuation_heat_score` | multiple premium and crowding proxy |
| `research_action_implication` | actionability consequence |

Default rule:

- If `theme_purity_score >= 4` and `expectation_burden_score >= 4`, do not issue an actionability conclusion without a complete expectation map.

## ETN vs VRT Method Takeaway

| case | purity | operating evidence | valuation heat | workflow action |
| --- | --- | --- | --- | --- |
| ETN | medium-high | strong | high | watch_only_pending_expectation_map |
| VRT | high | very strong | extreme | watch_only_pending_expectation_map |

The pair improves the workflow because it shows the method can handle two different reasons to avoid overconfidence:

- ETN: diversified exposure and acquisition/ROIC questions
- VRT: high purity but extreme expectation burden

## Validation Impact

This is a real step toward institutional usability because the same workflow produced differentiated conclusions for two names inside the same hot theme.

Still not public-grade:

- no FY2 consensus
- no peer/historical valuation range
- no transcript evidence
- no historical failure backtest
- no follow-through refresh

## Next Trial

Move to a different hot theme:

- `enterprise_ai_agents_and_software_monetization`

Recommended first candidate:

- `CRM` or `NOW`

Reason:

- This will stress the product evidence ladder rather than infrastructure/backlog quality.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: VRT Q2 2026 results change growth/margin assumptions; order/backlog evidence becomes available; valuation multiple changes materially; or ETN/VRT peer comparison contradicts the purity-vs-burden framing.
