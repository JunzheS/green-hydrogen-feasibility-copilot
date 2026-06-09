# Cost Confidence Framework — CAPEX Data Quality Classification

**Document:** Cost Data Confidence Classification
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Industrial Project Controller
**Applies To:** All cost records in the Cost Library
**Derived From:** Source Governance Framework + AACE International Estimate Classification

---

## 1. Confidence Classes

| Class | Label | Description | Typical Source | Typical AACE Class |
|-------|-------|------------|---------------|-------------------|
| **A** | Actual Cost | Audited actual cost from a completed project. Verified by owner's engineer or independent auditor. | EPC close-out report, audited financial statements, lender's independent engineer report | Class 1 (definitive, actual) |
| **B** | Contracted Price | Binding contractual price from an executed EPC contract, OEM supply agreement, or fixed-price quotation. Not yet verified by actual outturn. | Signed EPC contract, OEM fixed-price quotation (valid <6 months), awarded tender documentation | Class 2-3 (control/budget) |
| **C** | Industry Benchmark | Cost data from authoritative industry reports (IEA, IRENA, Hydrogen Council), academic literature, or aggregated project databases with documented methodology. | IEA GHR 2025, IRENA Cost Reduction 2024, BNEF Hydrogen Market Outlook | Class 3-4 (budget/feasibility) |
| **D** | Analyst Estimate | Cost estimate from consulting reports, media articles, or expert judgment. May be based on generic process industry analogies rather than hydrogen-specific data. Methodology may not be fully documented. | Consultant report (unnamed methodology), media-reported CAPEX (unverified), expert judgment | Class 4-5 (feasibility/conceptual) |
| **E** | Extrapolated / Derived | Cost derived by scaling from a different project size, technology, or region. Always combined with a source class (e.g., "C-derived" = industry benchmark, scaled to target). | Any source class, mathematically scaled per cost_scaling_methodology.md | Varies with source |

---

## 2. Evidence Requirements per Class

### Class A — Actual Cost

| Requirement | Mandatory |
|------------|-----------|
| Cost data from a completed, operational project | ✅ |
| Audited by independent third party (owner's engineer, lender's IE, or statutory auditor) | ✅ |
| Project name and location publicly attributable OR anonymized with verifiable characteristics | ✅ |
| Cost year and cost basis explicitly stated | ✅ |
| Cost breakdown by major category available (stack, BOP, civil, indirect) | Recommended |
| Single-source acceptable (if Level A source per Source Governance Framework) | ✅ |
| Second independent source confirming total | Recommended |

**Example:** *"Normand'Hy EPC close-out report, audited by owner's engineer, 2026. Total installed stack cost €160M for 200 MW PEM = €800/kW (2024 EUR). Breakdown confirms stack, auxiliaries, and installation inclusive. Verified by Air Liquide annual report CAPEX disclosure."*

### Class B — Contracted Price

| Requirement | Mandatory |
|------------|-----------|
| Binding contract, fixed-price quotation (<6 months old), or awarded tender | ✅ |
| Counterparty identified (OEM, EPC contractor) — may be confidential in published record | ✅ |
| Scope of supply clearly defined (what is included/excluded) | ✅ |
| Cost year stated | ✅ |
| Not yet verified by actual project outturn — may still be subject to change orders | Flagged |
| Recommended: two independent quotations for same scope | Recommended |

**Example:** *"Siemens Energy fixed-price quotation for 100 MW PEM electrolyzer package (12 × 8.3 MW modules), Q2 2024. Scope: stacks, auxiliaries, DC power supply, commissioning support. FCA Berlin. €75M = €750/kW. Valid 6 months. Not including BOP integration, civil works, or owner's costs."*

### Class C — Industry Benchmark

| Requirement | Mandatory |
|------------|-----------|
| Published by recognized institution with documented methodology (IEA, IRENA, BNEF, WoodMac, Hydrogen Council) | ✅ |
| Methodology section accessible (how the benchmark was derived) | ✅ |
| Year of data and geographic scope stated | ✅ |
| Sample size disclosed (how many projects/data points) | Recommended |
| Range (low-high) or confidence interval provided | Recommended |
| Peer-reviewed or editorially reviewed | Recommended |

