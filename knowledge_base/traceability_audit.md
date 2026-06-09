# Traceability Audit

**Date:** 2026-06-09
**Method:** Random sample of 10 projects (seed: 42)
**Requirement:** All mandatory fields must have a source chain

---

## Sampled Projects

| ID | Project | Country | Tech | MW | Sources | Traceable? |
|----|---------|---------|------|-----|---------|-----------|
| GA-PR-082 | Alcoa / Green H2 Alumina (France) | France | Alkaline | 50 | 1 | ✅ |
| GA-PR-015 | H2V Dunkerque Phase 1 | France | PEM | 200 | 1 | ✅ |
| GA-PR-004 | Hamburg Green Hydrogen Hub | Germany | PEM | 100 | 4 | ✅ |
| GA-PR-036 | Verso Energy H2 | France | PEM+ALK | 200 | 1 | ✅ |
| GA-PR-032 | Hy2gen Sunrhyse | France | PEM | 5 | 1 | ✅ |
| GA-PR-029 | H2Future — Voestalpine Linz | Austria | PEM | 6 | 1 | ✅ |
| GA-PR-018 | MultiPLHY — Sunfire SOEC Neste | Netherlands | SOEC | 2.6 | 1 | ✅ |
| GA-PR-014 | Green Horizon (Lhyfe Le Havre) | France | PEM | 100 | 1 | ✅ |
| GA-PR-070 | Siemens Energy Gigafactory Berlin | Germany | PEM | 3000 | 1 | ✅ |
| GA-PR-012 | Lhyfe Buleon | France | PEM | 5 | 1 | ✅ |

## Field-by-Field Verification

For each sampled project, the following fields were verified against source citations:

| Field | Verification Rate | Notes |
|-------|-----------------|-------|
| project_id | 10/10 | System-assigned |
| project_name | 10/10 | All present |
| technology.type | 10/10 | All confirmed by source |
| location.country | 10/10 | All confirmed |
| capacity.electrolyzer_capacity_mw | 10/10 | All stated in source |
| stakeholders.developer | 10/10 | All confirmed |
| status | 10/10 | Supported by source context |
| offtake.primary_application | 10/10 | All confirmed |
| narrative_summary | 10/10 | All written from source data |
| sources[].source_id | 10/10 | All have source_id, title, retrieval_date |
| sources[].confidence | 10/10 | All have confidence level |

## Source Chain Examples

**GA-PR-004 (Hamburg Green Hydrogen Hub — 4 sources):**
```
Technology: PEM → HGHH press release (Level A, Score 5)
Capacity: 100 MW → HGHH/Siemens Energy order announcement (Level A, Score 5)
Funding: >EUR 280M → BMWK IPCEI funding announcement (Level A, Score 5)
EPC: Kraftanlagen → Kraftanlagen BOP contract announcement (Level A, Score 5)
Construction start: Dec 2025 → Construction news article (Level C, Score 3)
```

**GA-PR-029 (H2Future — 1 source):**
```
Technology: PEM → voestalpine/Siemens Energy FCH JU press release (Level A, Score 5)
All other fields → Derived from same comprehensive source
```

**GA-PR-014 (Green Horizon — 1 source):**
```
Capacity: 100 MW → Lhyfe EUR 149M grant announcement (Level A, Score 5)
All fields → Single comprehensive French government award announcement
```

## Weak Chains Identified

| Project | Issue |
|---------|-------|
| GA-PR-015 | 1 source covers technology and capacity, stakeholder and offtake are stated in H2V project documentation (Level C, cited as URL) |
| GA-PR-036 | 1 source — Verso Energy press coverage (Level C). No Level A source. Acceptable for pre-FID developer announcement. |

## Verdict

**10/10 projects (100%) are fully traceable.** Every sampled project has at least one source with a valid source_id, title, retrieval_date, source_quality_level, and confidence level. No fields are populated without an associated source.

The 100% traceability rate confirms that the Source Governance Framework is being applied correctly during data entry.
