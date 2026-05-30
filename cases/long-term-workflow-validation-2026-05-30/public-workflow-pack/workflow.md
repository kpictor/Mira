# Workflow

## 0. Setup

Define the research object before collecting evidence:

- company / industry / theme
- market scope
- time boundary
- thesis horizon
- current market label
- source availability
- expected decision use

If the task is not a long-term thesis or regime-transition question, route to a narrower workflow.

## 1. Theme-To-Company Handoff

Use this gate whenever a hot theme is being converted into a stock idea.

Required fields:

- theme definition
- value-chain nodes
- public company expressions
- investable purity
- value-capture path
- why this company and not just the theme
- read-through type
- theme purity score
- expectation burden score
- evidence maturity score
- valuation heat score

Stop rules:

- If value capture is unclear, build an industry map first.
- If theme purity and expectation burden are both high, do not issue an actionability conclusion without a complete expectation map.

## 2. Six-Lens Thesis Test

### Consumer Demand

Answer:

- who is the end user and who pays?
- what triggers adoption?
- what budget funds demand?
- what proves frequency, retention or repeat purchase?
- what substitutes or trading-down paths exist?

### Product Reality

Answer:

- what customer job is solved?
- why is this product better than alternatives?
- where is the product evidence ladder today?
- does usage bridge to revenue, retention, pricing or margin?

Product evidence ladder:

`concept -> demo -> pilot -> paid_deployment -> repeat_usage -> expansion -> retention -> pricing_power -> margin_conversion`

### Macro Economy

Answer:

- which macro variables affect revenue, margins, financing, discount rates or risk premium?
- is macro a background condition, secondary lens or primary price-setter?
- what macro path does the stock already appear to price?

### Industry Structure

Answer:

- where is the profit pool?
- is the industry growing, consolidating, commoditizing or regulated?
- who has supplier, customer and channel power?
- is value migrating toward or away from this company?

### Company Execution

Answer:

- can management convert opportunity into ROIC and cash flow?
- is capital allocation additive or distorting per-share metrics?
- what execution KPI would prove or disprove the thesis?
- is the balance sheet survivable if the thesis takes longer?

### Valuation Expectations

Answer:

- what does current price imply about growth, margin, ROIC and duration?
- what is already priced?
- what must go right?
- what is the downside path?
- what data would force valuation refresh?

Stop rules:

- If anchor quality is `source_gap`, no actionability conclusion.
- If market heat is high and FY1/FY2 expectation mapping is missing, use `watch_only_pending_expectation_map`.

## 3. Triggered Overlays

### Product Monetization Map

Trigger when product usage, ARR, bookings, tokens, active users, records or API calls drive the thesis.

Block actionability if product metrics do not bridge to retention, pricing, margin or total-company growth.

### Pull-Forward Vs Structural Demand

Trigger when the thesis forms during a pandemic, stimulus, regulatory deadline, supply shortage, replacement cycle, credit shock or inventory restocking.

Block actionability if normalized demand or post-shock retention is a source gap.

### Payer Access / Net Price

Trigger when product demand depends on insurance coverage, reimbursement, employer benefits, government access, cash-pay price or healthcare policy.

Block actionability if clinical demand is strong but payer coverage, net price, access friction or persistence is a source gap.

### Hardware / Subscription Mix

Trigger when subscription growth depends on devices, equipment, installation, supply chain or installed-base expansion.

Block actionability if normalized hardware demand or hardware gross margin is a source gap.

### Backlog Quality

Trigger when backlog, RPO, order book or book-to-bill drives the thesis.

Block actionability if backlog firmness, timing, cancellation risk or margin quality is unclear.

### Acquisition-Driven Value Capture

Trigger when exposure or growth is acquired.

Block actionability until purchase price, integration, incremental margin and ROIC path are explicit.

### Capital Allocation Distortion

Trigger when buybacks, ASRs, acquisitions, divestitures or debt materially affect per-share results.

Do not treat per-share acceleration as operating acceleration until share count, debt and acquired contribution are separated.

### Cash Flow Quality

Trigger when FCF or cash conversion is part of the thesis.

Do not treat one quarter of FCF strength as durable without working-capital and capex decomposition.

### Power Contract / Regulatory Quality

Trigger when data-center power, nuclear, SMR, utility or independent-power-producer exposure drives the thesis.

Block actionability if contract economics, offtaker credit, regulatory approval, interconnection treatment, cost allocation or commercial operation timing is unclear.

### Stablecoin Reserve / Regulatory Quality

Trigger when stablecoin, tokenized cash, tokenized treasury or payment-network adoption drives the thesis.

Block actionability if reserve asset quality, reserve-yield sensitivity, distribution costs, redemption liquidity, regulatory status, AML/BSA obligations or real payment usage is unclear.

### Government Procurement / Program Quality

Trigger when defense, government procurement, drones, autonomy, counter-UAS, national-security software or federally funded infrastructure drives the thesis.

Block actionability if funding status, contract type, program-of-record path, production/delivery status, compliance requirements, export constraints or margin risk is unclear.

## 4. Evidence Classification

Separate every durable conclusion into:

- fact
- company claim
- guidance
- market pricing
- third-party estimate
- derived calculation
- inference
- judgment

Every durable conclusion needs a source trail.

## 5. Decision

Write the decision as:

- research action
- weakest assumption
- strongest evidence
- biggest source gap
- valuation expectation burden
- next refresh trigger
- kill criteria

If the workflow does not change confidence, actionability, sizing, refresh conditions or kill criteria, record that as a methodology failure.

## 6. Refresh

Every case must include:

- `stale_after`
- `must_refresh_if`
- observable trigger
- thesis variable affected
- expected state change if trigger fires

Refreshes should update the thesis state, not rewrite the original memo from scratch.

### Source-Gap Refresh

Use this when a case is blocked by a high-impact `source_gap`.

Required fields:

- original blocked claim
- missing source type
- new source found
- source authority level
- thesis variable affected
- action label before refresh
- action label after refresh
- reason this is or is not a true follow-through refresh

Rules:

- A source-gap refresh can improve publication quality and change the research action.
- It cannot satisfy the public-grade follow-through gate unless the triggering evidence occurred after the original memo was completed.
- Favorable new evidence does not upgrade actionability unless it also changes the weakest lens, stop rule or valuation expectation burden.
