# UI Consistency Audit — Sprint 4F

**Date:** 2026-06-09
**Pages audited:** 14 (app.py + 13 page scripts)
**Design system scope:** colors, typography, cards, sidebar, navigation, expert pages

---

## 1. Color Palette Audit

### Design System Canon (from theme.py)

| Role | Value | Name |
|------|-------|------|
| Primary green | `#1B5E20` | Dark green (headers, landmarks) |
| Secondary green | `#2E7D32` | Mid green (gate badges, KPIs, backgrounds) |
| Accent green | `#558B2F` | Light green (captions, labels, metadata) |
| Success / PROCEED | `#2E7D32` | Gate outcome color |
| Warning / CAUTION | `#F9A825` | Amber gate / medium severity |
| Critical / STOP | `#C62828` | Red gate / critical severity |
| Grey / neutral | `#78909C` | Insufficient data / neutral |
| Background light | `#E8F5E9` | Lightest green tint |
| Surface white | `#FFFFFF` | Metric card backgrounds |
| Heatmap critical | `#D32F2F` | Risk heatmap only |
| Heatmap high | `#EF6C00` | Risk heatmap only |
| Heatmap medium | `#F9A825` | Risk heatmap only |
| Heatmap low | `#A5D6A7` | Risk heatmap only |

### Issues Found

| # | File | Line | Color Used | Canon? | Severity | Verdict |
|---|------|------|-----------|--------|----------|---------|
| 1 | `09_Technology_Comparison.py` | 49 | `#F9FBE7` (card bg) | NO | HIGH | **FIX** — should be `#FFFFFF` or `#E8F5E9` |
| 2 | `09_Technology_Comparison.py` | 40 | `#37474F` (text) | NO | MEDIUM | **FIX** — should be `#1B5E20` |
| 3 | `02_Assessment_Report.py` | 104 | `#FFF3E0` (insight variant) | NO | MEDIUM | **KEEP** — deliberate semantic variant for non-financial insights |
| 4 | `02_Assessment_Report.py` | 75 | `#FFFDE7` (adeq. bg) | NO | LOW | **KEEP** — gate severity signal, not decoration |
| 5 | `02_Assessment_Report.py` | 75 | `#FFEBEE` (fail bg) | NO | LOW | **KEEP** — gate severity signal |
| 6 | `07_Agent_Trace.py` | 55 | `#FAFAFA` (card bg) | NO | MEDIUM | **FIX** — use `#FFFFFF` matching theme surface |
| 7 | `07_Agent_Trace.py` | 53 | `#999` (step number) | NO | LOW | **FIX** — use `#558B2F` (accent) |
| 8 | `32_Contradiction_Detection.py` | 45 | `#FAFAFA` (card bg) | NO | MEDIUM | **FIX** — same as #6 |
| 9 | `05_Risk_Assessment.py` | 48 | `#A5D6A7` (low risk in heatmap) | YES | OK | **KEEP** |
| 10 | All pages | — | `#558B2F` for caption text | YES | OK | **KEEP** |
| 11 | `06_CAPEX_LCOH.py` | 29 | `#E0E0E0` (range bar) | NO | LOW | **KEEP** — functional UI element, not branding |
| 12 | `06_CAPEX_LCOH.py` | 33 | `#A5D6A7` in gradient | YES | OK | **KEEP** |
| 13 | `07_Agent_Trace.py` | 100-105 | `#A5D6A7`, `#81C784`, `#66BB6A`, `#43A047` (agent steps) | DEPENDS | OK | **KEEP** — semantic agent differentiation, consistent with homepage pipeline |
| 14 | `app.py` | 24-40 | `#C8E6C9`, `#A5D6A7`, `#81C784`, `#4CAF50`, `#1B5E20` (agent pipeline) | YES | OK | **KEEP** |

---

## 2. Typography Audit

