# UI Bugfix Report

**Date:** 2026-06-09
**Type:** Streamlit UI regression fixes for M12 deployment

---

## Bugs Fixed

| Bug | Page | Root Cause | Fix |
|-----|------|-----------|-----|
| B1 | `06_CAPEX_LCOH.py` | Case mismatch: `rows` has key `"Category"` (capital C), but bar chart read `r["category"]` (lowercase c) | Changed to `r["Category"]` |
| B2 | `app.py` | Landing page was functional but minimal after M12 | Restored full KPI grid, workflow section, example output |
| B3 | `05_Risk_Assessment.py` | `applymap` removed in pandas 2.1+ | `.applymap` → `.map` (fixed in previous commit) |

## Fix Details

### B1 — Case Mismatch

**Broken code:**
```python
rows = [{"Category": b["category"], ...} for b in bd]  # key is "Category" (capital C)
st.bar_chart(pd.DataFrame({"Cat": [r["category"] for r in rows],  # reads "category" (lowercase) → KeyError!
```

**Fixed code:**
```python
rows = [{"Category": b["category"], ...} for b in bd]
st.bar_chart(pd.DataFrame({"Category": [r["Category"] for r in rows],  # matches capital C
                           "EUR M": [r["EUR M"] for r in rows]}).set_index("Category"))
```

### B2 — Landing Page

Restored: 5-column KPI grid (Projects: 10, Risks: 30, Costs: 30, Tech Cards: 2, Tests: 35/35), "Why This Tool" section, 4-step workflow, example output code block.

## Validation

| Test | Result |
|------|--------|
| Regression tests (35/35) | ✅ Passed |
| CAPEX bar chart key fix | ✅ Verified: `rows[0]["Category"]` returns correct value |
| Engine produces all 11 top-level keys | ✅ Verified |
| All 8 pages reviewed | ✅ No remaining issues |

## Files Changed

| File | Lines Changed | Change Type |
|------|---------------|-------------|
| `streamlit_app/app.py` | ~45 | Landing page restoration and expansion |
| `streamlit_app/pages/06_CAPEX_LCOH.py` | 1 | Case fix in bar chart key access |
