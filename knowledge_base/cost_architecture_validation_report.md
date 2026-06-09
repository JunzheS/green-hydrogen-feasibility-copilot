# Cost Architecture Validation Report — M7B Final

**Document:** Comprehensive Architecture Validation
**Date:** 2026-06-05
**Author:** Senior Cost Engineer, Project Controls Manager & Knowledge Validation Lead
**Scope:** All M7A Cost Architecture deliverables + M7B validation tests
**Decision:** Go / No-Go for Cost Library Construction

---

## 1. Executive Summary

The Cost Knowledge Architecture (M7A) has been subjected to 6 validation tests (M7B) against realistic pre-feasibility scenarios. The architecture demonstrates strong reasoning capability, appropriate uncertainty communication, and adequate source traceability.

**RECOMMENDATION: CONDITIONAL GO for Cost Library Construction.**

Conditions:
1. Mitigate GAP-C1 (scaling exponent uncertainty documentation) before Sprint 1 begins
2. Schedule M7C milestone for OPEX/LCOH integration (GAP-C2)
3. Resolve 5 important gaps during Cost Library Sprint 1

---

## 2. Validation Test Results

| # | Test | Key Finding | Status |
|---|------|------------|--------|
| 1 | **Cost Explainability** | Architecture successfully explains WHY a 100 MW PEM plant costs ~€160M across 4 layers (total→category→driver→narrative). Every category has a traceable cost driver chain. | ✅ PASS |
| 2 | **Scale Sensitivity** | Per-category power law scaling with documented exponents produces logically consistent results across 20/100/300 MW for both technologies. Diminishing returns correctly captured. | ✅ PASS |
| 3 | **Technology Comparison** | PEM vs Alkaline cost differential correctly identified at category level. Architecture recognizes scenarios where higher-cost PEM wins on total system cost (mobility offtake, space constraints). | ✅ PASS |
| 4 | **Uncertainty** | Confidence framework prevents false precision. Class system correctly downgrades extrapolated data. Weighted confidence aggregation prevents hidden low-confidence components. | ✅ PASS |
| 5 | **Traceability** | 10/10 cost assumptions have identifiable source chains. 60% fully traceable to primary sources. 40% partially traceable (judgment-based parameters with reference class support). No untraceable assumptions. | ✅ PASS |
| 6 | **Gap Analysis** | 2 critical, 5 important, 4 optional gaps identified. All mitigatable within Sprint 1-2 timeline. | ⚠️ PASS WITH CONDITIONS |

---

## 3. Architecture Strengths

### S1: Multi-Layered Explainability

The architecture enables cost explanation at four layers:
- **Layer 1 (Total):** "Your plant will cost ~€150-200M"
- **Layer 2 (Category):** "€48M for electrolyzer, €44M for indirect, €21M for electrical..."
- **Layer 3 (Driver):** "The stack cost drives this because PEM uses iridium at €150K/kg..."
- **Layer 4 (Decision):** "If you choose a brownfield site, you save €14M on electrical + civil"

This layered approach means the architecture supports both executive summaries and detailed engineering review — essential for a multi-audience Copilot.

### S2: Technology-Differentiated Cost Decomposition

The architecture correctly identifies 5 of 8 cost categories as technology-dependent and quantifies the differential with documented reasoning. It does NOT simply say "PEM costs more" — it explains that PEM's stack premium (€15M) is partially offset by compression savings (€2M) and civil savings (€2M), yielding a net €19M (13%) premium at 100 MW.

### S3: AACE-Aligned Confidence Framework

The 5-class confidence system maps directly to AACE International estimate classes. This is critical for industrial credibility — project controllers and lenders use AACE classification. The architecture speaks their language.

### S4: Honest Uncertainty Communication

The framework's greatest strength is its honesty. When no Class A/B data exists (typical for hydrogen in 2026), it produces Class C estimates with ±20-30% ranges. It does not invent precision. A Cost Agent built on this framework will never produce "€159,347,000" — it will produce "€128-208M, weighted confidence 0.60 (Medium)."

### S5: Source Traceability as a Design Principle

Every cost assumption has a traceability chain: estimate → intermediate source → primary source → evidence class. The framework enforces this through mandatory source fields and confidence classification. 60% of tested assumptions are fully traceable; the remaining 40% are judgment-based parameters that CANNOT be fully sourced regardless of architecture quality.

