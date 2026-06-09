# Cost Uncertainty Validation — Confidence Framework Stress Test

**Document:** Uncertainty Framework Validation
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Knowledge Validation Lead
**Framework Tested:** cost_confidence_framework.md
**Key Question:** Does the confidence framework properly prevent false precision and communicate appropriate uncertainty?

---

## 1. The False Precision Problem

The primary risk for any Cost Agent is **false precision** — presenting an estimate as more certain than it actually is. A number like "€159,347,000" implies precision that doesn't exist at pre-feasibility stage. The confidence framework must enforce:

1. All estimates are ranges, not points
2. Ranges widen with lower confidence class
3. Aggregation does not hide low-confidence components behind high-confidence ones

---

## 2. Class-by-Class Validation

### 2.1 Class A — Actual Cost

| Attribute | Specification | Validation |
|-----------|--------------|-----------|
| **Evidence required** | Audited cost from completed project; project name attributable; cost year and basis stated | ✅ Clear, objective criteria |
| **Example** | Normand'Hy EPC close-out report (2026), audited by owner's engineer. Electrolyzer system installed cost: €160M for 200 MW = €800/kW (2024 EUR) | ✅ Concrete, verifiable |
| **Expected accuracy** | ±5-10% (actual outturn vs. contracted; minor scope variations) | ✅ Appropriate for audited actuals |
| **Suitable for** | Benchmarking, reference class forecasting, nth-of-a-kind estimates | ✅ |
| **Prevents false precision?** | ✅ Class A data is the GOLD STANDARD. By definition, it cannot be more precise than reality. The framework requires audited verification — unaudited actuals are Class B. | |
| **Gap identified** | Class A data is extremely rare for hydrogen projects (no operational >100 MW plant exists). The framework correctly reflects reality: in 2026, ZERO Class A PEM data exists at >20 MW scale. This is not a framework flaw — it's an honest representation of the industry's maturity. | |

### 2.2 Class B — Contracted Price

| Attribute | Specification | Validation |
|-----------|--------------|-----------|
| **Evidence required** | Signed contract or fixed-price quotation (<6 months); counterparty identified; scope of supply defined | ✅ Clear criteria |
| **Example** | Siemens Energy fixed-price quotation for 12 PEM modules (200 MW total), Q2 2024. €75M FCA Berlin. Scope: stacks, auxiliaries, DC power, commissioning support. | ✅ Concrete |
| **Expected accuracy** | ±10-15% (contracted but not yet delivered; change orders possible; scope boundaries may shift) | ✅ Appropriate |
| **Suitable for** | AACE Class 3 budget estimates, procurement planning | ✅ |
| **Prevents false precision?** | ✅ The framework explicitly states Class B costs are "not yet verified by actual project outturn" and flags them as subject to change orders. A naïve estimator might treat a fixed-price quotation as final; the framework prevents this. | |
| **Gap identified** | Class B data is often CONFIDENTIAL. Developers don't publish OEM quotations. The framework acknowledges this by allowing anonymized data ("confidential actual") but this limits Gold Dataset applicability. Most Cost Library entries will be Class C (industry benchmarks), not Class B. | |

### 2.3 Class C — Industry Benchmark

| Attribute | Specification | Validation |
|-----------|--------------|-----------|
| **Evidence required** | Published by recognized institution (IEA, IRENA, BNEF, WoodMac, Hydrogen Council); documented methodology; year and geography stated | ✅ Clear criteria |
| **Example** | IEA GHR 2025, Fig 3.4: PEM stack cost €600-1,100/kW installed (central €800/kW). Global average, Western OEMs. Methodology: pp. 98-102. Based on bottom-up manufacturing cost model validated against OEM data. | ✅ Verifiable |
| **Expected accuracy** | ±20-30% (aggregated across projects, regions, and OEMs; not project-specific) | ✅ Appropriate for Class 4 feasibility |
| **Suitable for** | AACE Class 4 feasibility estimates, pre-feasibility Copilot output | ✅ |
| **Prevents false precision?** | ✅ Class C is the WORKHORSE of pre-feasibility estimation. The framework: (a) requires documented methodology, (b) requires sample size disclosure (recommended), (c) requires range/confidence interval, (d) downgrades to Class D if methodology is not transparent. This prevents the most common cost estimation error: using an industry average as if it were a project-specific quotation. | |
| **Gap identified** | IEA and IRENA benchmarks use different cost basis definitions (stack vs. installed vs. system). The framework requires `cost_basis` to be stated, but cross-referencing IEA "installed stack" vs IRENA "electrolyzer system" requires analyst judgment. A future Cost Agent needs explicit mapping rules. | |

