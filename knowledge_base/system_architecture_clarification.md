# System Architecture Clarification — Current State & Future Roadmap

**Document:** Architecture Transparency Report
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Purpose:** Clarify what IS built vs what IS designed vs what IS planned

---

## Executive Answer

**The current system is ARCHITECTURE A: a single integrated Preliminary Feasibility Agent with 4 internal reasoning pipelines.** The Retrieval Agent (M5) exists as a standalone service used by the integrated agent as a sub-component, not as a peer in a multi-agent system.

**The future system (designed but not yet built) is ARCHITECTURE B: a true multi-agent architecture** with 6 specialized agents orchestrated by a Feasibility Orchestrator.

---

## 1. Current Architecture — What IS Built (June 2026)

### 1.1 Single Integrated Agent with Internal Pipelines

```
                                USER INPUT
        { country, industry, technology, capacity_mw, target_cod }
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│            PRELIMINARY FEASIBILITY AGENT (M9) — SINGLE AGENT            │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      QUERY NORMALIZER                            │   │
│  │   Map industry → offtake enum | Normalize country | Validate     │   │
│  └───────────────────────────┬─────────────────────────────────────┘   │
│                              │                                         │
│     ┌────────────┬───────────┼───────────┬────────────┐               │
│     ▼            ▼           ▼           ▼            ▼               │
│  ┌──────┐   ┌──────┐    ┌──────┐    ┌──────┐    ┌──────────┐         │
│  │  P1  │   │  P2  │    │  P3  │    │  P4  │    │EVIDENCE  │         │
│  │PROJ. │   │TECH. │    │RISK  │    │COST  │    │AGGREGATOR│         │
│  │MATCH │   │ASSESS│    │ASSESS│    │ASSESS│    │          │         │
│  └──┬───┘   └──┬───┘    └──┬───┘    └──┬───┘    └────┬─────┘         │
│     │          │           │           │              │               │
│     │  calls   │           │           │              │               │
│     ▼          │           │           │              │               │
│  ┌──────────────────┐      │           │              │               │
│  │ RETRIEVAL AGENT  │      │           │              │               │
│  │ (M5 - standalone │      │           │              │               │
│  │  service)        │      │           │              │               │
│  └──────────────────┘      │           │              │               │
│     │          │           │           │              │               │
│     ▼          ▼           ▼           ▼              ▼               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      REPORT COMPOSER                             │   │
│  │   §1 Exec Summary | §2 Projects | §3 Technology | §4 Risks      │   │
│  │   §5 CAPEX | §6 Evidence | §7 Gaps | §8 Next Studies            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│              KNOWLEDGE BASE (all local files)                           │
│   Gold Dataset │ Technology Cards │ Risk Library │ Cost Library         │
│   (10 projects)│ (PEM + ALK)      │ (30 risks)   │ (30 records)         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 What Each Pipeline Does (All Inside ONE Agent)

| Pipeline | Function | Data Source | Status |
|----------|----------|------------|--------|
| **P1 — Project Matching** | Finds similar projects using 5-dimension weighted scoring | Gold Dataset (10 projects) | ✅ BUILT & VALIDATED |
| **P2 — Technology Assessment** | Retrieves TRL, performance, suitability for application | Technology Cards (TC-PEM-001, TC-ALK-001) | ✅ BUILT & VALIDATED |
| **P3 — Risk Assessment** | Identifies risks filtered by technology, scale, phase | Risk Library (30 risks) | ✅ BUILT & VALIDATED |
| **P4 — Cost Assessment** | Estimates CAPEX range with scaling + learning curves | Cost Library (30 records) | ✅ BUILT & VALIDATED |
| **Evidence Aggregator** | Collects, de-duplicates, quality-scores all sources | All pipelines | ✅ BUILT & VALIDATED |
| **Report Composer** | Generates 8-section structured report | All pipeline outputs | ✅ BUILT & VALIDATED |

### 1.3 The Retrieval Agent (M5) — Standalone but Subordinate

The Retrieval Agent (M5) was built FIRST as a standalone service. It performs project matching, technology card lookup, risk retrieval, and source aggregation independently. In the current architecture, the Preliminary Feasibility Agent calls the Retrieval Agent for **P1 (project matching)** but runs P2-P4 internally. The Retrieval Agent is a **sub-component**, not a peer agent.

---

## 2. What Is DESIGNED But NOT BUILT (Requirements Only)

These agent specifications exist as requirement documents but have NOT been implemented as separate agents:

| Agent | Requirements Doc | Designed Capabilities | Why Not Built Yet |
|-------|-----------------|----------------------|-------------------|
| **Risk Agent** | risk_agent_requirements.md (M6A) | Risk identification, FMEA scoring, mitigation retrieval, technology comparison, trigger monitoring | Risk Library population (M6B) took priority. Risk reasoning is currently handled by P3 pipeline inside Preliminary Agent. |
| **Cost Agent** | cost_agent_requirements.md (M7A) | CAPEX breakdown, cost driver analysis, scale adjustment, uncertainty quantification, technology cost comparison | Cost Library population (M8A) took priority. Cost reasoning is currently handled by P4 pipeline inside Preliminary Agent. |
| **LCOH Agent** | (M9A OPEX architecture) | LCOH calculation, sensitivity analysis, breakeven analysis | OPEX Library not yet populated. LCOH reasoning was just architected (M9A). |
| **Regulatory Agent** | (not yet designed) | Country-specific permitting pathways, RFNBO compliance | Regulatory knowledge base not yet built. Identified as CRITICAL gap in M9 gap analysis. |
| **Offtake/Market Agent** | (not yet designed) | Regional H₂ pricing, offtake agreement structures, carbon price scenarios | Market data not yet collected. Identified as CRITICAL gap in M9 gap analysis. |

---

## 3. Future Architecture — Planned Multi-Agent System

### 3.1 Target Architecture (M10 Full Feasibility Agent)

```
                                USER INPUT
        { country, industry, technology, capacity_mw, target_cod }
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                   FEASIBILITY ORCHESTRATOR (M10)                        │
│                   ┌─────────────────────────┐                           │
│                   │  Query Classifier       │                           │
│                   │  Task Decomposer        │                           │
│                   │  Evidence Integrator    │                           │
│                   │  Confidence Calibrator  │                           │
│                   │  Report Composer        │                           │
│                   └───────┬─────────────────┘                           │
│                           │                                             │
│     ┌─────────────────────┼─────────────────────────┐                   │
│     │                     │                         │                   │
│     ▼                     ▼                         ▼                   │
│ ┌─────────┐                                   ┌──────────┐             │
│ │ AGENT 1 │  KNOWLEDGE RETRIEVAL AGENT (M5)    │          │             │
│ │  BUILT  │  • Project similarity matching      │          │             │
│ │    ✅   │  • Technology card lookup           │ KNOWLEDGE │             │
│ │         │  • Source aggregation              │   BASE    │             │
│ └────┬────┘                                   │          │             │
│      │                                        │ Gold     │             │
│      ▼                                        │ Dataset  │             │
│ ┌─────────┐                                   │ Tech     │             │
│ │ AGENT 2 │  TECHNICAL ASSESSMENT AGENT        │ Cards    │             │
│ │  BUILT  │  • TRL & maturity evaluation       │ Risk     │             │
│ │  (IN P2) │  • Application suitability        │ Library  │             │
│ │    ✅   │  • Scale/deployment evidence       │ Cost     │             │
│ └────┬────┘                                   │ Library  │             │
│      │                                        │ OPEX     │             │
│      ▼                                        │ Library  │             │
│ ┌─────────┐  RISK & ECONOMIC ASSESSMENT AGENT  │ (future) │             │
│ │ AGENT 3 │  ┌─────────────────────────────┐   │ Reg. DB  │             │
│ │ DESIGNED│  │ RISK SUB-MODULE (M6A design)│   │ (future) │             │
│ │    ⚠️   │  │ • Risk filtering & ranking  │   │          │             │
│ │         │  │ • FMEA scoring (P×I×D)      │   └──────────┘             │
│ │         │  │ • Mitigation retrieval       │                           │
│ │         │  │ • Project evidence linking   │                           │
│ │         │  ├─────────────────────────────┤                           │
│ │         │  │ COST SUB-MODULE (M7A design)│                           │
│ │         │  │ • CAPEX breakdown            │                           │
│ │         │  │ • Scale & learning adjust.   │                           │
│ │         │  │ • Uncertainty quantification │                           │
│ │         │  ├─────────────────────────────┤                           │
│ │         │  │ LCOH SUB-MODULE (M9A design)│                           │
│ │         │  │ • OPEX aggregation           │                           │
│ │         │  │ • LCOH waterfall             │                           │
│ │         │  │ • Sensitivity tornado        │                           │
│ │         │  │ • Breakeven analysis         │                           │
│ │         │  └─────────────────────────────┘                           │
│ └────┬────┘                                                            │
│      │                                                                 │
│      ▼                                                                 │
│ ┌─────────┐  PROJECT MANAGER REVIEW AGENT                              │
│ │ AGENT 4 │  • Cross-dimension consistency check                       │
│ │ DESIGNED│  • Evidence quality gating                                 │
│ │    ⚠️   │  • Knowledge gap prioritization                            │
│ │         │  • Next-study recommendation engine                        │
│ │         │  • Report quality assurance                                │
│ └─────────┘                                                            │
│                                                                         │
│   FUTURE EXTENSIONS (post-M10):                                        │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                             │
│   │ AGENT 5  │  │ AGENT 6  │  │ AGENT 7  │                             │
│   │REGULATORY│  │ OFFTAKE/ │  │ FINANCIAL│                             │
│   │ ASSESSOR │  │  MARKET  │  │  MODELING│                             │
│   │ (M9B)    │  │ (M9C)    │  │ (future) │                             │
│   └──────────┘  └──────────┘  └──────────┘                             │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent Responsibility Matrix — Current vs Future

