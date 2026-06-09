# OPEX Taxonomy Framework — Green Hydrogen Project Operating Costs

**Document:** OPEX Classification System v1.0
**Date:** 2026-06-05
**Author:** Hydrogen Economist & Industrial Cost Engineer
**Scope:** PEM and Alkaline electrolysis projects, pre-feasibility through operations
**Reference:** Technology Cards TC-PEM-001 §cost_profile.opex_breakdown, TC-ALK-001 §cost_profile.opex_breakdown; IEA GHR 2025; IRENA 2024

---

## 1. Design Principles

| Principle | Implementation |
|-----------|---------------|
| **IEA/IRENA-consistent** | OPEX categories align with IEA GHR and IRENA cost reporting for direct benchmark comparability |
| **Technology-differentiated** | Every category identifies PEM vs Alkaline cost differential |
| **Scale-aware** | Categories identify scaling behavior (fixed, linear, sub-linear) |
| **Electricity-first** | Electricity is 70-75% of OPEX — the taxonomy reflects this dominance without treating other categories as negligible |
| **Full-lifecycle** | Covers 20+ year operational life including stack replacement cycles |
| **LCOH-ready** | Designed to feed directly into the LCOH calculation framework (lcoh_methodology_framework.md) |

---

## 2. Taxonomy Overview — 9 Categories

```
GREEN HYDROGEN PROJECT OPEX TAXONOMY
│
├── CAT-O1 ELECTRICITY (70-75% of OPEX, 50-55% of LCOH)
│   └── Grid electricity, PPA costs, renewable self-generation O&M, grid tariffs, taxes/levies
│
├── CAT-O2 STACK REPLACEMENT (10-15% of OPEX, 7-11% of LCOH)
│   └── Periodic stack/module replacement at end of useful life, including installation labor
│
├── CAT-O3 MAINTENANCE (8-10% of OPEX, 6-8% of LCOH)
│   ├── O3.1 Preventive Maintenance (scheduled inspections, component replacement, calibrations)
│   ├── O3.2 Corrective Maintenance (unplanned repairs, equipment failure response)
│   └── O3.3 Service Contracts (OEM long-term service agreements, BOP maintenance contracts)
│
├── CAT-O4 LABOR (5-8% of OPEX, 4-6% of LCOH)
│   ├── O4.1 Operations Staff (shift operators, control room, plant management)
│   ├── O4.2 Maintenance Staff (electrical, mechanical, I&C technicians)
│   └── O4.3 Support Staff (HSE, administration, security, training)
│
├── CAT-O5 WATER & CONSUMABLES (2-4% of OPEX, 1.5-3% of LCOH)
│   ├── O5.1 Raw Water (municipal supply, desalination, groundwater extraction)
│   ├── O5.2 Water Treatment Consumables (RO membranes, EDI modules, ion exchange resin, chemicals)
│   └── O5.3 Electrolyte & Process Consumables (KOH for Alkaline, nitrogen purge, lubricants)
│
├── CAT-O6 INSURANCE (1-2% of OPEX, 0.7-1.5% of LCOH)
│   └── Property damage, business interruption, third-party liability, construction all-risk (during construction)
│
├── CAT-O7 LAND LEASE & FACILITIES (1-2% of OPEX, 0.7-1.5% of LCOH)
│   └── Land lease/rent, property taxes, facility management, security, utilities (non-process)
│
├── CAT-O8 REGULATORY & COMPLIANCE (0.5-1.5% of OPEX, 0.4-1% of LCOH)
│   └── Environmental monitoring, emissions trading, RFNBO certification maintenance, safety audits
│
└── CAT-O9 OTHER (1-3% of OPEX, 0.7-2% of LCOH)
    └── Corporate overhead allocation, IT/OT systems, training, contingencies, miscellaneous
```

---

## 3. Category Detail

### CAT-O1: Electricity (70-75% of OPEX)

**Description:** The cost of electrical energy consumed by the electrolyzer stack and balance of plant. Electricity is the dominant OPEX component — surpassing all other categories combined by a factor of ~3×. This makes electricity price the single most important economic assumption for any green hydrogen project.

| Attribute | PEM | Alkaline |
|-----------|-----|----------|
| **System efficiency** | 55 kWh/kg H₂ | 53 kWh/kg H₂ |
| **At €40/MWh** | €2.20/kg H₂ | €2.12/kg H₂ |
| **At €60/MWh** | €3.30/kg H₂ | €3.18/kg H₂ |
| **At €100/MWh** | €5.50/kg H₂ | €5.30/kg H₂ |

