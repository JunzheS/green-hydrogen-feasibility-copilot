# Project Matching Methodology — Similarity Scoring Engine v1.0

**Document:** Project Similarity Matching Specification
**Date:** 2026-06-05
**Author:** Senior AI Solution Architect
**Dependency:** retrieval_agent_architecture.md
**Dataset:** Gold Dataset v1 (10 projects: GA-PR-001 through GA-PR-010)

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Dimension Weights & Rationale](#2-dimension-weights--rationale)
3. [Scoring Functions — Detailed Specification](#3-scoring-functions--detailed-specification)
4. [Composite Score Calculation](#4-composite-score-calculation)
5. [Worked Example](#5-worked-example)
6. [Full Dataset Scoring Reference](#6-full-dataset-scoring-reference)
7. [Edge Cases & Special Handling](#7-edge-cases--special-handling)
8. [Ranking Tier Definitions](#8-ranking-tier-definitions)

---

## 1. Design Philosophy

### 1.1 Principles

| Principle | Implementation |
|-----------|---------------|
| **Transparent** | Every score component is calculable by hand; no black-box ML models |
| **Explainable** | For every rank, a human-readable rationale is generated from the score components |
| **Deterministic** | Same query + same dataset = same results every time |
| **Graceful** | Handles missing query fields without breaking; degrades dimension by dimension |
| **Bounded** | All scores in [0, 1]; composite score in [0, 1]; minimum threshold 0.30 |

### 1.2 Why Weighted Sum and Not Vector Embeddings?

For a 10-project dataset, cosine similarity on text embeddings would produce unstable results — small wording differences would dominate true project similarity. A weighted sum on structured dimensions:

- Is transparent and auditable
- Works well for small datasets (10-100 projects)
- Produces explainable rankings
- Can be tuned per dimension as the dataset grows

Vector embedding similarity will be added as a supplementary dimension when the dataset exceeds 50 projects.

---

## 2. Dimension Weights & Rationale

| # | Dimension | Weight | Rationale |
|---|-----------|--------|-----------|
| 1 | **Technology match** | **30%** | Different electrolysis technologies have fundamentally different cost structures, supply chains, operating characteristics, and risk profiles. A PEM project learning from Alkaline projects gets limited value. |
| 2 | **Industry (offtake) match** | **25%** | The offtake application drives project design: a refinery H₂ project has different purity, pressure, and scale requirements than a mobility or ammonia project. Cross-industry learning is useful but secondary. |
| 3 | **Capacity similarity** | **25%** | Scale economics are non-linear. A 20 MW project and a 200 MW project face different engineering, procurement, and financing challenges. The logarithmic scoring function reflects that absolute MW difference matters less at larger scales. |
| 4 | **Country/region match** | **15%** | Country context affects regulation, permitting timelines, grid access, workforce availability, and supply chain. Same-country projects are the best comparators, but neighboring countries in the same region (e.g., EU) share many characteristics. |
| 5 | **Project maturity** | **5%** | A small tiebreaker. Operational projects provide the most lessons learned. Under-construction projects represent the current state of the art. Planned projects provide aspirational benchmarks but limited hard data. |

### 2.1 Weight Sensitivity Analysis

The weights were calibrated against the 5 test cases (see retrieval_agent_test_report.md). Sensitivity:

- **Technology ±5%:** Minor rank shifts at the margin between adjacent projects. No top-3 shifts.
- **Industry ±5%:** Can reorder projects #2-#4 when industry match is the key differentiator.
- **Capacity ±5%:** Most impactful for 20 MW vs 100 MW queries. At large scales (>500 MW), the log function compresses differences.
- **Country ±5%:** Most impactful when the dataset has multiple projects in the queried country.

The chosen weights (30/25/25/15/5) represent a balanced configuration validated against all 5 test cases. No single dimension dominates, and the ranking is robust to ±5% weight variations.

---

## 3. Scoring Functions — Detailed Specification

### 3.1 Technology Match Score

| Query Technology | Project Technology | Score | Example |
|-----------------|-------------------|-------|---------|
| `PEM` | `PEM` | **1.00** | Query: PEM, Project: Normand'Hy (PEM) |
| `Alkaline` | `Alkaline` | **1.00** | Query: Alkaline, Project: HH1 (Alkaline) |
| `PEM` | `Alkaline` | **0.00** | Query: PEM, Project: HH1 (Alkaline) |
| `Alkaline` | `PEM` | **0.00** | Query: Alkaline, Project: Normand'Hy (PEM) |
| Any | `PEM+Alkaline` | **0.50** | Query: PEM, Project: HyDeal España (PEM+Alkaline) |
| `PEM+Alkaline` | `PEM` | **0.50** | Query: PEM+Alkaline, Project: any single-tech |
| `PEM+Alkaline` | `Alkaline` | **0.50** | Query: PEM+Alkaline, Project: any single-tech |
| `null`/unknown | Any | **0.70** | Query: unknown tech, Project: any (both technologies potentially relevant) |

**Rationale:** Technology is the most discriminating dimension. A PEM project gains limited value from Alkaline references and vice versa. The 0.50 for hybrid projects reflects that PEM+Alkaline is partially relevant to both.

### 3.2 Industry (Offtake) Match Score

The industry score is computed as a composite of primary and secondary offtake matching.

| Match Type | Score |
|-----------|-------|
| Exact primary offtake match | **1.00** |
| Query industry is in project's secondary_applications | **0.70** |
| Query industry is in a related offtake category | **0.40** |
| No match | **0.00** |

**Related offtake categories (for the 0.40 tier):**

| Category Group | Members |
|---------------|---------|
| **Industrial processes** | `refinery`, `steel`, `ammonia`, `methanol` |
| **Energy & mobility** | `mobility`, `grid_injection`, `industrial_heat` |
| **Trade** | `export` |

**Multi-match for broad industry queries:**

| Query Industry | Matches scored against |
|---------------|----------------------|
| "Chemical Industry" | `ammonia` (1.0), `methanol` (1.0), `refinery` (0.4) |
| "Industrial Hydrogen" | `refinery` (1.0), `steel` (1.0), `ammonia` (1.0), `industrial_heat` (0.7) |
| "Transport" | `mobility` (1.0) |

When multiple primary offtakes are targeted, the **maximum** score across all is used.

### 3.3 Capacity Similarity Score

Uses a logarithmic function to reflect that scale differences matter more at small scales:

```
CapacityScore = max(0, 1.0 − 0.5 × |log₁₀(query_MW / project_MW)|)
```

| Query MW | Project MW | Ratio | log₁₀(ratio) | Score | Interpretation |
|----------|-----------|-------|-------------|-------|----------------|
| 100 | 100 | 1.00 | 0.00 | **1.00** | Exact match |
| 100 | 200 | 0.50 | -0.30 | **0.85** | 2× larger — very close |
| 100 | 50 | 2.00 | 0.30 | **0.85** | 2× smaller — very close |
| 100 | 20 | 5.00 | 0.70 | **0.65** | 5× smaller — relevant but different scale |
| 100 | 500 | 0.20 | -0.70 | **0.65** | 5× larger — relevant but different scale |
| 20 | 100 | 0.20 | -0.70 | **0.65** | Same as above — symmetric |
| 20 | 200 | 0.10 | -1.00 | **0.50** | 10× larger — borderline |
| 100 | 7400 | 0.014 | -1.87 | **0.07** | 74× larger — minimal relevance |
| 7400 | 100 | 74.0 | 1.87 | **0.07** | Same — symmetric |

**Key property:** The function is symmetric — a 20 MW query matching a 200 MW project gets the same score as a 200 MW query matching a 20 MW project. Both are equally relevant or irrelevant.

**When capacity_mw is null:** This dimension is excluded. The composite score is re-weighted: Technology (35%), Industry (30%), Country (20%), Maturity (15%).

### 3.4 Country/Region Match Score

| Geographic Relationship | Score | Example |
|------------------------|-------|---------|
| Same country | **1.00** | Query: France → Project: Normand'Hy (France) |
| Neighboring country (shared land border) | **0.70** | Query: France → Project: HGHH (Germany) |
| Same sub-region (e.g., Western Europe, Southern Europe) | **0.50** | Query: France → Project: HH1 (Netherlands) |
| Same continent (Europe) | **0.40** | Query: France → Project: HySynergy (Denmark) |
| Different continent | **0.10** | Query: France → Project: NEOM (MENA — future dataset) |
| Unknown country / no match | **0.25** | Query: "Unknown" → all projects get flat 0.25 |

**Neighboring country pairs in the current dataset:**

| Country | Neighbors (in dataset) |
|---------|----------------------|
| France | Germany, Spain, Belgium |
| Germany | France, Netherlands, Denmark, Belgium |
| Spain | France, Portugal |
| Netherlands | Germany, Belgium |
| Belgium | France, Germany, Netherlands |
| Portugal | Spain |
| Denmark | Germany |

**Sub-region groupings:**

| Sub-region | Countries in Dataset |
|-----------|---------------------|
| Western Europe | France, Germany, Netherlands, Belgium |
| Southern Europe | Spain, Portugal |
| Northern Europe | Denmark |

### 3.5 Project Maturity Score

| Status | Score | Rationale |
|--------|-------|-----------|
| `under_construction` | **1.00** | Best reference: represents current industry practice, real CAPEX data, active supply chains |
| `operational` | **0.80** | Excellent reference: proven performance data, but may reflect older technology/costs |
| `planned` | **0.50** | Useful but limited: aspirational data, no verified CAPEX, may be scaled down or cancelled |
| `decommissioned` | **0.30** | Historical interest only: lessons learned, risk evidence |
| `cancelled` | **0.20** | Risk evidence only: what went wrong |

When query includes `target_cod`:
- `target_cod` ≤ 2027: boost `operational` to 1.00 and `under_construction` to 0.90 (immediate precedents matter more)
- `target_cod` ≥ 2030: boost `planned` to 0.60 (future landscape matters more)

---

## 4. Composite Score Calculation

```
CompositeScore = w_tech    × TechScore
               + w_ind     × IndustryScore
               + w_cap     × CapacityScore
               + w_country × CountryScore
               + w_mat     × MaturityScore

Where:
  w_tech    = 0.30
  w_ind     = 0.25
  w_cap     = 0.25
  w_country = 0.15
  w_mat     = 0.05
```

**Handling missing dimensions:**

| Missing Query Dimension | Action |
|------------------------|--------|
| `technology` missing | Set TechScore = 0.70 for all projects. Weights remain unchanged. |
| `industry` missing | Set IndustryScore = 0.50 for all projects (neutral). Weights remain unchanged. |
| `capacity_mw` missing | Exclude capacity dimension. Re-weight: Tech 35%, Industry 30%, Country 20%, Maturity 15%. |
| `country` missing | Set CountryScore = 0.40 for all projects (continental default). Weights remain unchanged. |
| All 5 missing | All projects score 0.50. Return all 10 projects unsorted with note "No query criteria provided — returning full dataset." |

---

## 5. Worked Example

### Query: France, Steel, PEM, 100 MW, 2029 (Test Case 1)

#### Step 1: Apply technology filter

Projects filtered IN (PEM or PEM+Alkaline): GA-PR-001, GA-PR-002, GA-PR-004, GA-PR-005, GA-PR-006, GA-PR-008, GA-PR-010
Projects filtered OUT (Alkaline only): GA-PR-003, GA-PR-007, GA-PR-009

#### Step 2: Compute scores for each candidate

**GA-PR-001: Normand'Hy (France, PEM, 200 MW, refinery, under_construction)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ refinery (industrial group) | 0.40 | 0.25 | 0.100 |
| Capacity | 100 MW ↔ 200 MW, log₁₀(0.5) = -0.30 | 0.85 | 0.25 | 0.213 |
| Country | France ↔ France | 1.00 | 0.15 | 0.150 |
| Maturity | under_construction | 1.00 | 0.05 | 0.050 |
| **Total** | | | | **0.813** |

**GA-PR-004: HGHH (Germany, PEM, 100 MW, industrial_heat, under_construction)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ industrial_heat (different) | 0.00 | 0.25 | 0.000 |
| Capacity | 100 MW ↔ 100 MW, log₁₀(1.0) = 0.00 | 1.00 | 0.25 | 0.250 |
| Country | France ↔ Germany (neighbor) | 0.70 | 0.15 | 0.105 |
| Maturity | under_construction | 1.00 | 0.05 | 0.050 |
| **Total** | | | | **0.705** |

**GA-PR-008: REFHYNE II (Germany, PEM, 100 MW, refinery, under_construction)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ refinery (industrial group) | 0.40 | 0.25 | 0.100 |
| Capacity | 100 MW ↔ 100 MW, log₁₀(1.0) = 0.00 | 1.00 | 0.25 | 0.250 |
| Country | France ↔ Germany (neighbor) | 0.70 | 0.15 | 0.105 |
| Maturity | under_construction | 1.00 | 0.05 | 0.050 |
| **Total** | | | | **0.805** |

**GA-PR-010: Galp Sines (Portugal, PEM, 100 MW, refinery, under_construction)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ refinery (industrial group) | 0.40 | 0.25 | 0.100 |
| Capacity | 100 MW ↔ 100 MW, log₁₀(1.0) = 0.00 | 1.00 | 0.25 | 0.250 |
| Country | France ↔ Portugal (neighbor via Spain, sub-region) | 0.50 | 0.15 | 0.075 |
| Maturity | under_construction | 1.00 | 0.05 | 0.050 |
| **Total** | | | | **0.775** |

**GA-PR-006: Puertollano (Spain, PEM, 20 MW, ammonia, operational)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ ammonia (industrial group) | 0.40 | 0.25 | 0.100 |
| Capacity | 100 ↔ 20, log₁₀(5.0) = 0.70 | 0.65 | 0.25 | 0.163 |
| Country | France ↔ Spain (neighbor) | 0.70 | 0.15 | 0.105 |
| Maturity | operational (target_cod 2029 → boost to 1.00) | 1.00 | 0.05 | 0.050 |
| **Total** | | | | **0.718** |

**GA-PR-002: Masshylia (France, PEM, 20 MW, refinery, planned)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM | 1.00 | 0.30 | 0.300 |
| Industry | steel ↔ refinery (industrial group) | 0.40 | 0.25 | 0.100 |
| Capacity | 100 ↔ 20, log₁₀(5.0) = 0.70 | 0.65 | 0.25 | 0.163 |
| Country | France ↔ France | 1.00 | 0.15 | 0.150 |
| Maturity | planned | 0.50 | 0.05 | 0.025 |
| **Total** | | | | **0.738** |

**GA-PR-005: HyDeal España (Spain, PEM+Alkaline, 7400 MW, steel, planned)**

| Dimension | Raw Value | Score | Weight | Weighted |
|-----------|-----------|-------|--------|----------|
| Technology | PEM ↔ PEM+Alkaline | 0.50 | 0.30 | 0.150 |
| Industry | steel ↔ steel | 1.00 | 0.25 | 0.250 |
| Capacity | 100 ↔ 7400, log₁₀(0.014) = -1.87 | 0.07 | 0.25 | 0.018 |
| Country | France ↔ Spain (neighbor) | 0.70 | 0.15 | 0.105 |
| Maturity | planned | 0.50 | 0.05 | 0.025 |
| **Total** | | | | **0.548** |

#### Step 3: Final Ranking

| Rank | Project | Score | Tier | Why Here |
|------|---------|-------|------|----------|
| **#1** | **Normand'Hy** (FR, 200 MW) | **0.813** | Highly Relevant | Same country, same technology, closest scale above query, industrial offtake |
| **#2** | **REFHYNE II** (DE, 100 MW) | **0.805** | Highly Relevant | Same technology, exact scale match, neighboring country, refinery (industrial process) |
| **#3** | **Galp Sines** (PT, 100 MW) | **0.775** | Highly Relevant | Same technology, exact scale match, refinery reference, Southern Europe |
| **#4** | **Masshylia** (FR, 20 MW) | **0.738** | Highly Relevant | Same country, same technology, refinery—steel industrial link; small scale limits relevance |
| **#5** | **Puertollano** (ES, 20 MW) | **0.718** | Highly Relevant | Same technology, operational reference, neighboring country; small scale and ammonia offtake differ |
| **#6** | **HGHH** (DE, 100 MW) | **0.705** | Highly Relevant | Same technology, exact scale match, neighboring country; industrial_heat offtake differs from steel |

*Projects below top-6: HyDeal España (0.548, Tier 2 Relevant)*

### Why Normand'Hy ranks #1 instead of REFHYNE II at #2

The 0.008 point difference is driven entirely by the **Country** dimension:
- Normand'Hy: France = France (1.00 × 0.15 = 0.150)
- REFHYNE II: France ↔ Germany (0.70 × 0.15 = 0.105)

Difference: 0.045 points → Normand'Hy gains 0.045 from being in France. This is partially offset by REFHYNE II getting the full CapacityScore (1.00 vs 0.85) because 100 MW = 100 MW, while Normand'Hy is at 200 MW. The net is 0.008 in Normand'Hy's favor — a razor-thin margin that correctly reflects that both projects are excellent references.

---

## 6. Full Dataset Scoring Reference

For rapid lookup, here are the key attributes used in scoring:

| ID | Name | Country | Tech | MW | Primary Offtake | Status |
|----|------|---------|------|----|-----------------|--------|
| GA-PR-001 | Normand'Hy | France | PEM | 200 | refinery | under_construction |
| GA-PR-002 | Masshylia | France | PEM | 20 | refinery | planned |
| GA-PR-003 | Holland Hydrogen I | Netherlands | Alkaline | 200 | refinery | under_construction |
| GA-PR-004 | Hamburg Green Hydrogen Hub | Germany | PEM | 100 | industrial_heat | under_construction |
| GA-PR-005 | HyDeal España | Spain | PEM+Alkaline | 7400 | steel | planned |
| GA-PR-006 | Puertollano | Spain | PEM | 20 | ammonia | operational |
| GA-PR-007 | HySynergy | Denmark | Alkaline | 20 | refinery | operational |
| GA-PR-008 | REFHYNE II | Germany | PEM | 100 | refinery | under_construction |
| GA-PR-009 | Hyoffwind | Belgium | Alkaline | 25 | mobility | under_construction |
| GA-PR-010 | Galp Sines | Portugal | PEM | 100 | refinery | under_construction |

### Country Neighbor Matrix

```
         FR  DE  ES  NL  BE  PT  DK
France    X   Y   Y   -   Y   -   -
Germany   Y   X   -   Y   Y   -   Y
Spain     Y   -   X   -   -   Y   -
Netherl.  -   Y   -   X   Y   -   -
Belgium   Y   Y   -   Y   X   -   -
Portugal  -   -   Y   -   -   X   -
Denmark   -   Y   -   -   -   -   X
```

(Y = shared land border → CountryScore 0.70; sub-region pairs → 0.50; same continent → 0.40)

---

## 7. Edge Cases & Special Handling

### 7.1 Giga-Scale Projects (HyDeal España, GA-PR-005, 7,400 MW)

HyDeal España is an extreme outlier at 7,400 MW — 37× larger than the next biggest project (200 MW). The logarithmic capacity function handles this gracefully: for most queries (20-200 MW), HyDeal gets a CapacityScore of 0.07-0.18, correctly reflecting minimal scale relevance. However, for queries >500 MW, HyDeal's CapacityScore rises to 0.50+, correctly surfacing it as the only giga-scale reference.

**Special rule:** HyDeal España is ALWAYS included in the top-6 when the query capacity ≥ 500 MW, regardless of composite score, because it is the sole giga-scale reference.

### 7.2 Pre-FID Projects with Minimal Data

Masshylia (GA-PR-002) and HyDeal España (GA-PR-005) are `planned` with significant data gaps (null CAPEX, no confirmed technology for Masshylia, no FID date for HyDeal). Their MaturityScore of 0.50 appropriately penalizes them. They will only rank highly when:
- They are in the same country as the query (country score compensates)
- The query is also a planned project (peer comparison)
- No better references exist

### 7.3 Technology "PEM+Alkaline"

HyDeal España (GA-PR-005) is the only project with `PEM+Alkaline`. It scores 0.50 against both PEM and Alkaline queries. This reflects that it is partially relevant to both but not an exact match for either. A hybrid project query would score 1.00 against it.

### 7.4 Single Reference Per Country

Some queries target a country with only 1 reference project:
- Portugal: only GA-PR-010 (Galp Sines, PEM, 100 MW)
- Denmark: only GA-PR-007 (HySynergy, Alkaline, 20 MW)
- Netherlands: only GA-PR-003 (HH1, Alkaline, 200 MW)
- Belgium: only GA-PR-009 (Hyoffwind, Alkaline, 25 MW)

When only 1 in-country reference exists, the agent notes this and expands to neighboring countries automatically.

### 7.5 No Same-Technology Projects

If a query specifies a technology and no projects with that technology exist that meet the minimum score threshold (0.30), the agent:
1. Notes the gap: "No {technology} projects found matching your criteria."
2. Retrieves the other technology's projects with a disclaimer: "The following {other_tech} projects may provide partial reference for scale/industry/country, but technology-specific factors differ."
3. Flags this as a knowledge base gap in the gap analysis.

---

## 8. Ranking Tier Definitions

| Tier | Score Range | Label | Agent Behavior |
|------|------------|-------|---------------|
| **Tier 1** | ≥ 0.70 | **Highly Relevant** | Presented first with full detail. Directly comparable to the query. Core reference for feasibility. |
| **Tier 2** | 0.50–0.69 | **Relevant** | Presented second with key details. Shares important dimensions but has significant differences. Useful with caveats. |
| **Tier 3** | 0.30–0.49 | **Partially Relevant** | Presented with summary only. Shares at least one dimension. Useful for specific comparisons (e.g., same country but different technology). |
| **Excluded** | < 0.30 | Not retrieved | Insufficient relevance to the query. |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior AI Solution Architect | Initial matching methodology with full worked example |

---

*This methodology produces transparent, explainable, and deterministic project rankings. Every score component is calculable by hand, and every ranking is accompanied by a human-readable rationale. The methodology is designed for the Gold Dataset's 10-project scale and will be enhanced with vector embedding similarity when the dataset exceeds 50 projects.*
