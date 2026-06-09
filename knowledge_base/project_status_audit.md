# Project Status Audit

**Date:** 2026-06-09
**Scope:** All 82 Gold Dataset projects

---

## Status Distribution

| Status | Count | Percentage |
|--------|-------|-----------|
| operational | 27 | 33% |
| under_construction | 15 | 18% |
| planned | 40 | 49% |

## Status Gaps

| Missing Status | Count Needed | Reasoning |
|---------------|-------------|-----------|
| decommissioned | ≥1 | No cancelled or decommissioned projects exist. Lessons from failed projects are valuable for risk assessment. |
| cancelled | ≥1 | Same — adds risk evidence for the Risk Library. |

## Dataset Realism Score

The realism of the dataset is evaluated by comparing the status distribution against the real-world hydrogen project pipeline.

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **Operational share** | 7/10 | 33% operational is realistic for an emerging industry. Real-world: approximately 15-20% of announced projects reach operations. The dataset overweights operational projects (which is intentional — they provide better data). |
| **Under-construction share** | 8/10 | 18% is reasonable. Global hydrogen pipeline has approximately 10-15% of projects under construction. |
| **Planned share** | 6/10 | 49% planned is slightly below real-world share (~60-70% planned). This reflects intentional curation toward more concrete projects. |
| **Scale distribution** | 7/10 | Dominated by <20 MW (35%) and 50-100 MW (17%). Missing 20-50 MW projects (only 4). |
| **Technology diversity** | 9/10 | PEM (55%), Alkaline (30%), SOEC (4%), AEM (1%) — reasonably matches market distribution. |
| **Geographic spread** | 8/10 | 18 countries including major European + 2 non-European references. |
| **Real-to-planned ratio** | 7/10 | 51% real (operational + construction) vs 49% planned. Target: 60/40. |

## Realism Score: 7.4/10

## Recommendations

| Action | Priority | Impact |
|--------|----------|--------|
| Add 1 cancelled project for risk evidence | LOW | Improves risk coverage |
| Add 1 decommissioned project | LOW | Lessons learned reference |
| Target 60% real by Sprint 5 | MEDIUM | Improves dataset weight |
| Add 3-5 operational Alkaline projects | MEDIUM | Balances tech distribution |
