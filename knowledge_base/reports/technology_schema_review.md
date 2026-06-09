# Technology Card Schema Review Report

**Document:** Schema Review — Technology Knowledge Card v1.0
**Date:** 2026-06-05
**Author:** Senior Hydrogen Technology Expert & Knowledge Engineer
**Purpose:** Validate whether the existing schema supports Technical Feasibility Agent reasoning for pre-feasibility assessments

---

## 1. Validation Against Target Questions

Each target question was tested against the current Technology Knowledge Card Schema v1.0 fields.

### Q1: Is this technology mature enough for this project?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `maturity.trl_level` | TRL 1–9 + rationale | ✅ Adequate |
| `maturity.commercial_maturity` | r_and_d → mature | ✅ Adequate |
| `maturity.cumulative_global_capacity_mw` | Total installed base | ✅ Adequate |
| `maturity.technology_learning_rate_percent` | Learning rate | ✅ Adequate |
| `maturity.mrl_level` | Manufacturing readiness | ✅ Adequate |

**Gap:** No distinction between "lab-validated" and "field-proven-at-scale." Two technologies at TRL 8 may have very different operating hours in the field. A "cumulative operating hours across all deployed plants" field would complement TRL.

**Verdict:** ⚠️ Mostly adequate. Minor enhancement recommended.

### Q2: What TRL level does it have?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `maturity.trl_level` | Integer 1–9 | ✅ Adequate |
| `maturity.trl_rationale` | Free-text justification | ✅ Adequate |
| `maturity.trl_assessment_date` | Date of assessment | ✅ Adequate |
| `maturity.trl_assessed_by` | Who assessed | ✅ Adequate |

**Verdict:** ✅ Fully adequate. TRL is well-covered with traceability.

### Q3: Has it already been deployed at this scale?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `scalability.max_plant_size_known_mw` | Largest single plant | ✅ Adequate |
| `scalability.typical_plant_size_range_mw` | Range data | ✅ Adequate |
| `applications.reference_project_ids` | FK to real projects | ✅ Adequate |

**Gap:** The schema tells you the largest plant exists but not how many plants exist at a given scale. A `deployment_count_by_scale` or `number_of_plants_above_X_MW` field would support "has this been done N times before?" reasoning.

**Verdict:** ⚠️ Adequate for basic checking. Missing deployment frequency data.

### Q4: What are the main technical risks?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `limitations` | String[] of limitations | ⚠️ Partial |
| `technology_differentiators` | vs. other technology | ❌ Not risk-focused |
| *(No risk-specific block)* | | ❌ Gap |

**Gap:** The schema has `limitations` (7 items in template) but no dedicated `technical_risks` block. A feasibility agent needs to answer "what could go wrong with this technology choice?" with structured risk data, not just a list of limitations. The Risk Database (separate schema) has project-level risks but not technology-inherent risks.

**Verdict:** ❌ Insufficient. A `technical_risks` block is needed with probability, impact, and mitigation mapped per technology.

### Q5: What infrastructure is required?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `infrastructure.power_supply_requirements` | String | ✅ Adequate |
| `infrastructure.water_infrastructure_needed` | String | ✅ Adequate |
| `infrastructure.cooling_requirements` | String | ✅ Adequate |
| `infrastructure.control_system_requirements` | String | ✅ Adequate |
| `infrastructure.supply_chain_critical_materials` | String[] | ✅ Adequate |
| `infrastructure.workforce_skill_requirements` | String | ✅ Adequate |

**Verdict:** ✅ Fully adequate. Infrastructure is the best-covered dimension in the current schema.

### Q6: Is it suitable for industrial decarbonization?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| `applications.primary_applications` | Enum[] | ✅ Adequate |
| `applications.unsuitable_applications` | Enum[] | ✅ Adequate |
| `applications.application_notes` | String | ✅ Adequate |

**Gap:** Suitability is binary (suitable/unsuitable) but real pre-feasibility asks "how suitable?" A `suitability_score_per_application` field with 1–5 rating per application would enable weighted comparison. A steel plant may be "suitable" for both PEM and Alkaline but for different reasons.

**Verdict:** ⚠️ Adequate for binary filtering. Missing suitability grading.

### Q7: What are the CAPEX implications?

| Schema Coverage | Fields | Adequacy |
|----------------|--------|----------|
| *(No cost-related fields exist)* | | ❌ Gap |
| *(No OPEX-related fields exist)* | | ❌ Gap |

