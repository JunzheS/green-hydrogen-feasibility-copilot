"""Page 5 — Risk Dashboard with charts and consequence analysis."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
risk = report.get("risk_assessment", {})
consequences = report.get("risk_consequences", [])
top = risk.get("top_risks", [])

st.title("Risk Dashboard")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")

# ─── CLASS DISTRIBUTION — donut-style via KPIs ───
st.markdown("#### Risk Profile")
counts = risk.get("risk_count_by_class", {})
rc1, rc2, rc3, rc4 = st.columns(4)
with rc1: st.metric("Critical", counts.get("critical",0))
with rc2: st.metric("High", counts.get("high",0))
with rc3: st.metric("Medium", counts.get("medium",0))
with rc4: st.metric("Low", counts.get("low",0))

# Visual distribution
if counts:
    dist_df = pd.DataFrame([
        {"Class": "Critical", "Count": counts.get("critical",0)},
        {"Class": "High", "Count": counts.get("high",0)},
        {"Class": "Medium", "Count": counts.get("medium",0)},
        {"Class": "Low", "Count": counts.get("low",0)},
    ])
    st.bar_chart(dist_df.set_index("Class")["Count"], use_container_width=True, height=150)

st.divider()

# ─── P×I MATRIX HEATMAP PREVIEW ───
st.markdown("#### Probability x Impact Matrix")
matrix_data = []
for r in consequences if consequences else top[:12]:
    matrix_data.append({"Risk": r.get("risk_name","")[:40], "P": r.get("probability",3),
                        "I": r.get("impact",3), "RPN": r.get("rpn",0), "Class": r.get("risk_class","")})
# Heatmap via bar chart colored by class
if matrix_data:
    hm_df = pd.DataFrame(matrix_data)
    hm_df["Color"] = hm_df["Class"].map({"critical":4,"high":3,"medium":2,"low":1}).fillna(0)
    # Top 5 by RPN
    top5 = hm_df.nlargest(5, "RPN")
    st.markdown("**Top 5 Risks by Priority**")
    st.dataframe(top5[["Risk","P","I","RPN","Class"]], use_container_width=True, hide_index=True,
                 column_config={"RPN": st.column_config.NumberColumn(format="%d")})

st.divider()

# ─── CATEGORY BREAKDOWN ───
st.markdown("#### Risk by Category")
by_cat = risk.get("risks_by_category", {})
if by_cat:
    cats, rpns = [], []
    for cn, rl in by_cat.items():
        if rl:
            cats.append(cn.replace("_"," ").title())
            rpns.append(max(r["rpn"] for r in rl))
    if cats:
        st.bar_chart(pd.DataFrame({"Category": cats, "Max RPN": rpns}).set_index("Category"),
                     use_container_width=True, height=200)

st.divider()

# ─── FULL REGISTER ───
st.markdown("#### Risk Register")
if consequences:
    rows = []
    for r in consequences:
        refs = r.get("reference_projects", [])
        rows.append({
            "ID": r.get("risk_id",""), "Risk": r.get("risk_name","")[:55],
            "Class": r.get("risk_class","").upper(), "RPN": r.get("rpn",0),
            "Category": r.get("category","").replace("_"," ").title(),
            "Mitigation": r.get("mitigation","")[:70],
            "Evidence": ", ".join(refs[:2]) if refs else "-",
        })
    df_reg = pd.DataFrame(rows)
    def color_cls(v):
        cs = {"CRITICAL":"background:#C62828;color:white;font-weight:600",
              "HIGH":"background:#EF6C00;color:white;font-weight:600",
              "MEDIUM":"background:#F9A825;color:#1B5E20;font-weight:600",
              "LOW":"background:#2E7D32;color:white;font-weight:600"}
        return cs.get(v, "")
    st.dataframe(df_reg.style.map(color_cls, subset=["Class"]), use_container_width=True, hide_index=True,
                 column_config={"RPN": st.column_config.NumberColumn(format="%d")})

st.divider()

# ─── DETAILS ───
st.markdown("#### Risk Details")
for r in (consequences if consequences else top[:10]):
    with st.expander(f"[{r.get('risk_class','').upper()}] {r.get('risk_id','')} — {r.get('risk_name','')[:70]} (RPN: {r.get('rpn',0)})"):
        st.markdown(f"**Category:** {r.get('category','').replace('_',' ').title()}")
        st.markdown(f"**Description:** {r.get('description','')[:300]}")
        if r.get("mitigation"): st.markdown(f"**Mitigation:** {r['mitigation'][:250]}")
        refs = r.get("reference_projects", [])
        if refs: st.caption(f"Evidence: {', '.join(refs[:4])}")
