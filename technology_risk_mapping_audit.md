# Technology Risk Mapping Audit

**Date:** 2026-06-10
**Sprint:** 5D — V1.1 Credibility Improvements
**Risk Library:** `knowledge_base/risk_library/` — 30 risk records across 8 categories
**Filter Engine:** `src/engines/risk_assessment_engine.py`

---

## 1. Filtering Rules (V1.1 — Fixed)

### 1.1 Rule

A risk record is included in an assessment **if and only if** the query technology is explicitly listed in the risk's `technology_types` field, OR the risk's `technology_types` is empty (treated as technology-agnostic).

```
IF risk.technology_types is empty:
    → INCLUDE (technology-agnostic)
ELIF query.technology IN risk.technology_types:
    → INCLUDE (exact match)
ELSE:
    → EXCLUDE
```

### 1.2 Cross-Technology Leakage Prevention

| Query Technology | Risks Tagged ["PEM"] | Risks Tagged ["Alkaline"] | Risks Tagged ["PEM", "Alkaline"] |
|-----------------|---------------------|--------------------------|----------------------------------|
| PEM | ✅ Included | ❌ Excluded | ✅ Included |
| Alkaline | ❌ Excluded | ✅ Included | ✅ Included |
| SOEC | ❌ Excluded | ❌ Excluded | ❌ Excluded |
| AEM | ❌ Excluded | ❌ Excluded | ❌ Excluded |

---

## 2. Complete Risk Inventory by Technology Applicability

### 2.1 Technology-Agnostic Risks (Apply to All Technologies)

Risks with `technology_types: ["PEM", "Alkaline"]` — applicable to both.

| Risk ID | Risk Name | Category | RPN | Class |
|---------|----------|----------|-----|-------|
| RK-TEC-003 | Hydrogen Processing Equipment Failure (Compression, Purification, Drying) | technical | 27 | medium |
| RK-TEC-005 | Stack Commissioning — Performance Below Specification | technical | 36 | medium |
| RK-SCP-001 | Electrolyzer Supply Chain Concentration (OEM Dependency) | supply_chain | 36 | high |
| RK-SCP-004 | Long-Lead Equipment — Transformers, Rectifiers, Compressors | supply_chain | 24 | medium |
| RK-SCP-005 | Critical Mineral Supply (Nickel, Stainless Steel, Titanium) | supply_chain | 18 | medium |
| RK-GRD-001 | Grid Connection — TSO Interconnection Delays and Costs | grid_energy | 45 | high |
| RK-GRD-002 | Grid Congestion — Renewable Power Availability Risk | grid_energy | 30 | medium |
| RK-GRD-003 | Electricity Price Volatility Impact on OPEX | grid_energy | 24 | medium |
| RK-GRD-004 | Grid Code Compliance — Power Quality and Ancillary Services | grid_energy | 18 | medium |
| RK-GRD-005 | Renewable Matching — RFNBO Certification Compliance | grid_energy | 24 | medium |
| RK-REG-001 | IPCEI / State Aid — Application Complexity and Delay | regulatory | 27 | medium |
| RK-REG-002 | RFNBO / Renewable Fuels of Non-Biological Origin Certification | regulatory | 24 | medium |
| RK-REG-003 | Permitting — Environmental Impact Assessment and Public Consultation | regulatory | 24 | medium |
| RK-REG-004 | Safety Case — Seveso III / COMAH Compliance | regulatory | 18 | medium |
| RK-REG-005 | Carbon Border Adjustment Mechanism (CBAM) — Future Cost Impact | regulatory | 18 | medium |
| RK-FIN-001 | CAPEX Overrun — Pre-FEED Estimate Uncertainty (±20-30%) | financial | 36 | high |
| RK-FIN-002 | LCOH Competitiveness — Gap to Grey/Blue Hydrogen | financial | 30 | medium |
| RK-FIN-003 | Financing Availability — Limited Lender Appetite for First Projects | financial | 24 | medium |
| RK-FIN-004 | Currency and Commodity Price Exposure During Construction | financial | 18 | medium |
| RK-CST-001 | Construction Schedule Delay — Permitting, Weather, Labour | construction | 27 | medium |
| RK-CST-002 | Commissioning and Ramp-Up — Performance Below Guarantee | construction | 24 | medium |
| RK-CST-003 | Supply Chain Disruption During Construction | construction | 18 | medium |
| RK-OPS-001 | Plant Availability Below Target (<95%) | operational | 27 | medium |
| RK-OPS-002 | Hydrogen Offtake — Demand Risk and Offtake Agreement Default | operational | 24 | medium |
| RK-ENV-001 | Water Consumption — Local Water Stress and Permit Risk | environmental | 24 | medium |

**Total technology-agnostic risks: 25**

---

### 2.2 PEM-Specific Risks

Risks with `technology_types: ["PEM"]` — applicable to PEM assessments only.

