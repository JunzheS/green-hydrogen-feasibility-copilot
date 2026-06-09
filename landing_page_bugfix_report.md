# Landing Page Bugfix Report

**Date:** 2026-06-09
**Commit:** *(pending)*

---

## Root Cause

`app.py` wrapped the entire landing page in:
```python
if not st.session_state.get("assessment_complete"):
```

After running an assessment, `01_Project_Input.py` set `st.session_state["assessment_complete"] = True`. This made the landing page content **disappear** on return to the home page — leaving an empty title and subtitle.

## Fix

Removed the `if not st.session_state.get("assessment_complete"):` guard. The landing page now renders **unconditionally**.

After an assessment exists, a **"Recent Assessment" summary** row appears below the persistent landing page content with KPI metrics and navigation hints.

## Files Modified

| File | Change |
|------|--------|
| `streamlit_app/app.py` | Removed conditional guard; landing page always visible; added "Recent Assessment" section when report exists |

## Before / After

| Scenario | Before | After |
|----------|--------|-------|
| First visit | Landing page visible | Same |
| After running assessment, back to Home | Landing page hidden (empty) | Landing page visible + "Recent Assessment" summary at top |
| Sidebar current assessment | Visible | Unchanged |
| All other pages | Unchanged | Unchanged |

## Validation

| Test | Result |
|------|--------|
| Regression tests (35/35) | ✅ Passed |
| App starts with full landing page | ✅ Verified |
| Assessment completes without error | ✅ Verified |
| Landing page persists after assessment | ✅ Verified |
