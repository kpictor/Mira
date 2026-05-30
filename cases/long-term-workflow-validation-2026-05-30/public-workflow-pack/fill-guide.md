# Fill Guide

## Evidence Log

Use `evidence-log.csv` for all durable claims.

Minimum columns:

- `source_id`
- `claim_area`
- `claim_type`
- `claim_text`
- `source_speaker`
- `verification_status`
- `authority_level`
- `source_date`
- `as_of_date`
- `url_or_path`
- `confidence`
- `notes`

Authority levels:

- `L1`: company filing, regulator filing, official company release
- `L2`: official transcript, official presentation, exchange filing
- `L3`: recognized independent dataset or industry body
- `L4`: market data / third-party aggregator
- `L5`: media / expert commentary
- `L6`: Mira-derived calculation or analyst inference

Rule: L6 can support interpretation, but it cannot be the only evidence for a durable conclusion.

## Expectation Map

Use `templates/long-term-expectation-map.csv`.

Minimum fields:

- current price
- market cap
- enterprise value
- valuation anchor type
- anchor quality
- FY1/FY2 revenue estimates
- FY1/FY2 EPS estimates
- FY1/FY2 FCF estimates, or explicit `source_gap`
- company guidance midpoint
- current multiple
- historical multiple range
- peer multiple range
- implied growth duration
- implied margin path
- implied ROIC path
- what must go right
- what is already priced
- false precision warning
- downside case
- valuation refresh trigger

Public-grade expectation map requires:

- primary source for company guidance
- source trail for price, share count, market cap and EV
- source trail for consensus or estimate data
- at least one peer range
- at least one historical range
- explicit treatment of missing FY2 FCF, if unavailable

### Unavailable-Data Exception

Use this only when a required valuation field is not available from the public sources used.

Required treatment:

- keep the field as `source_gap`
- document source attempts
- label modeled values as `modeled`, not consensus
- add a `false_precision_warning`
- state whether the missing field blocks actionability

Stop rule:

- If valuation is a gating lens, unavailable FY2 FCF, historical EV/FCF or historical forward P/E should keep the case watch-only unless an independent reviewer accepts the unavailable-data exception.

## Product Monetization Map

Use when product evidence drives the thesis.

Map each product metric to an economic link:

- `direct_revenue`
- `expansion_signal`
- `retention_signal`
- `usage_proxy`
- `cost_driver`
- `adoption_breadth`

Stop rule:

- Usage, tokens, records, active users or pilots do not prove monetization unless linked to revenue, retention, pricing or margin.

## Theme Value-Capture Screen

Use before single-company research when a hot theme has unclear public-company value capture.

Required fields:

- value-chain node
- public expression
- role in theme
- theme purity
- value-capture evidence
- evidence maturity
- valuation risk
- workflow decision

Stop rule:

- If no public expression has direct, material and measurable value capture, route to `industry_map_first` instead of forcing a stock conclusion.

## Pull-Forward Check

Use when demand may be abnormal.

Required fields:

- shock source
- duration of shock
- normalized usage or demand baseline
- post-shock retention
- payer or budget persistence
- valuation if growth normalizes

Stop rule:

- If normalized demand is unknown, do not promote shock-era growth into a long-term actionability conclusion.

## Payer Access / Net Price Check

Use when healthcare product demand depends on reimbursement or policy.

Required fields:

- patient demand
- prescriber demand
- clinical evidence
- regulatory status
- payer coverage
- employer or government reimbursement
- cash-pay price
- gross-to-net / realized-price trend
- prior authorization or access friction
- adherence or persistence
- competitive formulary risk
- policy or regulatory risk

Stop rule:

- Clinical demand does not prove economic demand unless payer access, net price and persistence are evidenced.

## Hardware / Subscription Mix Check

Use when subscription economics depend on physical product placement.

Required fields:

- hardware revenue growth
- hardware gross margin
- subscriber growth source
- retention or churn
- engagement quality
- inventory or capacity commitment
- replacement cycle
- normalized new-user demand
- unit economics after normalization

Stop rule:

- Subscription growth cannot rescue the thesis if hardware demand and hardware gross margin are deteriorating and the installed base depends on new hardware placement.

## Backlog Quality Check

Use when backlog, RPO, order book or book-to-bill drives the thesis.

Required fields:

- backlog metric
- backlog growth
- order growth or book-to-bill
- conversion timing
- cancellation or deferral risk
- margin quality
- customer concentration
- capacity or supply constraint
- valuation dependency
- refresh trigger

Stop rule:

