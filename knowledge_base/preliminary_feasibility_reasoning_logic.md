# Preliminary Feasibility Agent — Reasoning Logic v1.0

**Document:** Assessment Logic Specification
**Date:** 2026-06-05
**Author:** Senior Hydrogen Project Consultant & PMO Lead

---

## 1. Reasoning Principles

| Principle | Implementation |
|-----------|---------------|
| **Evidence-first** | Every assessment statement must cite a source. If no source exists, flag as a knowledge gap. |
| **Confidence-calibrated** | Communication of certainty matches the underlying evidence quality. Class D data is never presented with Class C confidence. |
| **Technology-differentiated** | PEM and Alkaline assessments use different reference data, risk profiles, and cost benchmarks. No generic "electrolyzer" assessment. |
| **Scale-aware** | Costs, risks, and technology suitability are assessed at the queried scale, not a generic "all scales" answer. |
| **Gap-transparent** | What is NOT known is as important as what IS known. Every report section includes explicit gap identification. |

---

## 2. Technology Assessment Logic

### 2.1 Maturity Assessment

```
IF technology = "PEM":
  TRL = 8 (TC-PEM-001 §maturity)
  Commercial maturity = "early_commercial"
  Largest plant = 200 MW (Normand'Hy GA-PR-001, under construction)
  Operational plants >10 MW = 15 (TC-PEM-001 §deployment_evidence)
  Assessment: "PEM is commercially deployed at >100 MW scale. At {capacity_mw} MW, the project is {within/beyond} proven scale."

IF technology = "Alkaline":
  TRL = 9 (TC-ALK-001 §maturity)
  Commercial maturity = "mature"
  Largest plant = 200 MW (Holland Hydrogen I GA-PR-003, under construction); >300 MW in chlor-alkali
  Operational plants >10 MW = 50+ (TC-ALK-001 §deployment_evidence)
  Assessment: "Alkaline is a fully mature technology. At {capacity_mw} MW, the project is {within/beyond} proven scale for dedicated green hydrogen."
```

### 2.2 Application Suitability

```
RETRIEVE suitability_per_application[{industry}] from Technology Card

IF suitability = "high":
  "This technology is well-suited for {industry}. {rationale from card}. Reference projects: {reference_project_ids}."
IF suitability = "medium":
  "This technology is adequate for {industry} but has limitations. {rationale}. Alternative: consider {other technology} for comparison."
IF suitability = "low":
  "This technology has significant limitations for {industry}. {rationale}. Strongly recommend evaluating {other technology}."
IF industry not covered:
  FLAG as knowledge gap. "The Technology Card does not assess suitability for '{industry}'. This is a knowledge base gap."
```

### 2.3 Scale Assessment

```
IF query.capacity_mw <= technology_card.scalability.max_plant_size_known_mw:
  "The project scale ({capacity_mw} MW) is within proven deployment range."
  IF query.capacity_mw > technology_card.scalability.max_plant_size_under_construction_mw:
    "However, no plant of exactly this scale is operational. The largest under construction is {max_under_construction} MW."

IF query.capacity_mw > technology_card.scalability.max_plant_size_known_mw:
  "WARNING: The project scale ({capacity_mw} MW) exceeds the largest known deployment ({max_known} MW). This would be first-of-a-kind at this scale. Apply FOAK premium to costs and risks."
```

---

## 3. Risk Assessment Logic

### 3.1 Risk Filtering

```
FOR each risk in RiskLibrary:
  PASS_filter = TRUE
  
  IF risk.applicability.technology_types does NOT contain query.technology:
    PASS_filter = FALSE
  
  IF query.capacity_mw NOT IN risk.applicability.project_scale range:
    PASS_filter = FALSE
  
  IF risk.applicability.first_of_a_kind_only = TRUE AND project is NOT FOAK:
    PASS_filter = FALSE
  
  IF PASS_filter:
    ADD to filtered_risks

SORT filtered_risks by RPN descending
GROUP by risk_category
```

### 3.2 Risk Presentation Logic

```
FOR each category:
  SELECT top 2 risks by RPN
  
  FOR each selected risk:
    PRESENT risk_name + RPN + risk_class
    EXPLAIN why this risk matters for THIS project (contextualize)
    PRESENT consequences summary
    PRESENT mitigation summary (preventive + corrective actions)
    CITE reference projects where this risk was observed
    IF no reference project evidence exists:
      FLAG: "No Gold Dataset project evidence for this risk. Assessment based on Technology Card / industry reports."
```

### 3.3 Risk Severity Contextualization

The same risk (e.g., RK-GRD-001 Grid Connection Delay, RPN 32) has different implications depending on project context:

```
IF query site is brownfield:
  "Risk is REDUCED — brownfield sites with existing grid connections (HGHH/Moorburg model) significantly mitigate this risk."
IF query country has known grid congestion (Netherlands, Germany):
  "Risk is ELEVATED — {country} has documented grid congestion in industrial zones."
IF query capacity >200 MW:
  "Risk is ELEVATED — at this scale, grid connection requires dedicated HV substation (HH1/TenneT model)."
```

---

## 4. Cost Assessment Logic

### 4.1 Cost Record Selection

```
FOR each cost category:
  SELECT cost records WHERE:
    context.technology_type = query.technology (or "technology_agnostic")
    AND context.project_scale_mw is closest to query.capacity_mw
  
  IF multiple records match:
    PREFER records with project_reference_id (project-specific) over generic benchmarks
    PREFER records with higher confidence level
```

### 4.2 Scaling Logic

