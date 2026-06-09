"""Enterprise theme — professional green, large fonts, consulting aesthetic.
Single source of truth for all design tokens (colors, typography, spacing).
"""
import streamlit as st

# ═══════════════════════════════════════════════════════════════
# DESIGN TOKENS — the canonical color palette
# ═══════════════════════════════════════════════════════════════
GREEN_PRIMARY   = "#1B5E20"
GREEN_SECONDARY = "#2E7D32"
GREEN_ACCENT    = "#558B2F"
GREEN_TINT_1    = "#E8F5E9"
GREEN_TINT_2    = "#C8E6C9"
GREEN_TINT_3    = "#A5D6A7"
GREEN_TINT_4    = "#F1F8E9"

AMBER_WARNING   = "#F9A825"
RED_CRITICAL    = "#C62828"
RED_HEAT        = "#D32F2F"
ORANGE_HIGH     = "#EF6C00"
GREY_NEUTRAL    = "#78909C"
SURFACE_WHITE   = "#FFFFFF"
SURFACE_LIGHT   = "#F8FAF8"
DISABLED_GREY   = "#9E9E9E"
DISABLED_BG     = "rgba(255,255,255,0.25)"

CARD_BORDER      = "#E0E0E0"
CARD_BORDER_GREEN = "#C8E6C9"
CARD_RADIUS      = "8px"
GATE_RADIUS      = "12px"


def gate_colors():
    """Return gate outcome → (background, text-color) mappings."""
    return {
        "PROCEED":              (GREEN_SECONDARY, "white"),
        "PROCEED WITH CAUTION": (AMBER_WARNING, GREEN_PRIMARY),
        "DO NOT PROCEED":       (RED_CRITICAL, "white"),
        "INSUFFICIENT DATA":    (GREY_NEUTRAL, "white"),
    }


def _page_is_locked(path_key: str) -> bool:
    """Return True if the page requires an assessment but none exists."""
    return not bool(st.session_state.get("report"))