| Function | Current (M9) | Future (M10) |
|----------|-------------|-------------|
| **Project matching** | P1 pipeline inside Preliminary Agent, calls Retrieval Agent | Agent 1 — standalone Retrieval Agent |
| **Technology assessment** | P2 pipeline inside Preliminary Agent | Agent 2 — Technical Assessment Agent |
| **Risk identification & scoring** | P3 pipeline inside Preliminary Agent (simplified: top 2 per category) | Agent 3 Risk Sub-Module (full FMEA scoring, residual risk, monitoring indicators) |
| **CAPEX estimation** | P4 pipeline inside Preliminary Agent (simplified: central + range) | Agent 3 Cost Sub-Module (per-category scaling, learning curves, confidence-weighted aggregation) |
| **OPEX/LCOH estimation** | ❌ NOT YET BUILT | Agent 3 LCOH Sub-Module (waterfall decomposition, tornado sensitivity, breakeven analysis) |
| **Regulatory assessment** | ❌ NOT YET BUILT | Agent 5 — Regulatory Assessor |
| **Offtake/market assessment** | ❌ NOT YET BUILT | Agent 6 — Offtake/Market Agent |
| **Cross-dimension quality check** | Simple evidence aggregator (de-duplication + level counting) | Agent 4 — PM Review Agent (cross-dimension consistency, gap prioritization, QA) |
| **Report composition** | Report Composer inside Preliminary Agent | Orchestrator (aggregates all agent outputs into unified report) |

