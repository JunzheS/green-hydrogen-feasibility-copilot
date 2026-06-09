# Preliminary Feasibility Agent — Architecture v1.0

**Document:** Agent Architecture
**Date:** 2026-06-05
**Author:** Senior Hydrogen Project Consultant, PMO Lead & AI Solution Architect
**Agent Type:** Knowledge Integration Agent — preliminary feasibility assessment
**Dependencies:** Retrieval Agent (M5), Technology Cards, Risk Library (M6B), Cost Library (M8A), Gold Dataset

---

## 1. Agent Identity & Boundaries

### 1.1 What This Agent IS

The Preliminary Feasibility Agent is the first **multi-source integration agent** of the Copilot platform. It orchestrates four knowledge domains — projects, technology, risks, costs — into a single structured report answering the question: **"What do we currently know about the feasibility of this project?"**

It is an **evidence aggregator and contextualizer**, not a decision-maker.

### 1.2 What the Agent DOES

| ✅ | Description |
|----|-------------|
| Retrieve similar reference projects and explain why they are relevant |
| Assess technology readiness and suitability for the proposed application |
| Identify the key risks and their severity |
| Estimate indicative CAPEX ranges with documented confidence |
| Aggregate and quality-score all supporting evidence |
| Identify what is NOT known (knowledge gaps) |
| Recommend next studies to address gaps |

### 1.3 What the Agent DOES NOT Do

| ❌ | Why Not |
|----|---------|
| Generate feasibility scores or ratings | Scoring methodology not yet defined (future M10) |
| Make Go / No-Go recommendations | Decision authority belongs to project governance |
| Estimate OPEX or LCOH | OPEX library not yet built (future M7C) |
| Assess offtake market economics | Market analysis module not yet in scope |
| Generate financial model outputs (IRR, NPV) | Requires project-specific financial modeling |
| Replace expert engineering judgment | Agent is an advisor, not an authority |

### 1.4 Agent Persona

The agent behaves like a **junior engineering consultant** assigned to a pre-feasibility study who:
- Searches the firm's knowledge base for relevant precedents
- Reads technology specifications and assesses fit
- Checks the risk register for applicable risks
- Pulls cost benchmarks and adjusts for scale
- Writes a structured report with findings, evidence, and gaps
- Never pretends to know something not in the knowledge base

---

## 2. Architecture Overview

