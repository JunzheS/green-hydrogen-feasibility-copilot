"""Green Hydrogen Project Feasibility Copilot — Product Home."""
import streamlit as st

st.set_page_config(page_title="H2 Feasibility Copilot", page_icon=" ", layout="wide", initial_sidebar_state="expanded")

from utils.session import init_session
from utils.theme import apply_theme
init_session(); apply_theme()

# ─── Sidebar ───
with st.sidebar:
    st.markdown("### H2 Feasibility Copilot")
    st.markdown("Decision-Support Platform")
    st.divider()
    nav_items = [
        ("/", "Home"),
        ("Project_Input", "Project Input"),
        ("Assessment_Report", "Assessment Report"),
        ("Reference_Projects", "Reference Projects"),
        ("Technology_Assessment", "Technology Assessment"),
        ("Risk_Assessment", "Risk Dashboard"),
        ("CAPEX_LCOH", "CAPEX & LCOH"),
        ("Technology_Comparison", "Tech Comparison"),
        ("Agent_Trace", "Agent Trace"),
        ("Assessment_History", "History"),
    ]
    st.markdown("**Pages**")
    for href, label in nav_items:
        st.markdown(f"<a href='/{href}' target='_self'>- {label}</a>", unsafe_allow_html=True)

    st.divider()
    if st.session_state.get("report"):
        r = st.session_state["report"]
        pm = r.get("pm_review", {})
        gate = pm.get("gate_outcome", "-")
        gcolor = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}.get(gate,"#78909C")
        st.markdown("**Current Assessment**")
        q = st.session_state.get("query", {})
        st.caption(f"{q.get('country','')} | {q.get('capacity_mw','')} MW")
        st.markdown(f"<span style='background:{gcolor};padding:4px 12px;border-radius:4px;color:white;font-weight:600;'>{gate}</span>", unsafe_allow_html=True)
    st.caption("v1.0 | KB: 10 projects, 30 risks, 30 costs")

# ─── Main content (always persistent) ───
st.title("Green Hydrogen Feasibility Copilot")
st.markdown("<p style='color:#558B2F;font-size:1.15rem;'>Decision-Support for PEM and Alkaline Electrolysis Projects</p>", unsafe_allow_html=True)

st.divider()

# Capabilities
st.markdown("#### Platform Capabilities")
ca, cb, cc, cd = st.columns(4)
with ca: st.markdown("**Reference Matching**"); st.caption("5-dimension similarity scoring against a curated European project dataset.")
with cb: st.markdown("**Technology Assessment**"); st.caption("TRL evaluation, application suitability, and FOAK risk analysis per ISO 16290.")
with cc: st.markdown("**Risk & Cost Engine**"); st.caption("FMEA-based risk scoring and AACE Class 4 CAPEX estimation with power-law scaling.")
with cd: st.markdown("**Decision Intelligence**"); st.caption("PMBOK phase-gate review with full evidence traceability.")

st.divider()

# Featured reference projects
st.markdown("#### Featured Reference Projects")
fp1, fp2, fp3, fp4 = st.columns(4)
with fp1:
    st.markdown("**Normand'Hy**"); st.caption("200 MW PEM | France | Under construction")
    st.caption("Air Liquide. World's largest PEM plant (2026 COD).")
with fp2:
    st.markdown("**Holland Hydrogen I**"); st.caption("200 MW Alkaline | Netherlands")
    st.caption("Shell. Thyssenkrupp Nucera stacks. EUR 1B investment.")
with fp3:
    st.markdown("**Puertollano**"); st.caption("20 MW PEM | Spain | Operational")
    st.caption("Iberdrola. Europe's first industrial green H2 plant (2022).")
with fp4:
    st.markdown("**Hamburg HGHH**"); st.caption("100 MW PEM | Germany | Under construction")
    st.caption("Brownfield coal repurposing. IPCEI-funded.")
st.caption("Dataset: 10 European green hydrogen projects with structured schemas, peer-reviewed sources.")

st.divider()

# Recent assessment summary
if st.session_state.get("assessment_complete") and st.session_state.get("report"):
    r = st.session_state["report"]
    q = st.session_state.get("query", {})
    pm = r.get("pm_review", {})
    capex = r.get("capex_assessment", {})
    lcoh = r.get("lcoh_assessment", {})
    gate = pm.get("gate_outcome", "-")
    st.markdown("#### Recent Assessment")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1: st.metric("Project", f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")
    with rc2: st.metric("Gate", gate)
    with rc3: st.metric("CAPEX", f"EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M")
    with rc4: st.metric("LCOH", f"EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg")
    st.caption("See Assessment Report, Risk Dashboard, or CAPEX & LCOH for full analysis.")
    st.divider()

# How it works
st.markdown("#### How It Works")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**1. Input**"); st.caption("Five parameters define your project: country, industry, technology, capacity, COD.")
with col2:
    st.markdown("**2. Analysis**"); st.caption("Multi-agent engine evaluates 4 dimensions: references, technology, risk, economics.")
with col3:
    st.markdown("**3. Decision**"); st.caption("PMBOK gate review with executive insights, conditions, and traceable evidence.")

st.divider()
st.markdown("""
<div style="background:#F1F8E9;padding:16px;border-radius:8px;border-left:4px solid #2E7D32;">
<strong>Getting started:</strong> Navigate to <strong>Project Input</strong> in the sidebar and enter your project parameters.
</div>
""", unsafe_allow_html=True)
