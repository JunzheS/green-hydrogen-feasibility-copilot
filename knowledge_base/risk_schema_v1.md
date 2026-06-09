# Risk Record Schema v1 — Green Hydrogen Projects

**Document:** Risk Record Structure Specification
**Date:** 2026-06-05
**Author:** Senior Project Risk Manager & PMO Director
**Schema Version:** 1.0.0
**Parent Architecture:** database_architecture_v1.1.md §6
**Taxonomy Reference:** risk_taxonomy_framework.md
**Replaces:** database_architecture.md §6.3 (v1.0) — enhanced with PMO-grade fields

---

## 1. Schema Evolution (v1.0 → v1.0 PMO)

The v1.0 Risk Database schema in the original architecture was a general-purpose risk container. This v1.0 PMO-enhanced schema adds:

| Enhancement | Rationale |
|-------------|-----------|
| **Structured root cause + trigger events** | Enables future automated risk detection by the Risk Agent |
| **Detectability dimension** | Completes the PMI-standard FMEA triad: Probability × Impact × Detectability |
| **Multi-dimensional consequence analysis** | Separates schedule, cost, performance, safety, and reputation impacts |
| **Residual risk scoring** | Tracks risk after mitigation, enabling risk reduction effectiveness measurement |
| **Structured monitoring indicators** | Enables the Risk Agent to monitor trigger conditions against project data |
| **Risk review cadence** | Ties into project governance cycle |
| **Integration hooks** | Explicit FK links to Technology Cards, Project References, and Cost Library |

---

## 2. Schema Definition

### 2.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `risk_id` | `string` | Unique identifier. Format: `RK-{CATEGORY_ABBR}-{NNN}`. Category abbreviations: TEC (Technical), SCP (Supply Chain), GRD (Grid & Energy), REG (Regulatory), FIN (Financial), CST (Construction), OPS (Operational), ENV (Environmental). Example: `RK-TEC-001` | **Yes** |
| 2 | `risk_name` | `string` | Concise, descriptive risk name (max 120 chars). Written as a negative outcome statement. Example: "PEM Stack Degradation Exceeding Warranty Rate Under Dynamic Operation" | **Yes** |
| 3 | `risk_category` | `enum` | Top-level category per risk_taxonomy_framework.md §2. Values: `technical`, `supply_chain`, `grid_energy`, `regulatory`, `financial`, `construction`, `operational`, `environmental` | **Yes** |
| 4 | `risk_subcategory` | `enum` | Subcategory code + name from the taxonomy. Values: e.g., `01.1_electrolyzer_performance`, `03.4_electricity_price_volatility`. Complete list in risk_taxonomy_framework.md §3-10. | **Yes** |
| 5 | `risk_version` | `string` | Semantic version (e.g., `1.0.0`). Increment on significant reassessment. | **Yes** |
| 6 | `risk_status` | `enum` | `draft` \| `reviewed` \| `published` \| `superseded` \| `archived`. Follows standard knowledge base lifecycle. | **Yes** |
| 7 | `supersedes` | `string` | Previous risk_id if this risk replaces an older version | No |
| 8 | `last_review_date` | `string` | ISO 8601 date of last risk review | **Yes** |
| 9 | `next_review_date` | `string` | ISO 8601 date of scheduled next review. Default: last_review_date + 6 months. | No |

### 2.2 Risk Description Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 10 | `description.summary` | `string` | 2-3 sentence risk summary suitable for executive reporting | **Yes** |
| 11 | `description.detailed` | `string` | Full description (max 2000 chars): what could happen, how, and why it matters | **Yes** |
| 12 | `description.root_cause` | `string` | The underlying cause(s) that enable this risk. Separated from the trigger for future agent reasoning. Example: "Global iridium supply is a byproduct of platinum mining with inelastic production capacity." | No |
| 13 | `description.trigger_events` | `string[]` | Observable events or conditions that would indicate the risk is materializing. Machine-readable for future automated detection. Example: `["Iridium spot price exceeds $5,000/toz for >30 consecutive days", "Major South African PGM mine announces production cut >10%"]` | No |