---

## 4. Key Architectural Insight — Why Not Multi-Agent Yet?

The transition from single-agent to multi-agent was deferred for two deliberate reasons:

### 4.1 Knowledge Base Had to Come First

A multi-agent system where each agent queries an empty knowledge base is useless. The build order was:
1. **Schema & architecture** (M1-M4, M6A, M7A, M9A) — design the containers
2. **Knowledge base population** (M4, M6B, M8A) — fill the containers with validated data
3. **Single-agent integration** (M9) — prove the data can support integrated reasoning
4. **Multi-agent decomposition** (M10) — split into specialized agents once reasoning patterns are validated

### 4.2 Reasoning Patterns Validated Before Decomposition

The P1-P4 pipelines inside the Preliminary Agent are **proto-agents** — they exercise the same reasoning logic that future standalone agents will use. By running them inside one agent first, we:
- Validated that the 5-dimension project matching works across 5 test cases
- Proved that risk filtering by technology + scale + phase produces correct results
- Confirmed that cost scaling with per-category exponents produces logically consistent estimates
- Demonstrated that technology cards support application suitability reasoning

Decomposing these pipelines into separate agents is now a **mechanical refactoring**, not an architectural risk — the reasoning patterns are proven.

---

## 5. Migration Path — Single Agent → Multi-Agent

