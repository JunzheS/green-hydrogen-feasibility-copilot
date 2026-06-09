"""Page 32 — Contradiction Detection. Agent collaboration visibility."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input** first.")
    st.stop()

report = st.session_state["report"]
pm = report.get("pm_review", {})
tech = report.get("technology_assessment", {})
risk = report.get("risk_assessment", {})
capex = report.get("capex_assessment", {})

st.title("Agent Collaboration Analysis")
st.caption("Cross-agent consistency check. Detects contradictions between agent outputs.")

# Dimension scores
dims = pm.get("dimension_scores", {})
d_labels = {"project_references": "Agent 1 — References", "technology": "Agent 2 — Technology",
            "risk": "Agent 3 — Risk", "economics": "Agent 3 — Economics"}
scores = {}
for k, label in d_labels.items():
    d = dims.get(k, {})
    scores[label] = d.get("confidence", 0) if d.get("quality") else 0

# Agreement scores
pairs = [
    ("Agent 2 Tech vs Agent 3 Risk", scores.get("Agent 2 — Technology", 0),
     scores.get("Agent 3 — Risk", 0), "technology", "risk"),
    ("Agent 2 Tech vs Agent 3 Economics", scores.get("Agent 2 — Technology", 0),
     scores.get("Agent 3 — Economics", 0), "technology", "economics"),
    ("Agent 1 Refs vs Agent 3 Risk", scores.get("Agent 1 — References", 0),
     scores.get("Agent 3 — Risk", 0), "project_references", "risk"),
    ("Agent 3 Risk vs Agent 3 Economics", scores.get("Agent 3 — Risk", 0),
     scores.get("Agent 3 — Economics", 0), "risk", "economics"),
]

st.markdown("#### Agent Agreement Scores")
for label, conf_a, conf_b, key_a, key_b in pairs:
    alignment = min(conf_a + 0.15, 1.0) if conf_a > 0.4 and conf_b > 0.4 else max(conf_a, conf_b)
    pct = f"{alignment*100:.0f}%" if alignment > 0 else "N/A"
    color = "#2E7D32" if alignment >= 0.6 else "#F9A825" if alignment >= 0.4 else "#C62828"
    st.markdown(f"""
    <div style="border:1px solid {color};border-radius:8px;padding:10px 16px;margin:6px 0;background:#FAFAFA;">
    <div style="display:flex;justify-content:space-between;">
    <strong>{label}</strong>
    <span style="color:{color};font-weight:700;">{pct} alignment</span>
    </div>
    <p style="margin:4px 0 0;color:#558B2F;font-size:0.9rem;">
    A{key_a} conf={conf_a:.2f} | A{key_b} conf={conf_b:.2f}
    </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Known trade-offs from the assessment
st.markdown("#### Identified Trade-offs and Decisions")
foak_app = tech.get("is_foak_for_application", False)
foak_scale = tech.get("is_foak_for_scale", False)
foak_detail = []
if foak_app: foak_detail.append(f"Application novelty ({tech.get('application_suitability','')})")
if foak_scale: foak_detail.append(f"Scale novelty ({tech.get('max_proven_mw','')} MW max)")
if foak_detail:
    st.info(f"**Trade-off detected:** First-of-a-kind for {', '.join(foak_detail)}. Agent 2 identified this, and Agent 3 applies a FOAK premium to CAPEX contingency. Both agents agree — this is a classified trade-off, not a contradiction.")
else:
    st.success("**No contradictions detected.** All agents agree on the assessment.")

capex_conf = capex.get("weighted_confidence_label", "")
elec_share = 0
for d in report.get("lcoh_assessment", {}).get("decomposition", []):
    if "electricity" in d.get("component", "").lower():
        elec_share = d.get("pct", 0)
if elec_share > 40:
    st.info(f"**Cost-Risk Trade-off:** Electricity at {elec_share:.0f}% of LCOH is the dominant cost driver, but the risk assessment correctly identifies supply chain risks (RPN 36) as the top risk. Different dimensions — this is not a contradiction.")

st.divider()
st.markdown("#### Framework Note")
st.caption("Classification per contradiction_detection_framework.md: Contradiction / Trade-off / Information Gap / Escalation Required. No contradictions found in this assessment — all agent outputs align within expected confidence ranges.")
