"""Page 30 — OEM Intelligence. Hidden data exposed."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()
from src.main import FeasibilityEngine
from src.engines.oem_intelligence_engine import get_oem_summary

st.title("OEM Intelligence")
st.caption("Electrolyzer manufacturer deployment data extracted from all 82 project records.")

engine = FeasibilityEngine() if "fe_engine" not in st.session_state else st.session_state["fe_engine"]
st.session_state["fe_engine"] = engine
projects = engine.projects

# Build OEM index from project data
oem_map = {}
for p in projects:
    oem_raw = getattr(p, 'oem', None)
    if not oem_raw:
        oem_raw = "Not Disclosed"
    if oem_raw not in oem_map:
        oem_map[oem_raw] = []
    oem_map[oem_raw].append(p)

# Aggregated summary
oem_summary = []
for oem, projs in sorted(oem_map.items(), key=lambda x: -len(x[1])):
    techs = {}
    mw_total = 0
    countries = set()
    for p in projs:
        techs[p.technology] = techs.get(p.technology, 0) + 1
        if p.capacity_mw and p.capacity_mw < 5000:
            mw_total += p.capacity_mw
        countries.add(p.country)
    oem_summary.append({
        "OEM": oem, "Projects": len(projs),
        "Total MW": mw_total if mw_total > 0 else "-",
        "Technologies": ", ".join(f"{k} ({v})" for k, v in techs.items()),
        "Countries": ", ".join(sorted(countries)),
    })

st.markdown("#### Global OEM Deployment")
st.dataframe(pd.DataFrame(oem_summary), use_container_width=True, hide_index=True,
             column_config={"Total MW": st.column_config.NumberColumn(format="%.0f")})
st.caption("OEM data is extracted from the `technology.electrolyzer_manufacturer` field in project records.")

st.divider()

# Filter by OEM
st.markdown("#### Filter by OEM")
oem_names = sorted(oem_map.keys(), key=lambda x: -len(oem_map[x]))
selected_oem = st.selectbox("Select OEM", ["All"] + oem_names)
if selected_oem != "All":
    projs = oem_map[selected_oem]
    st.markdown(f"**{selected_oem}** — {len(projs)} project(s)")
    rows = [{"ID": p.project_id, "Project": p.project_name, "Country": p.country,
             "MW": f"{p.capacity_mw:.0f}" if p.capacity_mw else "-",
             "Tech": p.technology, "Status": p.status.replace("_", " ").title(),
             "Offtake": p.primary_offtake.replace("_", " ").title()} for p in sorted(projs, key=lambda x: x.project_id)]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    if len(projs) > 1:
        chart_df = pd.DataFrame([{"Country": p.country, "MW": p.capacity_mw} for p in projs if p.capacity_mw])
        if not chart_df.empty:
            st.bar_chart(chart_df.groupby("Country").sum(numeric_only=True))
else:
    # Top OEMs chart
    top_oems = [(k, len(v)) for k, v in oem_map.items() if k != "Not Disclosed"]
    top_oems.sort(key=lambda x: -x[1])
    if top_oems:
        st.markdown("#### OEMs by Project Count")
        st.bar_chart(pd.DataFrame(top_oems[:10], columns=["OEM", "Projects"]).set_index("OEM"))

st.caption("47 projects have 'Not Disclosed' OEM data. This is a data completion opportunity for future sprints.")
