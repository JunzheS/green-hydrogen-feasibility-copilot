"""Page 6 -- CAPEX & LCOH Assessment with technology comparison."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})

st.title("CAPEX & LCOH Assessment")

# CAPEX Section
st.header("CAPEX Estimate")
t = capex.get("total", {})
central = t.get("central_eur_m", 0)
low = t.get("p10_eur_m", 0)
high = t.get("p90_eur_m", 0)
central_kw = t.get("central_eur_per_kw", 0)

col1, col2, col3 = st.columns(3)
with col1: st.metric("Central Estimate", f"EUR {central:.0f}M", f"EUR {central_kw:.0f}/kW")
with col2: st.metric("P10 (Optimistic)", f"EUR {low:.0f}M")
with col3: st.metric("P90 (Pessimistic)", f"EUR {high:.0f}M")

pct = ((central - low) / (high - low)) * 100 if high > low else 50
st.markdown(f"""
<div style="background:#F1F8E9;border-radius:8px;padding:8px 16px;border:1px solid #C8E6C9;margin:10px 0;">
<div style="display:flex;justify-content:space-between;font-size:0.85em;color:#558B2F;">
<span>P10: EUR {low:.0f}M</span><span style="font-weight:600;">Central: EUR {central:.0f}M</span><span>P90: EUR {high:.0f}M</span>
</div>
<div style="background:#E0E0E0;border-radius:4px;height:10px;margin-top:4px;">
<div style="background:linear-gradient(90deg,#A5D6A7,#2E7D32);width:{pct:.0f}%;height:10px;border-radius:4px;"></div>
</div>
</div>
""", unsafe_allow_html=True)

wc = capex.get('weighted_confidence_label','')
wc_c = "#2E7D32" if wc == "GOOD" else "#F9A825" if wc == "ADEQUATE" else "#C62828"
st.markdown(f"AACE: {capex.get('aace_class','')} | "
    f"Confidence: <span style='color:{wc_c};font-weight:600;'>{wc} ({capex.get('weighted_confidence',0):.2f})</span>",
    unsafe_allow_html=True)
st.divider()

# Cost breakdown
st.subheader("Cost Breakdown by Category")
bd = capex.get("breakdown", [])
if bd:
    rows = [{"Category": b["category"], "EUR/kW": b["eur_per_kw"], "EUR M": b["eur_m"],
             "%": b["pct_of_total"], "Conf.": b.get("confidence","C")} for b in bd]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True,
                 column_config={"EUR/kW": st.column_config.NumberColumn(format="%.0f"),
                                "EUR M": st.column_config.NumberColumn(format="%.1f"),
                                "%": st.column_config.NumberColumn(format="%.1f%%")})
    st.bar_chart(pd.DataFrame({"Category": [r["Category"] for r in rows], "EUR M": [r["EUR M"] for r in rows]}).set_index("Category"))

st.divider()

# LCOH Section
st.header("Levelized Cost of Hydrogen (LCOH)")
lc = lcoh.get("central_eur_per_kg", 0)
lp10 = lcoh.get("p10_eur_per_kg", 0)
lp90 = lcoh.get("p90_eur_per_kg", 0)

col_l1, col_l2, col_l3 = st.columns(3)
with col_l1: st.metric("Central LCOH", f"EUR {lc:.2f}/kg")
with col_l2: st.metric("P10 (Optimistic)", f"EUR {lp10:.2f}/kg")
with col_l3: st.metric("P90 (Pessimistic)", f"EUR {lp90:.2f}/kg")

st.markdown(f"**Dominant Driver:** {lcoh.get('dominant_driver','').replace('_',' ').title()}")
st.caption(f"Assumptions: {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)} EUR/MWh, "
    f"{lcoh.get('assumptions',{}).get('full_load_hours',4500)} hrs/yr, "
    f"{lcoh.get('assumptions',{}).get('wacc_pct',7):.0f}% WACC")
if lcoh.get("data_quality_note"):
    st.warning(lcoh["data_quality_note"][:200])

st.divider()

# LCOH Waterfall
st.subheader("LCOH Decomposition")
decomp = lcoh.get("decomposition", [])
if decomp:
    dc = [{"Component": d["component"], "EUR/kg": d["eur_per_kg"], "%": d["pct"]} for d in decomp]
    df = pd.DataFrame(dc)
    cd1, cd2 = st.columns([1, 1])
    with cd1: st.dataframe(df, use_container_width=True, hide_index=True,
                           column_config={"EUR/kg": st.column_config.NumberColumn(format="%.2f")})
    with cd2: st.bar_chart(df.set_index("Component")["EUR/kg"])

# Sensitivity
st.subheader("Sensitivity Tornado")
for t_item in lcoh.get("tornado", []):
    st.markdown(f"-  **{t_item['driver']}**: {t_item['impact']}")

st.divider()
st.caption("LCOH is CLASS D (preliminary). OPEX Library not yet populated.")