### S6: Gap Self-Awareness

The architecture identifies its own limitations: scaling exponents are based on chemical industry analogs, not hydrogen-specific data; FOAK premiums are judgment-based; the C/D confidence boundary is subjective. This self-awareness is itself an architectural strength — it prevents overconfidence.

---

## 4. Architecture Weaknesses

### W1: No OPEX/LCOH Integration (CRITICAL)

**Impact:** A Cost Agent that only covers CAPEX answers "what does it cost to build?" but not "what does it cost to produce hydrogen?" For pre-feasibility, LCOH is the more important metric — it determines project viability.

**Mitigation:** M7C milestone required before Feasibility Agent development (M9+). OPEX categories already defined in Technology Cards (TC-PEM-001, TC-ALK-001 §cost_profile.opex_breakdown) — these provide the foundation.

### W2: Scaling Exponents Not Empirically Calibrated (CRITICAL)

**Impact:** The power law exponents are based on general chemical engineering references, not hydrogen project data. At 3× scale extrapolation, a 0.05 exponent error produces ~5% cost error — material for pre-feasibility.

**Mitigation:** Document exponent uncertainty explicitly. Use ranges (n=0.40 ±0.10). Flag all scaling operations as "chemical industry analog — pending hydrogen-specific calibration."

### W3: Regional Multipliers Are Qualitative (IMPORTANT)

The taxonomy mentions regional cost variation but has no structured database. A Cost Agent answering "Saudi Arabia vs. Germany" must rely on analyst judgment rather than systematic factors.

### W4: No Automated Aggregation Logic (IMPORTANT)

The schema defines individual cost records but has no structure for "benchmark sets" — complete plant estimates. A Cost Agent must aggregate multiple records, and the aggregation rules (interaction effects, scope overlap prevention) are not specified.

### W5: Cost Basis Translation Not Automated (IMPORTANT)

The framework defines cost basis levels (equipment_only → installed_cost → epc_total → all_in) but translating between them requires analyst judgment. A Cost Agent aggregating an "equipment_only" stack cost with an "installed_cost" civil cost must add installation factors manually.

---

## 5. Readiness Assessment by Agent Capability

| Future Capability | Architecture Ready? | Confidence |
|------------------|--------------------|------------|
| Explain costs (why does category X cost Y?) | ✅ YES | HIGH — multi-layered explainability demonstrated |
| Compare technologies (PEM vs Alkaline) | ✅ YES | HIGH — technology-differentiated decomposition |
| Compare scales (20 vs 100 vs 300 MW) | ✅ YES | MEDIUM — scaling methodology works but exponents need calibration |
| Communicate uncertainty (range, not point) | ✅ YES | HIGH — confidence framework validated |
| Provide traceable evidence | ✅ YES | HIGH — 100% of tested assumptions have source chains |
| Estimate total CAPEX for a project profile | ✅ YES | MEDIUM — aggregation logic needs specification |
| Adjust for region (Europe vs MENA vs China) | ⚠️ PARTIAL | LOW-MEDIUM — qualitative multipliers only |
| Project costs to future year (2028, 2030) | ⚠️ PARTIAL | MEDIUM — learning curves defined but manual |
| Estimate OPEX/LCOH | ❌ NO | N/A — out of scope (requires M7C) |
| Recommend cost optimization | ❌ NO | N/A — out of scope (future Cost Agent reasoning) |

---

## 6. Cost Library Construction Readiness

### 6.1 What IS Ready for Population

| Cost Category | Data Availability | Confidence Level Expected |
|--------------|------------------|--------------------------|
| 01 Electrolyzer System | IEA/IRENA benchmarks, TC cost profiles, Gold Dataset project CAPEX | Class C (benchmark-dominated) |
| 02 Electrical Infrastructure | IEA grid reports, Gold Dataset evidence (HH1, HGHH) | Class C-D |
| 03 Water Systems | IRENA benchmarks, TC infrastructure data | Class C |
| 04 Hydrogen Processing | Compressor OEM data, IRENA benchmarks | Class C |
| 05 Civil & Construction | Industry norms, Gold Dataset brownfield evidence | Class C-D |
| 06 Thermal Management | Cooling equipment vendor data | Class C-D |
| 07 I&C | DCS vendor data, Gold Dataset evidence (Yokogawa MAC) | Class C |
| 08 Indirect & Owner's | AACE standards, Gold Dataset contingency evidence | Class C-D |