### 2.3 Risk Assessment Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 14 | `assessment.probability` | `integer` | 1-5 scale per risk_scoring_methodology.md. 1=Rare (<5%), 2=Unlikely (5-15%), 3=Possible (15-35%), 4=Likely (35-65%), 5=Almost Certain (>65%) | **Yes** |
| 15 | `assessment.probability_rationale` | `string` | Justification for probability rating, citing evidence where available | No |
| 16 | `assessment.impact` | `integer` | 1-5 scale per risk_scoring_methodology.md. 1=Negligible, 2=Minor, 3=Moderate, 4=Major, 5=Critical | **Yes** |
| 17 | `assessment.impact_rationale` | `string` | Justification for impact rating | No |
| 18 | `assessment.detectability` | `integer` | 1-5 scale. 1=Almost certain to detect before impact, 2=High chance, 3=Moderate, 4=Low, 5=Very low/undetectable until too late | **Yes** |
| 19 | `assessment.detectability_rationale` | `string` | How and when this risk could be detected | No |
| 20 | `assessment.risk_priority_number` | `integer` | RPN = Probability × Impact × Detectability. Range: 1-125. Computed field. | **Yes** |
| 21 | `assessment.risk_class` | `enum` | `low` \| `medium` \| `high` \| `critical`. Derived from RPN per risk_scoring_methodology.md thresholds. | **Yes** |
| 22 | `assessment.assessment_method` | `string` | e.g., "Expert elicitation (Delphi, 2 rounds, 5 SMEs)", "FMEA workshop", "Monte Carlo simulation", "Industry benchmark analysis" | No |
| 23 | `assessment.assessment_date` | `string` | ISO 8601 date of this assessment | **Yes** |
| 24 | `assessment.assessed_by` | `string` | Person, role, or organization performing the assessment | No |

### 2.4 Residual Risk Block (Post-Mitigation)

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 25 | `residual.probability` | `integer` | Post-mitigation probability (1-5) | No |
| 26 | `residual.impact` | `integer` | Post-mitigation impact (1-5) | No |
| 27 | `residual.detectability` | `integer` | Post-mitigation detectability (1-5) | No |
| 28 | `residual.risk_priority_number` | `integer` | Post-mitigation RPN. If lower than assessment RPN, mitigation is effective. | No |
| 29 | `residual.risk_class` | `enum` | Post-mitigation risk class | No |

### 2.5 Applicability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 30 | `applicability.technology_types` | `enum[]` | `PEM`, `Alkaline`, or `both`. Which electrolysis technologies does this risk apply to? | **Yes** |
| 31 | `applicability.project_scale` | `enum[]` | `any` \| `small_<10mw` \| `medium_10-100mw` \| `large_100-500mw` \| `very_large_>500mw` | **Yes** |
| 32 | `applicability.project_phases` | `enum[]` | `pre_feasibility` \| `feasibility` \| `feed` \| `construction` \| `commissioning` \| `operations` \| `all_phases` | **Yes** |
| 33 | `applicability.regions` | `enum[]` | Regions where this risk is particularly relevant. Values from Project Reference Schema. Default: `["all"]`. | No |
| 34 | `applicability.first_of_a_kind_only` | `boolean` | Is this risk specific to first-of-a-kind projects? Default: `false`. | No |
| 35 | `applicability.project_type` | `enum[]` | `greenfield` \| `brownfield` \| `expansion`. Default: `["greenfield", "brownfield", "expansion"]`. | No |

### 2.6 Multi-Dimensional Consequence Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 36 | `consequences.schedule.impact` | `enum` | `none` \| `<1_month` \| `1-3_months` \| `3-6_months` \| `6-12_months` \| `>12_months` | **Yes** |
| 37 | `consequences.schedule.description` | `string` | Narrative of schedule impact | No |
| 38 | `consequences.cost.impact_eur` | `number` | Estimated financial impact if risk materializes (EUR). Best estimate (P50). | No |
| 39 | `consequences.cost.description` | `string` | Narrative of cost impact, including breakdown if available | No |
| 40 | `consequences.performance.description` | `string` | Impact on H₂ output (kg/day), plant availability (%), or system efficiency (kWh/kg) | No |
| 41 | `consequences.safety.impact` | `enum` | `none` \| `minor_injury` \| `major_injury` \| `fatality_risk` \| `multiple_fatality_risk` | No |
| 42 | `consequences.safety.description` | `string` | Narrative of safety consequences | No |
| 43 | `consequences.reputation.description` | `string` | Impact on developer reputation, community relations, or industry standing | No |
| 44 | `consequences.regulatory.description` | `string` | Regulatory consequences: fines, permit revocation, certification loss, legal action | No |
| 45 | `consequences.worst_case_scenario` | `string` | Plausible worst-case outcome description | No |
| 46 | `consequences.cascading_risk_ids` | `string[]` | FK references to other risk entries that may be triggered if this risk materializes | No |