**Cost drivers:**
- Wholesale electricity price (market or PPA)
- Grid tariffs and network charges (location-dependent)
- Renewable energy taxes and levies (country-specific)
- Electrolyzer system efficiency (technology-dependent)
- BOP electricity consumption (pumps, compressors, cooling — ~3-5% of stack consumption)
- Renewable integration strategy (dedicated PPA vs. market purchase vs. self-generation)

**Technology dependency: HIGH** — Alkaline is 4% more efficient (53 vs 55 kWh/kg). At €40/MWh, this saves €0.08/kg H₂. At €100/MWh, it saves €0.20/kg H₂.

**Scale dependency: LOW** — Electricity cost per kg H₂ is independent of plant scale (assuming same efficiency). Larger plants may secure more favorable PPAs.

**Data sources:** Technology Cards TC-PEM-001 §performance, TC-ALK-001 §performance; IEA GHR 2025; IRENA 2024.

---

### CAT-O2: Stack Replacement (10-15% of OPEX)

**Description:** The periodic replacement of electrolyzer stacks at the end of their useful life. This is a CAPEX-like cost that recurs every 6-12 years depending on technology and operating profile. It is treated as OPEX through a sinking fund or annualized replacement provision.

| Attribute | PEM | Alkaline |
|-----------|-----|----------|
| **Stack lifetime** | 60,000-80,000 hours (~8 years at 8,000 hr/yr) | 80,000-100,000 hours (~10-12 years) |
| **Replacement cost (€/kW)** | €350/kW (stack portion only) | €200/kW |
| **Annualized (€/kW/year)** | ~€35-45/kW/year | ~€16-22/kW/year |
| **Annualized (€/kg H₂)** | ~€0.10-0.15/kg | ~€0.05-0.08/kg |
| **Replacements in 20-year life** | 1.5-2.5 replacements | 1-1.5 replacements |

**Cost drivers:**
- Stack degradation rate (higher degradation → earlier replacement)
- Operating profile (dynamic operation accelerates degradation, especially for PEM)
- Warranty terms (OEM degradation guarantee limits financial exposure)
- OEM pricing for replacement stacks (may differ from initial CAPEX pricing)
- Technology learning (replacement stack in year 8 may be 40% cheaper than year 0 stack)

**Technology dependency: HIGH** — PEM replacement cost is ~2× Alkaline due to higher stack cost and shorter lifetime.

**Scale dependency: MEDIUM** — Replacement cost scales sub-linearly with plant size (volume pricing, but less than initial CAPEX due to smaller order quantity).

**Data sources:** TC-PEM-001 §cost_profile.stack_replacement_cost_eur_per_kw; TC-ALK-001 §cost_profile; IEA Electrolyser Durability 2025.

---

### CAT-O3: Maintenance (8-10% of OPEX)

| Subcategory | Description | Typical % of OPEX | PEM vs Alkaline |
|------------|------------|-------------------|-----------------|
| **O3.1 Preventive** | Scheduled inspections, filter changes, oil changes, calibrations, valve exercising, instrumentation checks | 5-6% | PEM +10% (more frequent stack monitoring required) |
| **O3.2 Corrective** | Unplanned repairs: pump failures, compressor valve replacement, heat exchanger cleaning, instrument replacement | 2-3% | Technology-neutral |
| **O3.3 Service Contracts** | OEM LTSA fees, BOP equipment service agreements, DCS/SIS software maintenance | 1-2% | PEM +20% (OEM service for PEM stacks is more specialized) |

**Technology dependency: MODERATE** — PEM maintenance is ~10-15% higher than Alkaline due to: (a) more specialized PEM stack maintenance (Ti/PFSA expertise), (b) stricter water quality requiring more frequent treatment system maintenance, (c) fewer qualified service providers.

**Scale dependency: LOW-MEDIUM** — Maintenance staff and service contracts scale sub-linearly. A 200 MW plant needs ~50% more maintenance staff than a 100 MW plant, not 2×.

**Data sources:** TC-PEM-001 §infrastructure.maintenance_requirements; TC-ALK-001 §infrastructure.maintenance_requirements; IEA GHR 2025.

---

### CAT-O4: Labor (5-8% of OPEX)

