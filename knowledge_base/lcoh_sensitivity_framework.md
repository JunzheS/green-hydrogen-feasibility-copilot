# LCOH Sensitivity Framework — Driver Analysis & Uncertainty

**Document:** Sensitivity Analysis Methodology
**Date:** 2026-06-05
**Author:** Hydrogen Economist & Industrial Cost Engineer
**Basis:** lcoh_methodology_framework.md; Technology Card cost profiles; IEA/IRENA cost data

---

## 1. The LCOH Driver Hierarchy

```
LCOH Drivers Ranked by Impact (±€/kg from central):

TIER 1 — DOMINANT (>±€0.30/kg):
  1. Electricity price      (±€0.55/kg per €10/MWh)
  2. Capacity factor        (±€0.45/kg per 1,000 hrs/year)

TIER 2 — SIGNIFICANT (±€0.10-0.30/kg):
  3. System efficiency      (±€0.22/kg per 5 kWh/kg)
  4. Total CAPEX            (±€0.11/kg per €300/kW)

TIER 3 — MINOR (±€0.03-0.10/kg):
  5. WACC                   (±€0.08/kg per 2% change)
  6. Stack replacement cost (±€0.03/kg per €100/kW)
  7. Maintenance cost       (±€0.03/kg per €0.05/kg change)

TIER 4 — NEGLIGIBLE (<±€0.03/kg):
  8. Stack lifetime         (±€0.02/kg per 5,000 hrs)
  9. Labor cost             (±€0.01/kg per 20% change)
  10. Water/consumables     (±€0.01/kg)
```

---

## 2. Tornado Diagram — Quantitative

**Reference case:** 100 MW PEM, 4,500 hrs/yr, €40/MWh, 55 kWh/kg, €1,500/kW CAPEX, 7% WACC, €350/kW stack replacement, 65,000 hrs stack life. **Central LCOH: €3.60/kg.**

| Rank | Driver | Low Scenario | High Scenario | Low LCOH | High LCOH | Swing (±€/kg) |
|------|--------|-------------|--------------|----------|-----------|--------------|
| 1 | **Electricity price** | €30/MWh | €60/MWh | €3.05 | €4.70 | **±0.83** |
| 2 | **Capacity factor** | 5,500 hrs | 3,500 hrs | €3.15 | €4.05 | **±0.45** |
| 3 | **System efficiency** | 50 kWh/kg | 60 kWh/kg | €3.38 | €3.82 | **±0.22** |
| 4 | **Total CAPEX** | €1,200/kW | €2,100/kW | €3.49 | €3.93 | **±0.22** |
| 5 | **WACC** | 5% | 9% | €3.44 | €3.76 | **±0.16** |

---

## 3. Multi-Dimensional Scenario Analysis

| Scenario | Electricity | Hours | CAPEX | Efficiency | LCOH | Note |
|----------|-----------|-------|-------|-----------|------|------|
| **P10 Optimistic** | €30/MWh (low-cost solar PPA) | 5,500 (high wind) | €1,200/kW (brownfield, nth-of-a-kind) | 50 kWh/kg (best-in-class) | **€2.30/kg** | Competitive with grey H₂ at €50/tCO₂ carbon price |
| **P25 Favorable** | €35/MWh | 5,000 | €1,350/kW | 53 kWh/kg | **€2.80/kg** | |
| **P50 Central** | €40/MWh | 4,500 | €1,500/kW | 55 kWh/kg | **€3.60/kg** | Requires green premium or carbon support |
| **P75 Unfavorable** | €50/MWh | 4,000 | €1,800/kW | 57 kWh/kg | **€4.60/kg** | |
| **P90 Pessimistic** | €60/MWh (wholesale, no PPA) | 3,500 (low solar) | €2,100/kW (FOAK greenfield) | 58 kWh/kg (degraded) | **€5.80/kg** | Project likely uneconomic |

---

## 4. Key Sensitivity Insights

### 4.1 Electricity Price — The Dominant Driver

