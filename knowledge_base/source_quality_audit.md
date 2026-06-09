# Source Quality Audit

**Date:** 2026-06-09
**Scope:** All 110 source citations across 82 project records

---

## Source Level Distribution

| Level | Count | Percentage | Definition |
|-------|-------|-----------|------------|
| **A** — Official Primary | 57 | 51.8% | Developer press releases, government announcements, OEM datasheets |
| **B** — Authoritative Industry | 19 | 17.3% | IEA, IRENA, Hydrogen Council reports |
| **C** — Professional Media | 34 | 30.9% | Industry news, trade publications |
| **D** — Unverified | 0 | 0.0% | Not used |

## Quality Per Project

| Level A % | Projects | Rating |
|-----------|----------|--------|
| 100% Level A | 0 projects | Excellent |
| ≥50% Level A | 62 projects | Good |
| <50% Level A, Level B+C | 20 projects | Adequate (needs follow-up) |
| Only Level C | 20 projects | Weak |

## Projects Requiring Stronger Sourcing

These 20 projects have only Level C (professional media) sources. Data is plausible but not verified against official or authoritative sources.

| Project ID | Project Name | Country | MW | Status |
|-----------|-------------|---------|-----|--------|
| GA-PR-016 | H4 Marseille Fos | France | 390 | planned |
| GA-PR-023 | MadoquaPower2X | Portugal | 500 | planned |
| GA-PR-026 | HH2E Lubmin | Germany | 100 | planned |
| GA-PR-031 | DH2 Dunkirk | France | 400 | planned |
| GA-PR-033 | TES Zeebrugge | Belgium | 200 | planned |
| GA-PR-034 | Hyport Green Ammonia | Denmark | 100 | planned |
| GA-PR-036 | Verso Energy | France | 200 | planned |
| GA-PR-040 | Hydrogen Pancevo | Serbia | 5 | planned |
| GA-PR-041 | LHC Methanol | France | 20 | planned |
| GA-PR-042 | Green H2 Atlantic | Portugal | 100 | planned |
| GA-PR-053 | P2X Joensuu | Finland | 40 | planned |
| GA-PR-060 | Uniper Maasvlakte | Netherlands | 100 | planned |
| GA-PR-066 | HH2E Hydrogen City | Germany | 500 | planned |
| GA-PR-067 | ERM Dolphyn | UK | 10 | planned |
| GA-PR-071 | Ferrara Chemical Park | Italy | 50 | planned |
| GA-PR-072 | GreeN e-LNG | Netherlands | 150 | planned |
| GA-PR-073 | Morbihan H2 Valley | France | 10 | under_construction |
| GA-PR-077 | H2V Belfort | France | 200 | planned |
| GA-PR-079 | Valorem Aquitaine | France | 10 | planned |
| GA-PR-081 | Alcazar Suez | France | 50 | planned |

**Common pattern:** All 20 are planned/pre-FID projects, mostly pre-commercial. Level C sources are characteristic for early-stage projects that have not yet issued official press releases. Acceptable for the dataset purpose with appropriate confidence flagging.

## Source Quality vs Project Status

| Status | Count | Avg Sources/Project | Level A % | Level B % | Level C % |
|--------|-------|-------------------|-----------|-----------|-----------|
| operational | 27 | 1.6 | 62% | 21% | 17% |
| under_construction | 15 | 1.4 | 57% | 19% | 24% |
| planned | 40 | 1.1 | 33% | 14% | 53% |

**Finding:** Operational projects have the strongest sourcing (62% Level A). Planned projects rely more on Level C media sources (53%), consistent with their pre-FID status.

## Improvement Actions

| Action | Projects Affected | Effort |
|--------|------------------|--------|
| Add Level A source when project reaches FID | 20 Level C-only projects | Ongoing |
| Add Level B sources (IEA/IRENA cross-ref) | 20 Level C-only projects | 0.5 days |
| Remove/flag projects that stall or cancel | 0 currently | Review every 6 months |
