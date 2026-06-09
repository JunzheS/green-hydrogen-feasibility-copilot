"""Page 5 — Risk Dashboard with real 5x5 heatmap and full register."""
import streamlit as st
import pandas as pd

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

# Risk class KPIs
st.markdown("#### Risk Profile")
counts = risk.get("risk_count_by_class", {})
r1, r2, r3, r4 = st.columns(4)
with r1: st.metric("Critical", counts.get("critical",0))
with r2: st.metric("High", counts.get("high",0))
with r3: st.metric("Medium", counts.get("medium",0))
with r4: st.metric("Low", counts.get("low",0))
dist_df = pd.DataFrame([
    {"Class":"Critical","Count":counts.get("critical",0)},{"Class":"High","Count":counts.get("high",0)},
    {"Class":"Medium","Count":counts.get("medium",0)},{"Class":"Low","Count":counts.get("low",0)},
])
st.bar_chart(dist_df.set_index("Class")["Count"], height=140)
st.divider()

# ─── REAL 5x5 RISK HEATMAP ───
st.markdown("#### Probability x Impact Matrix")
risks_plot = consequences if consequences else top[:12]
hm = [[[] for _ in range(5)] for _ in range(5)]
for r in risks_plot:
    p = min(r.get("probability",3)-1, 4)
    im = min(r.get("impact",3)-1, 4)
    hm[p][im].append(r.get("risk_name","")[:30])

def heat_color(p_idx, i_idx):
    s = (p_idx+1)*(i_idx+1)
    if s >= 16: return "#D32F2F"
    if s >= 9: return "#EF6C00"
    if s >= 4: return "#F9A825"
    return "#A5D6A7"

html = '<table style="width:100%;border-collapse:collapse;font-size:0.9rem;">'
html += '<tr><td style="padding:4px;font-weight:600;text-align:right;">Impact 5→</td>'
for c in range(5): html += f'<td style="width:18%;text-align:center;padding:2px;">{5-c}</td>'
html += '</tr>'
for i in range(5):
    html += f'<tr><td style="padding:2px;font-weight:600;text-align:right;">{5-i}</td>'
    for p in range(5):
        cell = hm[4-i][p]
        label = cell[0] if cell else ""
        c = heat_color(p, 4-i)
        fg = "white" if (p+1)*(5-i) >= 9 else "#1B5E20"
        html += f'<td style="background:{c};color:{fg};padding:6px;border-radius:4px;text-align:center;font-size:0.8rem;">{label if label else "·"}</td>'
    html += '</tr>'
html += '<tr><td></td>'
for c in range(5): html += f'<td style="text-align:center;font-size:0.8rem;color:#558B2F;">{c+1}</td>'
html += '</tr><tr><td></td><td colspan="5" style="text-align:center;font-size:0.8rem;color:#558B2F;">Probability →</td></tr></table>'
st.markdown(html, unsafe_allow_html=True)
st.caption("Top risk names plotted at their P x I coordinates. Full details in register below.")
st.divider()

# Top 5
st.markdown("#### Top 5 Risks by Priority")
if consequences:
    hm_df = pd.DataFrame([{"Risk":r.get("risk_name","")[:40],"P":r.get("probability",3),"I":r.get("impact",3),"RPN":r.get("rpn",0),"Class":r.get("risk_class","").upper()} for r in consequences])
    st.dataframe(hm_df.nlargest(5,"RPN")[["Risk","P","I","RPN","Class"]], use_container_width=True, hide_index=True,
                 column_config={"RPN": st.column_config.NumberColumn(format="%d")})

st.divider()

# Category chart
st.markdown("#### Risk by Category")
by_cat = risk.get("risks_by_category", {})
if by_cat:
    cats, rpns = [], []
    for cn, rl in by_cat.items():
        if rl: cats.append(cn.replace("_"," ").title()); rpns.append(max(r["rpn"] for r in rl))
    if cats: st.bar_chart(pd.DataFrame({"Category":cats,"Max RPN":rpns}).set_index("Category"), height=180)

st.divider()

# Full register
st.markdown("#### Risk Register")
if consequences:
    rows = [{"ID":r.get("risk_id",""),"Risk":r.get("risk_name","")[:55],"Class":r.get("risk_class","").upper(),
             "RPN":r.get("rpn",0),"Category":r.get("category","").replace("_"," ").title(),
             "Mitigation":r.get("mitigation","")[:70],"Evidence":", ".join(r.get("reference_projects",[])[:2]) or "-"} for r in consequences]
    df = pd.DataFrame(rows)
    def cc(v):
        cs = {"CRITICAL":"background:#D32F2F;color:white;font-weight:600","HIGH":"background:#EF6C00;color:white;font-weight:600",
              "MEDIUM":"background:#F9A825;color:#1B5E20;font-weight:600","LOW":"background:#2E7D32;color:white;font-weight:600"}
        return cs.get(v,"")
    st.dataframe(df.style.map(cc,subset=["Class"]), use_container_width=True, hide_index=True,
                 column_config={"RPN": st.column_config.NumberColumn(format="%d")})

st.divider()

# Details
st.markdown("#### Risk Details")
for r in (consequences if consequences else top[:10]):
    with st.expander(f"[{r.get('risk_class','').upper()}] {r.get('risk_id','')} — {r.get('risk_name','')[:65]} (RPN: {r.get('rpn',0)})"):
        st.markdown(f"**{r.get('category','').replace('_',' ').title()}**")
        st.markdown(r.get('description','')[:300])
        if r.get("mitigation"): st.markdown(f"**Mitigation:** {r['mitigation'][:250]}")
        if r.get("reference_projects"): st.caption(f"Evidence: {', '.join(r['reference_projects'][:4])}")

st.divider()
st.markdown("""<div style="display:flex;gap:16px;font-size:0.9rem;">
<a href='/Assessment_Report' target='_self' style="color:#2E7D32;">← Assessment Report</a>
<a href='/Contradiction_Detection' target='_self' style="color:#2E7D32;">Agent Collaboration Analysis →</a>
</div>""", unsafe_allow_html=True)
