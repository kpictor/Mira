# CPO / Silicon Photonics Industry Map

- concept_name: `CPO / silicon photonics for AI networking`
- research_question: Does roadmap-to-bottleneck recursion identify the next investable bottlenecks behind NVIDIA's CPO / silicon photonics roadmap?
- market_scope: global with US-listed proxies
- research_cutoff_date: 2026-06-01
- thesis_horizon: 12-36 months
- depth: standard methodology trial
- focus: supply_shortage / volume_ramp / stock_mapping / risk_scan
- stale_after: 2026-07-01
- not_investment_advice: true

## One-Page Industry Map

### One-Sentence Definition

CPO moves optical I/O closer to the switch or compute package, while silicon photonics integrates optical functions onto chip-scale platforms; the AI networking problem is to cut power, latency and failure points as clusters scale toward million-GPU factories.

### Current Judgment

The roadmap is real enough for a methodology trial: NVIDIA says Spectrum-X Ethernet Photonics is in production and TSMC says its COUPE package-level optical engine platform is scheduled for production in 2026. The investable question is no longer "is CPO a theme?" but "which upstream node becomes the next binding constraint as CPO moves from demonstrations to production scale?"

Current bottleneck ranking:

1. `external_laser_and_InP_chain`
   Most likely near-term upstream bottleneck because high-power, reliable laser sources are necessary, specialized and capacity-sensitive.
2. `photonic_engine_and_package_integration`
   Highest strategic value but harder to isolate in public markets because the best assets are inside TSMC, NVIDIA and private silicon-photonics companies.
3. `fiber_connector_and_optical_infrastructure`
   Real scaling requirement, but likely better represented by large diversified suppliers and capacity execution than by a pure scarcity story.
4. `generic optical transceivers`
   Relevant but less differentiated for this specific method because the roadmap shifts value toward co-packaged and integrated optics.

### Where It Is Tight

- Tight or likely tight: external lasers, InP laser manufacturing equipment, InP substrates, laser arrays, package attach, fiber attach, optical connector scale, thermal/power integration and production test/yield.
- Not enough evidence yet: whether TFLN, silicon photonics foundry capacity or specific connector formats are the dominant public-market bottleneck.
- Not the right shortcut: buying every optical name, every semiconductor equipment name or every AI networking stock without proving exposure purity.

### Best Economic Layers

1. `Laser sources and InP laser manufacturing`
   Directly enabled by NVIDIA / Coherent and Lumentum evidence; also supported by Veeco's InP laser equipment order commentary.
2. `CPO package integration / COUPE ecosystem`
   Technically central, but public-market value capture is mostly inside TSMC, NVIDIA and private partners unless suppliers disclose direct content.
3. `Fiber and connectivity scale`
   Corning/NVIDIA partnership indicates real buildout needs, but economics depend on volume, fiber mix and contract terms.

### Best Stock Proxies

- `COHR`: high direct relevance through NVIDIA partnership, advanced optics and manufacturing capacity commitments.
- `LITE`: direct laser-source relevance; useful for testing external laser value capture.
- `VECO`: picks-and-shovels proxy for InP laser manufacturing equipment, based on explicit AI/CPO-related order commentary.
- `AXTI`: higher-risk substrate proxy for InP, small-cap and geopolitically exposed; useful only after company-level diligence.
- `GLW`: optical connectivity scale proxy, less pure but supported by a named NVIDIA partnership.
- `TSM`: strategic COUPE platform proxy, but too diversified for a clean CPO bottleneck trade.

### Core Formula

Demand pressure:

`AI cluster scale x switch radix/bandwidth x optical I/O per switch or accelerator x CPO adoption rate x optical power/fiber attach intensity`

Supply capacity:

`qualified external laser output x InP substrate and epi capacity x photonic engine foundry capacity x CPO package yield x fiber/connector manufacturing capacity x customer qualification pass rate`

### Key Debate

The market debate should be reframed from "CPO is coming" to:

- Is the first binding constraint external laser/InP, package integration yield, fiber/connectivity scale, or foundry photonics capacity?
- Which public companies have enough exposure purity and value capture to matter?
- Will CPO pull forward demand into 2026-2027, or does adoption remain limited to flagship systems while pluggables keep most near-term volume?

### What To Monitor

- NVIDIA Spectrum-X / Quantum-X Photonics production updates, customer deployments and power efficiency claims.
- TSMC COUPE production timing, qualified customers, packaging yield and ecosystem partner disclosures.
- Coherent and Lumentum datacom laser orders, capex, customer concentration, gross margin and CPO-related language.
- Veeco InP equipment backlog, shipments and customer concentration.
- AXT InP substrate revenue, 6-inch progress, export constraints and customer qualification.
- Corning optical fiber/connectivity capacity expansion and AI data-center revenue conversion.
- Evidence that CPO attach rate is rising versus pluggable optics.

### Falsification

