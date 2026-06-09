"""Page 7 — Agent Trace: timeline workflow for decision auditability."""
import streamlit as st

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
pm = report.get("pm_review", {})
gate = pm.get("gate_outcome", "-")
conf = pm.get("overall_confidence", {})

st.title("Decision Trace")
st.caption("Complete reasoning chain — every decision, its evidence, and its confidence.")

# ─── TIMELINE OVERVIEW ───
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;margin:16px 0;">
<div style="flex:1;background:#C8E6C9;padding:10px;border-radius:8px;margin:2px;text-align:center;color:#1B5E20;font-size:0.85rem;">
<strong>User Input</strong><br>5 parameters</div>
<div style="color:#558B2F;font-size:1.2rem;">→</div>
<div style="flex:1;background:#A5D6A7;padding:10px;border-radius:8px;margin:2px;text-align:center;color:#1B5E20;font-size:0.85rem;">
<strong>Agent 1</strong><br>Retrieval</div>
<div style="color:#558B2F;font-size:1.2rem;">→</div>
<div style="flex:1;background:#81C784;padding:10px;border-radius:8px;margin:2px;text-align:center;color:#1B5E20;font-size:0.85rem;">
<strong>Agent 2</strong><br>Technical</div>
<div style="color:#558B2F;font-size:1.2rem;">→</div>
<div style="flex:1;background:#66BB6A;padding:10px;border-radius:8px;margin:2px;text-align:center;color:white;font-size:0.85rem;">
<strong>Agent 3</strong><br>Risk & Economic</div>
<div style="color:#558B2F;font-size:1.2rem;">→</div>
<div style="flex:1;background:#43A047;padding:10px;border-radius:8px;margin:2px;text-align:center;color:white;font-size:0.85rem;">
<strong>Agent 4</strong><br>PM Review</div>
<div style="color:#558B2F;font-size:1.2rem;">→</div>
<div style="flex:1;background:#2E7D32;padding:10px;border-radius:8px;margin:2px;text-align:center;color:white;font-size:0.85rem;">
<strong>Decision</strong><br>{gate}</div>
</div>
""", unsafe_allow_html=True)

# ─── FINAL DECISION CARD ───
gate_colors = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
gcolor = gate_colors.get(gate,"#78909C")
st.markdown(f"""
<div style="background:{gcolor};border-radius:10px;padding:20px;color:white;margin-bottom:16px;">
<h2 style="margin:0;color:inherit;">{gate}</h2>
<p style="margin:6px 0 0;opacity:0.9;">Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f})</p>
</div>
""", unsafe_allow_html=True)

# ─── AGENT TIMELINE STEPS ───

def step_card(step_num: str, title: str, color: str, decision: str, evidence: str, why: str):
    st.markdown(f"""
<div style="border-left:4px solid {color};padding:8px 16px;margin:8px 0;background:#FAFAFA;border-radius:0 8px 8px 0;">
<small style="color:#999;">Step {step_num}</small>
<h4 style="margin:2px 0;color:{color};">{title}</h4>
<p style="margin:4px 0;"><strong>Decision:</strong> {decision}</p>
<p style="margin:2px 0;"><strong>Why:</strong> {why}</p>
<p style="margin:2px 0;"><strong>Evidence:</strong> {evidence}</p>
</div>
""", unsafe_allow_html=True)

tech = report.get("technology_assessment", {})
rd = report.get("risk_assessment", {})
cd = report.get("capex_assessment", {})
ld = report.get("lcoh_assessment", {})
matching = report.get("similar_projects", {})
ranked = matching.get("ranked_projects", [])

# Step 0
step_card("0", "User Input", "#78909C",
    f"{query.get('country','')}, {query.get('industry','')}, {query.get('technology','')}, {query.get('capacity_mw','')} MW, COD {query.get('target_cod','')}",
    "Project parameters entered by user",
    "Defines the scope of the pre-feasibility assessment")

# Step 1
top_name = ranked[0]["project_name"] if ranked else "N/A"
top_score = ranked[0]["composite_score"] if ranked else 0
step_card("1", "Agent 1 — Knowledge Retrieval", "#A5D6A7",
    f"Top match: {top_name} (score: {top_score:.2f}). {matching.get('total_scored',0)} projects scored.",
    "Gold Dataset: 10 project records. TC-PEM-001 / TC-ALK-001. 5-dimension similarity scoring.",
    "Identifies reference projects most comparable to the query for benchmarking cost, risk, and technology.")

# Step 2
step_card("2", "Agent 2 — Technical Assessment", "#81C784",
    f"TRL {tech.get('trl','')}/9. Suitability: {tech.get('application_suitability','').upper()}. Scale: {tech.get('scale_status','').replace('_',' ')}.",
    "Technology Cards: TRL, maturity, deployment_evidence, applications, performance.",
    "Evaluates whether the technology is mature enough and suitable for the application and scale.")

# Step 3
top_rpn = rd.get('top_risks',[{}])[0].get('rpn','-') if rd.get('top_risks') else '-'
step_card("3", "Agent 3 — Risk & Economic Assessment", "#66BB6A",
    f"Risks: {rd.get('total_filtered',0)} filtered, top RPN={top_rpn}. "
    f"CAPEX: EUR {cd.get('total',{}).get('central_eur_m',0):.0f}M. "
    f"LCOH: EUR {ld.get('central_eur_per_kg',0):.2f}/kg.",
    "Risk Library: 30 records. Cost Library: 30 benchmarks. IEA GHR 2025, IRENA 2024.",
    "Quantifies risk exposure and estimates CAPEX range and levelized cost of hydrogen.")

# Step 4
step_card("4", "Agent 4 — PM Review", "#43A047",
    f"Gate: {gate}. Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f}). "
    f"Gaps: {len(pm.get('critical_gaps',[]))} critical, {len(pm.get('important_gaps',[]))} important.",
    "Cross-dimension consistency check. Evidence audit. Confidence calibration. PMBOK phase-gate methodology.",
    "Quality-gates all upstream agent outputs and produces the final gate decision with conditions.")

st.divider()

# Confidence evolution
st.markdown("#### Confidence Evolution")
st.markdown("""
<div style="display:flex;align-items:center;gap:8px;margin:8px 0;">
<div style="background:#C8E6C9;padding:6px 12px;border-radius:4px;color:#1B5E20;font-weight:600;">Input</div>
<span>→</span>
<div style="background:#A5D6A7;padding:6px 12px;border-radius:4px;color:#1B5E20;font-weight:600;">A1</div>
<span>→</span>
<div style="background:#81C784;padding:6px 12px;border-radius:4px;color:#1B5E20;font-weight:600;">A2</div>
<span>→</span>
<div style="background:#66BB6A;padding:6px 12px;border-radius:4px;color:white;font-weight:600;">A3</div>
<span>→</span>
<div style="background:#43A047;padding:6px 12px;border-radius:4px;color:white;font-weight:600;">A4</div>
<span>→</span>
<div style="background:#2E7D32;padding:6px 12px;border-radius:4px;color:white;font-weight:600;">Decision</div>
</div>
""", unsafe_allow_html=True)

st.caption("This trace demonstrates complete evidence-to-decision auditability. Every conclusion links to a specific knowledge source and methodology.")