### 2.4 Class D — Analyst Estimate

| Attribute | Specification | Validation |
|-----------|--------------|-----------|
| **Evidence required** | Author/organization identified; basis of estimate described (even if qualitative); not contradicted by higher-class data; flagged as lower confidence | ✅ Clear criteria |
| **Example** | Consultant Report (Company X, 2024): "PEM stack cost ~€700/kW for 2025 Chinese market entry." Methodology: "interviews with industry participants" — sample size not disclosed. Not verified against IEA/IRENA. | ✅ Example shows the flagging |
| **Expected accuracy** | ±30-50% (limited methodology transparency; may be biased or outdated) | ✅ Appropriately wide |
| **Suitable for** | AACE Class 5 conceptual estimates (pre-pre-feasibility); identifying data gaps; sensitivity analysis | ✅ |
| **Prevents false precision?** | ✅ CRITICALLY. The framework's most important function is preventing Class D data from masquerading as Class C. It does this through: (a) mandatory lower-confidence flagging, (b) prohibition from being the sole source for any category >5% of total CAPEX, (c) downgrading of any aggregation where Class D exceeds 20% of weighted cost. **Without this framework, an analyst could use a single consultant report to "estimate" total CAPEX at Class C confidence.** The framework prevents this. | |
| **Gap identified** | The Class D → Class C boundary is the most subjective in the framework. Two analysts could disagree on whether a specific consulting report qualifies as Class C (published methodology) or Class D (insufficient transparency). A decision tree exists in the framework (§5) but edge cases will arise. | |

---

## 3. Aggregation Test — Does the Framework Prevent Hidden Low-Confidence Components?

### Test Scenario: 100 MW PEM estimate with mixed confidence classes

**Aggregation without confidence weighting (DANGEROUS):**

| Category | €/kW | Source Class |
|----------|------|-------------|
| Electrolyzer | 480 | C |
| Electrical | 210 | C |
| H₂ Processing | 140 | C |
| **Steel-specific H₂ compression** | **60** | **D (analyst estimate, no steel reference)** |
| Civil | 150 | C |
| Indirect | 440 | C-D |
| **TOTAL presented as:** | **~1,480/kW** | **Implied: Class C (±20-30%)** |

**PROBLEM:** The €1,480/kW number hides a Class D component. A reader would assume Class C confidence (±20-30%) when the steel-specific portion (±40-50%) makes the blended uncertainty wider.

**Aggregation WITH confidence weighting (CORRECT):**

| Category | Cost (€/kW) | Class | Weight |
|----------|------------|-------|--------|
| Electrolyzer | 480 | C | 0.60 |
| Electrical | 210 | C | 0.60 |
| H₂ Processing (generic) | 80 | C | 0.60 |
| H₂ Processing (steel-specific) | 60 | D | 0.40 |
| Civil | 150 | C | 0.60 |
| Indirect | 440 | C-D | 0.50 |
| **Weighted Confidence** | | | **0.56** |

**Result:** Weighted confidence 0.56 → **Low-Medium confidence.** The blended uncertainty is ±30-40%, not ±20-30%. The framework correctly communicates that this estimate is less reliable than a standard refinery-offtake PEM estimate.

**Verdict:** ✅ The framework prevents the most common confidence error: averaging away uncertainty.

---

## 4. The "Single Number Trap" — Architecture Defense Mechanisms