```
                        USER INPUT
  { country, industry, technology, capacity_mw, target_cod }
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     QUERY NORMALIZER                                 │
│  • Map industry → offtake enum                                       │
│  • Normalize country → ISO name                                      │
│  • Validate technology → PEM / Alkaline                              │
│  • Flag missing fields for graceful degradation                     │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┬──────────────────┐
          ▼                 ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   PIPELINE   │  │   PIPELINE   │  │   PIPELINE   │  │   PIPELINE   │
│      1       │  │      2       │  │      3       │  │      4       │
│   PROJECT    │  │  TECHNOLOGY  │  │     RISK     │  │     COST     │
│   MATCHING   │  │  ASSESSMENT  │  │  ASSESSMENT  │  │  ASSESSMENT  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │                 │
       ▼                 ▼                 ▼                 ▼
  Top-6 similar     Technology Card    Top risks by       Scaled CAPEX
  projects with     with suitability   category +         range with
  relevance         scores and TRL     mitigation         confidence
  scores                               evidence
       │                 │                 │                 │
       └─────────────────┼─────────────────┼─────────────────┘
                         │                 │
                         ▼                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EVIDENCE AGGREGATOR                               │
│  • Collect all sources from all four pipelines                      │
│  • De-duplicate by source_id                                        │
│  • Classify by quality level (A/B/C/D)                              │
│  • Compute evidence quality score                                   │
│  • Identify knowledge gaps (missing data categories)                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    REPORT COMPOSER                                   │
│  §1 Executive Summary                                                │
│  §2 Similar Reference Projects                                       │
│  §3 Technology Assessment                                            │
│  §4 Key Risks                                                        │
│  §5 Indicative CAPEX Assessment                                      │
│  §6 Evidence Quality Assessment                                      │
│  §7 Knowledge Gaps                                                   │
│  §8 Recommended Next Studies                                         │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Pipeline Execution Model

All four knowledge pipelines execute in parallel:

| Pipeline | Source | Output | Duration |
|----------|--------|--------|----------|
| P1 — Project Matching | Retrieval Agent (M5) + Gold Dataset | Top-6 similar projects with relevance scores and selection rationale | ~1s |
| P2 — Technology Assessment | Technology Cards (TC-PEM-001 / TC-ALK-001) | TRL, maturity, suitability per application, performance specs, cost profile | ~0.5s |
| P3 — Risk Assessment | Risk Library (30 risks) + Technology Card risks | Top risks filtered by technology + phase + scale, with mitigation evidence | ~1s |
| P4 — Cost Assessment | Cost Library (30 records) + Scaling Methodology | CAPEX range by category with confidence classes | ~1s |

The Evidence Aggregator waits for all four pipelines, then collects, de-duplicates, and quality-scores all sources.

---

## 3. Pipeline Specifications

### 3.1 Pipeline P1 — Project Matching

**Input:** `{ technology, country, capacity_mw, industry }`
**Engine:** Retrieval Agent v1.0 (M5)
**Method:** 5-dimension weighted similarity scoring (technology 30%, industry 25%, capacity 25%, country 15%, maturity 5%)
**Output:** Top 6 projects ranked by relevance score with explanations

**Degradation handling:**
- If no projects match technology: retrieve both technologies with disclaimer
- If country not in dataset: expand to neighboring countries → continent
- If capacity >500 MW: include HyDeal España (GA-PR-005) regardless of score

### 3.2 Pipeline P2 — Technology Assessment

**Input:** `{ technology }`
**Source:** Technology Cards TC-PEM-001, TC-ALK-001
**Output sections:**
1. **Maturity:** TRL, commercial status, cumulative capacity, oldest operational plant
2. **Performance:** System efficiency, stack lifetime, degradation rate, dynamic response
3. **Scalability:** Typical plant size range, max plant known, scaling constraints
4. **Application Suitability:** Score for the queried industry with rationale
5. **Cost Profile:** Stack cost range, cost drivers, learning rate, 2030 projection
6. **Key Advantages & Limitations** for this project context

**If technology = "not_selected":** Retrieve BOTH cards. Present side-by-side comparison.

### 3.3 Pipeline P3 — Risk Assessment

**Input:** `{ technology, capacity_mw, industry, target_cod }`
**Source:** Risk Library (30 records) + Technology Card technical_risks[]

**Filtering logic:**
```
1. FILTER by applicability.technology_types matching query.technology
2. FILTER by applicability.project_scale matching query.capacity range
3. FILTER by applicability.project_phases relevant to query (pre-feasibility → operations)
4. RANK by RPN descending within each category
5. SELECT top 2 risks per category (8 categories × top 2 = up to 16 risks)
6. ENRICH with mitigation actions and project evidence
```

**Output:** Risks grouped by category, each with RPN, class, consequences summary, mitigation summary, and evidence from Gold Dataset projects.

### 3.4 Pipeline P4 — Cost Assessment

**Input:** `{ technology, capacity_mw, country, target_cod }`
**Source:** Cost Library (30 records) + cost_scaling_methodology.md

**Process:**
```
1. SELECT applicable cost records matching technology + nearest scale
2. SCALE each record to target capacity using per-category power law exponents
3. ADJUST for target year using learning curves (if COD ≥ 2028)
4. DISCOUNT for brownfield site if applicable (inferred from industry context)
5. AGGREGATE bottom-up by cost category
6. COMPUTE P10-P90 range
7. ASSIGN weighted confidence score
```

**Output:** CAPEX breakdown by 8 categories with €/kW, M€, % of total, confidence class per category, and aggregated total range.

---

## 4. Evidence Aggregator

### 4.1 Source Collection

Sources are collected from all four pipelines:
- P1: `sources[]` from all 6 retrieved project records
- P2: `sources[]` from the Technology Card(s)
- P3: `sources[]` from all retrieved risk records
- P4: `sources[]` from all used cost records

### 4.2 De-duplication

By `source_id`. The IEA GHR 2025 is cited by Technology Cards, multiple cost records, and multiple risk records — it appears once in the aggregated evidence with a note: "Cited by: TC-PEM-001, CS-ELC-001, CS-ELC-002, RK-TEC-001, RK-TEC-004"

### 4.3 Evidence Quality Scoring

```
Evidence Quality Score = Σ(Source_Level_Weight × Source_Reliability) / Total_Sources

