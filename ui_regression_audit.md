# UI Regression Audit — M12 Post-Fix

**Date:** 2026-06-09
**Status:** All regressions identified and fixed

---

## Audit Results

| Page | Status | Issue | Fix |
|------|--------|-------|-----|
| `app.py` | Fixed | Minimal landing page after M12 | Restored KPI grid (5 columns), "Why This Tool" section, 4-step workflow, example output |
| `01_Project_Input.py` | OK | No issues | — |
| `02_Assessment_Report.py` | OK | No issues | — |
| `03_Reference_Projects.py` | OK | No issues | — |
| `05_Risk_Assessment.py` | Previously fixed | `applymap` removed in pandas 2.1 | `.map()` already applied |
| `06_CAPEX_LCOH.py` | Fixed | `KeyError: 'category'` — case mismatch | `r["category"]` → `r["Category"]` |
| `07_Agent_Trace.py` | OK | No issues | — |
| `08_Assessment_History.py` | OK | No issues | — |

## Regression Details

### Issue 1 — CAPEX Page Failure

- **Root cause:** The bar chart list comprehension used `r["category"]` (lowercase) but the preceding `rows` list had key `"Category"` (capital C)
- **Fix:** Changed to `r["Category"]` and `r["EUR M"]` to match the actual keys in the rows list

### Issue 2 — Landing Page Regression

- **Root cause:** The app.py landing page after M12 was functional but sparse — missing technology cards KPI, validation badge, workflow section, and example output
- **Fix:** Restored 5-column KPI grid (Projects, Risks, Cost Records, Tech Cards, Tests), added "Why This Tool", 4-step workflow, and example output code block

### Issue 3 — CAPEX schema verified

| Field | Type | Example | Used in page? |
|-------|------|---------|---------------|
| `category` | `str` | `01 Electrolyzer System` | ✅ |
| `eur_per_kw` | `float` | `480.0` | ✅ |
| `eur_m` | `float` | `48.0` | ✅ |
| `pct_of_total` | `int` | `32` | ✅ |
| `confidence` | `str` | `C` | ✅ |
| `cost_id` | `str` | `CS-IND-006` | Not displayed (internal) |

## Files Modified

| File | Change |
|------|--------|
| `streamlit_app/app.py` | Restored/expanded landing page with full KPI grid, workflow, example output |
| `streamlit_app/pages/06_CAPEX_LCOH.py` | Fixed KeyError: `r["category"]` → `r["Category"]` |