- NVIDIA or TSMC delays or narrows CPO / photonics deployment.
- Pluggable optics or linear drive optics solve enough of the power/latency problem to delay CPO adoption.
- Laser and InP suppliers add capacity faster than demand, removing pricing or margin leverage.
- Candidate companies report no CPO-related backlog, margin improvement, capex absorption or customer validation.
- Public proxies have too little exposure purity relative to valuation and narrative heat.

## Full Diligence

### Core Conclusion

The recursion did change the research output. A normal industry map would likely stop at "CPO / silicon photonics benefits optical suppliers." The trial map narrows the first validation path to the external laser and InP chain, with package integration as the strategic but less publicly isolatable bottleneck.

Current action label: `watchlist_and_company_handoff`, not `single_equity_thesis`.

### Concept Boundary

#### Plain-Language Definition

CPO puts optical connections closer to the chip package so data can move in and out of AI switches and accelerators with less power and latency than conventional pluggable optics.

#### Technical Definition

CPO integrates optical engines adjacent to switching or compute silicon. Silicon photonics implements optical components such as modulators, waveguides and detectors on silicon-based platforms. External laser sources often provide the optical light source, while the package must handle electrical I/O, optical I/O, thermal load, fiber attach and reliability.

#### Adjacent Concepts

- `Pluggable optics`: modules plugged into the front panel. Still important, but not the same as CPO.
- `Linear drive optics`: an intermediate power-efficiency route that can delay or complement CPO.
- `Optical circuit switching`: related network architecture, not identical to CPO.
- `TFLN`: promising electro-optic material platform, not yet proven as the dominant bottleneck for this map.
- `InP`: compound semiconductor platform for lasers and photonic devices; central to external laser source discussion.

#### What It Is Not

- It is not all optical networking.
- It is not every fiber or connector company.
- It is not a generic AI semiconductor equipment screen.
- It is not a proof that every CPO participant captures economics.

#### Why It Matters Now

NVIDIA has moved CPO / silicon photonics from concept into product roadmap language, and the Vera Rubin announcement states Spectrum-X Ethernet Photonics is in production. TSMC's 2026 symposium materials also give COUPE a 2026 production timing. That creates a roadmap anchor strong enough to start recursive bottleneck work.

### Value Chain Map

| Layer | Function | Representative companies | Key bottleneck | Trial read |
| --- | --- | --- | --- | --- |
| Roadmap owner / system integrator | Defines AI networking architecture and pulls supply chain | NVIDIA, hyperscalers | CPO attach rate and deployment timing | Roadmap anchor, not the bottleneck proxy |
| Foundry / photonic engine platform | Integrates optical engine with package and silicon | TSMC COUPE, Intel, private silicon-photonics firms | package integration, yield, thermal and optical attach | strategically central, low public purity |
| External laser source | Supplies optical light source for photonic engines | Coherent, Lumentum, Sivers, private suppliers | reliability, power, arrays, volume manufacturing | first public-company validation path |
| InP substrate and epi chain | Substrate/device platform for lasers and photonic devices | AXT, Sumitomo Electric, IQE and others | substrate quality, diameter, export/geography, epi capacity | high-risk upstream candidate |
| Laser manufacturing equipment | Enables InP laser device capacity | Veeco and peers | equipment qualification and customer capex timing | useful picks-and-shovels proxy |
| Fiber / connector / cabling | Connects AI factory fabric | Corning, Amphenol, TE, Molex/private | capacity, fiber attach, connector reliability | real scale node, lower purity |
| Test / inspection / reliability | Validates optical package performance | Teradyne, Advantest, FormFactor, Keysight and others | test complexity and yield learning | source gap |

### Recursive Bottleneck Ladder

See `recursive-bottleneck-ladder.csv`.

The first recursion is:

`NVIDIA AI factory roadmap -> Spectrum-X / Quantum-X Photonics -> CPO package -> photonic engine -> external laser source -> InP laser manufacturing -> InP substrate/epi and laser equipment`

The second recursion is:

`NVIDIA AI factory roadmap -> Spectrum-X / Quantum-X Photonics -> optical fabric scale -> fiber attach -> fiber/connectivity capacity -> glass/fiber manufacturing footprint`

### Demand Map

Demand is pulled by AI cluster bandwidth and power limits. The larger the AI factory, the more front-panel pluggable optics becomes a power, density and reliability challenge. CPO is therefore most relevant where switching bandwidth, interconnect length, power budget and system scale make optical integration a system-level requirement.

The strongest current demand source is NVIDIA's own roadmap and partnership activity, not a broad market attach-rate dataset. That means this is still a roadmap-led thesis and needs later customer/deployment validation.

### Supply Map

The supply chain is not one bottleneck:

- `Laser and InP`: supported by named NVIDIA/Coherent and NVIDIA/Lumentum relationships plus Veeco equipment order commentary.
- `Package integration`: supported by TSMC COUPE timing and claimed power/latency improvements, but public proxy quality is weaker.
- `Fiber/connectivity`: supported by Corning/NVIDIA manufacturing expansion, but GLW is a diversified proxy.

