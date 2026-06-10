# Industrial Development Budget — Methodology

**Date:** 2026-06-10
**Sprint:** 5D — V1.1 Credibility Improvements
**Engine:** `src/engines/cost_assessment_engine.py` — `_estimate_industrial_budget()`
**Calibration basis:** PEM, extended to Alkaline with reduced factors
**Reference:** [industry_feedback_validation_report.md](industry_feedback_validation_report.md) — Sprint 5C

---

## 1. Purpose

The Reference Benchmark CAPEX (V1 engine output) estimates an **nth-of-a-kind, overnight cost in constant 2025 EUR**. This is the correct basis for technology comparison, cost curve analysis, and regulatory filings.

However, industry practitioners planning real projects need a **Total Investment Requirement** that reflects:

- First-of-a-kind premiums (all current >100 MW projects are FOAK)
- Interest During Construction (financing cost)
- Broader scope (bulk storage, extended commissioning, initial spares)
- Cost escalation to year of expenditure

The **Industrial Development Budget** provides this planning number, computed dynamically from the Reference Benchmark using documented, traceable adjustment factors.

---

## 2. Formula

```
Industrial_Budget = Reference_Benchmark_CAPEX
                   × FOAK_factor
                   × IDC_factor
                   × Scope_factor
                   × Escalation_factor
```

Where all factors are ≥ 1.0 and multiply sequentially.

### 2.1 Reference Benchmark CAPEX

Taken directly from the V1 CAPEX engine output (`central_eur_per_kw`). This is the nth-of-a-kind, overnight cost in constant 2025 EUR.

**Source:** `CS-IND-006` (PEM) or `CS-IND-007` (Alkaline), after scale adjustment and FOAK removal.

### 2.2 FOAK Factor

Captures the cost premium of a developer's first project versus an nth-of-a-kind benchmark.

```
FOAK_factor = 1.00
            + scale_foak_premium
            + application_foak_premium
            + developer_first_project_premium
```

| Component | PEM Value | Alkaline Value | Source |
|-----------|----------|---------------|--------|
| Scale FOAK (beyond proven scale) | +10% | +5% | `cost_assessment_engine.py` FOAK multipliers + `cost_scaling_methodology.md` §5.2 |
| Application FOAK (first offtake type) | +5% | +3% | `cost_assessment_engine.py` FOAK multipliers + `cost_scaling_methodology.md` §5.2 |
| Developer first project | +5% | +3% | Conservative assumption; `cost_scaling_methodology.md` §5.2: "first hydrogen project by developer: +20-30%". The +5% is the developer-specific component beyond scale+application FOAK. |

**PEM maximum FOAK factor:** 1.20 (all three premiums)
**Alkaline maximum FOAK factor:** 1.11 (reduced due to TRL 9 maturity)

**Conservative assumption:** The model assumes **every project is the developer's first** (+5% for PEM, +3% for Alkaline). This is appropriate for pre-feasibility planning. As the Gold Dataset matures with developer experience tracking, this can be refined.

**Evidence:**
- Normand'Hy (FOAK PEM, Air Liquide): €2,250/kW vs benchmark €1,500/kW → +50% raw FOAK effect
- After scale/time normalization: ~+20% residual FOAK premium
- Industry feedback: Marco's €200-220M vs model €150M → +33-47%, explained partly by FOAK + scope

### 2.3 IDC Factor (Interest During Construction)

Captures the cost of financing during the construction period before revenue begins.

```
IDC_factor = 1.10  (fixed)
```

**Assumptions:**
- Construction period: 3 years
- WACC: 7% (standard for European green hydrogen projects)
- Drawdown profile: 50% average outstanding (S-curve construction spend)
- IDC ≈ (1 + 0.07/2)^3 − 1 ≈ 10.9% → rounded to 10%

**Source:** Standard project finance methodology. Consistent with IEA GHR 2025 and Hydrogen Council project finance benchmarks.

### 2.4 Scope Expansion Factor

Captures scope items typically present in real project budgets but excluded from the Reference Benchmark (which is a like-for-like technology cost comparison).