| # | File | Issue | Consistency | Verdict |
|---|------|-------|-------------|---------|
| 1 | `04_Technology_Assessment.py` | Uses `st.subheader()` for sections | Pages 02, 05, 06 use `st.markdown("#### ...")` | **FIX** — standardize to `####` markdown |
| 2 | `03_Reference_Projects.py` | `st.subheader("Why Each Project Was Selected")` | Rest uses `####` | **FIX** — change to `####` |
| 3 | `04_Technology_Assessment.py` | Title uses `st.title()` | Consistent across all pages | **KEEP** |
| 4 | All pages | `st.caption()` usage | Consistent | **KEEP** |
| 5 | `06_CAPEX_LCOH.py` | Section headers use `st.markdown("#### ...")` | Consistent with 02, 05, 07 | **KEEP** |

### Typography Hierarchy (canon)

| Level | Element | Size (CSS) | Color |
|-------|---------|-----------|-------|
| H1 | `st.title()` | 1.8rem | `#1B5E20` |
| H2 | `st.markdown("### ...")` | 1.2rem | `#2E7D32` |
| H3 | `st.markdown("#### ...")` | 1.1rem | `#2E7D32` |
| Body | `st.markdown("...")` | 1.05rem | default |
| Caption | `st.caption("...")` | 0.9rem | `#558B2F` |
| Metric value | `st.metric(...)` | 1.5rem | `#2E7D32` |
| Dataframe | `st.dataframe(...)` | 0.95rem | default |

---

## 3. Cards and Metrics Audit

| # | Page | Card Type | Height | Border Radius | Background | Verdict |
|---|------|-----------|--------|---------------|------------|---------|
| 1 | 02 | Gate banner | auto | 12px | gate color | **KEEP** — unique decision element |
| 2 | 02 | Dimension score cards | auto | 8px | conditional | **KEEP** |
| 3 | 02 | Insight cards | auto | 8px | `#E8F5E9` / `#FFF3E0` | **KEEP** |
| 4 | 03 | Project container | auto | default | `border=True` | **KEEP** — Streamlit native |
| 5 | 07 | Step cards | auto | 0 8px 8px 0 | `#FAFAFA` → **FIX** `#FFFFFF` | **FIX** bg |
| 6 | 09 | Tech comparison cards | auto | 10px | `#F9FBE7` → **FIX** `#FFFFFF` | **FIX** bg + radius (should be 8px) |
| 7 | 09 | Recommendation banner | auto | 10px | `#E8F5E9` | **FIX** radius to 8px |
| 8 | 32 | Agreement cards | auto | 8px | `#FAFAFA` → **FIX** `#FFFFFF` | **FIX** bg |
| 9 | 02 | Expert drill-down buttons | auto | 6px | `#E8F5E9` / `#FFFDE7` | **KEEP** — functional buttons |

### Metric Cards
All pages use `st.metric()` which is styled globally by theme.css → **CONSISTENT**.

---

## 4. Sidebar Audit

| # | Issue | Severity | Verdict |
|---|-------|----------|---------|
| 1 | No disabled/locked state exists for assessment-gated pages | HIGH | **FIX** — add greyed-out disabled links |
| 2 | No active page indicator | MEDIUM | **FIX** — use `st.page_link` with current page highlight |
| 3 | No section separator between Core and Expert pages | MEDIUM | **FIX** — add collapsible "Expert Results" section |
| 4 | `st.sidebar.divider()` usage consistent | OK | **KEEP** |
| 5 | Gate outcome badge uses consistent colors | OK | **KEEP** |
| 6 | Sidebar CSS in theme.py: link color `#C8E6C9` | OK | **KEEP** |

---

## 5. Expert Pages vs Core Pages Audit

| # | Page | Uses `####` headers | Has caption subtitle | Has divider sections | Uses Styler | Consistent? |
|---|------|---------------------|----------------------|----------------------|-------------|------------|
| 1 | 02 Core | YES | NO (gate banner) | YES | rich HTML | BASELINE |
| 2 | 03 Expert | `st.subheader()` | YES | YES | NO | **PARTIAL** — FIX subheader |
| 3 | 04 Expert | `st.subheader()` | YES | YES | NO | **PARTIAL** — FIX subheader |
| 4 | 05 Core | `####` | YES | YES | YES (style.map) | **OK** |
| 5 | 06 Core | `####` | YES | YES | YES | **OK** |
| 6 | 07 Expert | `####` | YES | YES | YES (rich HTML) | **OK** |
| 7 | 09 Expert | `####` | YES | YES | custom HTML | **PARTIAL** — FIX card bg |
| 8 | 30 Expert | `####` | YES | YES | NO | **OK** (minimal) |
| 9 | 31 Expert | `####` | YES | YES | NO | **OK** (minimal) |
| 10 | 32 Expert | `####` | YES | YES | custom HTML | **PARTIAL** — FIX card bg |
| 11 | 33 Expert | `####` | YES | YES | YES | **OK** |