**Example:** *"IEA Global Hydrogen Review 2025, Figure 3.4: PEM electrolyser stack cost (installed). Based on bottom-up manufacturing cost model validated against OEM data. 2025 estimate: €600-1,100/kW, central €800/kW. Global average, Western OEMs. Methodology: pp. 98-102."*

### Class D — Analyst Estimate

| Requirement | Mandatory |
|------------|-----------|
| Author or organization identified | ✅ |
| Basis of estimate described (even if qualitative) | ✅ |
| Not contradicted by higher-class data | ✅ |
| Flagged as "lower confidence" in any aggregation | ✅ |

**Example:** *"Consultant report (Company X, 2024) estimates PEM stack cost at €700/kW for 2025 Chinese market entry. Methodology: 'interviews with industry participants' — sample size and participant names not disclosed. Not verified against IEA/IRENA benchmarks."*

### Class E — Extrapolated / Derived

Derived costs inherit the confidence level of their source but are downgraded one notch for transparency:

| Source + Operation | Resulting Class |
|-------------------|-----------------|
| Class A, scaled to different size | B (downgraded — scaling introduces uncertainty) |
| Class B, scaled to different size | C |
| Class C, scaled to different size | D |
| Class C, scaled to different technology | D |
| Class D, scaled to different size | D (no downgrade — already minimum for use) |

---

## 3. Class Usage Rules for Cost Aggregation

| Aggregation Type | Minimum Acceptable Class | Notes |
|-----------------|------------------------|-------|
| **AACE Class 5 (Conceptual, ±30-50%)** | D or better | Broad ranges acceptable; Class D data with wide uncertainty bands |
| **AACE Class 4 (Feasibility, ±20-30%)** | C or better | Requires at least one Class C benchmark per major category |
| **AACE Class 3 (Budget, ±10-20%)** | B or better | Requires contracted prices for major equipment (>60% of CAPEX) |
| **Pre-feasibility Copilot output** | C or better (80%+ of weighted cost must be Class C+) | Ensures Copilot estimates have defensible basis |
| **Gold Dataset project CAPEX field** | B or better | Project CAPEX recorded in Gold Dataset should be from contracted or actual costs |

---

## 4. Confidence Scoring for Aggregated Estimates

When combining multiple cost entries for a total CAPEX range, compute a weighted confidence score:

```
Weighted Confidence = Σ (Cost_i × ClassWeight_i) / Σ (Cost_i)

Where ClassWeight:
  Class A = 1.00
  Class B = 0.80
  Class C = 0.60
  Class D = 0.40
  Class E = 0.30 (extrapolated, regardless of source)
```

| Weighted Confidence | Interpretation |
|--------------------|---------------|
| ≥ 0.80 | **High confidence**: majority of cost based on actual or contracted data |
| 0.60–0.79 | **Medium confidence**: mix of benchmarks and estimates; adequate for pre-feasibility |
| 0.40–0.59 | **Low confidence**: primarily analyst estimates; flagged for sensitivity analysis |
| < 0.40 | **Speculative**: not suitable for decision-making; data collection priority |

---

## 5. Class Assignment Decision Tree

```
Is the cost from an audited, completed project?
  YES → Can you name the project and cite the audit?
    YES → CLASS A
    NO  → CLASS B (confidential actual)

Is the cost from a binding contract or fixed-price quotation?
  YES → Is the scope of supply clearly defined?
    YES → CLASS B
    NO  → CLASS C (incomplete scope definition)

Is the cost from an authoritative industry report with documented methodology?
  YES → Does it cite a sample size?
    YES → CLASS C
    NO  → CLASS D (insufficient methodology transparency)

Is the cost from a consulting report, media article, or expert?
  YES → CLASS D

Is the cost mathematically derived from another cost entry?
  YES → CLASS E (source class − 1 notch)
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial cost confidence framework |