**Gap:** This is the biggest deficiency. The Cost Database (separate schema) stores project-specific cost data, but the Technology Card has no technology-level cost ranges, no typical €/kW ranges, no cost driver analysis, and no OEM pricing landscape. A feasibility agent answering "what are the CAPEX implications of choosing PEM vs Alkaline?" must query the Cost Database but has no technology-anchored cost context.

**Verdict:** ❌ Critical gap. A `cost_profile` block is needed with technology-level CAPEX and OPEX reference ranges.

---

## 2. Schema v1.1 Recommended Changes

### 2.1 New Block: `technical_risks`

A dedicated risk block for technology-inherent risks (not project-specific, which is covered by the Risk Database).

```json
"technical_risks": [
  {
    "risk_id": "TCR-PEM-001",
    "risk_name": "string",
    "risk_category": "degradation | supply_chain | performance | integration | safety",
    "probability": "low | moderate | high",
    "impact": "minor | moderate | major | critical",
    "description": "string",
    "mitigation_approaches": ["string"],
    "relevant_project_evidence": ["project_id references"]
  }
]
```

### 2.2 New Block: `cost_profile`

Technology-level CAPEX and OPEX reference ranges sourced from IEA/IRENA/industry benchmarks.

```json
"cost_profile": {
  "capex_eur_per_kw": {
    "typical_range_low": 0,
    "typical_range_high": 0,
    "source": "IEA GHR 2025",
    "source_reliability": "high",
    "year_of_estimate": 2025,
    "notes": "string",
    "scale_dependency": "high | medium | low"
  },
  "opex_breakdown": {
    "electricity_share_percent": 0,
    "maintenance_share_percent": 0,
    "stack_replacement_share_percent": 0,
    "water_share_percent": 0,
    "other_share_percent": 0
  },
  "stack_replacement_cost_eur_per_kw": 0,
  "stack_replacement_interval_hours": 0,
  "learning_rate_percent_per_doubling": 0,
  "cost_drivers": ["string"],
  "cost_reduction_trajectory": "string"
}
```

### 2.3 New Block: `deployment_evidence`

Quantitative deployment data to support "has this been done before?" reasoning.

```json
"deployment_evidence": {
  "number_of_operational_plants_total": 0,
  "number_of_plants_above_10mw": 0,
  "number_of_plants_above_100mw": 0,
  "total_global_operating_hours_estimated": "string",
  "oldest_operating_plant_year": 0,
  "regions_with_deployment": ["string"],
  "major_oems": [
    {
      "name": "string",
      "headquarters_country": "string",
      "max_stack_size_mw": 0,
      "gigafactory_annual_capacity_mw": 0
    }
  ]
}
```

### 2.4 Enhanced Field: `applications.suitability_scores`

Replace simple suited/unsuited with graded assessment.

```json
"applications": {
  "suitability_per_application": [
    {
      "application": "steel",
      "suitability": "high | medium | low | not_recommended",
      "rationale": "string",
      "reference_project_ids": ["string"]
    }
  ]
}
```

### 2.5 Field: `CAPEX implications` — Covered by new `cost_profile` block

---

## 3. Impact Assessment

| Change | Impact on Existing Data | Migration Complexity | Priority |
|--------|------------------------|---------------------|----------|
| Add `technical_risks` block | None (new block) | Low | P1 — Critical for feasibility reasoning |
| Add `cost_profile` block | None (new block) | Low | P1 — Critical for CAPEX reasoning |
| Add `deployment_evidence` block | None (new block) | Low | P2 — Important for scale reasoning |
| Enhance `applications` block | Existing `primary_applications` and `unsuitable_applications` remain; new `suitability_scores` is additive | Low | P2 — Improves decision support |
| All changes | All additive | Low | — |

---

## 4. Recommendation

**Adopt Schema v1.1 immediately.** All changes are additive — no fields are removed or reclassified. The three new blocks (`technical_risks`, `cost_profile`, `deployment_evidence`) close critical gaps for feasibility agent reasoning. The enhanced `applications` block improves decision-support granularity.

The v1.1 Technology Cards built in Phase 2 (PEM) and Phase 3 (Alkaline) should use this enhanced schema.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Hydrogen Technology Expert | Initial schema review and v1.1 recommendations |

---

*This review confirms that the Technology Card Schema v1.0 is well-designed for basic technology lookup but requires the addition of risk, cost, and deployment evidence blocks to support full Technical Feasibility Agent reasoning.*
