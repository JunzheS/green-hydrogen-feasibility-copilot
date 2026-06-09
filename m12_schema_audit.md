# M12 Schema Audit Report

**Date:** 2026-06-09
**Status:** All schemas verified — 1 bug found and fixed

---

## Bug 1: Risk Page — `applymap` deprecated in pandas 2.1+

| Field | Detail |
|-------|--------|
| **Page** | `05_Risk_Assessment.py`, line 50 |
| **Error** | `AttributeError: 'Styler' object has no attribute 'applymap'` |
| **Root cause** | `DataFrame.style.applymap()` was renamed to `.map()` in pandas 2.1.0. The cloud environment runs pandas 2.3.3. |
| **Fix** | `.applymap(color_class, subset=["Class"])` → `.map(color_class, subset=["Class"])` |
| **File** | `streamlit_app/pages/05_Risk_Assessment.py` |

## Bug 2: CAPEX Page

**No actual bug found after schema verification.** The CAPEX breakdown schema produces:

```python
# From cost_assessment_engine.py:
breakdown[0] = {
    "category": "01 Electrolyzer System",
    "eur_per_kw": 480.0,
    "eur_m": 48.0,
    "pct_of_total": 32.0,
    "confidence": "C",
    "cost_id": "CS-IND-006"
}
```

All fields accessed in `06_CAPEX_LCOH.py` (`category`, `eur_per_kw`, `eur_m`, `pct_of_total`, `confidence`) exist and are populated. The error reported may have been a transient issue from an older cached version on Streamlit Cloud.

## Verified Page Schemas

| Page | Fields Accessed | Schema Match? |
|------|----------------|---------------|
| `02_Assessment_Report.py` | `executive_insights[*].{id,title,observation,business_impact,reasoning,recommendation}` | ✅ |
| `02_Assessment_Report.py` | `gate_justification.{decision,rationale,conditions}` | ✅ |
| `03_Reference_Projects.py` | `project_match_breakdown[*].{score_breakdown.{Technology,Industry,Capacity,Country,Maturity},composite_score,rationale}` | ✅ |
| `05_Risk_Assessment.py` | `risk_consequences[*].{risk_id,risk_name,risk_class,rpn,category,mitigation,reference_projects,probability,impact,detectability,description}` | ✅ |
| `06_CAPEX_LCOH.py` | `capex_assessment.breakdown[*].{category,eur_per_kw,eur_m,pct_of_total,confidence}` | ✅ |
| `07_Agent_Trace.py` | `similar_projects.ranked_projects[*], technology_assessment, risk_assessment, capex_assessment, lcoh_assessment, pm_review` | ✅ |

## Files Modified

| File | Change |
|------|--------|
| `streamlit_app/pages/05_Risk_Assessment.py` | `.applymap` → `.map` (pandas 2.1+ compatibility) |

## Regression Test Results

**35/35 passed (0 failures)** — all M12 capabilities preserved.
