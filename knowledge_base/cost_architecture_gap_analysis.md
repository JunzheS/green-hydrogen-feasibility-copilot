# Cost Architecture Gap Analysis — Critical Evaluation

**Document:** Architecture Gap Identification
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Knowledge Validation Lead
**Frameworks Evaluated:** cost_taxonomy_framework.md, cost_schema_v1.md, cost_scaling_methodology.md, cost_confidence_framework.md, cost_agent_requirements.md

---

## Gap Classification

| Severity | Definition |
|----------|-----------|
| **CRITICAL** | Would cause the Cost Agent to produce misleading, incomplete, or untraceable estimates. Must be resolved before Cost Library construction begins. |
| **IMPORTANT** | Would reduce estimate quality, limit agent capability, or create maintenance burden. Should be resolved during Cost Library construction. |
| **OPTIONAL** | Would improve estimate quality or agent usability. Can be addressed post-MVP. |

---

## Critical Gaps (2 identified)

### GAP-C1: No Direct Hydrogen-Specific Scaling Exponents

| Attribute | Detail |
|-----------|--------|
| **Description** | The scaling exponents in cost_scaling_methodology.md §2.2 are based on general chemical engineering references (Peters & Timmerhaus), not hydrogen electrolysis project data. An exponent of 0.40 for grid connection may be reasonable, but it hasn't been calibrated against hydrogen project cost data. |
| **Impact** | Scaling from a 100 MW benchmark to 300 MW could be off by 10-15% if the true exponent differs from the assumed value. For an electrolyzer system, a 0.05 error in the exponent at 3× scale produces a ~5% cost estimate error. |
| **Root cause** | Not enough hydrogen projects have been built at multiple scales to empirically calibrate exponents. This is an industry data gap, not an architecture design flaw. |
| **Mitigation** | (a) Document the uncertainty from exponent assumptions explicitly, (b) Use exponent ranges (e.g., n=0.40 ±0.10) rather than point values, (c) Flag all scaling operations with a notation that exponents are based on chemical industry analogs pending hydrogen-specific calibration. |
| **Resolution** | Add `scaling_exponent_uncertainty` field to cost_schema_v1.md. Add exponent range sensitivity to cost_scaling_methodology.md. |

### GAP-C2: No OPEX/LCOH Integration in Cost Architecture

| Attribute | Detail |
|-----------|--------|
| **Description** | The Cost Architecture covers CAPEX comprehensively but does not address OPEX (electricity, maintenance, stack replacement, water, labor) or LCOH (levelized cost of hydrogen). A Cost Agent that only estimates CAPEX cannot answer "what is the total cost of hydrogen production?" |
| **Impact** | The Feasibility Agent (future M9+) needs both CAPEX and OPEX to assess project viability. Without OPEX, the Cost Agent provides only half the cost picture. |
| **Root cause** | M7A scope defined CAPEX-only. OPEX was deferred to a future milestone. |
| **Mitigation** | Add an OPEX taxonomy (aligned with Technology Card cost_profile.opex_breakdown) and OPEX estimation methodology to the Cost Architecture in M7C. The Technology Cards (TC-PEM-001, TC-ALK-001) already contain OPEX breakdowns (electricity 70-75%, maintenance 8-10%, stack replacement 10-15%) — these provide the foundation. |
| **Resolution** | Create cost_opex_methodology.md as a companion to cost_scaling_methodology.md. Include OPEX categories in cost_taxonomy_framework.md. |

---

## Important Gaps (5 identified)

### GAP-I1: No Regional Multiplier Database

| Attribute | Detail |
|-----------|--------|
| **Description** | The taxonomy and schema mention regional multipliers ("China −20-30%, North America +5-15%") but these are qualitative estimates, not a structured database. A Cost Agent answering "what does this cost in Saudi Arabia vs Germany?" needs systematic regional adjustment factors. |
| **Impact** | Regional cost comparisons rely on analyst judgment rather than structured data. |
| **Mitigation** | Create `regional_multipliers.json` with labor, material, and productivity factors per region, sourced from IEA/IRENA/industry cost data. |
| **Priority** | Resolve during Cost Library Sprint 1. |

### GAP-I2: No Temporal Cost Projection Model

| Attribute | Detail |
|-----------|--------|
| **Description** | The learning curve methodology exists but requires manual calculation. A Cost Agent needs to answer "what will this cost in 2030 vs 2028?" automatically. This requires an explicit temporal model combining learning curves, inflation, and technology-specific forecasts. |
| **Impact** | Temporal projections are currently manual and inconsistent. |
| **Mitigation** | Build `cost_temporal_projection.py` script that applies learning rates + inflation + technology roadmaps to project costs to a target year. |
| **Priority** | Resolve before Cost Agent development (M8). |