### 2.7 Mitigation Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 47 | `mitigation.strategy` | `enum` | `avoid` \| `reduce` \| `transfer` \| `accept` \| `contingency`. Standard ISO 31000 risk treatment strategies. | **Yes** |
| 48 | `mitigation.strategy_rationale` | `string` | Why this strategy was chosen | No |
| 49 | `mitigation.risk_owner` | `string` | Role or entity accountable for managing this risk. Example: "EPC Contractor", "Developer (Procurement)", "Operations Manager". | **Yes** |

#### Mitigation Actions Array

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 50 | `mitigation.preventive_actions[]` | `object[]` | Actions that reduce probability (preventive) | No |
| 50a | `preventive_actions[].action_id` | `string` | Unique action identifier. Format: `MIT-{RISK_ID}-P-{NN}`. Example: `MIT-TEC-001-P-01` | **Yes** |
| 50b | `preventive_actions[].description` | `string` | What will be done | **Yes** |
| 50c | `preventive_actions[].responsible_party` | `string` | Who is responsible | No |
| 50d | `preventive_actions[].timing` | `enum` | When in the project lifecycle: `pre_fid` \| `pre_construction` \| `during_construction` \| `pre_commissioning` \| `during_operations` \| `ongoing` | No |
| 50e | `preventive_actions[].cost_eur` | `number` | Estimated cost to implement (EUR) | No |
| 50f | `preventive_actions[].status` | `enum` | `planned` \| `in_progress` \| `completed` \| `deferred` | No |

| 51 | `mitigation.corrective_actions[]` | `object[]` | Actions that reduce impact if risk materializes (corrective/contingency). Same sub-schema as preventive_actions. | No |

| 52 | `mitigation.monitoring_indicators[]` | `object[]` | Observable metrics to track risk status | No |
| 52a | `monitoring_indicators[].indicator` | `string` | What to monitor. Example: "Iridium spot price (USD/toz, monthly average)" | **Yes** |
| 52b | `monitoring_indicators[].threshold_green` | `string` | Normal range. Example: "<$3,000/toz" | No |
| 52c | `monitoring_indicators[].threshold_amber` | `string` | Warning range. Example: "$3,000-$5,000/toz" | No |
| 52d | `monitoring_indicators[].threshold_red` | `string` | Action required. Example: ">$5,000/toz" | No |
| 52e | `monitoring_indicators[].current_value` | `string` | Latest observed value (updated at review) | No |
| 52f | `monitoring_indicators[].last_updated` | `string` | ISO 8601 date of last update | No |

### 2.8 Evidence & Reference Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 53 | `evidence.reference_project_ids` | `string[]` | FK → Gold Dataset project IDs where this risk was observed. Example: `["GA-PR-001", "GA-PR-008"]` | No |
| 54 | `evidence.incident_descriptions` | `string[]` | Brief factual descriptions of real incidents in reference projects | No |
| 55 | `evidence.lessons_learned` | `string` | Key lessons from real project experiences | No |
| 56 | `evidence.frequency_observed` | `string` | Qualitative frequency. Example: "Observed in 3 of 18 reference PEM projects >20 MW with >3 years operational data (~17%)" | No |
| 57 | `evidence.technology_card_references` | `string[]` | FK → Technology Card IDs (e.g., `["TC-PEM-001"]`) where this risk is documented as a technology-inherent risk | No |
| 58 | `evidence.industry_standards` | `string[]` | Relevant standards. Example: `["ISO 31000:2018", "IEC 62282-8-101"]` | No |

### 2.9 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 59 | `sources` | `object[]` | Array of source references. Inherits from Project Reference Schema §4.2.13 source sub-schema + adds `source_quality_level` and `source_reliability_score` from Source Governance Framework. | **Yes** |