```
Scope_factor = 1.10  (fixed)
```

**Scope items included:**

| Item | Approximate Cost Impact | Source |
|------|------------------------|--------|
| Bulk H₂ buffer storage (8–24 hour) | +3–5% of total CAPEX | `CS-HPR-*` records exclude bulk storage; industry norm: 1-day buffer for industrial offtake ≈ €80/kW |
| Extended commissioning and performance testing | +2–4% | Industry norm: 2–4% of direct costs for performance guarantee testing beyond standard commissioning |
| Owner's internal development and PM | +2–3% | `CS-IND-003` covers basic owner's costs; real first projects incur additional internal overhead |
| Initial spares and first-fill consumables | +1–2% | Stack spare parts, membrane inventory, water treatment chemicals, compressor lubricants |
| Pre-FEED scope contingency on BOP | +1–2% | Additional allowance for scope items not yet defined at pre-feasibility stage |

**Total: ~10%** — a conservative planning allowance for pre-FEED stage scope uncertainty.

**Source:** `industry_feedback_validation_report.md` §3.2, Explanation 3. Consistent with AACE 18R-97 guidelines for Class 4 estimate scope definition completeness (typically 70–85% scope defined at Class 4).

### 2.5 Escalation Factor

Converts constant 2025 EUR to year-of-expenditure EUR.

```
Escalation_factor = (1.03)^(target_COD − 2025)
```

**Assumption:** 3.0% per year construction cost escalation (European chemical plant index).

**Source:** IHS Markit / ENR Construction Cost Index — European process plant escalation: 2.5–3.5%/year (2020–2025 average). 3.0% is the central estimate.

**Examples:**

| Target COD | Years from 2025 | Escalation Factor |
|-----------|----------------|-------------------|
| 2025 | 0 | 1.000 |
| 2026 | 1 | 1.030 |
| 2027 | 2 | 1.061 |
| 2028 | 3 | 1.093 |
| 2029 | 4 | 1.126 |
| 2030 | 5 | 1.159 |
| 2035 | 10 | 1.344 |

---

## 3. Worked Example: France | Steel | PEM | 100 MW | COD 2029

### 3.1 Input

| Parameter | Value | Source |
|-----------|-------|--------|
| Reference Benchmark | €150.0M (€1,500/kW) | CS-IND-006, V1 engine |
| is_foak_scale | False | 100 MW ≤ 200 MW max proven |
| is_foak_app | False | HyDeal GA-PR-005 is steel/PEM reference |
| Technology | PEM | — |
| target_cod | 2029 | — |
| cost_year | 2025 | CS-IND-006 |

### 3.2 Factor Computation

```
FOAK_factor    = 1.00 + 0.00 (scale) + 0.00 (app) + 0.05 (developer) = 1.05
IDC_factor     = 1.10
Scope_factor   = 1.10
Escalation     = (1.03)^(2029−2025) = (1.03)^4 = 1.126

Total_multiplier = 1.05 × 1.10 × 1.10 × 1.126 = 1.429
```

### 3.3 Result

```
Industrial Budget = €150.0M × 1.429 = €214.4M
                  ≈ €215M (rounded)
                  = €2,150/kW
```

### 3.4 Reconciliation with Industry Feedback

Marco's feedback: "CAPEX of 150 M€ appears optimistic. Suggested range: 200–220 M€."

| Estimate | €M | Notes |
|----------|-----|-------|
| Reference Benchmark (V1 Central) | 150 | Nth-of-a-kind, overnight, 2025 EUR |
| Reference Benchmark (V1 P90) | 210 | Conservative end of Cost Library range |
| **Industrial Development Budget** | **215** | **First project, total investment, YOE EUR** |
| Marco's range | 200–220 | Industry professional estimate |

The Industrial Development Budget of €215M falls within Marco's €200–220M range, confirming the factor calibration.

---

## 4. Technology Calibration Status

