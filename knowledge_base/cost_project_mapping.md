# Cost Project Mapping — Sprint 1

**Document:** Cost Record ↔ Gold Dataset & Technology Card Cross-Reference
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Knowledge Engineer

---

## Gold Dataset Project Mapping

| Cost Record | Gold Dataset Project | Link Type | Evidence |
|------------|---------------------|-----------|----------|
| CS-ELC-008 | **GA-PR-001 Normand'Hy** | Direct — total CAPEX disclosure | Stack cost derived from >€400M Air Liquide total CAPEX |
| CS-ELC-010 | **GA-PR-009 Hyoffwind** | Direct — total CAPEX disclosure | Stack cost derived from €72M Virya Energy total CAPEX |
| CS-ELI-002 | **GA-PR-004 HGHH** | Qualitative validation | Brownfield 380 kV grid reuse cited as cost advantage |
| CS-ELI-003 | **GA-PR-003 Holland Hydrogen I** | Direct — substation contract | TenneT Amaliahaven 380 kV dedicated substation |
| CS-CIV-003 | **GA-PR-004 HGHH** | Qualitative validation | Moorburg coal plant brownfield repurposing |
| CS-ELC-003 | **GA-PR-006 Puertollano** | Qualitative scale validation | 20 MW PEM operational — validates small-scale premium |
| CS-IND-006 | **GA-PR-001 Normand'Hy** | Qualitative total CAPEX benchmark | €2,250/kW all-in (consistent with FOAK adjustment) |
| CS-IND-007 | **GA-PR-003 Holland Hydrogen I** | Qualitative (FOAK context) | €5,000/kW FOAK not comparable as nth-of-a-kind |
| CS-IND-006 | **GA-PR-010 Galp Sines** | Qualitative | ~€2,500/kW (H₂ portion estimated) |
| CS-ELC-009 | **GA-PR-002 Masshylia** | Qualitative (learning curve context) | Scale-down illustrates cost uncertainty at pre-FID |

---

## Technology Card Mapping

| Cost Record | Technology Card | Section Referenced |
|------------|----------------|-------------------|
| CS-ELC-001, 003, 006, 008, 009 | **TC-PEM-001** | cost_profile.capex_eur_per_kw, cost_profile.cost_drivers |
| CS-ELC-002, 007, 010 | **TC-ALK-001** | cost_profile.capex_eur_per_kw, cost_profile.cost_drivers |
| CS-ELC-004 | **TC-PEM-001** | infrastructure.power_supply_requirements (IGBT) |
| CS-ELC-005 | **TC-ALK-001** | infrastructure.power_supply_requirements (thyristor) |
| CS-HPR-001, 003 | **TC-PEM-001** | performance (30 bar outlet, 99.99% purity) |
| CS-HPR-002, 005 | **TC-ALK-001** | performance (atmospheric, 99.9% purity) + technical_risks[TCR-ALK-005] |
| CS-CIV-001 | **TC-PEM-001** | scalability.footprint_sqm_per_mw (50 m²/MW) |
| CS-CIV-002 | **TC-ALK-001** | scalability.footprint_sqm_per_mw (80 m²/MW) |
| CS-IND-004 | **TC-PEM-001** | maturity (TRL 8, early commercial) |
| CS-IND-005 | **TC-ALK-001** | maturity (TRL 9, mature) |

---

## Risk Library Mapping

| Cost Record | Risk ID | Link |
|------------|---------|------|
| CS-ELC-001 | RK-TEC-001, RK-FIN-001 | PEM stack degradation drives replacement cost; CAPEX overrun risk |
| CS-ELC-010 | RK-SCP-001 | Alkaline OEM manufacturing capacity (John Cockerill) |
| CS-ELI-001, 002 | RK-GRD-001, RK-GRD-002 | Grid connection delay and congestion |
| CS-ELI-003 | RK-GRD-001, RK-SCP-004 | HH1 grid connection risk management; transformer lead times |
| CS-HPR-002 | RK-TEC-003 | H₂ compression equipment reliability |
| CS-IND-004, 005 | RK-FIN-001 | Contingency adequacy for CAPEX overrun |
| CS-IND-006, 007 | RK-FIN-001, RK-FIN-003 | Total CAPEX benchmarking; project financing |

---

## Coverage Summary

| Mapping Type | Count |
|-------------|-------|
| Gold Dataset projects referenced | 7 of 10 (GA-PR-001, 002, 003, 004, 006, 009, 010) |
| Technology Cards referenced | 2 of 2 (TC-PEM-001, TC-ALK-001) |
| Risk Library entries cross-referenced | 6 unique risk IDs |
| Cost records with at least one project/card/risk link | 17 of 30 (57%) |

**Non-mapped records (13):** These are generic industry benchmarks (CS-ELC-004/005 power electronics, CS-ELI-004/005 MV/LV and backup, CS-HPR-004/005 compression/purification variants, CS-IND-001/002/003 engineering/PM costs). They reference IEA/IRENA/AACE standards rather than specific projects — appropriate for benchmark-level cost data.

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer |
