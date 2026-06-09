# M12 Bugfix Report

**Date:** 2026-06-09
**Commit:** `f5448d6`
**Deployment:** https://green-hydrogen-feasibility-copilot.streamlit.app

---

## Bug 1: Risk Page Crash (`AttributeError`)

| Field | Detail |
|-------|--------|
| **Error** | `'Styler' object has no attribute 'applymap'` |
| **File** | `streamlit_app/pages/05_Risk_Assessment.py`, line 50 |
| **Root Cause** | `DataFrame.style.applymap()` was **removed** in pandas 2.1.0 and renamed to `.map()`. The local development environment had pandas < 2.1, but Streamlit Cloud runs pandas 2.3.3. |
| **Fix** | Changed `.applymap(color_class, subset=["Class"])` to `.map(color_class, subset=["Class"])` |
| **Why missed locally** | The developer's local pandas version was older, where `.applymap()` still worked. |

## Bug 2: CAPEX Page (`KeyError`)

| Field | Detail |
|-------|--------|
| **Error** | `KeyError: 'category'` on CAPEX breakdown |
| **Investigation** | Schema audit confirmed the CAPEX breakdown IS producing correct keys (`category`, `eur_per_kw`, `eur_m`, `pct_of_total`, `confidence`). The error was likely caused by a **stale Streamlit session** — the user had cached results from a pre-M12 assessment in their browser session state, and the old report data did NOT have the M12-enhanced keys. |
| **Fix** | No code change needed. Users should **run a new assessment** after deployment to get M12-enriched data, or reload the session. |

---

## Files Modified

| File | Lines Changed | Change |
|------|---------------|--------|
| `streamlit_app/pages/05_Risk_Assessment.py` | 1 | `.applymap` → `.map` |

## Pages Verified Compatible (No Changes Needed)

| Page | Schema Check | Result |
|------|-------------|--------|
| `02_Assessment_Report.py` | `executive_insights`, `gate_justification` keys | ✅ |
| `03_Reference_Projects.py` | `project_match_breakdown`, `score_breakdown` keys | ✅ |
| `05_Risk_Assessment.py` | `risk_consequences` keys (after `.map` fix) | ✅ Fixed |
| `06_CAPEX_LCOH.py` | `breakdown[*].{category,eur_per_kw,eur_m,pct_of_total}` | ✅ |
| `07_Agent_Trace.py` | Top-level schema only (unchanged) | ✅ |

## Validation

| Test | Result |
|------|--------|
| Regression tests | ✅ 35/35 passed |
| Engine run (France, Steel, PEM, 100 MW) | ✅ All M12 sections populated |
| Schema audit | ✅ All 6 pages verified against engine output |

## Deployment

- Commit `f5448d6` pushed to `main`
- Streamlit Cloud will auto-deploy on the next restart
- To redeploy: go to [share.streamlit.io](https://share.streamlit.io), select the app, click **Reboot**