---

## 6. Theme Management Audit

| # | Issue | Verdict |
|---|-------|---------|
| 1 | `theme.py` is sole CSS source | **KEEP** — verified, no page has its own `<style>` block |
| 2 | `_theme_applied` sentinel prevents duplicate injection | **KEEP** |
| 3 | Inline HTML colors scattered across 14 pages | **FIX** — move reusable color constants to `theme.py` functions |
| 4 | `apply_sidebar()` contains both navigation AND session logic | **KEEP** — proven working pattern |
| 5 | No page-specific `<style>` blocks found | **KEEP** — clean |

---

## 7. Navigation Audit

| # | Issue | Severity | Verdict |
|---|-------|----------|---------|
| 1 | `05_Risk_Assessment.py:117-118` uses `<a href>` not `st.page_link` | HIGH | **FIX** — use `st.page_link` |
| 2 | `06_CAPEX_LCOH.py:94-96` uses `<a href>` not `st.page_link` | HIGH | **FIX** — use `st.page_link` |
| 3 | `02_Assessment_Report.py:151-158` uses `<a href>` for expert drill-down | MEDIUM | **FIX** — update to `st.page_link` |
| 4 | No clear workflow path from Home → Input → Report → Risk → CAPEX | MEDIUM | **FIX** — sidebar should show locked/unlocked state |
| 5 | Expert tools buried in expander on page 02 but should also be in sidebar | MEDIUM | **FIX** — collapsible sidebar section |

---

## Summary: Classification

### KEEP (16 items)
- Gate outcome color palette (green/amber/red/grey)
- Heatmap risk colors (D32F2F/EF6C00/F9A825/A5D6A7)
- Agent pipeline gradient colors (C8E6C9 through 1B5E20)
- `st.title()` for page titles — consistent across all 14 pages
- `st.caption()` usage — consistent
- `###` / `####` markdown section headers (dominant pattern)
- `st.metric()` card structure — globally styled
- Theme.css as single source of style rules
- `_theme_applied` sentinel guard
- `apply_theme()` / `apply_sidebar()` called at module level on every page
- Sidebar dark green gradient + white text
- `st.sidebar.divider()` section breaks
- Gate outcome badge in sidebar footer
- Expert drill-down expander on page 02
- `#E0E0E0` range bar track (functional UI)
- `#FFF3E0` / `#FFFDE7` / `#FFEBEE` gate severity backgrounds

### FIX (12 items)
1. **`#F9FBE7`** → `#FFFFFF` in 09_Technology_Comparison card background
2. **`#F9FBE7`** → remove, use white cards
3. **`#37474F`** → `#1B5E20` in 09 recommendation banner text
4. **`04_Technology_Assessment.py`** — `st.subheader()` → `st.markdown("#### ...")` 
5. **`03_Reference_Projects.py`** — `st.subheader()` → `st.markdown("#### ...")`
6. **`#FAFAFA`** → `#FFFFFF` in 07, 32 card backgrounds
7. **`#999`** → `#558B2F` in 07 step number labels
8. **Breadcrumb links** in 05, 06 → use `st.page_link` not `<a href>`
9. **Expert drill-down** in 02 → use `st.page_link` not `<a href>`
10. **Sidebar** — add locked/disabled state with `.locked` CSS class
11. **Sidebar** — add collapsible "Expert Results" section
12. **09_Technology_Comparison** — card border-radius 10px → 8px

### REMOVE (0 items)
No elements need to be removed entirely.