### 2.10 Knowledge Base Integration Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 60 | `integration.related_risk_ids` | `string[]` | FK references to related risks (cascading, correlated, or similar risks in the library). Bidirectional — if A references B, B should reference A. | No |
| 61 | `integration.cost_library_references` | `string[]` | FK → Cost Library entries providing cost data for mitigation actions or consequence estimates | No |

### 2.11 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 62 | `rag_metadata.text_for_embedding` | `string` | Auto-generated concatenation for vector search. Template: `{risk_name}. Category: {risk_category} > {risk_subcategory}. Probability: {P}/5, Impact: {I}/5, Detectability: {D}/5, RPN: {RPN}. Class: {risk_class}. Applies to: {technology_types} at {project_scale} in {project_phases}. Consequences: {consequences.schedule.impact} schedule, {consequences.cost.impact_eur} EUR. Mitigation: {mitigation.strategy}. Evidence from {evidence.reference_project_ids}. Keywords: {keywords}.` | **Yes** |
| 63 | `rag_metadata.keywords` | `string[]` | Controlled-vocabulary keywords for hybrid search | **Yes** |
| 64 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last embedding pipeline run | No |

---

## 3. Mandatory Field Summary

The following 22 fields MUST be populated for a risk record to reach `published` status:

1. `risk_id`
2. `risk_name`
3. `risk_category`
4. `risk_subcategory`
5. `risk_version`
6. `risk_status`
7. `last_review_date`
8. `description.summary`
9. `description.detailed`
10. `assessment.probability`
11. `assessment.impact`
12. `assessment.detectability`
13. `assessment.risk_priority_number` (computed)
14. `assessment.risk_class` (computed)
15. `assessment.assessment_date`
16. `applicability.technology_types`
17. `applicability.project_scale`
18. `applicability.project_phases`
19. `consequences.schedule.impact`
20. `mitigation.strategy`
21. `mitigation.risk_owner`
22. `sources[]` (at minimum: source_id, source_type, title, confidence)

---

## 4. Field Cross-Reference with v1.0 Schema

This table maps the database_architecture.md §6.3 (v1.0) fields to this v1.0 PMO schema:

| v1.0 Field | v1.0 PMO Field | Change |
|-----------|----------------|--------|
| 1 `risk_id` | 1 `risk_id` | Unchanged |
| 2 `risk_name` | 2 `risk_name` | Unchanged |
| 4 `risk_category` | 3 `risk_category` | Enum values updated to match 8-category taxonomy |
| 5 `risk_subcategory` | 4 `risk_subcategory` | Enum values updated to coded subcategories |
| 8 `assessment.probability_qualitative` | 14 `assessment.probability` | Converted to integer 1-5 for RPN calculation |
| 9 `assessment.probability_quantitative_percent` | Removed (merged into rationale) | Quantitative % moved to rationale for flexibility |
| 10 `assessment.impact_qualitative` | 16 `assessment.impact` | Converted to integer 1-5 for RPN calculation |
| 11 `assessment.impact_cost_eur` | 38 `consequences.cost.impact_eur` | Moved to multi-dimensional consequence block |
| 12 `assessment.impact_schedule_months` | 36 `consequences.schedule.impact` | Moved to multi-dimensional consequence block |
| 13 `assessment.risk_score` | 20 `assessment.risk_priority_number` | Extended to P×I×D (was P×I only) |
| 14 `assessment.risk_level` | 21 `assessment.risk_class` | Renamed; thresholds updated for 1-125 scale |
| — (new) | 18 `assessment.detectability` | NEW — PMO-standard FMEA third dimension |
| — (new) | 25-29 `residual.*` | NEW — post-mitigation risk tracking |
| — (new) | 52 `mitigation.monitoring_indicators[]` | NEW — enables risk monitoring automation |
| — (new) | 57 `evidence.technology_card_references` | NEW — FK link to Technology Cards |
| — (new) | 60-61 `integration.*` | NEW — cross-entity integration hooks |

All existing v1.0 fields are preserved (some reorganized/moved). No v1.0 data would be lost in migration — only new structured fields are added.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Project Risk Manager & PMO Director | Initial PMO-enhanced risk record schema |

---

*This schema extends the original risk database design with PMO-grade structure: FMEA triad scoring, residual risk tracking, monitoring indicators, multi-dimensional consequences, and explicit integration hooks to the Technology Cards and Gold Dataset. It is designed to support future Risk Agent automated reasoning.*
