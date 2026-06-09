# Agent Interface Specification — Multi-Agent System v1.0

**Document:** Agent Communication Contracts
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Agents:** 4 agents (Knowledge Retrieval, Technical Assessment, Risk & Economic Assessment, PM Review)

---

## 1. Communication Architecture

### 1.1 Topology

```
USER QUERY
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                              │
│  • Receives user query                                       │
│  • Routes to Agent 1                                         │
│  • Passes Agent 1 output → Agent 2                          │
│  • Passes Agent 1+2 outputs → Agent 3                       │
│  • Passes Agent 1+2+3 outputs → Agent 4                     │
│  • Returns Agent 4 final report to user                      │
└─────────────────────────────────────────────────────────────┘
    │         │         │         │
    ▼         ▼         ▼         ▼
 Agent 1   Agent 2   Agent 3   Agent 4
 (M5)      (P2)      (P3+P4)   (NEW)
```

### 1.2 Execution Model

**Sequential pipeline with data dependencies.** Agents 1-3 execute in sequence because each depends on the previous agent's output. Agent 1 could theoretically run in parallel with Agent 2 if Agent 2 only uses technology + capacity from the original query, but the reference project comparison in Agent 2 benefits from Agent 1's project list.

```
Orchestrator:
  1. Agent1_output = Agent1.run(query)
  2. Agent2_output = Agent2.run(query + Agent1_output)
  3. Agent3_output = Agent3.run(query + Agent2_output)
  4. Agent4_output = Agent4.run(query + Agent1_output + Agent2_output + Agent3_output)
  5. Return Agent4_output.final_report
```

### 1.3 Why Sequential, Not Parallel?

- Agent 2's scale assessment references Agent 1's similar projects (e.g., "Normand'Hy at 200 MW is the closest reference")
- Agent 3's risk assessment uses Agent 2's technology verdict (e.g., "PEM TRL 8 → FOAK premium applies")
- Agent 4 needs all agent outputs for cross-dimension consistency check
- All agents run in <5 seconds total — parallelization would save <1 second at the cost of data dependency complexity

---

## 2. Message Protocol

### 2.1 Message Envelope

Every inter-agent message wraps content in a standard envelope:

```json
{
  "message_id": "MSG-YYYYMMDD-NNNNNN",
  "timestamp": "2026-06-05T14:30:00Z",
  "source_agent": "agent_1 | agent_2 | agent_3 | agent_4",
  "target_agent": "agent_2 | agent_3 | agent_4 | orchestrator",
  "message_type": "request | response | error | clarification",
  "query_id": "QRY-YYYYMMDD-NNNNNN",
  "payload": { }
}
```

### 2.2 Message Types

| Type | Direction | Purpose | Example |
|------|-----------|---------|---------|
| `request` | Orchestrator → Agent | "Run your assessment on this query + context" | Standard invocation |
| `response` | Agent → Orchestrator | "Here is my assessment output" | Standard return |
| `error` | Agent → Orchestrator | "I cannot complete this assessment because {reason}" | Missing technology card; empty knowledge base |
| `clarification` | Agent → Orchestrator | "I need {field} to complete assessment. Currently ambiguous: {values}." | Technology = "not_selected" → Agent 2 asks for clarification |

### 2.3 Error Handling Protocol

```
IF Agent responds with "error":
  Orchestrator logs error
  IF error is recoverable (e.g., technology not specified):
    Orchestrator retries with both technologies, noting ambiguity
  IF error is non-recoverable (e.g., knowledge base empty):
    Orchestrator returns graceful degradation to user with explicit gap statement
```

---

## 3. Agent 1 — Interface Specification

### 3.1 Input Contract

```json
{
  "query": {
    "country": "France",
    "industry": "Steel",
    "technology": "PEM",
    "capacity_mw": 100,
    "target_cod": 2029
  }
}
```

### 3.2 Output Contract

