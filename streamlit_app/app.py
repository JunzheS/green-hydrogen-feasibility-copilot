"""Green Hydrogen Project Feasibility Copilot — Decision-Support Platform."""
import streamlit as st

st.set_page_config(page_title="H2 Feasibility Copilot", page_icon=" ", layout="wide", initial_sidebar_state="expanded")

from utils.session import init_session
from utils.theme import apply_theme
init_session(); apply_theme()

with st.sidebar:
    st.markdown("## H2 Feasibility Copilot")
    st.markdown("Decision-Support Platform | v1.0")
    st.divider()
    if st.session_state.get("report"):
        r = st.session_state["report"]; pm = r.get("pm_review", {}); gate = pm.get("gate_outcome","-")
        conf = pm.get("overall_confidence",{})
        gcolor = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}.get(gate,"#78909C")
        st.markdown("**Current Assessment**")
        q = st.session_state.get("query",{}); st.caption(f"{q.get('country','')} | {q.get('capacity_mw','')} MW | {q.get('technology','')}")
        st.markdown(f"<span style='background:{gcolor};padding:4px 12px;border-radius:4px;color:white;font-weight:600;font-size:0.85em;'>{gate}</span>", unsafe_allow_html=True)
        st.caption(f"Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f})")
    st.divider()
    st.caption("KB: 10 projects | 30 risks | 30 cost records")

# ─── LANDING PAGE ───
if not st.session_state.get("assessment_complete"):
    col_logo, col_title = st.columns([1, 6])
    with col_title:
        st.title("Green Hydrogen Feasibility Copilot")
        st.markdown("<p style='color:#558B2F;font-size:1.1rem;'>Decision-Support for PEM and Alkaline Electrolysis Projects</p>", unsafe_allow_html=True)

    # Knowledge base KPI banner
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: st.metric("Reference Projects", "10")
    with k2: st.metric("Risk Records", "30")
    with k3: st.metric("Cost Benchmarks", "30")
    with k4: st.metric("Technology Cards", "2")
    with k5: st.metric("Tests Passing", "35/35")
    st.caption("Knowledge base: European hydrogen projects, IEA/IRENA benchmarks, peer-reviewed engineering methodologies.")

    st.divider()

    # How it works
    hcol1, hcol2, hcol3 = st.columns(3)
    with hcol1:
        st.markdown("##### 1. Enter Your Project")
        st.caption("Country, industry, technology, capacity, and target year. Five parameters define your project profile.")
    with hcol2:
        st.markdown("##### 2. Engine Analyses")
        st.caption("The system matches against 10 reference projects, assesses technology readiness, identifies risks, and estimates CAPEX and LCOH.")
    with hcol3:
        st.markdown("##### 3. Decision Output")
        st.caption("A structured gate assessment: should the project proceed? What are the conditions? What information is missing?")

    st.divider()

    # What you get
    st.markdown("#### Assessment Deliverables")
    d1, d2, d3, d4 = st.columns(4)
    with d1: st.markdown("**Executive Summary**"); st.caption("Gate decision with justification, dimension scores, and conditions for advancement.")
    with d2: st.markdown("**Risk Dashboard**"); st.caption("Class-ranked risk register with mitigation actions and reference project evidence.")
    with d3: st.markdown("**CAPEX & LCOH**"); st.caption("AACE Class 4 cost estimate, category breakdown, and LCOH sensitivity analysis.")
    with d4: st.markdown("**Full Traceability**"); st.caption("Agent Trace page showing the complete reasoning from input to decision.")

    st.divider()

    # Example
    st.markdown("#### Demonstration: France, Steel, PEM, 100 MW, 2029")
    st.code(
        "Gate: PROCEED WITH CAUTION (Confidence: GOOD)\n"
        "CAPEX: EUR 150M (EUR 1,500/kW)\n"
        "LCOH: EUR 4.96/kg\n"
        "Top Reference: Normand'Hy (Score 0.81)\n"
        "Top Risk: Manufacturing Capacity (RPN 36)\n"
        "Key Gap: No steel-offtake PEM project in reference dataset"
    )

    st.divider()
    st.info("Navigate to **Project Input** in the sidebar to begin a new assessment.")