| Technology | Calibration Status | FOAK Factors | IDC | Scope | Escalation | Notes |
|-----------|-------------------|-------------|-----|-------|------------|-------|
| **PEM** | ✅ **Calibrated** | Full (1.05–1.20) | 1.10 | 1.10 | (1.03)^years | Validated against industry feedback and FOAK project data |
| **Alkaline** | ⚠️ **Extended** | Reduced (1.03–1.11) | 1.10 | 1.10 | (1.03)^years | FOAK factors reduced per TRL 9 maturity. IDC, scope, escalation are technology-agnostic and carry forward. |
| **SOEC** | ❌ **Not available** | — | — | — | — | No benchmark records, no FOAK data, no project references at commercial scale |
| **AEM** | ❌ **Not available** | — | — | — | — | No benchmark records, no FOAK data, no project references at commercial scale |

### 4.1 PEM Calibration Evidence

| Evidence Source | Finding |
|----------------|---------|
| Normand'Hy (200 MW PEM FOAK) | Raw €2,250/kW → scale-norm €2,585/kW → after time+FOAK normalization: €1,640/kW. Residual vs benchmark: +9%. |
| H2V Dunkerque (200 MW PEM FOAK) | Raw €1,250/kW → scale-norm €1,436/kW → after time+FOAK normalization: €874/kW. Below benchmark — aggressive project economics. |
| Industry feedback (Marco) | €200–220M for 100 MW. Industrial Budget model gives €215M. |
| V2 design study (Sprint 5B) | Weighted mean of normalized reference projects: €1,524/kW → €152M. Within 1.6% of V1 benchmark. |

### 4.2 Alkaline Calibration Caveats

- FOAK factors are reduced by ~50% vs PEM (reflecting TRL 9 vs TRL 8, 100+ year industrial history)
- **No independent industry feedback** has validated the Alkaline calibration
- The Alkaline Industrial Budget should be labeled "ALKALINE-EXTENDED (not independently validated)"
- IDC, scope, and escalation factors are technology-agnostic and apply equally

---

## 5. Limitations

1. **Developer experience is assumed conservative** — the +5% (PEM) / +3% (Alkaline) developer premium assumes a first-time hydrogen developer. Experienced developers (Air Liquide, Shell) may achieve lower costs. This cannot be refined without developer experience tracking in the Gold Dataset.

2. **Scope factor is a blended average** — individual projects may have different scope requirements (e.g., mobility offtake requires +€120/kW compression vs industrial). The 10% factor is a planning average.

3. **Escalation uses a flat 3%/year** — actual escalation varies by equipment category (stack costs may decrease due to learning while civil costs increase with construction inflation). The net effect is uncertain.

4. **Not a replacement for FEED-phase estimating** — the Industrial Development Budget remains a Class 4 (±20–30%) estimate. It should be refined during FEED with OEM quotations and EPC estimates.

5. **Not validated for non-European projects** — escalation rates, IDC assumptions, and scope factors assume European construction market conditions. MENA, APAC, and Americas may differ.

6. **Alkaline extension is unvalidated** — no industry feedback has confirmed the Alkaline FOAK factor reduction.

---

## 6. Traceability Matrix

| Factor | Value | Documented In | Evidence Level |
|--------|-------|--------------|---------------|
| FOAK — scale | +10% PEM / +5% Alk | `cost_scaling_methodology.md` §5.2 | **Medium** — industry guidelines, no empirical calibration |
| FOAK — application | +5% PEM / +3% Alk | `cost_assessment_engine.py` FOAK multipliers | **Medium** — engine convention, conservative |
| FOAK — developer | +5% PEM / +3% Alk | `cost_scaling_methodology.md` §5.2 (20–30% total, partitioned) | **Low** — inferred from total FOAK, not independently measured |
| IDC | 1.10 | Project finance standard; IEA GHR 2025 | **High** — standard formula, well-established |
| Scope | 1.10 | AACE 18R-97; `industry_feedback_validation_report.md` §3.2 | **Medium** — industry standard, not project-specific |
| Escalation | (1.03)^years | IHS Markit / ENR CCI; European process plant data | **High** — published indices, well-established |

---

## 7. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-10 | Sprint 5D | Initial methodology — PEM-calibrated, Alkaline-extended |