```
M5: RETRIEVAL AGENT (standalone, built)
     │
     ▼
M9: PRELIMINARY FEASIBILITY AGENT (single integrated agent, built)
     │  P1 → calls Retrieval Agent
     │  P2 → Technology Assessment (proto-agent)
     │  P3 → Risk Assessment (proto-agent)
     │  P4 → Cost Assessment (proto-agent)
     │  Evidence Aggregator
     │  Report Composer
     │
     ▼
M10: FULL FEASIBILITY AGENT (multi-agent, planned)
     │
     ├─ Agent 1: Retrieval Agent (M5, promoted to peer)
     ├─ Agent 2: Technical Assessment Agent (P2 extracted, enhanced with OPEX)
     ├─ Agent 3: Risk & Economic Assessment Agent (P3+P4 extracted, enhanced with LCOH)
     ├─ Agent 4: PM Review Agent (NEW — cross-dimension QA)
     │
     └─ Future: Agent 5 (Regulatory), Agent 6 (Offtake), Agent 7 (Financial)
```

---

## 6. Current System — Honest Assessment

| Question | Honest Answer |
|----------|--------------|
| **Is this a multi-agent system?** | **No.** It is a single integrated agent with 4 internal reasoning pipelines. |
| **Does the Retrieval Agent run independently?** | **Partially.** It was built as a standalone agent (M5) and CAN run independently. In the current Preliminary Agent, it is called as a sub-component for project matching only. |
| **Do Risk Agent and Cost Agent exist as separate agents?** | **No.** Their requirements are documented but they have not been implemented as standalone agents. Their reasoning logic runs inside P3 and P4 pipelines of the single Preliminary Agent. |
| **When will it be multi-agent?** | **M10 (Full Feasibility Agent).** The migration is a mechanical refactoring of validated reasoning patterns into separate agent processes. |
| **What is the strongest part of the current architecture?** | **The knowledge base.** 129 files of validated, traceable, source-attributed data across projects, technology, risks, and costs. This is the platform's real asset — agents are consumers of this knowledge. |
| **What is the weakest part?** | **No true agent-to-agent communication.** The Preliminary Agent is a monolith. Agents don't negotiate, challenge each other's outputs, or escalate disagreements. |

---

## 7. Architecture Decision Record

| Decision | Rationale | Date |
|----------|----------|------|
| **Build Retrieval Agent first (M5)** | Needed a working retrieval engine before any reasoning agent could function | M5 |
| **Defer separate Risk/Cost/LCOH Agents** | Knowledge base population (M6B, M8A) was prerequisite. Design requirements documented for future implementation. | M6A, M7A, M9A |
| **Build Preliminary Feasibility Agent as single integrated agent (M9)** | Validate integrated reasoning across all 4 knowledge domains before decomposing into multi-agent. Proto-agents (P1-P4) exercise the same logic future agents will use. | M9 |
| **Plan multi-agent decomposition for M10** | Single-agent validated. Multi-agent refactoring is now low-risk. | 2026-06-05 |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect | Architecture clarification document |
