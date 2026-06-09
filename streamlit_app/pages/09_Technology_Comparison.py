"""Page 9 -- PEM vs Alkaline Technology Comparison."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

st.title("Technology Comparison")
st.caption("Side-by-side assessment of PEM and Alkaline electrolysis for your project profile.")

if not st.session_state.get("report"):
    st.warning("Run a full assessment first, then come here for the comparison.")
    st.info("This feature compares PEM and Alkaline for your project's country, industry, capacity, and COD.")
    if st.button("Run Comparison Now", type="primary"):
        st.session_state["run_comparison"] = True
        st.rerun()

from src.main import FeasibilityEngine
from src.engines.technology_comparison_engine import compare_technologies

query = st.session_state.get("query", {})
if not query:
    st.info("Enter a project profile on the **Project Input** page first.")
    st.stop()

with st.spinner("Running comparison..."):
    try:
        engine = FeasibilityEngine()
        comp = compare_technologies({
            "country": query.get("country","France"),
            "industry": query.get("industry","Steel"),
            "technology": "PEM",
            "capacity_mw": query.get("capacity_mw",100),
            "target_cod": query.get("target_cod",2029),
        }, engine)
    except Exception as e:
        st.error(f"Comparison failed: {e}")
        st.stop()

pem = comp.get("PEM", {})
alk = comp.get("Alkaline", {})

# Side-by-side table
st.subheader("PEM vs Alkaline")
rows = [
    ("Technology Readiness", pem.get("trl","-"), alk.get("trl","-")),
    ("Application Suitability", pem.get("suitability","-").upper(), alk.get("suitability","-").upper()),
    ("CAPEX (EUR/kW)", f"EUR {pem.get('capex_per_kw',0):,.0f}", f"EUR {alk.get('capex_per_kw',0):,.0f}"),
    ("CAPEX (EUR M)", f"EUR {pem.get('capex_eur_m',0):,.0f}M", f"EUR {alk.get('capex_eur_m',0):,.0f}M"),
    ("CAPEX Range", pem.get("capex_range","-"), alk.get("capex_range","-")),
    ("LCOH (EUR/kg)", f"EUR {pem.get('lcoh',0):.2f}", f"EUR {alk.get('lcoh',0):.2f}"),
    ("LCOH Range", pem.get("lcoh_range","-"), alk.get("lcoh_range","-")),
    ("Dominant Cost Driver", pem.get("dominant_driver","-"), alk.get("dominant_driver","-")),
    ("Max Proven Scale", pem.get("max_scale","-"), alk.get("max_scale","-")),
    ("Efficiency", pem.get("efficiency","-"), alk.get("efficiency","-")),
    ("Stack Lifetime", pem.get("stack_life","-"), alk.get("stack_life","-")),
    ("Output Pressure", pem.get("output_pressure","-"), alk.get("output_pressure","-")),
    ("Hydrogen Purity", pem.get("purity","-"), alk.get("purity","-")),
    ("Ramp Rate", pem.get("ramp_rate","-"), alk.get("ramp_rate","-")),
    ("Min Load", pem.get("min_load","-"), alk.get("min_load","-")),
    ("Top Risk", pem.get("top_risk","-"), alk.get("top_risk","-")),
    ("Gate Decision", pem.get("gate","-"), alk.get("gate","-")),
]
df = pd.DataFrame(rows, columns=["Parameter", "PEM", "Alkaline"])
st.dataframe(df, use_container_width=True, hide_index=True)

# CAPEX and LCOH deltas
delta_capex = comp.get("delta", {}).get("capex_per_kw", 0)
delta_lcoh = comp.get("delta", {}).get("lcoh", 0)
st.divider()

st.subheader("Economic Comparison")
ec1, ec2 = st.columns(2)
with ec1:
    premium = "PEM" if delta_capex > 0 else "Alkaline"
    st.metric("CAPEX Difference", f"EUR {abs(delta_capex):,.0f}/kW", f"{premium} premium")
with ec2:
    premium_l = "PEM" if delta_lcoh > 0 else "Alkaline"
    st.metric("LCOH Difference", f"EUR {abs(delta_lcoh):.2f}/kg", f"{premium_l} premium")

st.divider()

# Best applications
st.subheader("Recommended Applications")
ra_col1, ra_col2 = st.columns(2)
with ra_col1:
    st.markdown("**PEM is typically preferred for:**")
    for app in comp.get("recommended_applications", {}).get("PEM", []):
        st.markdown(f"- {app}")
with ra_col2:
    st.markdown("**Alkaline is typically preferred for:**")
    for app in comp.get("recommended_applications", {}).get("Alkaline", []):
        st.markdown(f"- {app}")

st.caption("Recommendations are indicative. Final selection requires project-specific engineering and commercial analysis.")
