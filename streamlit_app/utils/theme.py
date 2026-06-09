"""Enterprise-grade theme for H2 Feasibility Copilot."""
import streamlit as st


def apply_theme():
    st.markdown("""
<style>
    .stApp { background: #FFFFFF; }
    h1, h2, h3 { color: #1B5E20; font-weight: 500; letter-spacing: -0.01em; }

    /* ─── Sidebar — wider, larger text ─── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        min-width: 280px !important;
        width: 280px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] {
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
    }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); margin: 16px 0; }
    section[data-testid="stSidebar"] .stCaption { color: #A5D6A7 !important; font-size: 0.9rem !important; }
    section[data-testid="stSidebar"] label { font-size: 0.95rem !important; }
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        font-size: 1.0rem !important;
        margin-bottom: 4px;
    }
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] strong {
        font-size: 1.05rem !important;
    }

    /* ─── Sidebar nav links ─── */
    section[data-testid="stSidebar"] a {
        color: #C8E6C9 !important; text-decoration: none; font-size: 0.95rem !important;
        padding: 6px 0; display: block; border-bottom: 1px solid rgba(255,255,255,0.08);
        transition: color 0.2s;
    }
    section[data-testid="stSidebar"] a:hover { color: #FFFFFF !important; }

    /* ─── Metrics ─── */
    [data-testid="stMetricValue"] { color: #2E7D32 !important; font-weight: 700; font-size: 1.6rem !important; }
    [data-testid="stMetricLabel"] { color: #558B2F !important; font-weight: 500; }
    [data-testid="stMetricDelta"] { color: #1565C0 !important; }

    /* ─── Buttons — strong contrast, white text, hover ─── */
    .stButton button {
        background: linear-gradient(135deg, #1B5E20, #2E7D32) !important;
        color: #FFFFFF !important; border: none !important; border-radius: 6px;
        font-weight: 600; padding: 10px 24px; letter-spacing: 0.3px;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #0D3B0E, #1B5E20) !important;
        box-shadow: 0 4px 14px rgba(27,94,32,0.4);
        transform: translateY(-1px);
    }
    .stButton button:active {
        transform: translateY(0);
    }

    /* secondary buttons */
    .stButton button[kind="secondary"] {
        background: #FFFFFF !important; color: #1B5E20 !important; border: 1px solid #2E7D32 !important;
    }
    .stButton button[kind="secondary"]:hover {
        background: #F1F8E9 !important; box-shadow: 0 2px 8px rgba(46,125,50,0.2);
    }

    /* ─── Alerts ─── */
    .stAlert { border-radius: 8px; border-left: 4px solid #2E7D32; }
    [data-testid="stInfo"] { background: #F1F8E9; color: #1B5E20; }

    /* ─── Dividers ─── */
    hr { border-color: #E0E0E0; margin: 20px 0; }

    /* ─── DataFrames ─── */
    .stDataFrame { border: 1px solid #E8F5E9; border-radius: 8px; font-size: 0.9rem; }

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab"] { border-radius: 6px 6px 0 0; color: #558B2F; font-weight: 500; }
    .stTabs [aria-selected="true"] {
        background: #F1F8E9 !important; color: #1B5E20 !important; font-weight: 600;
    }

    /* ─── Expanders ─── */
    .streamlit-expanderHeader { font-weight: 600; color: #1B5E20; }

    /* ─── Headers within sections ─── */
    h4 { color: #1B5E20; font-weight: 600; margin-top: 16px; }

    /* ─── Responsive: laptop-friendly ─── */
    @media (max-width: 1200px) {
        section[data-testid="stSidebar"] { min-width: 240px !important; width: 240px !important; }
        [data-testid="stMetricValue"] { font-size: 1.3rem !important; }
    }
    @media (max-width: 992px) {
        section[data-testid="stSidebar"] { min-width: 200px !important; width: 200px !important; }
    }
</style>
""", unsafe_allow_html=True)
