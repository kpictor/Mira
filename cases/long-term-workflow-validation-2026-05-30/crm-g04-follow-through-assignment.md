# CRM G04 Follow-Through Assignment

- assignment_date: 2026-05-30
- case_id: `CRM_2026`
- status: waiting_for_later_event
- original_memo_cutoff: 2026-05-30
- original_action_label: `watch_only_pending_product_monetization_map`

## Trigger

Run after Salesforce publishes Q2 FY2027 earnings, a Q2 FY2027 10-Q, or another later product metric update that directly tests the product-to-company monetization bridge.

## Thesis Variables To Refresh

- Agentforce/Data 360 ARR
- Agentic Work Units
- bookings growth
- organic revenue acceleration
- margin guidance
- free cash flow guide or forecast
- ASR share count and debt/cash
- valuation multiple and FY2028 FCF forecast

## Original Stop Rule

CRM remains watch-only until product usage and ARR bridge to company-level organic growth, retention, pricing, margin conversion and durable free cash flow.

## Required Before / After Table

At minimum, compare:

| thesis_variable | before | required_after_evidence |
| --- | --- | --- |
| Agentforce/Data 360 ARR | nearly $3.4B disclosed in Q1 FY2027 | updated ARR or equivalent paid adoption metric |
| Agentforce ARR | $1.2B disclosed in Q1 FY2027 | updated ARR or growth rate |
| Agentic Work Units | 3.8B delivered to date | updated AWU count or usage growth |
| FY2027 revenue guide | $46.05B midpoint | updated revenue guide or Q2 trend |
| FY2027 FCF | modeled from FY2026 FCF and 4%-5% FCF growth guide | updated FCF guide or evidence of unchanged guide |
| FY2028 FCF forecast | MarketScreener $16.458B | updated forecast or source-stability check |

## Required Output

Use `templates/follow-through-refresh.md` to create:

- `follow-through-refresh-YYYY-MM-DD.md`

Then update:

- `evidence-log.csv`
- `expectation-map.csv`, if valuation changed
- `workflow-scorecard.csv`
- validation program audit files

## Non-Qualification Examples

Do not count as G04:

- adding a missed source from before 2026-05-30;
- updating current price only;
- restating Q1 FY2027 metrics;
- writing commentary without new source evidence;
- changing action label without before/after source trail.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Salesforce Q2 FY2027 materials become available, FY2028 FCF forecast changes materially, or reviewer requests a different first follow-through case.