def _sidebar_link(label: str, path: str, locked: bool = False):
    """Render a single sidebar navigation item — active, locked, or normal."""
    if locked:
        st.sidebar.markdown(
            f"<span style='color:{DISABLED_GREY};padding:4px 0 4px 12px;"
            f"display:block;font-size:0.95rem;border-left:3px solid transparent;"
            f"cursor:not-allowed;opacity:0.55;'>{label} 🗝</span>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.page_link(path, label=label)


def apply_sidebar():
    """Shared sidebar navigation — 3-tier guided workflow.

    Tier 1 — Always visible:
        Home, Project Input, Why This Matters

    Tier 2 — Unlocked after assessment (locked before):
        Assessment Report, Risk Dashboard, CAPEX & LCOH,
        Reference Projects, Assessment History

    Tier 3 — Expert Results (collapsible, collapsed by default):
        Technology Assessment, Technology Comparison, Agent Trace,
        Agent Collaboration, OEM Intelligence, Developer Intelligence,
        Source Transparency
    """
    # ── Session init + recovery ──
    from utils.session import init_session  # type: ignore
    init_session()
    has_report = bool(st.session_state.get("report"))

    if not has_report:
        history = st.session_state.get("history") or []
        if not history:
            from utils.session import load_history  # type: ignore
            history = load_history()
        if history:
            latest = history[0]
            st.session_state["report"] = latest.get("report")
            st.session_state["query"] = latest.get("query")
            st.session_state["assessment_complete"] = True
            st.session_state["current_assessment_id"] = latest.get("assessment_id")
            has_report = True

    # ── HEADER ──
    st.sidebar.markdown("### H2 Feasibility Copilot")
    st.sidebar.markdown("Multi-Agent Decision Platform")
    st.sidebar.divider()

    # ── TIER 1: ALWAYS VISIBLE ──
    _sidebar_link("Home", "app.py")
    _sidebar_link("Project Input", "pages/01_Project_Input.py")

    st.sidebar.divider()

    # ── TIER 2: CORE RESULTS (locked before assessment) ──
    st.sidebar.markdown("**Core Results**")
    _sidebar_link("Assessment Report", "pages/02_Assessment_Report.py", locked=not has_report)
    _sidebar_link("Risk Dashboard", "pages/05_Risk_Assessment.py", locked=not has_report)
    _sidebar_link("CAPEX & LCOH", "pages/06_CAPEX_LCOH.py", locked=not has_report)
    _sidebar_link("Reference Projects", "pages/03_Reference_Projects.py", locked=not has_report)
    _sidebar_link("History", "pages/08_Assessment_History.py", locked=not has_report)

    st.sidebar.divider()

    # ── TIER 3: EXPERT RESULTS (collapsible) ──
    with st.sidebar.expander("Expert Results", expanded=False):
        _sidebar_link("Technology Assessment", "pages/04_Technology_Assessment.py", locked=not has_report)
        _sidebar_link("Technology Comparison", "pages/09_Technology_Comparison.py", locked=not has_report)
        _sidebar_link("Agent Trace", "pages/07_Agent_Trace.py", locked=not has_report)
        _sidebar_link("Agent Collaboration", "pages/32_Contradiction_Detection.py", locked=not has_report)
        _sidebar_link("OEM Intelligence", "pages/30_OEM_Intelligence.py")
        _sidebar_link("Developer Intelligence", "pages/31_Developer_Intelligence.py")
        _sidebar_link("Source Transparency", "pages/33_Source_Transparency.py", locked=not has_report)

    st.sidebar.divider()

    # ── INFORMATION ──
    _sidebar_link("Why This Matters", "pages/99_Why_This_Matters.py")

    st.sidebar.divider()

    # ── ASSESSMENT STATUS ──
    if has_report:
        r, pm = st.session_state["report"], st.session_state["report"].get("pm_review", {})
        gate = pm.get("gate_outcome", "-")
        st.sidebar.markdown("**Current Assessment**")
        q = st.session_state.get("query", {})
        st.sidebar.caption(
            f"{q.get('capacity_mw','')} MW {q.get('technology','')}"
            f" | {q.get('country','')}"
        )
        gc = gate_colors()
        bg, fg = gc.get(gate, (GREY_NEUTRAL, "white"))
        st.sidebar.markdown(
            f"<span style='background:{bg};padding:4px 12px;border-radius:4px;"
            f"color:{fg};font-weight:600;'>{gate}</span>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.caption("Run an assessment to unlock analysis.")

    st.sidebar.caption("v1.0 | 141 validated knowledge assets")


def apply_theme():
    """Enterprise theme CSS — injected once per session.

    All design tokens defined in this module. Page scripts reference
    tokens via `theme.GREEN_PRIMARY` etc. rather than hard-coding colors.
    """
    if st.session_state.get("_theme_applied"):
        return

    st.markdown(f"""
<style>
    .stApp {{ background: {SURFACE_LIGHT}; }}

    /* ─── TYPOGRAPHY — 15-20% larger than default ─── */
    html, body, .stMarkdown, p, li {{ font-size: 1.05rem !important; line-height: 1.6; }}
    h1 {{ font-size: 1.8rem !important; color: {GREEN_PRIMARY}; font-weight: 600; }}
    h2 {{ font-size: 1.4rem !important; color: {GREEN_PRIMARY}; font-weight: 600; }}
    h3 {{ font-size: 1.2rem !important; color: {GREEN_SECONDARY}; font-weight: 600; }}
    h4 {{ font-size: 1.1rem !important; color: {GREEN_SECONDARY}; font-weight: 600; }}
    .stCaption, .stCaption p {{ font-size: 0.9rem !important; color: {GREEN_ACCENT}; }}

    /* ─── TABLES ─── */
    .stDataFrame {{ font-size: 0.95rem !important; border: 1px solid {CARD_BORDER}; border-radius: {CARD_RADIUS}; }}
    .stDataFrame td, .stDataFrame th {{ padding: 8px 12px !important; }}
    .stDataFrame th {{ background: {GREEN_TINT_4}; color: {GREEN_PRIMARY}; font-weight: 600; }}

    /* ─── METRICS ─── */
    [data-testid="stMetricValue"] {{ font-size: 1.5rem !important; font-weight: 700; color: {GREEN_SECONDARY} !important; }}
    [data-testid="stMetricLabel"] {{ font-size: 0.9rem !important; font-weight: 500; color: {GREEN_ACCENT} !important; }}
    [data-testid="stMetricDelta"] {{ font-size: 0.85rem !important; color: #1565C0 !important; }}

    /* ─── SIDEBAR ─── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {GREEN_PRIMARY} 0%, {GREEN_SECONDARY} 100%);
        min-width: 280px !important; width: 280px !important;
    }}
    section[data-testid="stSidebar"] * {{ color: {SURFACE_WHITE} !important; }}
    section[data-testid="stSidebar"] .stCaption {{ color: {GREEN_TINT_2} !important; }}
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        font-size: 1.0rem !important; line-height: 1.5;
    }}
    section[data-testid="stSidebar"] a {{
        color: {GREEN_TINT_2} !important; text-decoration: none; font-size: 0.95rem !important;
        padding: 6px 0; display: block; border-bottom: 1px solid rgba(255,255,255,0.08);
        transition: color 0.2s;
    }}
    section[data-testid="stSidebar"] a:hover {{ color: {SURFACE_WHITE} !important; }}

    /* ─── BUTTONS ─── */
    .stButton button {{
        background: linear-gradient(135deg, {GREEN_PRIMARY}, {GREEN_SECONDARY}) !important;
        color: {SURFACE_WHITE} !important; border: none !important; border-radius: 6px;
        font-weight: 600; padding: 10px 24px; font-size: 1rem !important;
        transition: all 0.2s ease;
    }}
    .stButton button:hover {{
        background: linear-gradient(135deg, #0D3B0E, {GREEN_PRIMARY}) !important;
        box-shadow: 0 4px 14px rgba(27,94,32,0.4); transform: translateY(-1px);
    }}

    /* ─── ALERTS ─── */
    .stAlert {{ border-radius: {CARD_RADIUS}; border-left: 4px solid {GREEN_SECONDARY}; font-size: 1rem !important; }}
    [data-testid="stInfo"] {{ background: {GREEN_TINT_4}; color: {GREEN_PRIMARY}; }}

    /* ─── DIVIDERS ─── */
    hr {{ border-color: {CARD_BORDER}; margin: 28px 0; }}

    /* ─── TABS ─── */
    .stTabs [data-baseweb="tab"] {{ font-size: 0.95rem !important; color: {GREEN_ACCENT}; }}
    .stTabs [aria-selected="true"] {{ background: {GREEN_TINT_4} !important; color: {GREEN_PRIMARY} !important; font-weight: 600; }}

    /* ─── EXPANDERS ─── */
    .streamlit-expanderHeader {{ font-size: 1rem !important; font-weight: 600; color: {GREEN_PRIMARY}; }}

    /* ─── METRIC CARDS — consistent: white bg, light border, subtle shadow ─── */
    div[data-testid="metric-container"] {{
        background: {SURFACE_WHITE}; border: 1px solid {CARD_BORDER}; border-radius: {CARD_RADIUS};
        padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}

    /* ─── CONTAINERS ─── */
    .stContainer, section[data-testid="stVerticalBlock"] > div[data-testid="element-container"] {{
        font-size: 1rem;
    }}

    /* ─── RESPONSIVE ─── */
    @media (max-width: 1200px) {{
        section[data-testid="stSidebar"] {{ min-width: 240px !important; width: 240px !important; }}
        [data-testid="stMetricValue"] {{ font-size: 1.3rem !important; }}
    }}
</style>
""", unsafe_allow_html=True)
    st.session_state["_theme_applied"] = True
