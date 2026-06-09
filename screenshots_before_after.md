# UI Fix — Before/After Screenshot Guide

**Date:** 2026-06-09
**Affected pages:** Landing page (`app.py`), CAPEX page (`06_CAPEX_LCOH.py`)

---

## How to Capture

1. Run the application
2. Open the app in a browser
3. For the **landing page**: open the app without running any assessment
4. For the **CAPEX page**: run France / Steel / PEM / 100 MW / 2029, then navigate to CAPEX & LCOH

## Before/After Reference

### Landing Page (app.py)

| Section | Before M12 | After M12 regression | After fix (current) |
|---------|-----------|---------------------|-------------------|
| KPI row | 3 columns (Projects, Risks, Costs) | 3 columns (same, no tech cards) | **5 columns** (Projects, Risks, Costs, Tech Cards, Tests) |
| Welcome banner | Present | Present | **Enhanced** |
| "Why This Tool" | Basic text | Basic text | **Full description with workflow** |
| Workflow | None | None | **4-step workflow diagram** |
| Example output | None | None | **Code block with sample output** |

### CAPEX Page (06_CAPEX_LCOH.py)

| Section | Before M12 | After M12 regression | After fix (current) |
|---------|-----------|---------------------|-------------------|
| CAPEX summary | ✅ Renders | ❌ KeyError | ✅ Fixed |
| Breakdown table | ✅ Renders | ❌ Blocked | ✅ Renders |
| Bar chart | ✅ Renders | ❌ Blocked | ✅ Renders (with category labels) |
| LCOH waterfall | ✅ Renders | ❌ Blocked | ✅ Renders |

---

## Visual Verification Checklist

- [ ] Landing page shows 5 KPI metrics
- [ ] CAPEX breakdown table has correct column headers
- [ ] CAPEX bar chart displays category labels on x-axis
- [ ] No error messages in any page
- [ ] All M12 sections (Executive Insights, Risk Consequences) render correctly
