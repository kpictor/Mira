# Evidence Posture Taxonomy

This file defines the cross-skill evidence posture Mira uses after a claim has
already been classified by `claim_type`.

`claim_type` describes what the information is. `evidence_category` describes
how decision-ready that information is for the current research use.

## Canonical Categories

| evidence_category | meaning | default treatment |
| --- | --- | --- |
| `verified_fact` | Directly supported by a primary or controlling source that matches the claim, period, unit and scope. | Use normally with source date, as-of date and scope note. |
| `reported_fact` | Stated by a source or data provider, but not independently checked against the controlling source. | Attribute to the source; verify if material. |
| `company_statement` | Company, IR or management commentary that is not itself a filed metric or binding commitment. | Use as company view, not proof of outcome or causality. |
| `management_guidance` | Formal guidance, target range, outlook or management case. | Use as expectation input; test against history, capacity, demand and peers. |
| `market_pricing` | Price, multiple, spread, options, estimate revision, positioning or other market-implied information. | Use to describe what is priced, not to verify fundamentals. |
| `assumption` | User, Mira, analyst, model or scenario input chosen for analysis. | Label visibly and sensitize if material. |
| `inference` | Mira or analyst conclusion drawn from evidence but not explicitly stated by a source. | Cite the underlying evidence and keep confidence bounded. |
| `estimate` | Calculated, consensus, benchmark, proxy or model-derived value. | Show formula, inputs, source chain and sensitivity when material. |
| `weak_signal` | Social, channel, media, expert, anecdotal or unverified signal. | Use for monitoring or hypothesis generation; do not anchor durable conclusions. |
| `stale` | Source exists but is superseded, outside the relevant time boundary or too old for the requested use. | Flag as stale and downgrade until refreshed. |
| `contradicted` | Material sources disagree on value, definition, period, unit, scope or interpretation. | Preserve the conflict and identify the controlling source or open item. |
| `unknown` | Needed but missing, inaccessible, unsupported or intentionally left as a placeholder. | Convert to source gap, diligence ask, watch-only action or refresh trigger. |

## Category Precedence

Use the most conservative applicable category:

1. `contradicted`
2. `stale`
3. `unknown`
4. `weak_signal`
5. `company_statement`, `management_guidance` or `assumption`
6. `estimate` or `inference`
7. `reported_fact`
8. `verified_fact`

`freshness_status` and `conflict_status` can carry the same information as
overlays. If a single field must carry the decision posture, use `stale` or
`contradicted` as `evidence_category` when either condition changes the
conclusion.

## Recommended Evidence Log Fields

New evidence logs should include these fields after the existing canonical
columns:

- `evidence_category`
- `freshness_status`
- `conflict_status`
- `treatment`
- `readiness_impact`

Allowed `freshness_status` values:

- `current`
- `acceptable_for_period`
- `preliminary`
- `stale`
- `unknown`

Allowed `conflict_status` values:

- `none`
- `unresolved`
- `contradicted`
- `not_checked`

Allowed `treatment` values:

- `use_normally`
- `attribute`
- `sensitize`
- `haircut`
- `source_gap`
- `monitor`
- `exclude`
- `open_item`

Allowed `readiness_impact` values:

- `supports_durable_conclusion`
- `supports_working_view`
- `monitoring_only`
- `blocks_actionability`
- `blocks_publication`
- `not_material`

## Language Discipline

- Do not call `company_statement`, `management_guidance`, `assumption`,
  `estimate`, `weak_signal` or `market_pricing` a verified fact.
- Do not use `market_pricing` as proof that fundamentals are true.
- Do not let a correctly calculated `estimate` upgrade weak source quality.
- When `evidence_category` is `stale`, `contradicted` or `unknown`, the linked
  thesis or actionability claim must be downgraded unless another current,
  controlling source resolves the issue.
