# Risk Agent Requirements — Future Agent Specification v1.0

**Document:** Risk Agent Functional & Technical Requirements
**Date:** 2026-06-05
**Author:** Senior Project Risk Manager & AI Solution Architect
**Target Agent:** RiskAgent (M7 in Copilot roadmap)
**Dependencies:** Risk Library (populated), Gold Dataset (GA-PR-001+), Technology Cards (TC-PEM-001, TC-ALK-001), Retrieval Agent (M5)

---

## Table of Contents

1. [Agent Identity & Boundaries](#1-agent-identity--boundaries)
2. [Core Capabilities](#2-core-capabilities)
3. [Input Schema](#3-input-schema)
4. [Reasoning Workflows](#4-reasoning-workflows)
5. [Output Specification](#5-output-specification)
6. [Knowledge Base Integration Points](#6-knowledge-base-integration-points)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Test Scenarios](#8-test-scenarios)

---

## 1. Agent Identity & Boundaries

### 1.1 Agent Definition

The **Risk Agent** is a knowledge retrieval and analysis agent that identifies, assesses, and contextualizes risks for green hydrogen projects at any phase from pre-feasibility through early operations. It operates as an **advisor** to the Project Manager, not a decision-maker.

### 1.2 What the Risk Agent DOES

| Capability | Description |
|-----------|-------------|
| ✅ Identify relevant risks | Query the Risk Library + Technology Cards + project evidence to find risks applicable to a specific project profile |
| ✅ Assess risk significance | Apply the scoring methodology (P×I×D) to contextualize risk severity |
| ✅ Explain consequences | Articulate schedule, cost, performance, safety, and regulatory consequences in project-relevant terms |
| ✅ Propose mitigation | Retrieve documented mitigation strategies, preventive/corrective actions, and monitoring indicators |
| ✅ Cite evidence | Link every risk to reference projects where it materialized, with source traceability |
| ✅ Compare risk profiles | Contrast risk profiles for PEM vs Alkaline choices at a given scale and application |
| ✅ Monitor triggers | Given project data, check whether any risk trigger events are active |
| ✅ Prioritize | Rank risks by RPN for management attention |

### 1.3 What the Risk Agent DOES NOT Do

| Non-Capability | Rationale |
|---------------|-----------|
| ❌ Make final risk acceptance decisions | Belongs to Project Manager / Steering Committee |
| ❌ Override Project Manager risk judgment | The agent advises; the human decides |
| ❌ Quantify financial impact with precision | General ranges (Low/Medium/High/Critical); precise quantification requires project-specific financial models |
| ❌ Design novel mitigation strategies | Retrieves and contextualizes documented mitigations; does not invent new engineering solutions |
| ❌ Predict black swan events | Limited to risks documented in the Risk Library and evidence base |
| ❌ Replace formal risk workshops | Supplements and informs workshops; does not replace SME judgment |
| ❌ Assign risk owners | Suggests typical ownership (e.g., "EPC Contractor" for construction risks); final assignment is PM's responsibility |

### 1.4 Agent Persona

The Risk Agent behaves like a **Senior Risk Manager** who:
- Systematically identifies what could go wrong
- Quantifies severity using established methodology
- Explains WHY each risk matters in project terms
- Shows what others have done about it (reference project evidence)
- Never says "this project will fail" or "this project is safe"
- Presents evidence and lets the project team decide

---

## 2. Core Capabilities

### 2.1 Risk Identification

**Input:** Project profile (technology, scale, country, industry, phase, FOAK status)  
**Output:** Ranked list of applicable risks from the Risk Library  

**Process:**
```
1. FILTER Risk Library by applicability.technology_types matching project.technology
2. FILTER by applicability.project_scale matching project.capacity_mw scale band
3. FILTER by applicability.project_phases containing project.current_phase
4. FILTER by applicability.first_of_a_kind_only matching project.is_first_of_a_kind
5. ENRICH with Technology Card technical_risks[] for the selected technology
6. RANK by RPN (descending)
7. GROUP by risk_category for structured presentation
```

### 2.2 Risk Contextualization

For each identified risk, the agent must:
1. State the risk in plain language
2. Explain why it matters for THIS specific project (not generic)
3. Map consequences to project dimensions: schedule, cost, production, safety
4. Provide detectability context: "You can see this coming X months in advance by monitoring Y"
5. Reference any similar projects where this risk materialized

### 2.3 Mitigation Retrieval

For High and Critical risks (RPN ≥ 46), retrieve:
- Preventive actions (reduce probability)
- Corrective actions (reduce impact)
- Monitoring indicators (improve detectability)
- Estimated cost of mitigation (where documented)
- Risk owner recommendation

### 2.4 Cross-Technology Risk Comparison

When the project has not yet selected a technology (or is evaluating both):
- Identify risks that are PEM-specific vs Alkaline-specific
- Compare risk profiles quantitatively (RPN per category)
- Highlight risks where technology choice is the dominant factor

### 2.5 Trigger Event Monitoring (Future — M8+)

Given structured project data (contract dates, commodity prices, TSO milestones):
- Scan trigger_events[] against current project state
- Flag any risks with active or approaching trigger conditions
- Recommend review for flagged risks

---

## 3. Input Schema

### 3.1 Required Input

```json
{
  "project_profile": {
    "technology": "<PEM | Alkaline | not_selected>",
    "capacity_mw": "<number>",
    "country": "<ISO country name>",
    "industry": "<offtake enum: refinery | ammonia | steel | etc.>",
    "current_phase": "<pre_feasibility | feasibility | feed | construction | commissioning | operations>",
    "is_first_of_a_kind": "<boolean>",
    "project_type": "<greenfield | brownfield | expansion>"
  }
}
```

### 3.2 Optional Enrichment Input

```json
{
  "enrichment": {
    "target_cod": "<year>",
    "estimated_capex_eur": "<number>",
    "renewable_type": "<solar_pv | offshore_wind | etc.>",
    "grid_connection_status": "<secured | in_negotiation | not_started>",
    "offtake_secured": "<boolean>",
    "epc_contract_type": "<lump_sum_turnkey | epcm | etc.>"
  }
}
```

---

## 4. Reasoning Workflows

### 4.1 Workflow 1: Full Risk Assessment (Pre-Feasibility)

```
User: "<project_profile>"

Step 1 — IDENTIFY
  Query Risk Library: 20-40 risks matched by technology + scale + phase + FOAK
  Enrich with Technology Card: 5-10 technology-inherent risks per card
  Enrich with Gold Dataset: risks evidenced in similar projects

Step 2 — ASSESS
  For each risk: present probability, impact, detectability, RPN, risk class
  Flag any risks where P≥4 AND I≥4 (high-critical regardless of detectability)

Step 3 — CONTEXTUALIZE
  For each High/Critical risk: explain consequences specific to THIS project
  Reference similar projects where this risk materialized
  Note detectability: "You'll have X months warning by monitoring Y"

Step 4 — MITIGATE
  Retrieve documented preventive and corrective actions
  Suggest risk owner
  Estimate residual RPN after mitigation (if documented)

Step 5 — PRIORITIZE
  Sort by RPN descending
  Group by risk_class: Critical → High → Medium → Low
  Flag risks with no documented mitigation as "mitigation gap"

Step 6 — CITE
  For every risk: list evidence sources (Risk Library sources, Gold Dataset project references, 
  Technology Card technical_risks evidence)
```

### 4.2 Workflow 2: Technology Risk Comparison

```
User: "Compare PEM vs Alkaline risk profiles for <project_profile>"

Step 1 — RUN Workflow 1 for PEM → risk profile A
Step 2 — RUN Workflow 1 for Alkaline → risk profile B
Step 3 — COMPARE
  Side-by-side: RPN per category for each technology
  Highlight risks unique to each technology
  Highlight risks where RPN differs by ≥20 between technologies
Step 4 — SYNTHESIZE
  Technology risk profile summary: PEM total RPN vs Alkaline total RPN
  Key differentiators: where technology choice most impacts risk
  No recommendation — present evidence, let project team decide
```

### 4.3 Workflow 3: Phase Gate Risk Check

```
User: "Check risks for moving from FEED to Construction for <project_id>"

Step 1 — RETRIEVE project from Gold Dataset
Step 2 — FILTER risks for phase = "construction"
Step 3 — CHECK each risk's trigger_events against current project data
Step 4 — FLAG any risks with active triggers
Step 5 — REPORT readiness: "X of Y construction-phase risks have active mitigations in place.
  Z risks have active or approaching trigger conditions."
```

### 4.4 Workflow 4: Single Risk Deep-Dive

```
User: "Tell me everything about electrolyzer degradation risk for my 200 MW PEM project"

Step 1 — RETRIEVE risk record RK-TEC-001 from Risk Library
Step 2 — ENRICH with Technology Card TC-PEM-001 technical_risks[TCR-PEM-001]
Step 3 — RETRIEVE evidence from Gold Dataset (GA-PR-001, GA-PR-006, GA-PR-008)
Step 4 — PRESENT full risk record: description → assessment → consequences → mitigation → evidence → sources
Step 5 — CONTEXTUALIZE for 200 MW: scale the cost impact accordingly
```

---

## 5. Output Specification

### 5.1 Output Format

```json
{
  "risk_assessment": {
    "project_summary": "<technology, scale, phase, FOAK status>",
    "assessment_date": "<ISO 8601>",
    "total_risks_identified": "<number>",
    "risk_class_summary": {
      "critical": "<count>",
      "high": "<count>",
      "medium": "<count>",
      "low": "<count>"
    },
    "top_risks": [
      {
        "rank": 1,
        "risk_id": "RK-XXX-NNN",
        "risk_name": "...",
        "rpn": "<number>",
        "risk_class": "critical",
        "why_top": "1-2 sentence explanation"
      }
    ],
    "risks_by_category": {
      "technical": {
        "risks": [
          {
            "risk_id": "RK-TEC-001",
            "risk_name": "...",
            "probability": 3,
            "impact": 4,
            "detectability": 2,
            "rpn": 24,
            "risk_class": "medium",
            "consequences_summary": "...",
            "mitigation_summary": "...",
            "evidence_projects": ["GA-PR-001", "GA-PR-008"],
            "sources_count": 3
          }
        ],
        "category_rpn_total": 85,
        "category_risk_count": 5
      }
    },
    "mitigation_gaps": [
      "RK-FIN-003: No documented mitigation actions. Risk class: High.",
      "RK-SCP-002: Preventive actions documented, no corrective actions."
    ],
    "evidence_summary": {
      "risk_library_sources": "<number>",
      "gold_dataset_references": "<number>",
      "technology_card_references": "<number>"
    }
  }
}
```

### 5.2 Human-Readable Summary

In addition to the structured JSON, the agent produces a natural-language summary:

```
RISK ASSESSMENT SUMMARY
Project: 100 MW PEM electrolysis, steel offtake, France, pre-feasibility

IDENTIFIED: 28 risks across 8 categories
  🔴 Critical: 2 risks | 🟠 High: 6 | 🟡 Medium: 14 | 🟢 Low: 6

TOP 3 RISKS:
1. [RK-FIN-003] Offtake Agreement Default (RPN 72, HIGH)
   If the steel offtaker delays or cancels its H₂ purchase agreement, 
   the project has no alternative offtake at comparable price.
   Detected 12-18 months before impact through offtaker financial monitoring.
   Mitigation: Diversify offtake portfolio; include minimum take-or-pay clauses.

2. [RK-TEC-001] PEM Stack Degradation Exceeding Warranty (RPN 60, HIGH)
   17% of reference PEM projects >20 MW experienced this. EIS monitoring 
   provides 12-18 month early warning. Mitigation: N+1 redundancy + sinking fund.

3. [RK-GRD-001] Grid Connection Delay (RPN 48, HIGH)
   >40% of European renewable projects experienced grid delays. Monthly TSO 
   reporting provides 6-12 month detection window. Mitigation: Early TSO engagement + 
   interim power solution (mobile substation).

MITIGATION GAPS: 3 High/Critical risks lack documented corrective actions.
See detailed report for full risk register.
```

---

## 6. Knowledge Base Integration Points

### 6.1 Cross-Entity Query Map

| Risk Agent Query | Knowledge Source | Fields Accessed |
|-----------------|-----------------|-----------------|
| "Find all PEM risks" | Risk Library | `risk_id`, `risk_name`, `applicability.technology_types` |
| "What technology risks exist for PEM?" | Technology Card (TC-PEM-001) | `technical_risks[]` block |
| "Which projects had stack degradation?" | Gold Dataset | `status_detail`, `evidence` in risk records |
| "What's the cost of this mitigation?" | Risk Library + Cost Library | `mitigation.preventive_actions[].cost_eur`, `cost_library` entries |
| "How does this risk affect schedule?" | Risk Library | `consequences.schedule` |
| "What's the PEM vs Alkaline risk profile?" | Risk Library + Technology Cards | All risk records, filtered by technology |

### 6.2 Retrieval Strategy

The Risk Agent uses the Retrieval Agent (M5) for initial risk discovery, then performs structured enrichment:

```
RetrievalAgent.query(risk_category, technology, phase) → risk_ids[]
→ RiskAgent.enrich(risk_ids[]) → full risk records
→ RiskAgent.enrich(technology_card) → technology-inherent risks
→ RiskAgent.enrich(gold_dataset) → project evidence
→ RiskAgent.assess() → scored + contextualized output
```

---

## 7. Non-Functional Requirements

| Requirement | Specification |
|------------|--------------|
| **Response time** | <5 seconds for full risk assessment (28 risks across 8 categories) |
| **Traceability** | 100% of factual claims linked to a source (Risk Library source, Gold Dataset project, or Technology Card) |
| **Explainability** | Every risk score includes rationale citing evidence. Every ranking explains why. |
| **Determinism** | Same input → same output. No probabilistic variation in risk scoring. |
| **Extensibility** | New risk categories/subcategories can be added to taxonomy without code changes |
| **Graceful degradation** | If Risk Library is empty: retrieve only Technology Card risks + Gold Dataset evidence. If Technology Card also missing: flag data gap. If all sources missing: return "Insufficient knowledge base to perform risk assessment." |
| **Auditability** | Full audit trail: which risks were considered, which were filtered out and why, which sources were consulted |

---

## 8. Test Scenarios

### 8.1 Scenario 1: Pre-Feasibility PEM Project

```
Input: 100 MW PEM, France, Steel, Pre-Feasibility, FOAK=false
Expected: 20-30 risks; top risks in Financial (offtake), Grid, Technical
Key check: RiskLibrary returns PEM-specific risks. No Alkaline-specific risks.
```

### 8.2 Scenario 2: Technology Comparison

```
Input: Compare PEM vs Alkaline for 500 MW, Spain, Ammonia, Feasibility
Expected: Side-by-side RPN comparison. PEM risks: iridium, OEM concentration. 
Alkaline risks: dynamic response, atmospheric compression. 
Alkaline total RPV likely lower (mature tech, lower supply chain risk).
```

### 8.3 Scenario 3: Phase Gate Check

```
Input: Move GA-PR-004 (HGHH) from Construction to Commissioning
Expected: Retrieve risks active in commissioning phase. Check trigger_events 
against HGHH project data. Flag commissioning-specific risks (module integration, 
H₂ purity testing, grid synchronization).
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Project Risk Manager & AI Solution Architect | Initial Risk Agent requirements specification |

---

*The Risk Agent is designed as an advisor, not a decision-maker. It identifies, assesses, contextualizes, and prioritizes risks using the Risk Library, Technology Cards, and Gold Dataset evidence. Every risk is scored, every claim is sourced, and every output is structured for both machine consumption (future Feasibility Agent) and human review (Project Manager dashboard).*
