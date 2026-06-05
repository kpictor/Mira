# Mira Routing JSON Examples

These examples show the machine-first routing contract. The `routing.json`
object is the canonical routing artifact; any user-visible routing card is a
depth-scaled rendering of that object, controlled by
[../data/output-surface-matrix.md](../data/output-surface-matrix.md).

`scripts/validate_repo.py` validates every JSON block in this file against
[../schemas/routing.schema.json](../schemas/routing.schema.json). Keep examples
small, schema-valid and behaviorally meaningful.

## 1. Quick Map Surface

Prompt: `Mira, 看一下 AAPL 方向就行`

Machine routing object:

```json
{
  "schema_version": "routing.v1",
  "interaction_mode": "quick_answer",
  "primary_intent": "directional quick map on AAPL",
  "task_mode": "first_pass_research",
  "research_object": "single_equity:AAPL",
  "market_scope": "US equities",
  "time_boundary": "as_of_today",
  "depth_mode": "quick_map",
  "information_value": "medium",
  "knowability_status": "partially_knowable",
  "primary_skill_or_loop": "skills/equity-research-core/SKILL.md",
  "routing_basis": "User asked for a one-line direction, so answer shape is quick_answer and research depth is quick_map.",
  "followup_prompt_mode": "light",
  "followup_questions": [
    {
      "question": "Should the AAPL quick map focus on near-term revision or long-term services and AI durability?",
      "rung": "Rung B - pricing_variable_or_consensus",
      "route_binding": "time_boundary",
      "object_anchor": "AAPL revision versus services/AI durability",
      "decision_impact": "evidence_path"
    }
  ]
}
```

Visible routing card:

```text
按美股 / quick_map / 截止今天看 AAPL；先给方向性 working view，若要判断贵不贵或能不能动，再升级 valuation / actionability 路由。
```

## 2. Standard Research Surface

Prompt: `Mira, 研究 NVDA，标准 research package，重点看 Blackwell 供给和云厂 capex 是否还能支撑上修。`

Machine routing object:

```json
{
  "schema_version": "routing.v1",
  "interaction_mode": "routed_research",
  "primary_intent": "standard NVDA research package focused on Blackwell supply and hyperscaler capex revision path",
  "task_mode": "first_pass_research",
  "research_object": "single_equity:NVDA",
  "market_scope": "US equities",
  "time_boundary": "FY1_FY2_revision",
  "depth_mode": "standard",
  "information_value": "high",
  "knowability_status": "partially_knowable",
  "quant_dependency": "high",
  "calculation_gate": "required",
  "primary_skill_or_loop": "skills/equity-research-core/SKILL.md",
  "routing_basis": "The question depends on revision, valuation-implied expectations and peer/customer read-through, so it requires standard single-equity research with quant gate.",
  "expected_output_package": "research-package",
  "readiness_level": "working_view",
  "private_state_action": "waive",
  "followup_prompt_mode": "standard",
  "followup_questions": [
    {
      "question": "Should consensus proxy be anchored to FY1/FY2 data-center revenue, gross margin, or hyperscaler capex read-through?",
      "rung": "Rung B - pricing_variable_or_consensus",
      "route_binding": "quant_dependency",
      "object_anchor": "NVDA Blackwell supply, data-center revenue, gross margin and hyperscaler capex",
      "decision_impact": "calculation_depth"
    },
    {
      "question": "Which evidence would falsify the NVDA revision thesis: Blackwell delivery delay, cloud capex slowdown, or margin compression?",
      "rung": "Rung C - falsification_or_next_route",
      "route_binding": "thesis_system_update",
      "object_anchor": "NVDA Blackwell delivery, cloud capex and margin path",
      "decision_impact": "thesis_state"
    }
  ]
}
```

Visible routing card:

```text
primary_intent: NVDA Blackwell/capex revision research
depth_mode: standard
source/quant boundary: company disclosure, cloud capex read-through, consensus proxy and valuation-implied expectations are required before durable judgment.
readiness_level: working_view until the quant gate is satisfied.
```