```json
{
  "normalized_query": {
    "country": "France", "country_iso": "FR",
    "industry_mapped_to_offtake": "steel",
    "technology": "PEM", "capacity_mw": 100, "target_cod": 2029,
    "scale_category": "medium_10-100mw",
    "region_classification": "europe"
  },
  "similar_projects": [
    {
      "rank": 1, "project_id": "GA-PR-001", "project_name": "Normand'Hy",
      "country": "France", "technology": "PEM", "capacity_mw": 200,
      "status": "under_construction", "offtake": "refinery",
      "similarity_score": 0.81, "tier": "highly_relevant",
      "rationale": "Same country (France), same technology (PEM), closest scale above query (200 MW). Refinery offtake shares industrial gas handling with steel."
    }
  ],
  "technology_cards_retrieved": ["TC-PEM-001"],
  "sources_collected": [
    { "source_id": "SRC-2022-003", "level": "A", "reliability": 5, "cited_by": ["GA-PR-001"] }
  ],
  "retrieval_metadata": {
    "total_projects_scored": 7,
    "projects_above_threshold": 6,
    "mean_relevance": 0.77,
    "degradations_applied": []
  }
}
```

### 3.3 Interface Guarantees

| Guarantee | Enforcement |
|-----------|------------|
| **Determinism** | Same query → same output (no ML models, no random sampling) |
| **Completeness** | All Gold Dataset projects scored; top 6 returned |
| **Graceful degradation** | Missing fields handled per documented degradation rules |
| **Source traceability** | Every project has at least 1 source in sources_collected |

---

## 4. Agent 2 — Interface Specification

### 4.1 Input Contract

```json
{
  "query": { "technology": "PEM", "capacity_mw": 100, "industry": "Steel", "target_cod": 2029 },
  "agent_1_output": {
    "similar_projects": [  ],
    "technology_cards_retrieved": ["TC-PEM-001"]
  }
}
```

### 4.2 Output Contract

```json
{
  "technology_verdict": {
    "technology_name": "PEM Electrolysis — Industrial Green Hydrogen Production",
    "technology_id": "TC-PEM-001",
    "trl": 8, "trl_rationale": "Commercially deployed at >100 MW scale. Normand'Hy 200 MW under construction.",
    "commercial_maturity": "early_commercial",
    "scale_status": "within_proven_range",
    "scale_detail": "100 MW query is within proven PEM range (max 200 MW under construction, 260 MW planned).",
    "is_foak_for_scale": false,
    "is_foak_for_application": true,
    "foak_rationale": "No PEM plant has supplied a DRI steel furnace. This is a first-of-a-kind application."
  },
  "application_assessment": {
    "industry": "steel",
    "suitability": "high",
    "rationale": "Green steel via H₂-DRI requires high-purity H₂ at scale. PEM's pressurized output (30 bar) reduces compression energy for DRI shaft furnace (10-20 bar).",
    "suitability_source": "TC-PEM-001 §applications.suitability_per_application[steel]",
    "reference_projects_for_application": ["GA-PR-005"]
  },
  "performance_relevant": {
    "output_pressure_bar": 30, "relevance": "DRI requires 10-20 bar. PEM 30 bar outlet eliminates first compression stage.",
    "hydrogen_purity_percent": 99.99, "relevance": "DRI purity requirements met. No additional purification needed.",
    "dynamic_response": "10%/s ramp, 5% min load", "relevance": "Less critical for baseload steel operation."
  },
  "key_advantages": ["Pressurized output matches DRI pressure requirement", "High purity eliminates purification CAPEX"],
  "key_limitations": ["No operational PEM→DRI reference exists — application novelty risk", "Iridium supply at portfolio scale"],
  "technology_comparison_note": "Alkaline also rated HIGH for steel. Alkaline's lower CAPEX may be advantageous at >100 MW but requires full compression train (atmospheric start).",
  "confidence": "HIGH (technology assessment) / MEDIUM (application assessment — no operational steel reference)"
}
```

### 4.3 Interface Guarantees

| Guarantee | Enforcement |
|-----------|------------|
| **Determinism** | Same inputs → same technology verdict |
| **Application must have suitability score** | If Technology Card has no suitability_per_application for this industry → explicitly flag "NOT ASSESSED" |
| **Scale must be compared to proven range** | Always report whether query scale is within/at frontier/beyond proven deployment |

---

## 5. Agent 3 — Interface Specification

### 5.1 Input Contract

```json
{
  "query": { "technology": "PEM", "capacity_mw": 100, "industry": "Steel", "target_cod": 2029, "country": "France" },
  "agent_2_output": {
    "technology_verdict": { "is_foak_for_scale": false, "is_foak_for_application": true, "scale_status": "within_proven_range" }
  }
}
```

