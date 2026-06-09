"""Page 6 -- CAPEX & LCOH. Cost driver analysis and economic assessment."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})

st.title("Cost & Economic Analysis")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")

# ─── CAPEX ───
st.markdown("#### Capital Expenditure")
t = capex.get("total", {})
central, low, high = t.get("central_eur_m",0), t.get("p10_eur_m",0), t.get("p90_eur_m",0)
ckw = t.get("central_eur_per_kw",0)

c1, c2, c3 = st.columns(3)
with c1: st.metric("Central Estimate", f"EUR {central:.0f}M", f"EUR {ckw:.0f}/kW")
with c2: st.metric("P10 (Optimistic)", f"EUR {low:.0f}M")
with c3: st.metric("P90 (Pessimistic)", f"EUR {high:.0f}M")

pct = ((central - low) / (high - low)) * 100 if high > low else 50
st.markdown(f"""
<div style="background:#F1F8E9;border-radius:8px;padding:8px 16px;border:1px solid #C8E6C9;margin:8px 0;">
<div style="display:flex;justify-content:space-between;font-size:0.85em;color:#558B2F;">
<span>P10: EUR {low:.0f}M</span><span style="font-weight:600;">Central: EUR {central:.0f}M</span><span>P90: EUR {high:.0f}M</span></div>
<div style="background:#E0E0E0;border-radius:4px;height:10px;margin-top:4px;">
<div style="background:linear-gradient(90deg,#A5D6A7,#2E7D32);width:{pct:.0f}%;height:10px;border-radius:4px;"></div></div></div>
""", unsafe_allow_html=True)

cls = capex.get('weighted_confidence_label','')
wc_c = "#2E7D32" if cls == "GOOD" else "#F9A825" if cls == "ADEQUATE" else "#C62828"
st.markdown(f"AACE Class 4 | Confidence: <span style='color:{wc_c};font-weight:600;'>{cls} ({capex.get('weighted_confidence',0):.2f})</span>", unsafe_allow_html=True)

st.divider()

# ─── COST BREAKDOWN ───
st.markdown("#### Cost Breakdown by Category")
bd = capex.get("breakdown", [])
if bd:
    rows = [{"Category": b["category"], "EUR/kW": b["eur_per_kw"], "EUR M": b["eur_m"],
             "%": b["pct_of_total"], "Conf.": b.get("confidence","C")} for b in bd]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True,
                 column_config={"EUR/kW": st.column_config.NumberColumn(format="%.0f"),
                                "EUR M": st.column_config.NumberColumn(format="%.1f"),
                                "%": st.column_config.NumberColumn(format="%.1f%%")})
    st.bar_chart(pd.DataFrame({"Category": [r["Category"] for r in rows],
                               "EUR M": [r["EUR M"] for r in rows]}).set_index("Category"))

st.divider()

# ─── COST DRIVERS ───
st.markdown("#### Cost Driver Analysis")
st.markdown(f"""
| Driver | Impact | Why It Matters |
|--------|--------|---------------|
| **Electrolyser Stack** | ~30% of CAPEX | Largest single category. PEM premium vs Alkaline. |
| **Grid Connection** | ~12% of CAPEX | Brownfield sites can reduce this by 50%. |
| **Indirect Costs** | ~24% of CAPEX | FOAK premium + contingency. Reduces with experience. |
| **Electricity Price** | ~46% of LCOH | Most important economic driver overall. |
""")

st.divider()

# ─── LCOH ───
st.markdown("#### Levelized Cost of Hydrogen")
lc = lcoh.get("central_eur_per_kg", 0)
lp10 = lcoh.get("p10_eur_per_kg", 0)
lp90 = lcoh.get("p90_eur_per_kg", 0)

cl1, cl2, cl3 = st.columns(3)
with cl1: st.metric("Central LCOH", f"EUR {lc:.2f}/kg")
with cl2: st.metric("P10 (Optimistic)", f"EUR {lp10:.2f}/kg")
with cl3: st.metric("P90 (Pessimistic)", f"EUR {lp90:.2f}/kg")

st.markdown(f"**Dominant Driver:** {lcoh.get('dominant_driver','').replace('_',' ').title()}")
st.caption(f"Assumptions: {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)} EUR/MWh, "
           f"{lcoh.get('assumptions',{}).get('full_load_hours',4500)} hrs/yr")

# LCOH waterfall
st.markdown("#### LCOH Decomposition")
decomp = lcoh.get("decomposition", [])
if decomp:
    dc = [{"Component": d["component"], "EUR/kg": d["eur_per_kg"], "%": d["pct"]} for d in decomp]
    df = pd.DataFrame(dc)
    cc1, cc2 = st.columns([1, 1])
    with cc1:
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={"EUR/kg": st.column_config.NumberColumn(format="%.2f")})
    with cc2:
        st.bar_chart(df.set_index("Component")["EUR/kg"])

# Sensitivity
st.markdown("#### Sensitivity: What Drives LCOH?")
for t_item in lcoh.get("tornado", []):
    st.markdown(f"- **{t_item['driver']}**: {t_item['impact']}")

if lcoh.get("data_quality_note"):
    st.warning(lcoh["data_quality_note"][:180])

st.caption("LCOH is CLASS D (preliminary). OPEX Library not yet populated.")