| Risk ID | Risk Name | Category | RPN | Class | PEM-Specific Reason |
|---------|----------|----------|-----|-------|--------------------|
| RK-TEC-001 | PEM Catalyst Degradation Under Dynamic Operation | technical | 45 | high | Iridium oxide anode catalyst degrades faster under variable renewable profiles. Not applicable to Alkaline (nickel-based electrodes). |
| RK-TEC-004 | PFSA Membrane Contamination from Water Quality Excursions | technical | 27 | medium | PFSA (Nafion) membrane is PEM-specific. Alkaline uses porous diaphragm, not solid polymer electrolyte. |
| RK-SCP-002 | Iridium Supply Constraint at GW-Scale Deployment | supply_chain | 36 | high | Iridium is used only in PEM (anode catalyst). Alkaline uses nickel/stainless steel electrodes — no PGM requirement. |
| RK-SCP-003 | PFSA Membrane Supply Concentration (Limited Global Suppliers) | supply_chain | 27 | medium | PFSA membrane is PEM-specific. Only 3-4 global suppliers. Alkaline uses asbestos-free diaphragm (lower cost, more suppliers). |

**Total PEM-specific risks: 4**

---

### 2.3 Alkaline-Specific Risks

Risks with `technology_types: ["Alkaline"]` — applicable to Alkaline assessments only.

| Risk ID | Risk Name | Category | RPN | Class | Alkaline-Specific Reason |
|---------|----------|----------|-----|-------|-------------------------|
| RK-TEC-002 | KOH Electrolyte Management and Contamination | technical | 36 | high | KOH (potassium hydroxide) liquid electrolyte is Alkaline-specific. PEM uses solid polymer electrolyte — no liquid electrolyte handling. KOH degradation from CO₂ absorption (carbonate formation) is unique to Alkaline. |

**Total Alkaline-specific risks: 1**

---

### 2.4 SOEC-Specific Risks

| Risk ID | Risk Name | Category | RPN | Class |
|---------|----------|----------|-----|-------|
| — | *No SOEC-specific risks in library* | — | — | — |

**Total SOEC-specific risks: 0**

*Note: The risk library does not currently contain SOEC-specific risks. SOEC assessments would only display technology-agnostic risks (25 records). This is a known gap for future library expansion.*

---

### 2.5 AEM-Specific Risks

| Risk ID | Risk Name | Category | RPN | Class |
|---------|----------|----------|-----|-------|
| — | *No AEM-specific risks in library* | — | — | — |

**Total AEM-specific risks: 0**

---

## 3. Impact of V1.1 Filter Fix

### 3.1 Risk Count Changes

| Assessment Type | Before Fix | After Fix | Delta | Affected Risks |
|----------------|-----------|----------|-------|---------------|
| PEM (100 MW) | 30 | 29 | −1 | RK-TEC-002 excluded (was incorrectly included) |
| Alkaline (100 MW) | 30 | 27 | −3 | RK-TEC-001, RK-TEC-004, RK-SCP-002, RK-SCP-003 excluded |
| SOEC | 25 | 25 | 0 | No technology-specific risks exist for SOEC |
| AEM | 25 | 25 | 0 | No technology-specific risks exist for AEM |

### 3.2 Regression Test Impact

All 5 regression test cases use `risk_count_min` (lower bound) assertions:
- Case 1 (PEM): `risk_count_min: 10` — new count 29 ≥ 10 → **PASS**
- Case 2 (Alkaline): `risk_count_min: 8` — new count 27 ≥ 8 → **PASS**
- Case 3 (PEM): `risk_count_min: 8` — new count 29 ≥ 8 → **PASS**
- Case 4 (Alkaline): `risk_count_min: 6` — new count 27 ≥ 6 → **PASS**
- Case 5 (PEM): `risk_count_min: 10` — new count 29 ≥ 10 → **PASS**

**Zero regression test failures expected.**

---

## 4. Filter Code Comparison

### Before (V1.0 — Bug)

```python
# OR logic: any risk tagged PEM OR Alkaline passes for either query
if query.technology.upper() not in [t.upper() for t in r.technology_types] and \
   "PEM" not in [t.upper() for t in r.technology_types] and \
   "ALKALINE" not in [t.upper() for t in r.technology_types]:
    tech_types_upper = [t.upper() for t in r.technology_types]
    if "PEM" not in tech_types_upper and "ALKALINE" not in tech_types_upper:
        continue
```

### After (V1.1 — Fixed)

```python
# Exact match: risk must explicitly list the query technology
risk_techs_upper = [t.upper() for t in r.technology_types]
tech_query = query.technology.upper()
if risk_techs_upper and tech_query not in risk_techs_upper:
    continue
```

---

## 5. Future Expansion

When adding new technology-specific risks to the library:

1. **Tag accurately** — use `["PEM"]`, `["Alkaline"]`, `["SOEC"]`, `["AEM"]`, or `["PEM", "Alkaline"]` for dual-applicable
2. **Never use `["PEM"]` for a risk that also applies to Alkaline** — this would hide it from Alkaline assessments
3. **For technology-agnostic risks** — use `["PEM", "Alkaline"]` explicitly (do not leave empty unless truly universal across all electrolysis technologies)
4. **For truly universal risks** (applicable to SOEC, AEM, etc.) — leave `technology_types` empty or add all known technologies
5. **Run this audit** after adding >5 new risks to verify no leakage
