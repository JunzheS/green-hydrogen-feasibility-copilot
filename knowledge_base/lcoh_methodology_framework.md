# LCOH Methodology Framework — Levelized Cost of Hydrogen

**Document:** LCOH Calculation & Communication Framework v1.0
**Date:** 2026-06-05
**Author:** Hydrogen Economist & Industrial Cost Engineer
**Basis:** IEA/IRENA LCOH methodology, adapted for Copilot pre-feasibility use
**Antipattern:** Black-box financial models. This framework is EXPLAINABLE by design.

---

## 1. Why an Explainable LCOH Framework?

A black-box LCOH calculator produces a number: "€4.23/kg." This is useless for pre-feasibility because:
- It hides which assumptions drive the result
- It implies precision that doesn't exist
- It cannot be challenged or updated as new data arrives

An explainable LCOH framework produces: **"LCOH is €3.50-5.50/kg (central €4.20). Electricity is 55% of this. If electricity is €30/MWh instead of €40, LCOH drops to €3.65. The biggest uncertainty is capacity factor — our assumption of 5,000 hours/year has a ±20% range."**

---

## 2. The LCOH Formula

```
LCOH = (CAPEX_annualized + OPEX_annual) / Annual_H2_Production

Where:

  CAPEX_annualized = Total_CAPEX × CRF
  CRF = r × (1+r)^n / ((1+r)^n − 1)    [Capital Recovery Factor]
  
  r = Weighted Average Cost of Capital (WACC) — typically 6-10% for green H₂
  n = Project economic life — typically 20-25 years

  OPEX_annual = Σ (OPEX_category_i × Annual_H2_Production)   for per-kg categories
              + Σ (OPEX_category_j)                           for fixed annual costs

  Annual_H2_Production = Capacity_MW × 1,000 × System_Efficiency_kWh_per_kg⁻¹ 
                       × Full_Load_Hours_per_Year / 1,000
                     = Capacity_MW × Full_Load_Hours × (1 / Efficiency)
```

---

## 3. LCOH Decomposition — The "Waterfall" View

Rather than presenting a single number, the framework presents LCOH as a **cost stack**:

```
LCOH = CAPEX contribution + Electricity + Stack Replacement + Maintenance + Labor + Other OPEX

For 100 MW PEM, 4,500 hours/year, €40/MWh, 7% WACC:

  CAPEX contribution:   €0.45/kg  (13%)  ← from Cost Library CS-IND-006
  Electricity:          €2.20/kg  (61%)  ← 55 kWh/kg × €0.040/kWh
  Stack Replacement:    €0.12/kg  (3%)   ← sinking fund
  Maintenance:          €0.30/kg  (8%)   ← Technology Card estimate
  Labor:                €0.18/kg  (5%)   ← scaled from staffing model
  Other OPEX:           €0.35/kg  (10%)  ← water, insurance, land, regulatory
  ─────────────────────────────────────
  LCOH (central):      ~€3.60/kg  (100%)
```

**Key insight: Electricity (61% of LCOH) is 4.7× larger than the CAPEX contribution (13%). The single most important number in any hydrogen project is the electricity price assumption — not the CAPEX.**

---

## 4. Assumption Transparency Table

Every LCOH estimate must be accompanied by an assumption table:

| Assumption | Value | Source | Confidence | Sensitivity |
|-----------|-------|--------|-----------|------------|
| Electricity price (€/MWh) | 40 | IEA WEO 2025 / PPA benchmark | C (±25%) | ±€0.55/kg per €10/MWh |
| Full-load hours/year | 4,500 | IRENA 2024 / project location solar/wind data | C (±20%) | ±€0.45/kg per 1,000 hrs |
| System efficiency (kWh/kg) | 55 (PEM) | TC-PEM-001 §performance | B (±10%) | ±€0.22/kg per 5 kWh/kg |
| Total CAPEX (€/kW) | 1,500 | Cost Library CS-IND-006 | C (±25%) | ±€0.11/kg per €100/kW |
| WACC (%) | 7% | Industry benchmark | C (±2%) | ±€0.08/kg per 1% WACC |
| Stack replacement (€/kW) | 350 | TC-PEM-001 §cost_profile | C (±25%) | ±€0.03/kg per €50/kW |
| Stack lifetime (hours) | 65,000 | TC-PEM-001 §performance | B (±15%) | ±€0.02/kg per 5,000 hrs |

---