- Backlog does not prove long-term demand unless firmness, conversion timing, cancellation risk and margin quality are evidenced.

## Acquisition Value-Capture Check

Use when growth, exposure or product capability is acquired.

Required fields:

- acquired asset
- purchase price
- strategic rationale
- revenue contribution
- margin contribution
- integration risk
- cross-sell or synergy evidence
- incremental ROIC path
- balance sheet impact
- refresh trigger

Stop rule:

- Acquired exposure cannot be treated as value creation until purchase price, integration, incremental margin and ROIC path are explicit.

## Cash-Flow Quality Check

Use when FCF, cash conversion or capital returns are central to the thesis.

Required fields:

- cash-flow metric
- operating cash-flow trend
- capex trend
- working-capital driver
- stock compensation or non-cash addback
- FCF margin
- FCF conversion
- debt or buyback dependency
- multi-year durability
- refresh trigger

Stop rule:

- One strong cash-flow period does not prove durable FCF without working-capital, capex and per-share quality decomposition.

## Power Contract / Regulatory Check

Use when data-center power, nuclear, SMR, utility or independent-power-producer exposure drives the thesis.

Required fields:

- project or contract
- public expression
- contract type
- offtaker credit
- term or capacity
- regulatory status
- interconnection or grid status
- cost recovery or tariff issue
- commercial operation timing
- developer execution evidence
- source id
- workflow decision

Stop rule:

- Signed demand or a headline PPA does not prove durable value capture unless contract economics, regulatory approval, interconnection treatment, cost allocation and commercial operation timing are evidenced.

## Stablecoin Reserve / Regulatory Check

Use when stablecoin, tokenized cash, tokenized treasury or payment-network adoption drives the thesis.

Required fields:

- issuer or network
- public expression
- role in theme
- reserve asset quality
- reserve-yield sensitivity
- distribution or partner costs
- redemption or liquidity risk
- regulatory status
- AML/BSA/sanctions status
- payment network evidence
- source id
- workflow decision

Stop rule:

- Stablecoin circulation or payment-network announcements do not prove durable equity value unless reserve economics, partner economics, redemption liquidity, regulatory status and real payment usage are evidenced.

## Government Procurement / Program Check

Use when defense, government procurement, drones, autonomy, counter-UAS, national-security software or federally funded infrastructure drives the thesis.

Required fields:

- program or contract
- public expression
- role in theme
- customer or authority
- budget or funding status
- contract status
- program-of-record status
- production or delivery status
- unit economics or margin risk
- compliance or security requirement
- export or allied sales status
- source id
- workflow decision

Stop rule:

- A policy priority, prototype, CSO, OTA or pilot does not prove durable equity value unless funding, program status, delivery, compliance and margin path are evidenced.

## Source-Gap Refresh

Use when a blocking `source_gap` is closed after the initial memo.

Required fields:

- original blocked claim
- missing source type
- new source found
- source authority level
- thesis variable affected
- action label before refresh
- action label after refresh
- whether the refresh qualifies as true post-memo follow-through

Stop rule:

- Source cleanup improves publication quality, but it does not satisfy the true follow-through gate unless the triggering evidence occurred after the original memo was completed.

## Workflow Scorecard

Score each case from 1 to 5 on:

- source quality
- lens coverage
- conflict detection
- valuation expectations
- refresh conditions
- decision impact
- cost efficiency
- institutional readiness

Minimum public-grade score is 4 in every dimension.

If any dimension is below 4, the case can still be useful internally but should not be used as an external example without caveats.

## Ordinary Vs Workflow Delta

Before treating a case as methodology evidence, record:

- ordinary likely conclusion
- workflow conclusion
- actionability change
- new stop rule
- source gap exposed
- whether the workflow changed the decision enough to justify its cost

Stop rule:

- If the workflow does not change conclusion, actionability, sizing, source-gap map, kill criteria or refresh conditions, record the case as a methodology failure or cost-efficiency failure.

## Writing Standard

Use this order:

1. Decision header
2. Core conclusion
3. Facts
4. Inferences
5. Judgments
6. Evidence gaps
7. Refresh triggers

Do not mix facts, inferences and judgments in one paragraph when the conclusion is durable.

## Reviewer Questions

Before sharing a case, another analyst should be able to answer:

- What would falsify the thesis?
- Which lens is weakest?
- Which evidence is company claim versus verified fact?
- What is already priced?
- What source gap blocks actionability?
- What event forces refresh?
- If a source gap is closed later, did the action label change for an evidence reason or only because the memo looks cleaner?
- Did the workflow change the decision versus an ordinary memo?
