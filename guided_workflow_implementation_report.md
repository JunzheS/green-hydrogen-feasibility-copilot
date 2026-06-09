# Guided Workflow Implementation Report — Sprint 4F

**Date:** 2026-06-09
**Branch:** `main`
**Commit:** (pending)

---

## What Changed

### 1. Guided Workflow Sidebar (`theme.py`)

The sidebar now implements a 3-tier progressive disclosure system:

```
┌──────────────────────────────────────┐
│  H2 Feasibility Copilot              │
│  Multi-Agent Decision Platform       │
├──────────────────────────────────────┤
│  Home                        (always)│
│  Project Input               (always)│
├──────────────────────────────────────┤
│  Core Results                        │
│  Assessment Report        🗝 (locked)│
│  Risk Dashboard           🗝 (locked)│
│  CAPEX & LCOH             🗝 (locked)│
│  Reference Projects       🗝 (locked)│
│  History                  🗝 (locked)│
├──────────────────────────────────────┤
│  ▶ Expert Results (collapsed)        │
│    ├ Technology Assessment  🗝       │
│    ├ Technology Comparison  🗝       │
│    ├ Agent Trace            🗝       │
│    ├ Agent Collaboration    🗝       │
│    ├ OEM Intelligence               │
│    ├ Developer Intelligence         │
│    └ Source Transparency     🗝      │
├──────────────────────────────────────┤
│  Why This Matters           (always)│
├──────────────────────────────────────┤
│  Current Assessment                  │
│  100 MW PEM | France                │
│  PROCEED ▓▓▓▓▓▓                     │
│  v1.0 | 141 validated assets        │
└──────────────────────────────────────┘
```

### 2. Session State Logic

| State | Sidebar Behavior |
|-------|-----------------|
| **Before assessment** (`report` is `None`) | Core Results: greyed out with 🗝 lock icon, not clickable. Expert Results: collapsed by default, same locked state for assessment-gated pages |
| **After assessment** (`report` exists) | Core Results: active clickable links. Expert Results: active for assessment-gated pages. OEM and Developer Intelligence always active (no report needed) |
| **After page navigation** (session state preserved by `st.page_link`) | Same as after assessment — sidebar reflects current state |

### 3. Locked Page Styling

Locked pages are rendered as HTML `<span>` elements with:
- `color: #9E9E9E` (disabled grey)
- `opacity: 0.55`
- `cursor: not-allowed`
- `🗝` lock icon suffix
- No click target (not wrapped in `st.page_link`)

---

### 4. Auto-Redirect After Assessment (`01_Project_Input.py`)

**Before:** `st.rerun()` — reloads the input form, user has to manually navigate to Assessment Report

**After:** `st.switch_page("pages/02_Assessment_Report.py")` — immediately opens the Assessment Report showing the results

---

### 5. UI Consistency Fixes

All 12 items from [ui_consistency_audit.md](ui_consistency_audit.md) resolved:

| # | Fix | Pages |
|---|-----|-------|
| 1 | Card bg `#F9FBE7` → `#FFFFFF`, radius 10px → 8px | 09 |
| 2 | Text `#37474F` → `#1B5E20` | 09 |
| 3 | `st.subheader()` → `st.markdown("#### ...")` | 03, 04 |
| 4 | Card bg `#FAFAFA` → `#FFFFFF` | 07, 32 |
| 5 | Step number `#999` → `#558B2F` | 07 |
| 6 | Breadcrumb `<a href>` → `st.page_link` | 05, 06 |
| 7 | Expert drill-down `<a href>` → `st.page_link` | 02 |
| 8 | All design tokens centralized in `theme.py` with named constants | theme.py |
| 9 | Locked state CSS added | theme.py |
| 10 | Expert Results collapsible section | theme.py |
| 11 | `apply_sidebar()` guided workflow | theme.py |
| 12 | `_sidebar_link()` helper with lock/unlock logic | theme.py |

### 6. Design System Centralization (`theme.py`)

All colors are now defined as module-level constants:

```python
GREEN_PRIMARY   = "#1B5E20"
GREEN_SECONDARY = "#2E7D32"
GREEN_ACCENT    = "#558B2F"
GREEN_TINT_1    = "#E8F5E9"
GREEN_TINT_2    = "#C8E6C9"
# ... etc
```

Plus helper function `gate_colors()` for consistent gate outcome rendering across all pages. Page scripts can import these tokens for custom HTML elements:

```python
from utils.theme import GREEN_PRIMARY, GREEN_SECONDARY
```

---

## User Journey (Before vs After)

### Before Sprint 4F
```
Home → Project Input → Run → (stays on Input) → click Report in sidebar
→ Risk → CAPEX → Reference → Technology → Comparison → Trace →
Agent Collab → OEM → Developer → Source → History → Why This Matters
```
14 links in sidebar, no lock indication, no workflow guidance.

### After Sprint 4F
```
Home → Why This Matters → Project Input → Run → (auto-opens Report)
→ Risk → CAPEX → Reference → History
→ (optional) Expand "Expert Results" → Tech, Comparison, Trace, etc.
```
5 core results visible, 7 expert results behind collapsible section, lock icons show what's unavailable, auto-redirect moves user through the workflow.

---

## Summary

| Metric | Before | After |
|--------|--------|-------|
| Sidebar links (always visible) | 7 | 12 total, 5 Core + 2 Info always + 7 Expert (collapsed) |
| Locked link states | None | 🗝 greyed-out spans for 10 assessment-gated pages |
| Expert drill-down location | Page 02 expander only | Sidebar "Expert Results" expander (always accessible) |
| Post-assessment redirect | `st.rerun()` (stays on Input) | `st.switch_page()` (opens Report) |
| `<a href>` breadcrumb links | 2 locations | 0 |
| `st.subheader()` usage | 2 pages | 0 (all `####` markdown) |
| Non-canon card backgrounds | 4 locations | 0 (all `#FFFFFF` or `#E8F5E9`) |
| Color constants | Scattered across files | Single source in `theme.py` |
| Files modified | — | 11 |

### Files Modified
1. `streamlit_app/utils/theme.py` — complete rewrite
2. `streamlit_app/pages/01_Project_Input.py` — auto-redirect
3. `streamlit_app/pages/02_Assessment_Report.py` — expert drill-down to st.page_link
4. `streamlit_app/pages/03_Reference_Projects.py` — subheader → markdown
5. `streamlit_app/pages/04_Technology_Assessment.py` — subheader → markdown (6 instances)
6. `streamlit_app/pages/05_Risk_Assessment.py` — breadcrumb to st.page_link
7. `streamlit_app/pages/06_CAPEX_LCOH.py` — breadcrumb to st.page_link
8. `streamlit_app/pages/07_Agent_Trace.py` — card bg + step number color
9. `streamlit_app/pages/09_Technology_Comparison.py` — card bg + radius + text color
10. `streamlit_app/pages/32_Contradiction_Detection.py` — card bg
11. `ui_consistency_audit.md` — new documentation
