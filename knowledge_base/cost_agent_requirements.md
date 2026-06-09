# Cost Agent Requirements — Future Agent Specification v1.0

**Document:** Cost Agent Functional & Technical Requirements
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & AI Solution Architect
**Target Agent:** CostAgent (M8 in Copilot roadmap)
**Dependencies:** Cost Library (populated), Gold Dataset, Technology Cards, Retrieval Agent (M5)

---

## 1. Agent Identity & Boundaries

### 1.1 Agent Definition

The **Cost Agent** is a knowledge retrieval and analysis agent that identifies, structures, and contextualizes CAPEX cost information for green hydrogen projects. It operates as a **cost engineer advisor** — it helps project teams understand what drives costs, which costs dominate, and how much confidence to place in different estimates. It does NOT produce false precision or replace detailed engineering estimates.

### 1.2 What the Cost Agent DOES

| Capability | Description |
|-----------|-------------|
| ✅ Structure cost breakdown | Present CAPEX by category with typical ranges and percentages |
| ✅ Identify cost drivers | Explain which factors most influence total CAPEX |
| ✅ Benchmark against references | Compare queried project against Gold Dataset and industry benchmarks |
| ✅ Scale costs | Apply power law scaling with documented exponents |
| ✅ Assess confidence | Classify each cost component and aggregate confidence |
| ✅ Explain uncertainty | Articulate what is known, what is estimated, and what is assumed |
| ✅ Cite sources | Every cost figure linked to a traceable source |

### 1.3 What the Cost Agent DOES NOT Do

| ❌ | Rationale |
|----|-----------|
| Produce a single-point CAPEX number | Misleading — creates false precision. Always present ranges with confidence. |
| Replace detailed engineering estimates | AACE Class 3+ requires FEED-level engineering, not agent inference. |
| Make investment decisions | NPV, IRR, and financial close decisions belong to human decision-makers. |
| Project future commodity prices | Uses documented IEA/IRENA forecasts; does not speculate. |
| Compare projects on "value for money" | Cost benchmarking, not value judgment. |

---

## 2. Core Capabilities

### 2.1 CAPEX Breakdown Generation

For a given project profile, generate a structured CAPEX breakdown:

```
Input: { technology: "PEM", capacity_mw: 100, country: "France", industry: "Steel" }

Output:
  CAT-01 Electrolyzer System:      €48M  (€480/kW) | 32% of total | Class C
  CAT-02 Electrical:               €21M  (€210/kW) | 14%         | Class C
  CAT-03 Water:                    €6M   (€60/kW)  | 4%          | Class C
  CAT-04 H₂ Processing:            €14M  (€135/kW) | 9%          | Class C
  CAT-05 Civil:                    €15M  (€150/kW) | 10%         | Class C
  CAT-06 Thermal:                  €5M   (€45/kW)  | 3%          | Class C
  CAT-07 I&C:                      €6M   (€60/kW)  | 4%          | Class C
  CAT-08 Indirect & Owner's:       €36M  (€360/kW) | 24%         | Class C
  ─────────────────────────────────────────────────
  TOTAL (central):                ~€150M (€1,500/kW)
  RANGE (P10-P90):                €120-195M (€1,200-1,950/kW)
  CONFIDENCE: Medium (weighted 0.62)
  AACE CLASS: Class 4 equivalent (±20-30%)
```

### 2.2 Cost Driver Analysis

Rank and explain cost drivers:

```
Top 5 Cost Drivers (100 MW PEM, France, Steel):
1. Electrolyzer stack technology choice (32% of total) — PEM @ ~€800/kW stack
2. Indirect costs (24%) — FOAK premium + contingency for steel offtake novelty
3. Electrical infrastructure (14%) — brownfield vs. greenfield decisive for grid connection
4. H₂ compression (9%) — steel DRI requires 10-20 bar; PEM 30 bar output reduces stages
5. Civil works (10%) — brownfield site can save 30-40% vs greenfield
```

### 2.3 Scale Adjustment

Apply scaling methodology with documented rationale:

```
"PEM stack cost benchmark: €800/kW at 100 MW (IEA GHR 2025).
Your project: 300 MW.
Applied scaling exponent 0.90: Cost_300 = 800 × (300/100)^0.90 = 800 × 2.69 = €2,150/kW total.
Per-kW: €2,150/kW / 3.0 = €717/kW.
Scale savings: 800 → 717 €/kW (10% reduction).
Caveat: Largest operational PEM plant is 200 MW (Normand'Hy). 300 MW extrapolation beyond proven reference — FOAK premium of +15% recommended → €825/kW."
```

### 2.4 Uncertainty Quantification

For each major category, present the uncertainty range:

```
Cost uncertainty by confidence class:
  Class A components (0% of total):   ±5%    — no actual costs available
  Class B components (15% of total):  ±10%   — OEM quotations for stack
  Class C components (65% of total):  ±25%   — IEA/IRENA benchmarks
  Class D components (20% of total):  ±40%   — analyst estimates for steel-specific H₂ processing

Blended uncertainty: approximately ±25-30%
→ AACE Class 4 equivalent estimate
```

### 2.5 Technology Cost Comparison

Compare PEM vs. Alkaline for a given profile:

```
100 MW, European supply chain, 2025:
  PEM all-in:  ~€1,500/kW (€150M)
  Alkaline all-in: ~€1,300/kW (€131M)
  Delta: Alkaline ~€19M (13%) cheaper

Primary drivers of difference:
  Stack: PEM +€35M (€80M vs €45M)
  Compression: Alkaline +€2M (atmospheric output requires additional stage)
  Civil: Alkaline +€2M (larger footprint)
  Contingency: PEM +€3M (higher technology uncertainty)
```

---

## 3. Input Schema

```json
{
  "project_profile": {
    "technology": "PEM | Alkaline | not_selected",
    "capacity_mw": "<number>",
    "country": "<ISO country>",
    "industry": "<offtake enum>",
    "site_type": "greenfield | brownfield | unknown",
    "required_output_pressure_bar": "<number, if known>",
    "target_cod": "<year>",
    "is_first_of_a_kind": "<boolean>",
    "aace_target_class": "class_5_conceptual | class_4_feasibility"
  }
}
```

---

## 4. Reasoning Workflows

### Workflow 1: CAPEX Range Estimate
1. Identify applicable cost records from Cost Library
2. Scale each to target capacity using power law
3. Adjust for target year using learning curves
4. Apply regional multipliers
5. Apply FOAK premium if applicable
6. Aggregate bottom-up with confidence weighting
7. Present as range (P10-P90) with category breakdown

### Workflow 2: Cost Driver Sensitivity
1. Identify top 5 cost categories by % of total
2. For each: ±20% sensitivity tornado diagram data
3. Explain which assumptions drive each category
4. Flag categories with lowest confidence for focused data collection

### Workflow 3: Project Benchmarking
1. Retrieve similar Gold Dataset projects via Retrieval Agent
2. Extract their CAPEX data (total and per-kW)
3. Normalize to same year (inflation adjustment)
4. Present side-by-side comparison
5. Explain differences (scale, region, offtake, FOAK status)

### Workflow 4: Technology Cost Comparison
1. Run Workflow 1 for PEM → estimate A
2. Run Workflow 1 for Alkaline → estimate B
3. Present side-by-side with deltas
4. Explain primary drivers of difference
5. No recommendation — present data

---

## 5. Output Specification

Structured JSON + human-readable summary. Every cost figure tagged with source, confidence class, and scaling method. No single-point CAPEX number without a range.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer & AI Solution Architect | Initial Cost Agent requirements |