## 5. Uncertainty Communication

### 5.1 LCOH as a Range, Not a Point

The framework presents LCOH with three scenarios rather than a single number:

| Scenario | Electricity | Capacity Factor | CAPEX | LCOH (€/kg) |
|----------|-----------|-----------------|-------|-------------|
| **Optimistic (P10)** | €30/MWh | 5,500 hrs | €1,200/kW | ~2.60 |
| **Central (P50)** | €40/MWh | 4,500 hrs | €1,500/kW | ~3.60 |
| **Pessimistic (P90)** | €60/MWh | 3,500 hrs | €2,100/kW | ~5.10 |

**Range:** €2.60-5.10/kg → The P10-P90 spread is ~€2.50/kg — almost as large as the central estimate itself. This is honest pre-feasibility communication.

### 5.2 Tornado Diagram (Text)

```
Impact on LCOH (±€/kg from central €3.60):

  Electricity ±€20/MWh          ████████████████  ±€1.10
  Capacity Factor ±1,000 hrs    ██████████        ±€0.45
  System Efficiency ±5 kWh/kg   ██████            ±€0.22
  Total CAPEX ±€300/kW          ████              ±€0.11
  WACC ±2%                      ███               ±€0.08
  Stack Replacement ±€100/kW    █                 ±€0.03
```

**Verdict: Electricity price dominates. Capacity factor is second. Everything else is details.** A pre-feasibility study that obsesses over CAPEX accuracy (±€0.11/kg) while treating electricity price as a fixed input is missing the point.

---

## 6. "What-If" Reasoning Template

The framework supports structured what-if reasoning:

```
Q: "What if electricity is €50/MWh instead of €40?"
A: Central LCOH increases from €3.60 → €4.15/kg (+€0.55/kg).
   At this LCOH, the project likely exceeds the grey H₂ benchmark (€2-3/kg)
   and requires green premium offtake pricing or carbon credit support.

Q: "What if capacity factor is only 3,500 hours?"
A: Central LCOH increases from €3.60 → €4.05/kg (+€0.45/kg).
   The fixed costs (CAPEX, labor) are spread over fewer kg → higher per-kg cost.
   PEM's dynamic response partially mitigates this vs Alkaline for solar profiles.

Q: "What is the breakeven electricity price for €3.00/kg LCOH?"
A: At central assumptions for all other parameters, electricity must be €26/MWh
   for PEM or €28/MWh for Alkaline. These prices are achievable with dedicated
   solar PV in MENA/Chile/Australia but difficult in Europe without subsidy.
```

---

## 7. Technology Comparison Template

| Parameter | PEM | Alkaline | Delta | LCOH Impact |
|-----------|-----|----------|-------|------------|
| Efficiency (kWh/kg) | 55 | 53 | −2 | ALK −€0.08/kg at €40/MWh |
| Stack CAPEX (€/kW) | 800 | 450 | −350 | ALK −€0.06/kg |
| Stack lifetime (hrs) | 65,000 | 90,000 | +25,000 | ALK −€0.04/kg |
| Maintenance (€/kg) | 0.30 | 0.23 | −0.07 | ALK −€0.07/kg |
| Compression (€/kg) | 0.05 | 0.12 | +0.07 | PEM −€0.07/kg |
| **Net LCOH difference** | | | | **ALK −€0.18/kg (5%)** |

**For a pre-feasibility estimate with ±20-30% uncertainty, a 5% LCOH difference between technologies is WITHIN THE ERROR BARS. Technology choice should be driven by operational fit (dynamic response, purity, offtake) and risk profile, not a marginal LCOH difference that disappears within estimation uncertainty.**

---

## 8. What the Framework Does NOT Do

| ❌ | Why Not |
|----|---------|
| Calculate IRR or NPV | Requires project-specific cash flow modeling; out of scope for pre-feasibility Copilot |
| Model tax and depreciation | Tax regimes are project/country-specific; a generic model would mislead |
| Optimize dispatch (when to run vs idle) | Requires hourly electricity price and renewable generation data; operational planning, not pre-feasibility |
| Include carbon pricing revenue | EU ETS free allowances and carbon border adjustments are evolving; add when regulatory module is built |
| Provide a single "bankable" LCOH number | Pre-feasibility estimates are ±25-30%; bankability requires FEED-level (±10-15%) |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Hydrogen Economist & Industrial Cost Engineer | Initial LCOH methodology |
