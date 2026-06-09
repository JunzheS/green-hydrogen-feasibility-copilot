"""Page 7 -- Agent Traceability Page (Flagship Feature)."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})

st.title("Agent Decision Trace")
st.caption("Complete reasoning chain -- every decision, its evidence, and its confidence.")

# Flow diagram
st.markdown("""
<div style="display:flex;justify-content:space-between;text-align:center;margin:20px 0;">
  <div style="flex:1;background:#C8E6C9;padding:8px;border-radius:6px;margin:2px;color:#1B5E20;font-size:0.9em;"><strong>User<br>Input</strong></div>
  <div style="flex:1;background:#A5D6A7;padding:8px;border-radius:6px;margin:2px;color:#1B5E20;font-size:0.9em;"><strong>Agent 1<br>Retrieval</strong></div>
  <div style="flex:1;background:#81C784;padding:8px;border-radius:6px;margin:2px;color:#1B5E20;font-size:0.9em;"><strong>Agent 2<br>Technical</strong></div>
  <div style="flex:1;background:#66BB6A;padding:8px;border-radius:6px;margin:2px;color:white;font-size:0.9em;"><strong>Agent 3<br>Risk & Econ</strong></div>
  <div style="flex:1;background:#43A047;padding:8px;border-radius:6px;margin:2px;color:white;font-size:0.9em;"><strong>Agent 4<br>PM Review</strong></div>
  <div style="flex:1;background:#2E7D32;padding:8px;border-radius:6px;margin:2px;color:white;font-size:0.9em;"><strong>Decision<br>Gate</strong></div>
</div>
""", unsafe_allow_html=True)

# Step 0
with st.container(border=True):
    st.subheader("Step 0: User Input")
    st.json(query)

# Step 1
with st.container(border=True):
    st.subheader("Step 1: Agent 1 - Knowledge Retrieval")
    matching = report.get("similar_projects", {})
    ranked = matching.get("ranked_projects", [])
    c1, c2 = st.columns([1, 1])
    with c1:
        if ranked:
            st.markdown(f"**Decision:** Top match -- **{ranked[0]['project_name']}** (score: {ranked[0]['composite_score']:.2f})")
        st.markdown(f"**Method:** 5-dimension weighted similarity scoring")
        st.markdown(f"**Projects scored:** {matching.get('total_scored',0)}")
    with c2:
        st.markdown("**Evidence Sources:**")
        st.caption("- Gold Dataset: 10 project records")
        st.caption(f"- Technology Cards: TC-{query.get('technology','PEM')}-001")
        st.caption("- Matching methodology: project_matching_methodology.md")
    if ranked:
        st.markdown("**Top 3 Matches:**")
        for p in ranked[:3]:
            st.markdown(f"-  #{p['rank']} **{p['project_name']}** ({p['composite_score']:.2f}) - {p.get('rationale','')[:120]}")

# Step 2
with st.container(border=True):
    st.subheader("Step 2: Agent 2 - Technical Assessment")
    tech = report.get("technology_assessment", {})
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"**Decision:** TRL {tech.get('trl','')}/9 - **{tech.get('application_suitability','').upper()}** suitability")
        st.markdown(f"**Scale:** {tech.get('scale_status','').replace('_',' ')} (max: {tech.get('max_proven_mw','')} MW)")
        st.markdown(f"**FOAK App:** {'Yes' if tech.get('is_foak_for_application') else 'No'} | **FOAK Scale:** {'Yes' if tech.get('is_foak_for_scale') else 'No'}")
    with c2:
        st.markdown("**Evidence Sources:**")
        st.caption(f"- TC-{query.get('technology','PEM')}-001: maturity, deployment_evidence, applications")
        st.caption(f"- Gold Dataset: max project capacity, application references")

# Step 3
with st.container(border=True):
    st.subheader("Step 3: Agent 3 - Risk & Economic Assessment")
    rd = report.get("risk_assessment", {})
    cd = report.get("capex_assessment", {})
    ld = report.get("lcoh_assessment", {})
    c1, c2 = st.columns([1, 1])
    with c1:
        tr = rd.get('top_risks', [{}])[0] if rd.get('top_risks') else {}
        st.markdown(f"**Risk:** {rd.get('total_filtered',0)} filtered, top RPN={tr.get('rpn','-')}")
        st.markdown(f"**CAPEX:** EUR {cd.get('total',{}).get('central_eur_m',0):.0f}M (range {cd.get('total',{}).get('p10_eur_m',0):.0f}-{cd.get('total',{}).get('p90_eur_m',0):.0f}M)")
        st.markdown(f"**LCOH:** EUR {ld.get('central_eur_per_kg',0):.2f}/kg (P10-P90: {ld.get('p10_eur_per_kg',0):.2f}-{ld.get('p90_eur_per_kg',0):.2f})")
    with c2:
        st.markdown("**Evidence Sources:**")
        st.caption("- Risk Library: 30 risks, filtered by tech + scale + phase")
        st.caption(f"- Cost Library: {len(cd.get('breakdown',[]))} categories, benchmark: {cd.get('benchmark_record','')}")
        st.caption("- LCOH: lcoh_methodology_framework.md, Tech Card OPEX proxies")

# Step 4
with st.container(border=True):
    st.subheader("Step 4: Agent 4 - PM Review")
    pm = report.get("pm_review", {})
    c1, c2 = st.columns([1, 1])
    with c1:
        gate = pm.get("gate_outcome", "-")
        gc = {"PROCEED": "#2E7D32", "PROCEED WITH CAUTION": "#F9A825", "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#78909C"}.get(gate, "#78909C")
        st.markdown(f"**Gate Decision:** <span style='color:{gc};font-weight:700;'>{gate}</span>", unsafe_allow_html=True)
        dims = pm.get("dimension_scores", {})
        st.markdown(f"**Dimensions:** P:{dims.get('project_references',{}).get('quality','-')} "
            f"T:{dims.get('technology',{}).get('quality','-')} "
            f"R:{dims.get('risk',{}).get('quality','-')} "
            f"E:{dims.get('economics',{}).get('quality','-')}")
        st.markdown(f"**Confidence:** {pm.get('overall_confidence',{}).get('label','')} ({pm.get('overall_confidence',{}).get('score',0):.2f})")
    with c2:
        st.markdown("**Review Methodology:**")
        st.caption("- Evidence audit across Agents 1-3")
        st.caption("- Cross-dimension consistency check")
        st.caption("- Confidence calibration")
        st.caption("- PMBOK phase-gate decision")

# Final Decision
with st.container(border=True):
    st.subheader("Final Decision")
    gate = pm.get("gate_outcome", "-")
    bg = {"PROCEED": "#E8F5E9", "PROCEED WITH CAUTION": "#FFFDE7", "DO NOT PROCEED": "#FFEBEE", "INSUFFICIENT DATA": "#ECEFF1"}
    fg = {"PROCEED": "#1B5E20", "PROCEED WITH CAUTION": "#F57F17", "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#546E7A"}
    st.markdown(f"""
    <div style="background:{bg.get(gate,'#ECEFF1')};padding:16px;border-radius:8px;color:{fg.get(gate,'#000')};text-align:center;">
    <h2 style="margin:0;color:inherit;">{gate}</h2>
    <p>Confidence: {pm.get('overall_confidence',{}).get('label','')} ({pm.get('overall_confidence',{}).get('score',0):.2f})</p>
    <p>Gaps: {len(pm.get('critical_gaps',[]))} critical | {len(pm.get('important_gaps',[]))} important</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("This trace demonstrates complete evidence-to-decision auditability.")
