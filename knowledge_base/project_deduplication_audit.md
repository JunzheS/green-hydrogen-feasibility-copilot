# Project Deduplication Audit

**Date:** 2026-06-09
**Scope:** All 82 Gold Dataset project records (GA-PR-001 through GA-PR-082)

---

## Methodology

Each project was checked for duplicates across six dimensions:
1. Exact project name match
2. Similar/alternative name match
3. Same developer + same country + same technology
4. Same location + same developer
5. Same location + same capacity + same technology
6. Alternative names listed in `alias_names` fields

## Results

| Check | Result |
|-------|--------|
| Exact duplicate names | **0** |
| Similar name pairs (near-match) | **0** |
| Same developer + country + tech | **0** |
| Same location + developer | **0** |
| Same location + capacity + tech | **0** |
| **Confirmed duplicates** | **0/82** |

## Cross-Reference Check

| GA-PR-ID | Project Name | Notes |
|----------|-------------|-------|
| GA-PR-005 | HyDeal Espana | Separate from GA-PR-076 (HyDeal Asturias) — different region (Castilla-La Mancha vs Asturias), different phase, different technology scope |
| GA-PR-015 | H2V Dunkerque Phase 1 | Separate from GA-PR-031 (DH2 Dunkirk) — different developer (H2V vs DH2 Energy), different technologies |
| GA-PR-020 | GET H2 Nukleus | Separate from GA-PR-044 (RWE Lingen 14 MW pilot) — distinct phases of the same site but different capacities and COD dates |
| GA-PR-022 | H2 Green Steel Boden | Separate from GA-PR-043 (HYBRIT) — different companies, locations, though same country and same offtake |
| GA-PR-001 | Normand'Hy | GA-PR-028 (Grandpuits) and GA-PR-037 (Seine Axis mobility) are all separate projects sharing the same developer |

## Verdict

**0 confirmed duplicates. All 82 records are unique.**

No projects share identical name, developer, location, and technology. Where projects share a developer (Air Liquide, Lhyfe, H2V), their capacities, locations, and offtakes are distinct. Where projects share a location (Dunkirk, Sines), their developers and technologies are distinct.