```
FOR each selected cost record:
  IF record.scale_is_extrapolated = false AND record matches query scale exactly:
    USE as-is
  ELSE:
    SCALE using power law: Cost_target = Cost_reference × (Scale_target / Scale_reference)^n
    Where n = category-specific exponent from cost_scaling_methodology.md §2.2
    
    IF extrapolation factor > 3×:
      FLAG: "Extrapolation warning — cost scaled {factor}× from reference. Apply wider uncertainty range."
      WIDEN range by +10% per 1× beyond 3×
    
    IF extrapolation factor > 10×:
      FLAG: "Extreme extrapolation — cost scaled {factor}×. Estimate is CLASS D (speculative)."
      DOWNGRADE confidence to D
```

### 4.3 Learning Curve Adjustment

```
IF query.target_cod ≥ 2028:
  CALCULATE doublings = log₂(cumulative_capacity_target_year / cumulative_capacity_2025)
  APPLY: Cost_target_year = Cost_2025 × (1 - learning_rate)^doublings
  
  PEM: learning_rate = 0.15, 2025 cumulative = 4.5 GW
  ALK: learning_rate = 0.10, 2025 cumulative = 8 GW
  
  IF target_cod > 2030:
    FLAG: "Learning curve projection beyond 2030 carries high uncertainty."
```

### 4.4 CAPEX Range and Confidence

```
FOR each category:
  COMPUTE category_central = scaled + learning-adjusted cost
  COMPUTE category_low = category_central × (record.eur_per_kw_low / record.eur_per_kw)
  COMPUTE category_high = category_central × (record.eur_per_kw_high / record.eur_per_kw)

AGGREGATE:
  Total_central = Σ category_central
  Total_low = Σ category_low  (Note: simple sum — assumes independent categories, which is conservative)
  Total_high = Σ category_high

COMPUTE weighted_confidence = Σ(category_cost × class_weight) / Σ(category_cost)
  Class weights: A=1.0, B=0.80, C=0.60, D=0.40

PRESENT as: "€{total_low}M – €{total_central}M – €{total_high}M (P10–P50–P90)"
```

---

## 5. Evidence Quality Logic

### 5.1 Source Aggregation

```
COLLECT all sources from all four pipelines
DE-DUPLICATE by source_id
FOR each unique source:
  ASSIGN quality_level (A/B/C/D)
  ASSIGN reliability_score (1-5)
  COUNT citations (how many report sections cite this source)
```

### 5.2 Evidence Quality Assessment

```
COMPUTE evidence_score = Σ(level_weight × reliability_score) / count(unique_sources)
  Level weights: A=1.0, B=0.8, C=0.5, D=0.2

CATEGORIZE:
  ≥ 0.80: EXCELLENT — "Assessment is supported by multiple official/primary sources."
  0.60-0.79: GOOD — "Assessment is supported by authoritative industry sources and project data."
  0.40-0.59: ADEQUATE — "Assessment relies primarily on industry benchmarks. Limited project-specific data."
  < 0.40: LIMITED — "Assessment is based on analyst estimates. Significant uncertainty. Primary data collection recommended."

IDENTIFY weakest dimension:
  WHICH pipeline has the lowest average source quality?
  FLAG for focused data collection
```

### 5.3 Knowledge Gap Detection

```
CHECKLIST:
  □ Is there at least one Gold Dataset project with the same technology AND industry?
  □ Is the project scale within proven deployment range?
  □ Is there a Class A or B cost data point for the dominant cost category?
  □ Are all identified High/Critical risks linked to at least one Gold Dataset project?
  □ Does the Technology Card have a suitability assessment for this industry?
  □ Is the target country represented in the Gold Dataset?
  □ Are there operational projects (not just planned) at this technology + scale?

FOR each unchecked item:
  ADD to §7 Knowledge Gaps with explanation and recommended action
```

---

## 6. Report Composition Logic

### 6.1 Executive Summary Construction

```
COMPOSE §1 from:
  - Project profile (1 sentence)
  - Technology readiness verdict (1 sentence)
  - Top 3 reference projects (1 sentence)
  - Top 3 risks (1 sentence)
  - CAPEX range (1 sentence)
  - Evidence quality (1 sentence)
  - Critical knowledge gaps (1 sentence)
  - Disclaimer (mandatory)
```

### 6.2 Gap-Driven Recommendations

```
FOR each gap in §7:
  GENERATE recommended action:
    "□ Conduct {data_collection / feasibility_study / OEM_engagement} to address {gap_description}"
  PRIORITIZE by gap impact:
    HIGH: Gap prevents meaningful feasibility assessment
    MEDIUM: Gap reduces confidence in specific dimension
    LOW: Gap is minor; can be addressed in later phase
```

---

## 7. Anti-Patterns — What the Agent Must Never Do

| Anti-Pattern | Why Forbidden | Detection Rule |
|-------------|---------------|---------------|
| "This project is feasible" | Agent does not make approval decisions | Output must never contain "feasible", "not feasible", "go", "no-go" |
| "Feasibility score: 7.2/10" | Scoring methodology not defined | Output must never contain numeric scores |
| "CAPEX will be €147,350,000" | False precision; single-point estimate | CAPEX must always be presented as range with confidence class |
| "We recommend PEM over Alkaline" | Agent does not make technology recommendations | May present comparison data; may NOT recommend one technology |
| Invented risk not in Risk Library | Violates source traceability | All risks must have a Risk Library RK-ID |
| Cost not traceable to a source | Violates source traceability | All costs must cite a Cost Library CS-ID or source |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Hydrogen Project Consultant & PMO Lead | Initial reasoning logic specification |
