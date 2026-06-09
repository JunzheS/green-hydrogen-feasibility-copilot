"""Page 1 -- Project Input Form."""
import streamlit as st
from utils.session import run_engine, save_assessment
from utils.theme import apply_theme, apply_sidebar; apply_theme(); apply_sidebar()

st.title("Project Input")
st.caption("Enter your green hydrogen project parameters below.")

col1, col2 = st.columns(2)

with col1:
    country = st.selectbox(
        "Country",
        ["France", "Germany", "Spain", "Netherlands", "Belgium", "Portugal", "Denmark"],
        index=0,
    )
    industry = st.selectbox(
        "Industry / Offtake",
        ["Steel", "Refinery", "Ammonia", "Methanol", "Mobility",
         "Industrial Hydrogen", "Chemicals", "Industrial Heat"],
        index=0,
    )
    technology = st.radio(
        "Electrolysis Technology",
        ["PEM", "Alkaline"],
        index=0,
        horizontal=True,
    )

with col2:
    capacity_mw = st.slider(
        "Capacity (MW)", min_value=5, max_value=1000, value=100, step=5,
    )
    target_cod = st.slider(
        "Target Commissioning Year", min_value=2026, max_value=2035, value=2029, step=1,
    )
    notes = st.text_area("Optional Notes", placeholder="e.g. Brownfield site at Dunkirk steel plant...", height=80)

st.divider()

with st.expander("Advanced Settings"):
    electricity_price = st.slider("Electricity Price (EUR/MWh)", 20, 120, 40, 5)
    full_load_hours = st.slider("Full-Load Hours / Year", 2000, 8000, 4500, 500)

st.divider()

col_run, _ = st.columns([3, 1])
with col_run:
    if st.button("Run Assessment", type="primary", use_container_width=True):
        with st.spinner("Running feasibility assessment..."):
            query = {
                "country": country,
                "industry": industry,
                "technology": technology,
                "capacity_mw": capacity_mw,
                "target_cod": target_cod,
            }
            report = run_engine(query, electricity_price, full_load_hours)
            assessment_id = save_assessment(query, report)
            st.session_state["assessment_complete"] = True
            st.session_state["report"] = report
            st.session_state["query"] = query
            st.session_state["current_assessment_id"] = assessment_id
        st.success(f"Assessment complete -- {assessment_id}")
        st.rerun()
