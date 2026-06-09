"""H2 Feasibility Copilot — Progressive disclosure navigation."""
import streamlit as st
st.set_page_config(page_title="H2 Feasibility Copilot", page_icon=" ", layout="wide", initial_sidebar_state="expanded")
from utils.session import init_session; from utils.theme import apply_theme, apply_sidebar
init_session(); apply_theme()

apply_sidebar()

# ─── HOME ───
st.title("Green Hydrogen Feasibility Copilot")
st.markdown("<p style='color:#558B2F;font-size:1.15rem;'>Multi-Agent Decision-Support for PEM and Alkaline Electrolysis Projects</p>", unsafe_allow_html=True)
st.divider()

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown("**Reference Matching**"); st.caption("5-dimension similarity scoring against 82 curated project records.")
with c2: st.markdown("**Technology Assessment**"); st.caption("TRL evaluation, application suitability, FOAK risk per ISO 16290.")
with c3: st.markdown("**Risk & Cost Engine**"); st.caption("FMEA risk scoring, AACE Class 4 CAPEX, power-law scaling, LCOH decomposition.")
with c4: st.markdown("**Decision Intelligence**"); st.caption("PMBOK phase-gate review, executive insights, full evidence traceability.")
st.divider()

st.markdown("#### How the Multi-Agent System Works")
st.markdown("""
<div style="display:flex;justify-content:space-between;gap:4px;text-align:center;margin:8px 0;">
<div style="flex:1;background:#E8F5E9;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>User<br>Input</strong><br><small>5 parameters</small></div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#C8E6C9;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>Agent 1</strong><br>Knowledge<br>Retrieval</div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#A5D6A7;padding:10px;border-radius:8px;color:#1B5E20;font-size:0.9rem;">
<strong>Agent 2</strong><br>Technical</div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#81C784;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Agent 3</strong><br>Risk & Economic</div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#4CAF50;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Agent 4</strong><br>PM Review</div>
<div style="flex:0.3;color:#558B2F;font-size:1.4rem;padding-top:20px;">→</div>
<div style="flex:1;background:#1B5E20;padding:10px;border-radius:8px;color:white;font-size:0.9rem;">
<strong>Decision<br>Report</strong></div>
</div>
""", unsafe_allow_html=True)
st.caption("4 deterministic agents processing 82 project references, 30 risks, 30 cost benchmarks, and 2 technology cards.")
st.divider()

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
    st.divider()

st.markdown("#### How It Works")
h1, h2, h3 = st.columns(3)
with h1: st.markdown("**1. Define**"); st.caption("Enter country, industry, technology, capacity, and target COD.")
with h2: st.markdown("**2. Analyze**"); st.caption("Four-agent engine evaluates references, technology, risks, and economics.")
with h3: st.markdown("**3. Decide**"); st.caption("Gate decision with executive insights, conditions, and traceable evidence.")
st.info("Navigate to **Project Input** in the sidebar to begin.")
