# Iteration 02 Seed: AI Power And Data-Center Infrastructure Handoff

- iteration_date: 2026-05-30
- theme: `ai_power_and_data_center_infrastructure`
- validation_stage: theme-to-company handoff seed
- status: partial_live_trial

## Research Setup

- research_object: AI data-center power / cooling / electrical infrastructure
- market_scope: US-listed public equities with global exposure
- time_boundary: 3-5 year long-term thesis, current evidence through 2026 Q1 company reports
- current_market_label: AI infrastructure / power bottleneck / grid-to-chip
- market_heat: high
- thesis_maturity: scaling
- heat_maturity_gap: moderate

## Source Notes

- Eaton reported Q1 2026 record results, raised 2026 organic growth guidance, and highlighted strong Electrical Americas demand, backlog and data-center momentum.
- Eaton's Q1 2026 analyst presentation frames its data-center portfolio from grid connection and power conditioning through cooling and software/services, including Boyd Thermal and a NVIDIA-linked AI factory architecture.
- GE Vernova reported Q1 2026 orders of $18.3B, organic order growth of 71%, and sequential backlog growth of $13.0B.
- Constellation's Q1 2026 release noted a 460 MW Texas peaking facility reaching commercial operation and a 380 MW agreement with CyrusOne for a data center adjacent to its Freestone site.

Source trail:

- Eaton Q1 2026 release: https://www.eaton.com/us/en-us/company/news-insights/news-releases/2026/eaton-reports-record-first-quarter-2026-results.html
- Eaton Q1 2026 analyst presentation: https://www.eaton.com/content/dam/eaton/company/investor-relations/quarterly-earnings/filings/2026/q1/q1-2026-analyst-presentation.pdf
- GE Vernova Q1 2026 release: https://www.gevernova.com/news/press-releases/ge-vernova-reports-first-quarter-2026-financial
- Constellation Q1 2026 release: https://investors.constellationenergy.com/news-releases/news-release-details/constellation-reports-first-quarter-2026-results

## Theme-To-Company Handoff

| node | examples | read_through_type | investable_purity | value_capture_path | handoff_decision |
| --- | --- | --- | --- | --- | --- |
| Electrical equipment / power management | ETN | supplier/enabler | medium-high | orders -> backlog -> revenue conversion -> margin durability -> ROIC | single_equity_research |
| Data-center thermal / power infrastructure | VRT | supplier/enabler | high | AI rack density -> cooling/power demand -> backlog -> capacity execution -> margin | single_equity_research |
| Grid equipment / power generation technology | GEV | supplier/enabler | medium | power demand -> equipment/service orders -> backlog -> execution and margin expansion | single_equity_research |
| Clean / firm power generation | CEG; VST | supplier/enabler | medium | data-center PPAs / co-location / power scarcity -> realized pricing and contracting | industry_map_first |
| Data-center operators | CRWV; DLR; EQIX; APLD | customer/derivative | mixed | compute demand -> power access -> utilization -> unit economics | separate research path |

## Six-Lens Quick Trial

### Consumer Demand

- relevance: indirect
- fact/inference: demand ultimately comes from AI model training/inference and enterprise/consumer AI usage, not retail consumers.
- source_gap: need AI workload growth, hyperscaler capex and inference monetization evidence.
- workflow_note: consumer lens should be waived or translated into end-compute demand for infrastructure themes.

### Product Reality

- relevance: medium
- fact/inference: product reality is not a consumer product test; it is whether power/cooling/grid solutions solve actual deployment bottlenecks.
- evidence_ladder_position: paid deployment / backlog, not merely concept.
- source_gap: need cancellation/delay rates, customer concentration and capacity execution data.

### Macro Economy

- relevance: high
- channel: financing + discount rate + electricity demand + grid constraints
- macro_weight: secondary
- risk: higher rates or permitting/grid delays can stretch deployment timelines and valuation duration.

### Industry Structure

- relevance: high
- strongest current lens
- evidence: order/backlog growth across Eaton and GE Vernova; data-center power contracting at Constellation.
- conflict: strong industry demand does not automatically mean all nodes earn excess returns.

### Company Execution

- relevance: high
- company-specific questions:
  - Can backlog convert on time?
  - Are acquisitions integrated without margin dilution?
  - Is capacity expansion enough?
  - Does the company have pricing power or only volume growth?

### Valuation Expectations

- relevance: high
- weakest current lens
- anchor_quality: source_gap at this stage
- what_must_go_right:
  - AI capex remains elevated for several years.
  - Backlogs convert without major cancellations.
  - Margins remain resilient despite capacity expansion and supply constraints.
  - Multiples do not compress as growth normalizes.
- false_precision_warning: no actionability conclusion until current valuation, consensus growth and implied margin assumptions are mapped by company.

## Workflow Evaluation

Score estimate against `workflow-scorecard.csv`:

| dimension | score | basis |
| --- | ---: | --- |
| source_quality | 4 | official company releases and presentations used, but no third-party demand/cancellation data yet |
| lens_coverage | 4 | all material lenses addressed; consumer lens translated rather than forced |
| conflict_detection | 4 | theme strength versus node-specific value capture identified |
| valuation_expectations | 2 | anchor still missing; no implied expectations map yet |
| refresh_conditions | 3 | triggers identified but not yet tied to company valuation |
| decision_impact | 4 | workflow prevents immediate blanket bullish theme conclusion |
| cost_efficiency | 3 | useful but still too manual |
| institutional_readiness | 3 | good internal trial note, not yet colleague-ready |

## What This Trial Proved

The new `theme_to_company_handoff` patch is necessary. Without it, AI power could become a broad theme conclusion. With the patch, the workflow forces node-specific research:

- ETN and VRT are likely better single-equity candidates for immediate workflow testing.
- CEG/VST need a different power-market contracting and regulatory framework.
- Data-center operators are a separate unit-economics and financing problem.

## What It Did Not Prove

- It did not prove any stock is attractive.
- It did not map current valuation expectations.
- It did not compare consensus estimates against the operating evidence.
- It did not test historical failure cases.

## Next Action

Run one full single-company trial on `ETN` or `VRT`, with mandatory valuation expectations:

- current valuation anchor
- consensus revenue/EPS/FCF trajectory
- implied duration of data-center growth
- backlog conversion assumptions
- margin normalization risk
- downside path if data-center deployments slip

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 2026 earnings, new hyperscaler capex guidance, data-center cancellation/delay evidence, backlog revisions, major power-market regulatory changes, or sharp valuation multiple compression.