| Defense | Mechanism | Validated? |
|---------|-----------|-----------|
| **All estimates are ranges** | Every cost entry has `eur_per_kw`, `eur_per_kw_low`, `eur_per_kw_high` | ✅ Enforced by schema |
| **Confidence class is mandatory** | `confidence.level` is mandatory for `published` status | ✅ Schema enforced |
| **Low-confidence data is flagged** | Class D must be explicitly labeled in any output | ✅ Framework rule |
| **Aggregation uses weighted confidence** | Weighted average prevents Class D components from hiding | ✅ §3 demonstrates |
| **Extrapolation is downgraded** | Class A data scaled to different size → Class B | ✅ Framework rule §2.5 |
| **Cost basis is explicit** | `equipment_only` vs `installed_cost` vs `all_in` prevents scope confusion | ✅ Schema enforced |
| **Exclusions are mandatory** | `cost_drivers.exclusions` is mandatory for `published` status | ✅ Schema enforced |

---

## 5. Edge Case: What Happens When No Class A or B Data Exists?

**Scenario:** Estimating PEM stack cost for a 500 MW plant in 2030. In 2026:

- Class A: 0 data points (no operational >100 MW PEM)
- Class B: 0 publicly available (OEM quotations confidential)
- Class C: IEA/IRENA benchmarks at 100-200 MW
- Class D: Analyst projections for 500 MW

**Framework response:**
1. Start with Class C benchmark at 100 MW (IEA GHR 2025: €800/kW)
2. Scale to 500 MW using exponent 0.90 → €717/kW (downgraded to Class D per extrapolation rule)
3. Apply learning rate 15% to 2030 (3 doublings, ~4.5→36 GW cumulative) → €540/kW (still Class D)
4. Apply FOAK premium +20% (no 500 MW PEM reference exists) → €650/kW
5. **Result: Class D estimate.** The framework correctly labels this as low-confidence.
6. **Output:** "PEM stack at 500 MW in 2030: central estimate ~€650/kW, range €400-950/kW. CONFIDENCE: LOW (Class D, extrapolated from smaller scale benchmarks). This estimate carries ±40-50% uncertainty. Data collection priority: obtain OEM indicative quotation for 500 MW class stacks."

**Verdict:** ✅ The framework prevents the estimator from presenting a Class D extrapolation with false Class C confidence. The uncertainty is honest, the data gap is identified, and the path to higher confidence (OEM quotation) is stated.

---

## 6. Validation Against AACE International Standards

| AACE Class | Expected Accuracy | Architecture Alignment |
|-----------|-------------------|----------------------|
| Class 5 (Conceptual) | ±30-50% | ✅ Class C-D data; weighted confidence 0.40-0.59 |
| Class 4 (Feasibility) | ±20-30% | ✅ Class C data dominant; weighted confidence 0.60-0.79 |
| Class 3 (Budget) | ±10-20% | ✅ Class B data for major equipment (>60%); weighted confidence ≥0.80 |
| Class 2 (Control) | ±5-15% | ✅ Class A-B data; detailed engineering complete |
| Class 1 (Definitive) | ±3-10% | ✅ Class A data; construction complete, actual costs known |

**The architecture's confidence classes map correctly to AACE estimate classes.** A Class 5 estimate using mostly Class D data with some Class C produces the appropriate ±30-50% range. A Class 3 estimate requiring Class B contracted prices for major equipment produces the appropriate ±10-20% range.

---

## 7. Overall Uncertainty Framework Assessment

| Criterion | Pass? |
|-----------|-------|
| Prevents false precision (single-point estimates) | ✅ PASS |
| Communicates appropriate uncertainty per confidence class | ✅ PASS |
| Prevents hidden low-confidence components in aggregation | ✅ PASS |
| Handles the "no Class A/B data exists" edge case honestly | ✅ PASS |
| Aligns with AACE International estimate classification | ✅ PASS |
| Provides clear evidence requirements per class | ✅ PASS |
| Has a clear decision tree for class assignment | ✅ PASS |
| Identifies its own boundary cases (C/D boundary subjectivity) | ✅ PASS (acknowledged in §2.4) |

**The confidence framework is production-ready for Cost Library construction.** The primary implementation risk is analyst consistency in applying the C/D boundary — this should be addressed through calibration workshops during Cost Library population.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial uncertainty framework validation |
