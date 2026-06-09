"""Page 31 — Developer Intelligence. Hidden portfolio data exposed."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()
from collections import Counter

from src.main import FeasibilityEngine
engine = FeasibilityEngine() if "fe_engine" not in st.session_state else st.session_state["fe_engine"]
st.session_state["fe_engine"] = engine
projects = engine.projects

st.title("Developer Intelligence")
st.caption("Developer portfolio data extracted from all 82 project records.")

dev_map = {}
for p in projects:
    dev = p.developer if p.developer else "Unknown"
    if dev not in dev_map:
        dev_map[dev] = []
    dev_map[dev].append(p)

summary = []
for dev, projs in sorted(dev_map.items(), key=lambda x: -len(x[1])):
    techs = Counter(p.technology for p in projs)
    countries = set(p.country for p in projs)
    total_mw = sum(p.capacity_mw for p in projs if p.capacity_mw and p.capacity_mw < 5000)
    statuses = Counter(p.status for p in projs)
    summary.append({
        "Developer": dev[:50], "Projects": len(projs),
        "Total MW": f"{total_mw:.0f}" if total_mw else "-",
        "Technologies": ", ".join(f"{k} ({v})" for k, v in sorted(techs.items(), key=lambda x: -x[1])),
        "Countries": ", ".join(sorted(countries)),
        "Statuses": ", ".join(f"{k.replace('_',' ').title()}: {v}" for k, v in sorted(statuses.items())),
    })

st.markdown("#### Developer Portfolio Overview")
st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

st.divider()

# Filter by developer
st.markdown("#### Developer Deep Dive")
dev_names = sorted(dev_map.keys(), key=lambda x: -len(dev_map[x]))
selected_dev = st.selectbox("Select Developer", dev_names)
if selected_dev:
    projs = dev_map[selected_dev]
    total_mw = sum(p.capacity_mw for p in projs if p.capacity_mw and p.capacity_mw < 5000)
    techs = Counter(p.technology for p in projs)
    offtakes = Counter(p.primary_offtake for p in projs)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Projects", len(projs))
    with col2: st.metric("Total MW", f"{total_mw:.0f}")
    with col3: st.metric("Technologies", len(techs))
    with col4: st.metric("Countries", len(set(p.country for p in projs)))

    rows = [{"ID": p.project_id, "Project": p.project_name, "Country": p.country,
             "MW": f"{p.capacity_mw:.0f}" if p.capacity_mw else "-",
             "Tech": p.technology, "Status": p.status.replace("_", " ").title(),
             "Offtake": p.primary_offtake.replace("_", " ").title(),
             "OEM": p.oem if p.oem else "Not Disclosed"} for p in sorted(projs, key=lambda x: -x.capacity_mw)]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    if len(projs) > 1:
        chart_df = pd.DataFrame([{"Tech": p.technology, "MW": p.capacity_mw} for p in projs if p.capacity_mw])
        if not chart_df.empty:
            st.bar_chart(chart_df.groupby("Tech").sum(numeric_only=True))
