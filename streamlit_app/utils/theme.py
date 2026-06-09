"""Enterprise theme — professional green, large fonts, consulting aesthetic."""
import streamlit as st

def apply_sidebar():
    """Shared sidebar navigation for all pages (replaces Streamlit auto-nav)."""
    st.sidebar.markdown("### H2 Feasibility Copilot")
    st.sidebar.markdown("Multi-Agent Decision Platform")
    st.sidebar.divider()
    st.sidebar.markdown("**Workflow**")
    st.sidebar.markdown("<a href='/' target='_self'>- Home</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='/Project_Input' target='_self'>- Project Input</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='/Assessment_Report' target='_self'>- Assessment Report</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='/Risk_Assessment' target='_self'>- Risk Dashboard</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='/CAPEX_LCOH' target='_self'>- CAPEX & LCOH</a>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='/Assessment_History' target='_self'>- History</a>", unsafe_allow_html=True)
    st.sidebar.markdown("**Information**")
    st.sidebar.markdown("<a href='/Why_This_Matters' target='_self'>- Why This Matters</a>", unsafe_allow_html=True)
    st.sidebar.divider()
    if st.session_state.get("report"):
        r, pm = st.session_state["report"], st.session_state["report"].get("pm_review", {})
        gate = pm.get("gate_outcome","-")
        gc = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
        st.sidebar.markdown("**Assessment**")
        q = st.session_state.get("query",{})
        st.sidebar.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")
        st.sidebar.markdown(f"<span style='background:{gc.get(gate,'#78909C')};padding:4px 12px;border-radius:4px;color:white;font-weight:600;'>{gate}</span>", unsafe_allow_html=True)
    st.sidebar.caption("v1.0 | 141 validated knowledge assets")

def apply_theme():
    st.markdown("""
<style>
    .stApp { background: #F8FAF8; }
    /* ─── GLOBAL FONTS — 15-20% larger ─── */
    html, body, .stMarkdown, p, li { font-size: 1.05rem !important; line-height: 1.6; }
    h1 { font-size: 1.8rem !important; color: #1B5E20; font-weight: 600; }
    h2 { font-size: 1.4rem !important; color: #1B5E20; font-weight: 600; }
    h3 { font-size: 1.2rem !important; color: #2E7D32; font-weight: 600; }
    h4 { font-size: 1.1rem !important; color: #2E7D32; font-weight: 600; }
    .stCaption, .stCaption p { font-size: 0.9rem !important; color: #558B2F; }

    /* ─── TABLES ─── */
    .stDataFrame { font-size: 0.95rem !important; border: 1px solid #E0E0E0; border-radius: 8px; }
    .stDataFrame td, .stDataFrame th { padding: 8px 12px !important; }
    .stDataFrame th { background: #F1F8E9; color: #1B5E20; font-weight: 600; }

    /* ─── METRICS ─── */
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; font-weight: 700; color: #2E7D32 !important; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; font-weight: 500; color: #558B2F !important; }
    [data-testid="stMetricDelta"] { font-size: 0.85rem !important; color: #1565C0 !important; }

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        min-width: 280px !important; width: 280px !important;
    }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] .stCaption { color: #C8E6C9 !important; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { font-size: 1.0rem !important; line-height: 1.5; }
    section[data-testid="stSidebar"] a {
        color: #C8E6C9 !important; text-decoration: none; font-size: 0.95rem !important;
        padding: 6px 0; display: block; border-bottom: 1px solid rgba(255,255,255,0.08);
        transition: color 0.2s;
    }
    section[data-testid="stSidebar"] a:hover { color: #FFFFFF !important; }

    /* ─── BUTTONS ─── */
    .stButton button {
        background: linear-gradient(135deg, #1B5E20, #2E7D32) !important;
        color: #FFFFFF !important; border: none !important; border-radius: 6px;
        font-weight: 600; padding: 10px 24px; font-size: 1rem !important;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #0D3B0E, #1B5E20) !important;
        box-shadow: 0 4px 14px rgba(27,94,32,0.4); transform: translateY(-1px);
    }

    /* ─── ALERTS ─── */
    .stAlert { border-radius: 8px; border-left: 4px solid #2E7D32; font-size: 1rem !important; }
    [data-testid="stInfo"] { background: #F1F8E9; color: #1B5E20; }

    /* ─── DIVIDERS ─── */
    hr { border-color: #E0E0E0; margin: 28px 0; }

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab"] { font-size: 0.95rem !important; color: #558B2F; }
    .stTabs [aria-selected="true"] { background: #F1F8E9 !important; color: #1B5E20 !important; font-weight: 600; }

    /* ─── EXPANDERS ─── */
    .streamlit-expanderHeader { font-size: 1rem !important; font-weight: 600; color: #1B5E20; }

    /* ─── METRIC CARDS ─── */
    div[data-testid="metric-container"] {
        background: #FFFFFF; border: 1px solid #E0E0E0; border-radius: 8px;
        padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }

    /* ─── CONTAINERS / CARDS ─── */
    .stContainer, section[data-testid="stVerticalBlock"] > div[data-testid="element-container"] {
        font-size: 1rem;
    }

    /* ─── RESPONSIVE ─── */
    @media (max-width: 1200px) {
        section[data-testid="stSidebar"] { min-width: 240px !important; width: 240px !important; }
        [data-testid="stMetricValue"] { font-size: 1.3rem !important; }
    }
</style>
""", unsafe_allow_html=True)
