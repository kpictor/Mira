# Template Inventory

- inventory_date: 2026-05-30
- template_root: `templates/`
- status: internal_candidate

## Required Base Templates

| template | use when | public-grade rule |
| --- | --- | --- |
| `long-term-expectation-map.csv` | Any single-equity long-term thesis. | Missing FY1/FY2 revenue, EPS, FCF, peer range or historical range must be explicit `source_gap`. |

## Triggered Overlay Templates

| template | trigger | stop rule |
| --- | --- | --- |
| `theme-value-capture-screen.csv` | Hot theme has unclear public-company value capture. | If no public expression has direct, material and measurable value capture, route to `industry_map_first`. |
| `product-monetization-map.csv` | Product usage, ARR, bookings, tokens, active users, records or API calls drive the thesis. | Product metrics must bridge to revenue, retention, pricing, margin or total-company growth. |
| `pull-forward-check.csv` | Demand may be abnormal because of pandemic, stimulus, shortage, replacement cycle, regulatory deadline or inventory restocking. | Normalized demand and post-shock retention must be evidenced before actionability. |
| `payer-access-net-price-check.csv` | Healthcare demand depends on coverage, reimbursement, employer benefits, cash-pay price or policy. | Clinical demand must convert into funded economic demand with payer access, net price and persistence evidence. |
| `hardware-subscription-mix-check.csv` | Subscription economics depend on devices, equipment, installation or installed-base expansion. | Subscription retention cannot rescue deteriorating normalized hardware demand and hardware gross margin. |
| `backlog-quality-check.csv` | Backlog, RPO, order book or book-to-bill drives the thesis. | Backlog firmness, conversion timing, cancellation risk and margin quality must be evidenced. |
| `acquisition-value-capture-check.csv` | Growth, exposure, product capability or value capture is acquired. | Purchase price, integration, incremental margin and ROIC path must be explicit. |
| `cash-flow-quality-check.csv` | FCF, cash conversion, capital returns or cash-flow multiple drives the thesis. | Working-capital, capex and per-share quality must be decomposed. |
| `power-contract-regulatory-check.csv` | Data-center power, nuclear, SMR, utility or IPP exposure drives the thesis. | Contract economics, offtaker credit, regulatory approval, interconnection, cost allocation and COD must be evidenced. |
| `stablecoin-reserve-regulatory-check.csv` | Stablecoin, tokenized cash, tokenized treasury or payment-network adoption drives the thesis. | Reserve economics, distribution costs, redemption liquidity, regulatory status, AML/BSA obligations and real payment usage must be evidenced. |
| `government-procurement-program-check.csv` | Defense, government procurement, drones, autonomy, counter-UAS, national-security software or federally funded infrastructure drives the thesis. | Funding, contract status, program-of-record path, delivery, compliance, export constraints and margin risk must be evidenced. |

## Refresh Template

| template | trigger | public-grade rule |
| --- | --- | --- |
| `source-gap-refresh.md` | A blocking `source_gap` is closed after the initial memo. | State whether the refresh qualifies as true post-memo follow-through; source cleanup alone is not enough. |
| `follow-through-refresh.md` | A later material event occurs after the original memo cutoff. | Must compare before/after thesis state, evaluate the original refresh trigger and state action-label impact. |

## Maintenance Rule

Every workflow overlay must appear in four places before the pack can be shared externally:

1. `workflow.md`
2. `fill-guide.md`
3. `analyst-checklist.csv`
4. this template inventory

If an overlay appears in a case but not in all four places, the pack is not public-grade.
