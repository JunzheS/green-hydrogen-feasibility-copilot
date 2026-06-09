"""H2 Feasibility Copilot — Multi-Agent Decision Platform homepage."""
import streamlit as st
st.set_page_config(page_title="H2 Feasibility Copilot", page_icon=" ", layout="wide", initial_sidebar_state="expanded")
from utils.session import init_session; from utils.theme import apply_theme
init_session(); apply_theme()

with st.sidebar:
    st.markdown("### H2 Feasibility Copilot")
    st.markdown("Multi-Agent Decision Platform")
    st.divider()
    st.markdown("<a href='/' target='_self'>- Home</a>", unsafe_allow_html=True)
    st.markdown("**Core Assessment**")
    st.markdown("<a href='/Project_Input' target='_self'>- Project Input</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Assessment_Report' target='_self'>- Assessment Report</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Risk_Assessment' target='_self'>- Risk Dashboard</a>", unsafe_allow_html=True)
    st.markdown("<a href='/CAPEX_LCOH' target='_self'>- CAPEX & LCOH</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Assessment_History' target='_self'>- History</a>", unsafe_allow_html=True)
    st.markdown("**Advanced Analysis**")
    st.markdown("<a href='/Reference_Projects' target='_self'>- Reference Projects</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Technology_Assessment' target='_self'>- Technology Assessment</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Technology_Comparison' target='_self'>- Technology Comparison</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Agent_Trace' target='_self'>- Agent Trace</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Contradiction_Detection' target='_self'>- Agent Collaboration</a>", unsafe_allow_html=True)
    st.markdown("**Market Intelligence**")
    st.markdown("<a href='/OEM_Intelligence' target='_self'>- OEM Intelligence</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Developer_Intelligence' target='_self'>- Developer Intelligence</a>", unsafe_allow_html=True)
    st.markdown("**About**")
    st.markdown("<a href='/Source_Transparency' target='_self'>- Source Quality</a>", unsafe_allow_html=True)
    st.markdown("<a href='/Why_This_Matters' target='_self'>- Why This Matters</a>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.get("report"):
        r, pm = st.session_state["report"], st.session_state["report"].get("pm_review", {})
        gate = pm.get("gate_outcome","-")
        gc = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
        st.markdown("**Assessment**")
        q = st.session_state.get("query",{}); st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")
        st.markdown(f"<span style='background:{gc.get(gate,'#78909C')};padding:4px 12px;border-radius:4px;color:white;font-weight:600;'>{gate}</span>", unsafe_allow_html=True)
    st.caption("v1.0 | 141 validated knowledge assets")

# ─── HOME ───
st.title("Green Hydrogen Feasibility Copilot")
st.markdown("<p style='color:#558B2F;font-size:1.15rem;'>Multi-Agent Decision-Support for PEM and Alkaline Electrolysis Projects</p>", unsafe_allow_html=True)
st.divider()

# Platform capabilities
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown("**Reference Matching**"); st.caption("5-dimension similarity scoring, 10 European projects, cross-industry benchmarking.")
with c2: st.markdown("**Technology Assessment**"); st.caption("TRL evaluation, application suitability, FOAK risk — per ISO 16290.")
with c3: st.markdown("**Risk & Cost Engine**"); st.caption("FMEA risk scoring, AACE Class 4 CAPEX, power-law scaling, LCOH decomposition.")
with c4: st.markdown("**Decision Intelligence**"); st.caption("PMBOK phase-gate review, executive insights, full evidence traceability.")

st.divider()

# Agent Architecture — Key Recruiter Section
st.markdown("#### How the Multi-Agent System Works")
st.markdown("""
<div style="display:flex;justify-content:space-between;gap:4px;text-align:center;margin:8px 0;">
<div style="flex:1;background:#E8F5E9;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>User<br>Input</strong><br><small>5 parameters</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#C8E6C9;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>Agent 1</strong><br>Knowledge<br>Retrieval<br><small>Project matching</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#A5D6A7;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>Agent 2</strong><br>Technical<br>Assessment<br><small>TRL, suitability</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#81C784;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Agent 3</strong><br>Risk & Economic<br>Assessment<br><small>Risk + CAPEX + LCOH</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#4CAF50;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Agent 4</strong><br>PM Review<br><small>Gate decision</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#1B5E20;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Decision</strong><br>Report</div>
</div>
""", unsafe_allow_html=True)
st.caption("Pipeline: 4 deterministic agents process a shared knowledge base of 141 validated assets — no ML, no black boxes.")

st.divider()

# Recent assessment
if st.session_state.get("assessment_complete") and st.session_state.get("report"):
    r = st.session_state["report"]; q = st.session_state.get("query",{})
    pm = r.get("pm_review",{}); cx = r.get("capex_assessment",{}); lc = r.get("lcoh_assessment",{})
    gate = pm.get("gate_outcome","-")
    st.markdown("#### Recent Assessment")
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1: st.metric("Project", f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")
    with rc2: st.metric("Gate", gate)
    with rc3: st.metric("CAPEX", f"EUR {cx.get('total',{}).get('central_eur_m',0):.0f}M")
    with rc4: st.metric("LCOH", f"EUR {lc.get('central_eur_per_kg',0):.2f}/kg")
    st.caption("See Dashboard, Risks, and CAPEX & LCOH for the full assessment.")
    st.divider()

# How it works
st.markdown("#### How It Works")
h1, h2, h3 = st.columns(3)
with h1: st.markdown("**1. Define**"); st.caption("Enter country, industry, technology, capacity, and target COD.")
with h2: st.markdown("**2. Analyze**"); st.caption("Four-agent engine evaluates reference projects, technology, risks, and economics.")
with h3: st.markdown("**3. Decide**"); st.caption("Gate decision with executive insights, conditions, and traceable evidence.")

st.info("Navigate to **Project Input** from the sidebar to begin a new assessment.")