### Pricing Mechanics

| Layer | Pricing logic | Current read |
| --- | --- | --- |
| External lasers | qualification, reliability, power efficiency, customer urgency, capacity | best near-term chance of value capture, needs company margin proof |
| InP substrates | material quality, diameter transition, supply concentration, export constraints | high optionality, high execution/geography risk |
| CPO packaging | strategic integration, foundry ecosystem, yield learning | high value but hard to isolate in public markets |
| Fiber/connectivity | volume contracts, manufacturing capacity, mix shift to AI connectivity | large volume opportunity, lower scarcity evidence |
| Generic optical modules | bandwidth cycle and datacom demand | relevant but may be less differentiated as CPO moves value inside package |

### Volume Mechanics

Volume is constrained by:

- CPO design wins and platform qualification.
- Laser array and external light source reliability.
- InP device and substrate output.
- COUPE / CPO package yield and production test.
- Fiber attach and connector process scale.
- AI networking system ramp timing.

### Tightness And Profit-Pool Ranking

| Layer | supply_demand_tightness | pricing_power | volume_visibility | margin_capture | stock_proxy_quality |
| --- | --- | --- | --- | --- | --- |
| External lasers / InP devices | tight | medium-high | medium-high | medium-high | strong for COHR/LITE, source-gap for others |
| InP substrates | tight in qualified grades | medium | medium | medium | usable but high risk |
| CPO / COUPE integration | tight / emerging | high | medium | high | weak to usable because purity is low |
| Fiber/connectivity | tight in AI-scale deployment | medium | high | medium | usable but diversified |
| Generic optical modules | cyclical tight | medium | high | medium | usable but not pure CPO recursion |

### Institutional + Practical + First-Principles Check

#### Institutional Lens

This is a roadmap-led supply-chain theme. The investment discipline should be exposure purity, backlog/margin conversion and valuation burden, not thematic excitement. A stock handoff should require company-level financial transmission.

#### Operator Lens

The hardest parts are not naming the chain. They are making lasers reliable at scale, packaging optical engines with acceptable yield, attaching fiber in a manufacturable way, testing the package, and qualifying customers. Lead times and yield curves matter more than TAM slogans.

#### First-Principles Lens

Electrical interconnect power and density get worse as bandwidth and cluster size rise. Moving optics closer to silicon can reduce electrical travel distance, but it creates new packaging, thermal, optical alignment and laser-source constraints. Bottleneck migration is therefore plausible.

#### Conflicts To Resolve

- Whether external lasers or package integration is the first binding constraint.
- Whether public companies have enough CPO exposure purity.
- Whether 2026 production language means broad commercial volume or early flagship deployment.
- Whether pluggables or linear drive optics delay CPO adoption.

### Company Shortlist

See `company-map.csv`.

### Stock Research Handoff

Priority handoff candidates:

1. `COHR`
   Why: named NVIDIA strategic partnership and optics manufacturing capacity commitment. Need to test margin conversion, customer concentration and valuation.
2. `LITE`
   Why: direct laser-source relevance and NVIDIA demo participation. Need to test whether CPO lasers are material relative to total revenue.
3. `VECO`
   Why: InP laser manufacturing equipment proxy with explicit AI/CPO order language. Need to test backlog quality and customer concentration.
4. `AXTI`
   Why: high-upstream InP substrate proxy. Need to test exposure purity, China/export risk, financial strength and qualification evidence.
5. `GLW`
   Why: optical fiber/connectivity scale proxy. Need to test AI data-center mix and margin impact.

### Monitoring Dashboard

| Metric | Why it matters | Source path |
| --- | --- | --- |
| Spectrum-X / Quantum-X Photonics deployment | Confirms roadmap timing | NVIDIA product and earnings updates |
| COUPE production / customer timing | Confirms package integration path | TSMC technology and earnings updates |
| COHR/LITE datacom laser revenue and margin | Tests laser value capture | company filings and earnings calls |
| VECO InP equipment orders | Tests laser manufacturing capacity buildout | company earnings and backlog |
| AXTI InP substrate revenue / 6-inch progress | Tests substrate bottleneck | company filings |
| GLW optical connectivity capacity and AI revenue | Tests fiber scaleout | company filings and NVIDIA partnership updates |

### Open Questions

- Which laser architecture becomes standard for NVIDIA-scale CPO?
- Does TSMC COUPE rely on a narrow set of suppliers or multiple qualified paths?
- What share of COHR/LITE revenue could be directly tied to CPO external laser sources?
- Are InP substrates genuinely the bottleneck, or is laser device manufacturing / epi / packaging more binding?
- Which public test equipment suppliers have direct CPO package exposure?

### Must Refresh If

- NVIDIA, TSMC, Coherent, Lumentum, Corning, Veeco or AXT disclose materially different CPO timing, capacity, orders, margins or customer qualification.
- CPO adoption is delayed by pluggables, linear drive optics or another interconnect path.
- Candidate companies show no measurable financial transmission by the next two earnings cycles.