| Subcategory | Description | Typical Staffing (100 MW plant) |
|------------|------------|-------------------------------|
| **O4.1 Operations** | Shift operators, control room operators, plant manager | 20-30 FTE (4-6 per shift × 5 shifts) |
| **O4.2 Maintenance** | Electrical, mechanical, I&C technicians | 10-15 FTE |
| **O4.3 Support** | HSE, administration, security, training | 5-8 FTE |
| **Total** | | **35-55 FTE** |

**Technology dependency: MODERATE** — PEM requires slightly more specialized (higher-cost) operations staff. Alkaline requires additional electrolyte management labor.

**Scale dependency: LOW — STRONG ECONOMIES OF SCALE** — A 20 MW plant may need 15-20 FTE (€0.05-0.08/kg labor cost). A 300 MW plant may need 50-70 FTE (€0.02-0.03/kg). Labor cost per kg H₂ drops ~50% from 20→300 MW.

**Regional dependency: HIGH** — Labor rates vary 3-5× between Western Europe (€60-100K/FTE fully loaded) and MENA/India (€15-30K/FTE).

**Data sources:** TC-PEM-001 §infrastructure.workforce_skill_requirements; TC-ALK-001 §infrastructure.workforce_skill_requirements; IEA GHR 2025.

---

### CAT-O5: Water & Consumables (2-4% of OPEX)

| Subcategory | Typical Cost (€/kg H₂) | PEM vs Alkaline |
|------------|------------------------|-----------------|
| **O5.1 Raw Water** | €0.01-0.03/kg | Technology-neutral (~10-11 L/kg H₂) |
| **O5.2 Water Treatment Consumables** | €0.01-0.02/kg | PEM +30-50% (stricter spec → more frequent RO/EDI replacement) |
| **O5.3 Electrolyte & Process Consumables** | €0.01-0.03/kg | Alkaline +100% (KOH replenishment, nitrogen purge) |

**Technology dependency: MODERATE** — The net cost is similar for both technologies. PEM spends more on water treatment; Alkaline spends more on KOH electrolyte.

**Scale dependency: LOW** — Consumable consumption scales near-linearly with production.

---

### CAT-O6 through CAT-O9: Minor OPEX (4-8% combined)

| Category | Typical €/kg H₂ | Key Characteristic |
|----------|----------------|-------------------|
| **O6 Insurance** | €0.02-0.05/kg | Immature H₂ insurance market; premiums may decrease as industry matures |
| **O7 Land & Facilities** | €0.02-0.04/kg | Brownfield sites reduce cost; greenfield adds lease/purchase |
| **O8 Regulatory & Compliance** | €0.01-0.03/kg | RFNBO certification adds €0.01-0.02/kg; Seveso compliance adds €0.005-0.01/kg |
| **O9 Other** | €0.02-0.05/kg | Corporate overhead allocation; varies by developer |

---

## 4. OPEX Summary — Reference Case (100 MW, 4,500 full-load hours/year)

| Category | PEM (€/kg) | PEM (%) | Alkaline (€/kg) | Alkaline (%) |
|----------|-----------|---------|----------------|-------------|
| O1 Electricity (@€40/MWh) | 2.20 | 72% | 2.12 | 74% |
| O2 Stack Replacement | 0.12 | 4% | 0.06 | 2% |
| O3 Maintenance | 0.30 | 10% | 0.23 | 8% |
| O4 Labor | 0.18 | 6% | 0.17 | 6% |
| O5 Water & Consumables | 0.08 | 3% | 0.08 | 3% |
| O6 Insurance | 0.05 | 2% | 0.05 | 2% |
| O7 Land & Facilities | 0.04 | 1% | 0.04 | 1% |
| O8 Regulatory | 0.03 | 1% | 0.03 | 1% |
| O9 Other | 0.05 | 2% | 0.05 | 2% |
| **TOTAL OPEX** | **~3.05** | **100%** | **~2.83** | **100%** |

**Key insight:** At €40/MWh, Alkaline's OPEX advantage is ~€0.22/kg (7%). This is driven by: (a) 4% higher efficiency, (b) lower stack replacement cost, (c) lower maintenance. At €100/MWh electricity, the OPEX advantage widens to ~€0.42/kg because the efficiency difference compounds with price.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Hydrogen Economist & Industrial Cost Engineer | Initial OPEX taxonomy |