### 5.2 Output Contract

```json
{
  "risk_assessment": {
    "risks_by_category": {
      "technical": [{ "risk_id": "RK-TEC-001", "risk_name": "...", "rpn": 24, "class": "medium" }],
      "supply_chain": [  ], "grid_energy": [  ], "regulatory": [  ],
      "financial": [  ], "construction": [  ], "operational": [  ], "environmental": [  ]
    },
    "top_8_risks": [{ "risk_id", "rpn", "class", "consequence_summary", "mitigation_summary", "project_evidence" } × 8],
    "risk_count": { "total": 28, "medium": 12, "low": 16 },
    "risk_evidence_quality": { "with_project_evidence": 6, "total_top_8": 8 }
  },
  "capex_assessment": {
    "breakdown": [{ "category": "01_electrolyzer_system", "eur_per_kw": 470, "eur_m": 47.0, "pct": 29, "confidence": "C" } × 8],
    "total": { "central_eur_per_kw": 1570, "central_eur_m": 157, "p10_eur_m": 120, "p90_eur_m": 210 },
    "aace_class": "class_4_feasibility",
    "weighted_confidence": 0.62,
    "key_drivers": [{ "driver": "PEM stack cost", "impact_eur_m": "±16", "why": "..." } × 3]
  },
  "lcoh_assessment": {
    "central_eur_per_kg": 4.78,
    "range": { "p10": 3.10, "p90": 6.90 },
    "decomposition": [{ "component": "Electricity", "eur_per_kg": 2.20, "pct": 46 }],
    "tornado": [{ "driver": "Electricity price", "impact": "±0.83/kg" } × 5],
    "dominant_driver": "electricity_price",
    "data_quality_note": "LCOH uses Technology Card OPEX proxies (Class C). OPEX Library not yet populated. Treat as CLASS D LCOH estimate."
  },
  "confidence": "MEDIUM"
}
```

### 5.3 Interface Guarantees

| Guarantee | Enforcement |
|-----------|------------|
| **CAPEX always presented as range** | `total` object must contain `p10_eur_m` and `p90_eur_m` |
| **LCOH always decomposed** | `lcoh_assessment.decomposition` must show component contributions |
| **No false precision** | All monetary values rounded to nearest €M or €0.05/kg |
| **OPEX/LCOH quality flagged** | If OPEX Library not populated, `data_quality_note` must state this |

---

## 6. Agent 4 — Interface Specification

### 6.1 Input Contract

```json
{
  "query": { },
  "agent_1_output": { },
  "agent_2_output": { },
  "agent_3_output": { }
}
```

### 6.2 Output Contract — Gate Review Report

```json
{
  "gate_review": {
    "gate": "PRE-FEASIBILITY GATE 1",
    "overall_assessment": "PROCEED WITH CAUTION",
    "dimension_scores": {
      "project_references": { "quality": "GOOD", "confidence": 0.64 },
      "technology": { "quality": "GOOD", "confidence": 0.68 },
      "risk": { "quality": "ADEQUATE", "confidence": 0.58 },
      "economics": { "quality": "ADEQUATE", "confidence": 0.52 }
    },
    "approved_for_next_phase": false,
    "conditions_for_approval": ["Resolve steel offtake application risk", "Obtain OEM indicative stack quotation"],
    "critical_gaps": ["No steel-offtake PEM reference", "OPEX Library not populated"],
    "consistency_issues": []
  },
  "final_report": { },
  "report_metadata": { }
}
```

---

## 7. Data Object Library — Shared Across Agents

| Object | Defined By | Consumed By | Schema Reference |
|--------|-----------|------------|-----------------|
| `normalized_query` | Agent 1 | All agents | §3.2 |
| `similar_projects[]` | Agent 1 | Agent 2, Agent 4 | §3.2 |
| `technology_verdict` | Agent 2 | Agent 3, Agent 4 | §4.2 |
| `risk_assessment` (subset) | Agent 3 | Agent 4 | §5.2 |
| `capex_assessment` | Agent 3 | Agent 4 | §5.2 |
| `lcoh_assessment` | Agent 3 | Agent 4 | §5.2 |
| `gate_review` | Agent 4 | Orchestrator → User | §6.2 |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect | Agent interface specification |