```
LCOH sensitivity to electricity price (per €10/MWh):
  PEM:  ±€0.55/kg  (55 kWh/kg × €0.010/kWh)
  ALK:  ±€0.53/kg  (53 kWh/kg × €0.010/kWh)

At €40/MWh central:  €2.20/kg (PEM) vs €2.12/kg (ALK) — ALK saves €0.08/kg
At €80/MWh:          €4.40/kg (PEM) vs €4.24/kg (ALK) — ALK saves €0.16/kg
At €20/MWh:          €1.10/kg (PEM) vs €1.06/kg (ALK) — ALK saves €0.04/kg

The higher the electricity price, the more Alkaline's efficiency advantage matters.
```

**Implication for pre-feasibility:** The electricity price assumption should be the most carefully researched input. A project that assumes €35/MWh from a solar PPA but actually pays €45/MWh will see LCOH increase by €0.55/kg — equivalent to a €550/kW CAPEX error.

### 4.2 Capacity Factor — The Second Driver

```
LCOH = Fixed_Costs_per_year / (Capacity × Hours) + Variable_Costs_per_kg

As capacity factor drops, fixed costs (CAPEX, labor, insurance) are spread over fewer kg:
  At 5,500 hrs: Fixed contribution = €0.82/kg
  At 4,500 hrs: Fixed contribution = €1.00/kg
  At 3,500 hrs: Fixed contribution = €1.29/kg

This is non-linear — each lost hour increases per-kg cost more than the previous one.
```

**Technology note:** PEM's superior dynamic response (5% minimum load vs 15%, 15-min cold start vs 60-min) translates to ~5-10% higher effective capacity factor for solar-coupled projects. This is an OPEX/LCOH advantage NOT captured in the simple efficiency comparison.

### 4.3 Interaction Effects

The drivers are NOT independent:

- **Electricity price × Efficiency:** Higher efficiency (lower kWh/kg) reduces electricity's contribution to LCOH. This is why Alkaline's 4% efficiency advantage compounds at high electricity prices.
- **CAPEX × WACC:** Higher WACC amplifies the impact of CAPEX on LCOH. At 9% WACC, a €100/kW CAPEX increase adds €0.04/kg more than at 5% WACC.
- **Capacity Factor × Fixed Costs:** Low capacity factor amplifies the impact of ALL fixed costs (CAPEX, labor, maintenance). A project with low capacity factor is more sensitive to CAPEX accuracy.

---

## 5. Breakeven Analysis

### 5.1 Breakeven Electricity Price

*"At what electricity price does LCOH equal €3.00/kg?"* (Competitive with grey H₂ at €80/tCO₂)

| Technology | CAPEX (€/kW) | Hours/yr | Breakeven Electricity |
|-----------|-------------|---------|----------------------|
| PEM 100 MW | 1,500 | 4,500 | **€26/MWh** |
| PEM 100 MW | 1,200 (optimistic) | 4,500 | €31/MWh |
| ALK 100 MW | 1,308 | 4,500 | **€28/MWh** |
| ALK 100 MW | 1,010 (optimistic) | 4,500 | €34/MWh |

**Interpretation:** At central CAPEX and capacity factor assumptions, breakeven with grey H₂ requires electricity at €26-28/MWh — achievable with dedicated solar PV in Spain/MENA/Chile/Australia, but challenging in Northern Europe without subsidy.

### 5.2 Breakeven Capacity Factor

*"At what capacity factor does LCOH equal €3.00/kg?"* (€40/MWh electricity)

| Technology | CAPEX (€/kW) | Electricity | Breakeven Hours |
|-----------|-------------|-----------|----------------|
| PEM 100 MW | 1,500 | €40/MWh | **6,200 hrs** (not achievable for solar-only) |
| ALK 100 MW | 1,308 | €40/MWh | **5,500 hrs** (achievable with offshore wind + grid) |

---

## 6. Framework Usage Rules for the LCOH Agent

1. **Always present LCOH as a range (P10-P90), never a point estimate**
2. **Always show the electricity price assumption prominently** — it's the dominant driver
3. **Always present the tornado diagram** — show which assumptions matter most
4. **Always communicate confidence** — an LCOH based on Class C CAPEX and Class B efficiency has different reliability than one based on Class A actuals
5. **Never present LCOH without assumptions** — the assumptions table is mandatory
6. **Always compare technology LCOH on consistent assumptions** — don't use €40/MWh for PEM and €35/MWh for ALK unless explicitly documenting why

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Hydrogen Economist & Industrial Cost Engineer |