### 6.2 What Data Will Be Difficult to Source

| Challenge | Reason |
|-----------|--------|
| Class A actual costs | No operational >100 MW plant exists |
| Class B contracted prices | OEM quotations are commercially confidential |
| Regional multipliers for MENA/Asia | Limited published hydrogen project data outside Europe |
| FOAK premium calibration | Requires multiple completed projects at different maturity stages |
| Decommissioning costs | No electrolyzer plant has been decommissioned yet |

### 6.3 Recommended Sprint 1 Scope (30 cost records)

| Category | Records | Priority Sources |
|----------|---------|-----------------|
| 01 Electrolyzer System | 8 (4 PEM + 4 Alkaline at different scales) | IEA GHR 2025, IRENA 2024, TC-PEM/ALK-001 |
| 02 Electrical Infrastructure | 4 (greenfield + brownfield at different scales) | IEA Electricity Grids 2025, Gold Dataset |
| 03 Water Systems | 2 (PEM + Alkaline benchmarks) | IRENA 2024 |
| 04 Hydrogen Processing | 4 (PEM + Alkaline, industrial + mobility offtake) | IRENA 2024, compressor OEM data |
| 05 Civil & Construction | 3 (greenfield, brownfield, FOAK) | Industry norms + Gold Dataset |
| 06 Thermal Management | 1 | Vendor data |
| 07 I&C | 2 (small scale + large scale) | Vendor data |
| 08 Indirect & Owner's | 6 (engineering, PM, contingency × 2 technologies) | AACE + Gold Dataset |
| **TOTAL** | **30** | |

---

## 7. Conditional Go Decision

### GO Conditions

| # | Condition | Owner | Deadline |
|---|-----------|-------|----------|
| 1 | Add `scaling_exponent_uncertainty` field to cost schema; document exponent ranges in scaling methodology | Cost Architect | Before Sprint 1 start |
| 2 | Schedule M7C milestone (OPEX/LCOH integration) in project roadmap | PM | Within 2 weeks |
| 3 | Create `regional_multipliers.json` with initial European factors (can be enriched later) | Cost Engineer | During Sprint 1 |
| 4 | Define cost benchmark set structure and aggregation rules | Cost Architect | During Sprint 1 |
| 5 | Create controlled vocabulary for `cost_drivers.exclusions` (20-30 standard terms) | Cost Engineer | During Sprint 1 |
| 6 | Define cost category interaction rules (dependency matrix) | Cost Architect | During Sprint 1 |

### Rationale for Conditional Go (Not Full Go)

A full Go would require:
- Empirically calibrated scaling exponents (not possible — insufficient built projects)
- OPEX/LCOH integration (requires separate milestone)
- Regional multiplier database for all regions (can start with Europe and expand)

These are NOT architecture design failures — they are inherent limitations of the hydrogen industry's maturity. The architecture is honest about them. The conditional Go reflects that the architecture is ready for construction WITH documented limitations — which is the correct posture for a pre-feasibility tool in an immature industry.

### Rationale for Not No-Go

A No-Go would be appropriate if:
- The confidence framework failed to prevent false precision ❌ (it passes)
- Source traceability was broken ❌ (100% of assumptions have source chains)
- Technology differentiation was incorrect ❌ (validated against IEA/IRENA benchmarks)
- The framework couldn't explain costs ❌ (4-layer explainability demonstrated)

None of these failure conditions exist. The architecture is fundamentally sound.

---

## 8. Sign-Off

| Role | Recommendation | Signature |
|------|---------------|-----------|
| Senior Cost Engineer | **CONDITIONAL GO** — Architecture is ready for Cost Library construction with 6 conditions | — |
| Project Controls Manager | **CONDITIONAL GO** — AACE alignment and confidence framework are production-ready | — |
| Knowledge Validation Lead | **CONDITIONAL GO** — All 6 validation tests passed; gaps are documented and mitigatable | — |

**Decision: CONDITIONAL GO. Cost Library Sprint 1 may proceed upon satisfaction of conditions 1-6 above.**

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer, Project Controls Manager & Knowledge Validation Lead | Comprehensive architecture validation — M7B complete |
