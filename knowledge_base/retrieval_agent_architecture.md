# Knowledge Retrieval Agent — Architecture v1.0

**Document:** Retrieval Agent Architecture
**Date:** 2026-06-05
**Author:** Senior AI Solution Architect
**Milestone:** M5 — Knowledge Retrieval Agent Prototype
**Agent Type:** Retrieval-only (no decision, no scoring, no recommendation)

---

## Table of Contents

1. [Agent Identity & Boundaries](#1-agent-identity--boundaries)
2. [Architecture Overview](#2-architecture-overview)
3. [Input Processing](#3-input-processing)
4. [Query Interpretation & Semantic Expansion](#4-query-interpretation--semantic-expansion)
5. [Retrieval Pipelines](#5-retrieval-pipelines)
6. [Similarity Matching Engine](#6-similarity-matching-engine)
7. [Ranking Logic](#7-ranking-logic)
8. [Source Aggregation](#8-source-aggregation)
9. [Output Generation](#9-output-generation)
10. [Retrieval Quality Metrics](#10-retrieval-quality-metrics)

---

## 1. Agent Identity & Boundaries

### 1.1 Agent Definition

The **Knowledge Retrieval Agent** is the first operational agent of the Green Hydrogen Project Feasibility Copilot platform. It is a purely informational agent — it finds, organizes, ranks, and presents relevant knowledge. It does not judge, decide, or recommend.

### 1.2 What the Agent DOES

| Capability | Description |
|-----------|-------------|
| ✅ Retrieve similar projects | Find and rank projects matching user-specified criteria |
| ✅ Retrieve relevant technology knowledge | Pull the correct Technology Card for the specified technology |
| ✅ Retrieve relevant risks | Surface risks documented in reference projects and Technology Cards |
| ✅ Retrieve supporting sources | Aggregate source documents backing all retrieved information |
| ✅ Explain selection rationale | For every retrieved item, state WHY it was retrieved |
| ✅ Rank by relevance | Order results by computed similarity |
| ✅ Handle partial queries | Gracefully degrade when some query fields are missing |

### 1.3 What the Agent DOES NOT Do

| Non-Capability | Why Not |
|---------------|---------|
| ❌ Judge feasibility | Belongs to Feasibility Agent (M7+) |
| ❌ Estimate CAPEX | Belongs to Cost Estimation Agent (M6+) |
| ❌ Calculate scores | Belongs to Feasibility Agent |
| ❌ Make recommendations | Belongs to Recommendation Agent (future) |
| ❌ Invent missing information | Violates source traceability principle |
| ❌ Compare technologies qualitatively | Presents Technology Card data; does not argue for one technology |
| ❌ Predict project success/failure | Predictive capability is not in scope |

### 1.4 Agent Persona

The agent behaves like a **junior engineering consultant** who:
- Finds relevant information quickly
- Explains why each piece of information is relevant
- Cites sources for every claim
- Does not offer opinions or recommendations
- Presents what exists, not what should exist

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INPUT                                    │
│  { country, industry, technology, capacity_mw, target_cod }        │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INPUT PROCESSOR                                   │
│  • Validate fields against controlled vocabularies                  │
│  • Normalize values (country → ISO name, industry → offtake enum)  │
│  • Flag missing fields for graceful degradation                    │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  QUERY INTERPRETER                                   │
│  • Map query dimensions to knowledge base fields                    │
│  • Expand semantically (industry="chemical" → offtake=[ammonia,     │
│    methanol, refinery])                                              │
│  • Generate explicit & implicit filters                             │
└───────┬───────────────────┬───────────────────┬─────────────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   PIPELINE   │   │   PIPELINE   │   │   PIPELINE   │
│      #1      │   │      #2      │   │      #3      │
│  PROJECT     │   │  TECHNOLOGY  │   │    RISK      │
│  REFERENCES  │   │    CARDS     │   │   LIBRARY    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │  Metadata filter │  Exact match     │  Metadata filter
       │  + similarity    │  on technology   │  on technology
       │  scoring         │  type            │  + applicability
       │                  │                  │
       ▼                  ▼                  ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  RANKED      │   │  SELECTED    │   │  FILTERED    │
│  PROJECTS    │   │  TECH CARD   │   │  RISKS       │
│  (Top 6)     │   │  (1 of 2)    │   │  (All        │
│              │   │              │   │   applicable) │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SOURCE AGGREGATOR                                 │
│  • Collect all source references from retrieved items               │
│  • De-duplicate by source_id                                        │
│  • Group by source_quality_level                                    │
│  • Preserve source_reliability_score                                │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OUTPUT GENERATOR                                  │
│  • Executive Query Summary                                          │
│  • Ranked Similar Projects (with selection rationale)               │
│  • Relevant Technology Knowledge                                    │
│  • Relevant Risks                                                   │
│  • Source Index                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Pipeline Execution Model

All three retrieval pipelines execute concurrently since they are independent:

```
Pipeline 1 (Projects) →  Metadata filter → Similarity score → Sort → Top-6
Pipeline 2 (Technology) → Exact match on technology.type → Retrieve card
Pipeline 3 (Risks) → Filter by technology applicability → Retrieve
```

The Source Aggregator waits for all three pipelines, then collects and de-duplicates sources.

---

## 3. Input Processing

### 3.1 Input Schema

```json
{
  "country": "<string — ISO country name>",
  "industry": "<string — mapped to offtake enum>",
  "technology": "<string — PEM | Alkaline | unknown>",
  "capacity_mw": "<number — plant capacity in MW>",
  "target_cod": "<number — target year of commissioning>"
}
```

### 3.2 Validation Rules

| Field | Rule | Error Handling |
|-------|------|---------------|
| `country` | Must match an ISO country name present in the Gold Dataset OR be null | If unknown country: note "No projects found in {country}; expanding to European region" |
| `industry` | Must map to a valid `offtake.primary_application` enum value | See §4.2 Industry-to-Offtake Mapping. If unmappable: flag as "Industry '{value}' not recognized; retrieval may be incomplete" |
| `technology` | Must be `PEM`, `Alkaline`, `PEM+Alkaline`, or `null`/`"unknown"` | If unknown: retrieve both technology cards, note "Technology not specified — both PEM and Alkaline knowledge retrieved" |
| `capacity_mw` | Must be a positive number | If null: capacity similarity not computed; projects ranked on other dimensions only |
| `target_cod` | Must be a 4-digit year ≥ 2024 | If null: not used for filtering; used only for technology cost projection if present |

### 3.3 Normalization

| Field | Input Example | Normalized Value |
|-------|--------------|-----------------|
| `country` | "FR", "france", "France" | "France" |
| `industry` | "steel manufacturing", "green steel" | "steel" |
| `technology` | "PEM electrolysis", "proton exchange" | "PEM" |
| `capacity_mw` | "100MW", "0.1 GW" | 100 |

---

## 4. Query Interpretation & Semantic Expansion

### 4.1 Dimension-to-Field Mapping

| Query Dimension | Gold Dataset Field(s) | Technology Card Field(s) |
|----------------|----------------------|--------------------------|
| `country` | `location.country` (exact) | — |
| `industry` | `offtake.primary_application`, `offtake.secondary_applications` | `applications.suitability_per_application[]` |
| `technology` | `technology.type` (exact) | `technology_id`, `technology_type` (exact) |
| `capacity_mw` | `capacity.electrolyzer_capacity_mw` (range) | `scalability.typical_plant_size_range_mw` |
| `target_cod` | `timeline.commissioning_date` (proximity) | — |

### 4.2 Industry-to-Offtake Mapping

The `industry` field in the user query uses natural language. It must be mapped to the controlled vocabulary of `offtake.primary_application`.

| User Input (Industry) | Mapped offtake enum(s) | Match Strategy |
|----------------------|----------------------|----------------|
| "Steel" | `steel` | Exact primary match |
| "Refinery" | `refinery` | Exact primary match |
| "Ammonia" / "Fertilizer" | `ammonia` | Exact primary match |
| "Methanol" | `methanol` | Exact primary match |
| "Mobility" / "Transport" | `mobility` | Exact primary match |
| "Chemicals" / "Chemical Industry" | `ammonia`, `methanol`, `refinery` | Multi-match (any of these) |
| "Industrial Hydrogen" / "Industrial Supply" | `industrial_heat`, `refinery`, `steel`, `ammonia` | Broad match (any industrial offtake) |
| "Power Generation" / "Grid" | `grid_injection` | Exact primary match |
| "Export" | `export` | Exact primary match |

### 4.3 Implicit Filters

| Condition | Implicit Action |
|-----------|----------------|
| `target_cod` ≤ 2027 | Boost `operational` and `under_construction` projects (they represent achievable precedents) |
| `target_cod` ≥ 2030 | Include `planned` projects (represent the future project landscape) |
| `capacity_mw` > 500 | Include HyDeal España (GA-PR-005) despite it being planned — it's the only giga-scale reference |
| `technology` = "PEM" | Exclude Alkaline-only projects from project matching; retrieve PEM Technology Card only |
| `technology` = "Alkaline" | Exclude PEM-only projects from project matching; retrieve Alkaline Technology Card only |
| `technology` = unknown | Retrieve both technology cards; match projects of both types |

---

## 5. Retrieval Pipelines

### 5.1 Pipeline #1: Project Reference Retrieval

**Goal:** Find the 6 most similar projects from the Gold Dataset.

**Process:**
```
1. FILTER: Apply technology filter (if specified)
           Exclude projects with non-matching technology.type
2. SCORE:   For each remaining project, compute weighted similarity score
3. SORT:    Sort by similarity score descending
4. SELECT:  Take top 6 projects
5. EXPLAIN: For each selected project, generate selection rationale
```

### 5.2 Pipeline #2: Technology Knowledge Retrieval

**Goal:** Retrieve the correct Technology Card and relevant sections.

**Process:**
```
1. MATCH:   Exact match on technology.type → TC-{TYPE}-001
2. SELECT:  Retrieve sections relevant to the query:
           • maturity (always)
           • deployment_evidence (always)
           • performance (always)
           • applications.suitability_per_application[query.industry] (if industry specified)
           • cost_profile (always)
           • technical_risks (always)
           • infrastructure (if brownfield/greenfield context available)
3. EXPAND:  If query.technology is unknown, retrieve BOTH cards
```

### 5.3 Pipeline #3: Risk Retrieval

**Goal:** Retrieve technology-inherent risks and reference project evidence.

**Process:**
```
1. SOURCE A: Technology Card → technical_risks[] block for the specified technology
2. SOURCE B: Project References → status_detail field for similar projects (may contain incident descriptions)
3. SOURCE C: If Risk Library entries exist → filter by technology applicability
4. DEDUPLICATE: Remove duplicate risks (same risk_name from multiple sources)
5. PRESENT: Group by risk_category
```

---

## 6. Similarity Matching Engine

*(See project_matching_methodology.md for the complete specification. This section summarizes.)*

### 6.1 Dimension Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Technology match | 30% | Most critical — different technologies have different cost structures, performance, risks |
| Industry (offtake) match | 25% | Second most critical — a refinery project learning from ammonia projects is limited |
| Capacity similarity | 25% | Important — scale economics differ dramatically between 20 MW and 200 MW |
| Country/region match | 15% | Useful — regulatory, supply chain, workforce contexts vary by country |
| Project maturity | 5% | Minor tiebreaker — operational projects provide more lessons than planned ones |

### 6.2 Scoring Functions

| Dimension | Scoring Function |
|-----------|-----------------|
| **Technology** | `1.0` if exact match; `0.5` if PEM+Alkaline matches either; `0.0` if mismatch |
| **Industry** | `1.0` if exact primary off_take match; `0.7` if secondary match; `0.3` if related category; `0.0` if unrelated |
| **Capacity** | `1.0 − 0.5 × |log₁₀(query_MW / project_MW)|` clamped to `[0, 1]` |
| **Country** | `1.0` same country; `0.6` neighboring/shared border; `0.4` same sub-region; `0.2` same continent; `0.0` different continent |
| **Maturity** | `1.0` under_construction; `0.8` operational; `0.5` planned; `0.3` decommissioned |

### 6.3 Final Score

```
Similarity = 0.30 × TechScore
           + 0.25 × IndustryScore
           + 0.25 × CapacityScore
           + 0.15 × CountryScore
           + 0.05 × MaturityScore
```

Range: [0.0, 1.0]. Minimum threshold for inclusion: 0.30.

---

## 7. Ranking Logic

### 7.1 Ranking Tiers

| Tier | Score Range | Label | Meaning |
|------|------------|-------|---------|
| Tier 1 | ≥ 0.70 | **Highly Relevant** | Strong match across most dimensions; directly comparable |
| Tier 2 | 0.50–0.69 | **Relevant** | Good match on key dimensions; relevant with caveats |
| Tier 3 | 0.30–0.49 | **Partially Relevant** | Shares some characteristics; useful but limited |

Projects scoring <0.30 are excluded.

### 7.2 Tie-Breaking

When two projects have identical scores (within 0.01):

1. **Data completeness** — prefer projects with higher `data_completeness_tier`
2. **Recency** — prefer projects with more recent `last_data_update`
3. **Source quality** — prefer projects with more Level A sources
4. **Project maturity** — prefer `operational` > `under_construction` > `planned`

### 7.3 Why Rank #1 vs #5

For each ranked project, the agent provides a natural-language explanation of why it ranks where it does. Example:

> *"Normand'Hy ranks #1 (score 0.82) because it exactly matches the technology (PEM), is in the same country (France), has a similar industrial application (refinery → steel shares industrial gas handling infrastructure), and at 200 MW is the closest scale reference above 100 MW."*

> *"Puertollano ranks #5 (score 0.48) because while it matches on technology (PEM) and country proximity (Spain borders France), its 20 MW scale is 5× smaller than the query, and its ammonia application differs from steel."*

---

## 8. Source Aggregation

### 8.1 Collection Strategy

Sources are collected from:
1. All retrieved project records (`sources[]` arrays)
2. The retrieved Technology Card (`sources[]` array)
3. Technology Card technical_risks (sources embedded in risk descriptions)

### 8.2 De-duplication

By `source_id`. If two retrieved items cite the same source (e.g., both Normand'Hy and the PEM Technology Card cite IEA GHR 2025), the source is listed once with a note: *"Cited by: Normand'Hy (GA-PR-001), PEM Technology Card (TC-PEM-001)"*.

### 8.3 Source Presentation

Sources are grouped:

| Group | Criteria | Display Label |
|-------|----------|---------------|
| **Primary Sources** | Level A, Score 4-5 | "Official Sources" |
| **Industry References** | Level B, Score 3-5 | "Authoritative Industry Sources" |
| **Supporting Sources** | Level C, Score 3-4 | "Professional Media Sources" |

---

## 9. Output Generation

### 9.1 Output Sections

The agent's output is a structured response with 5 sections:

#### Section 1: Executive Query Summary
- Restates the user's query in normalized form
- States what was retrieved and how many results
- Flags any query interpretation decisions (e.g., "Industry 'Chemical' was interpreted as ammonia + methanol + refinery")

#### Section 2: Similar Projects
For each of the top-6 projects:
- Project name (with Gold Dataset ID)
- Country, Capacity, Technology, Status
- Similarity score with tier label
- Reason selected (1-2 sentence explanation)

#### Section 3: Relevant Technology Knowledge
- Which Technology Card was retrieved and why
- Key technology facts relevant to this query (TRL, efficiency, scale proven, risks)
- Application suitability for the queried industry

#### Section 4: Relevant Risks
- Technology-inherent risks (from Technology Card)
- Project-evidenced risks (from similar projects' status_detail or linked risk entries)
- Grouped by risk category

#### Section 5: Sources
- Aggregated, de-duplicated source index
- Grouped by quality level
- Each source shows: title, author, date, confidence, and which items cited it

### 9.2 Traceability Requirement

Every factual statement in the output must be traceable to a source. The format is:

> *"PEM electrolysis has been deployed at ≥200 MW single-plant scale [Source: IEA GHR 2025, Level B, Score 5; Normand'Hy 200 MW, GA-PR-001]."*

---

## 10. Retrieval Quality Metrics

### 10.1 Metrics Tracked

| Metric | Definition | Target |
|--------|-----------|--------|
| **Precision@6** | Fraction of top-6 retrieved projects that are genuinely relevant (≥0.50 score) | ≥ 0.80 |
| **Recall@6** | Fraction of all relevant projects in the dataset that appear in top-6 | ≥ 0.60 |
| **MRR (Mean Reciprocal Rank)** | Average of 1/rank for the highest-ranked truly relevant project | ≥ 0.70 |
| **Mean relevance score** | Average similarity score of top-6 results | ≥ 0.55 |
| **Source traceability ratio** | Fraction of factual statements with source citations | 1.00 (mandatory) |
| **Query degradation handling** | Fraction of partial queries producing useful results (≥3 projects with score ≥0.30) | ≥ 0.90 |

### 10.2 Quality Monitoring

After each retrieval, log:
- Query parameters
- Top-6 project_ids and scores
- Technology Card retrieved
- Risk count
- Source count
- Whether all mandatory fields were present

This enables offline analysis of retrieval quality and identification of systematic weaknesses.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior AI Solution Architect | Initial Retrieval Agent Architecture |

---

*This architecture defines the first operational agent of the Copilot platform. It is intentionally narrow in scope — retrieval only — to establish a solid foundation before higher-level reasoning agents are built.*
