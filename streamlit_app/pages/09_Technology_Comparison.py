"""Page 9 — Technology Comparison with executive cards."""
import streamlit as st
from utils.theme import apply_theme, apply_sidebar; apply_theme(); apply_sidebar()
from src.main import FeasibilityEngine
from src.engines.technology_comparison_engine import compare_technologies

st.title("PEM vs Alkaline Comparison")
st.caption("Side-by-side assessment for your project profile. Reuses existing Technology Cards and Cost Library.")

if not st.session_state.get("report"):
    st.warning("Run an assessment first to populate your project profile.")
    q = st.session_state.get("query", {}) or {"country":"France","industry":"Steel","technology":"PEM","capacity_mw":100,"target_cod":2029}
else:
    q = st.session_state.get("query", {"country":"France","industry":"Steel","technology":"PEM","capacity_mw":100,"target_cod":2029})

with st.spinner("Running comparison..."):
    try:
        if "fe_engine" not in st.session_state:
            st.session_state["fe_engine"] = FeasibilityEngine()
        engine = st.session_state["fe_engine"]
        comp = compare_technologies({"country":q.get("country","France"),"industry":q.get("industry","Steel"),
                                       "technology":"PEM","capacity_mw":q.get("capacity_mw",100),
                                       "target_cod":q.get("target_cod",2029)}, engine)
    except Exception as e:
        st.error(f"Comparison failed: {e}")
        st.stop()

pem, alk = comp.get("PEM",{}), comp.get("Alkaline",{})
dc = comp.get("delta",{})
d_capex = dc.get("capex_per_kw",0)
d_lcoh = dc.get("lcoh",0)

# Decide which is cheaper
cheaper_tech = "Alkaline" if d_capex > 0 else "PEM"
cheaper_capex = f"EUR {d_capex:.0f}/kW less" if d_capex > 0 else f"EUR {abs(d_capex):.0f}/kW less"
cheaper_lcoh = f"EUR {abs(d_lcoh):.2f}/kg less" if d_lcoh != 0 else "comparable"

# Recommendation banner
st.markdown(f"""
<div style="background:#E8F5E9;border:2px solid #2E7D32;border-radius:10px;padding:16px;margin-bottom:16px;">
<p style="margin:0;color:#1B5E20;font-weight:600;font-size:1.1rem;">Comparison Summary</p>
<p style="margin:4px 0 0;color:#37474F;"><strong>{cheaper_tech}</strong> has {cheaper_capex} in CAPEX and {cheaper_lcoh} in LCOH for this profile. Selection depends on project-specific dynamic response, purity, and footprint requirements.</p>
</div>
""", unsafe_allow_html=True)

# Side-by-side cards
def tech_card(name, data, color):
    suit = {"high":"✓ High","medium":"⚠ Medium","low":"✗ Low"}.get(data.get("suitability",""),"-")
    st.markdown(f"""
<div style="border:1px solid #C8E6C9;border-radius:10px;padding:16px;margin:8px 0;background:#F9FBE7;">
<div style="background:{color};padding:8px 12px;border-radius:6px;color:white;margin:-16px -16px 12px -16px;">
<strong style="font-size:1.1rem;">{name}</strong></div>
<table style="width:100%;border-collapse:collapse;font-size:0.95rem;">
<tr><td style="padding:4px 0;color:#558B2F;">CAPEX</td><td style="text-align:right;font-weight:600;">EUR {data.get('capex_eur_m',0):,.0f}M ({data.get('capex_per_kw',0):,.0f}/kW)</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">LCOH</td><td style="text-align:right;font-weight:600;">EUR {data.get('lcoh',0):.2f}/kg</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">TRL</td><td style="text-align:right;">{data.get('trl','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Suitability</td><td style="text-align:right;">{suit}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Max Scale</td><td style="text-align:right;">{data.get('max_scale','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Efficiency</td><td style="text-align:right;">{data.get('efficiency','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Stack Life</td><td style="text-align:right;">{data.get('stack_life','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Output Pressure</td><td style="text-align:right;">{data.get('output_pressure','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Purity</td><td style="text-align:right;">{data.get('purity','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Ramp Rate</td><td style="text-align:right;">{data.get('ramp_rate','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Min Load</td><td style="text-align:right;">{data.get('min_load','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Top Risk</td><td style="text-align:right;font-size:0.85rem;">{data.get('top_risk','-')}</td></tr>
<tr><td style="padding:4px 0;color:#558B2F;">Gate</td><td style="text-align:right;"><span style="background:{'#2E7D32' if data.get('gate')=='PROCEED' else '#F9A825'};padding:2px 8px;border-radius:4px;color:white;font-weight:600;">{data.get('gate','-')}</span></td></tr>
</table></div>
""", unsafe_allow_html=True)

col_p, col_a = st.columns(2)
with col_p: tech_card("PEM Electrolysis", pem, "#1B5E20")
with col_a: tech_card("Alkaline Electrolysis", alk, "#2E7D32")

st.divider()

# Recommended applications
st.markdown("#### Recommended Applications")
ra1, ra2 = st.columns(2)
with ra1:
    st.markdown("**PEM is preferred for:**")
    for a in comp.get("recommended_applications",{}).get("PEM",[]): st.markdown(f"- {a}")
with ra2:
    st.markdown("**Alkaline is preferred for:**")
    for a in comp.get("recommended_applications",{}).get("Alkaline",[]): st.markdown(f"- {a}")
st.caption("Recommendations are indicative. Final selection requires project-specific engineering analysis.")