Level Weights: A=1.0, B=0.8, C=0.5, D=0.2
```

| Score Range | Evidence Quality |
|------------|-----------------|
| ≥ 0.80 | EXCELLENT — Multiple Level A sources, high reliability |
| 0.60–0.79 | GOOD — Mix of Level A/B sources |
| 0.40–0.59 | ADEQUATE — Primarily Level B/C sources |
| < 0.40 | LIMITED — Heavily reliant on Level C/D sources |

### 4.4 Knowledge Gap Detection

The aggregator checks for:
1. **Missing project references:** No operational project of this technology at this scale
2. **Missing cost data:** No Class A or B cost data available
3. **Missing risk evidence:** Risks without Gold Dataset project links
4. **Extrapolation warnings:** Cost scaled >3× from reference; no reference at this scale
5. **Technology novelty:** TRL ≤7 or no deployment at queried scale
6. **Industry novelty:** No project in dataset with this offtake application

---

## 5. Report Composer

### 5.1 Report Structure

| Section | Content | Primary Pipeline |
|---------|---------|-----------------|
| §1 Executive Summary | 1-page overview: project profile, key findings, top risks, CAPEX range, evidence quality, critical gaps | All |
| §2 Similar Reference Projects | Top 6 projects ranked by relevance with scores, key data points, and selection rationale | P1 |
| §3 Technology Assessment | TRL, maturity, performance, suitability for the application, advantages/limitations | P2 |
| §4 Key Risks | Top risks by category with RPN, consequences, mitigations, project evidence | P3 |
| §5 Indicative CAPEX Assessment | Cost breakdown by category, scaled to project size, with confidence classes and range | P4 |
| §6 Evidence Quality Assessment | Source count by level, evidence quality score, most/least confident areas | Aggregator |
| §7 Knowledge Gaps | What is NOT known — missing data, extrapolation beyond evidence, industry novelty | Aggregator |
| §8 Recommended Next Studies | Prioritized actions to close knowledge gaps and advance to feasibility stage | Agent reasoning |

### 5.2 Traceability Requirement

Every factual statement in the report must be traceable to:
- A Gold Dataset project (GA-PR-NNN)
- A Technology Card section (TC-PEM-001 §X)
- A Risk Library record (RK-XXX-NNN)
- A Cost Library record (CS-XXX-NNN)
- A source document (SRC-YYYY-NNN)

The traceability format is inline: *"PEM electrolysis has been deployed at 200 MW single-plant scale [Source: Normand'Hy GA-PR-001; TC-PEM-001 §deployment_evidence]"*

---

## 6. Agent Boundaries — Explicit Limitations

The report shall include this disclaimer in §1:

> *"This is a Preliminary Feasibility Assessment based on the Copilot's current knowledge base (June 2026). It does NOT constitute a feasibility study, investment recommendation, or engineering decision. All CAPEX estimates are AACE Class 4 (±20-30%) or Class 5 (±30-50%). OPEX, LCOH, offtake economics, and regulatory analysis are not yet covered. This report identifies what is KNOWN and what is NOT KNOWN — it does not fill gaps with assumptions."*

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Hydrogen Project Consultant, PMO Lead & AI Solution Architect | Initial agent architecture |