### GAP-I3: Missing Cost Category Interaction Rules

| Attribute | Detail |
|-----------|--------|
| **Description** | The taxonomy defines 8 independent cost categories, but in reality, categories interact. For example: choosing a brownfield site reduces Category 02 (electrical) AND Category 05 (civil) simultaneously. Choosing PEM over Alkaline affects Category 01 (stack), Category 03 (water), Category 04 (compression), and Category 05 (civil). The architecture has no explicit interaction rules. |
| **Impact** | A Cost Agent might double-count savings or fail to capture correlated cost benefits. |
| **Mitigation** | Define interaction rules as a dependency matrix. Example: `site_type=brownfield` → Category 02 multiplier 0.70, Category 05 multiplier 0.75, Category 08 multiplier 0.90. |

### GAP-I4: Incomplete Exclusions/Inclusions Standardization

| Attribute | Detail |
|-----------|--------|
| **Description** | `cost_drivers.exclusions` is mandatory but has no controlled vocabulary. One analyst might exclude "freight and import duties" while another excludes "logistics." A Cost Agent aggregating costs from multiple entries could inadvertently include/exclude items inconsistently. |
| **Impact** | Potential double-counting or gaps in CAPEX aggregation. |
| **Mitigation** | Create a controlled vocabulary of 20-30 standard exclusion/inclusion terms. Validate all Cost Library entries against this vocabulary. |

### GAP-I5: No Cost Benchmark Database Structure

| Attribute | Detail |
|-----------|--------|
| **Description** | The Cost Schema defines individual cost records but there is no structure for "benchmark sets" — a collection of cost records that together form a complete plant cost estimate at a given scale/technology/region. A Cost Agent providing a total CAPEX estimate needs to aggregate multiple cost records, and the aggregation logic is not specified. |
| **Impact** | Ad-hoc aggregation by the Cost Agent could produce inconsistent totals. |
| **Mitigation** | Define `cost_benchmark_set` entity: a named collection of cost records with defined scope, date, and confidence, representing a complete plant cost estimate. |

---

## Optional Gaps (4 identified)

### GAP-O1: No Cost Visualization Specifications

Future Cost Agent output should include waterfall charts, tornado diagrams, and heat maps. The architecture does not specify visualization requirements.

### GAP-O2: No EPC Contract Type Cost Adjustment Factors

LSTK contracts carry a 10-20% premium vs EPCM. The architecture mentions this in the taxonomy but has no quantitative adjustment factors by contract type.

### GAP-O3: No Cost Normalization for Capacity Factor

CAPEX benchmarks assume a certain capacity factor (full-load hours/year). A plant designed for 8,000 hours/year (baseload) may have different cost structure than one designed for 4,000 hours/year (solar-coupled). The architecture does not address this.

### GAP-O4: No Decommissioning Cost Provision

End-of-life decommissioning costs (stack disposal, PFSA membrane recycling, site restoration) are not covered in the taxonomy. For a 20-30 year project life, decommissioning costs should be provisioned.

---

## Gap Summary Matrix

| ID | Severity | Area | Resolution Timeline |
|----|----------|------|-------------------|
| C1 | CRITICAL | Scaling exponents not H₂-calibrated | Before Cost Library Sprint 1 |
| C2 | CRITICAL | No OPEX/LCOH integration | M7C milestone |
| I1 | IMPORTANT | No regional multiplier database | During Cost Library Sprint 1 |
| I2 | IMPORTANT | No temporal projection model | Before Cost Agent (M8) |
| I3 | IMPORTANT | Missing cost category interaction rules | During Cost Library Sprint 1 |
| I4 | IMPORTANT | Incomplete exclusions standardization | During Cost Library Sprint 1 |
| I5 | IMPORTANT | No benchmark set structure | During Cost Library Sprint 1 |
| O1 | OPTIONAL | No visualization specs | Post-MVP |
| O2 | OPTIONAL | No EPC contract type factors | During Cost Library Sprint 2 |
| O3 | OPTIONAL | No capacity factor normalization | During Cost Library Sprint 2 |
| O4 | OPTIONAL | No decommissioning provision | During Cost Library Sprint 2 |

---

## Verdict

**The Cost Architecture is fundamentally sound but has 2 critical gaps that must be addressed before Cost Library construction.** GAP-C1 (scaling exponent calibration) can be mitigated through documentation and uncertainty ranges within the Sprint 1 timeline. GAP-C2 (OPEX integration) requires a dedicated M7C milestone — it is out of scope for the current CAPEX-focused architecture.

The 5 important gaps can be resolved during Cost Library Sprint 1 without architecture changes — they primarily require structured data (regional multipliers, controlled vocabularies, interaction rules) rather than schema changes.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial architecture gap analysis |
