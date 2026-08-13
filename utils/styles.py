import streamlit as st

# ── Design tokens ──────────────────────────────────────────────────────────────
GOLD   = "#D97706"   # Amber 600 — less neon, more refined
TEAL   = "#0D9488"   # Teal 600
BLUE   = "#3B82F6"   # Blue 500
MUTED  = "#6B7280"   # Gray 500
BG     = "#0F1117"   # Very dark
CARD   = "#1A1D27"   # Card background
RED    = "#EF4444"   # Red 500
GREEN  = "#22C55E"   # Green 500
WHITE  = "#E5E7EB"   # Gray 200
BORDER = "rgba(255,255,255,0.07)"


def inject_css() -> None:
    st.markdown("""
<style>

/* ══ 1. Masquer le chrome Streamlit ══ */

#MainMenu { visibility: hidden !important; }
footer    { visibility: hidden !important; }

[data-testid="stDeployButton"]   { display: none !important; }
[data-testid="stToolbarActions"] { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }

[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* ══ 2. Boutons collapse sidebar ══ */

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button {
    display: flex !important; visibility: visible !important;
    opacity: 1 !important; pointer-events: auto !important;
}
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] button {
    display: flex !important; visibility: visible !important;
    opacity: 1 !important; pointer-events: auto !important; cursor: pointer !important;
}

/* ══ 3. Sidebar ══ */

[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid rgba(255,255,255,.06) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem !important; }

/* ══ 4. Layout principal ══ */

.main .block-container {
    padding-top: 1.6rem;
    padding-left: 2.4rem;
    padding-right: 2.4rem;
    max-width: 1280px;
}

/* ══ 5. KPI cards ══ */

.kpi-grid { display: flex; gap: .9rem; flex-wrap: wrap; margin: 1rem 0; }
.kpi-card {
    flex: 1; min-width: 140px;
    background: #1A1D27;
    border: 1px solid rgba(255,255,255,.07);
    border-top: 2px solid #D97706;
    border-radius: 8px;
    padding: .9rem 1rem;
    text-align: center;
}
.kpi-label {
    color: #6B7280; font-size: .67rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem;
}
.kpi-value { color: #D97706; font-size: 1.75rem; font-weight: 700; line-height: 1.1; }
.kpi-sub   { color: #6B7280; font-size: .66rem; margin-top: .2rem; }

/* ══ 6. Section headers ══ */

.sec-header {
    border-left: 3px solid #D97706;
    padding-left: .8rem;
    margin: 1.4rem 0 .65rem 0;
}
.sec-header h3 { margin: 0; color: #E5E7EB; font-size: 1rem; font-weight: 600; }
.sec-header p  { margin: .12rem 0 0 0; color: #6B7280; font-size: .78rem; line-height: 1.4; }

/* ══ 7. Info / warning boxes ══ */

.insight-box {
    background: #1A1D27;
    border: 1px solid rgba(255,255,255,.08);
    border-left: 3px solid #0D9488;
    border-radius: 6px;
    padding: .9rem 1.1rem;
    margin: .8rem 0;
    line-height: 1.6;
    font-size: .84rem;
    color: #D1D5DB;
}
.warning-box {
    background: #1A1D27;
    border: 1px solid rgba(255,255,255,.08);
    border-left: 3px solid #D97706;
    border-radius: 6px;
    padding: .9rem 1.1rem;
    margin: .8rem 0;
    font-size: .84rem;
    color: #D1D5DB;
}

/* ══ 8. Scenario cards ══ */

.scenario-row { display: flex; gap: .9rem; flex-wrap: wrap; margin: 1rem 0; }
.scenario-card {
    flex: 1; min-width: 200px;
    background: #1A1D27;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 8px;
    padding: 1.15rem 1.2rem;
    border-top: 3px solid #D97706;
}
.scenario-card.s2 { border-top-color: #0D9488; }
.scenario-card.s3 { border-top-color: #EF4444; }
.scenario-title { font-weight: 600; font-size: .85rem; margin-bottom: .35rem; color: #E5E7EB; }
.scenario-price {
    font-size: 1.8rem; font-weight: 700; color: #D97706; line-height: 1; margin-bottom: .35rem;
}
.scenario-price.s2 { color: #0D9488; }
.scenario-price.s3 { color: #EF4444; }
.scenario-desc { color: #6B7280; font-size: .77rem; line-height: 1.5; }

/* ══ 9. Step / pipeline cards ══ */

.step-row { display: flex; gap: .7rem; flex-wrap: wrap; margin: .8rem 0; }
.step-card {
    flex: 1; min-width: 130px;
    background: #1A1D27;
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 6px;
    padding: .9rem 1rem;
}
.step-num {
    font-size: .65rem; font-weight: 700; letter-spacing: .08em;
    color: #D97706; text-transform: uppercase; margin-bottom: .35rem;
}
.step-title { font-weight: 600; font-size: .84rem; color: #E5E7EB; margin-bottom: .2rem; }
.step-desc  { color: #6B7280; font-size: .74rem; line-height: 1.5; }

/* ══ 10. Narrative / prose blocks ══ */

.prose {
    color: #D1D5DB; font-size: .88rem; line-height: 1.75;
    max-width: 680px;
}
.lead {
    color: #E5E7EB; font-size: 1rem; line-height: 1.7;
    max-width: 700px; margin-bottom: 1.2rem;
}
.label-tag {
    display: inline-block; font-size: .62rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    padding: .12rem .5rem; border-radius: 4px;
    background: rgba(217,119,6,.12); color: #D97706;
    border: 1px solid rgba(217,119,6,.25); margin-bottom: .5rem;
}
.label-tag.teal  { background: rgba(13,148,136,.12); color: #0D9488; border-color: rgba(13,148,136,.25); }
.label-tag.blue  { background: rgba(59,130,246,.12); color: #3B82F6; border-color: rgba(59,130,246,.25); }
.label-tag.red   { background: rgba(239,68,68,.12);  color: #EF4444; border-color: rgba(239,68,68,.25); }
.stat-big  { font-size: 2.1rem; font-weight: 700; color: #D97706; line-height: 1; }
.stat-label{ color: #6B7280; font-size: .69rem; margin-top: .2rem; }
.divider   { border: none; border-top: 1px solid rgba(255,255,255,.06); margin: 1.4rem 0; }

/* ══ 11. Streamlit widget overrides ══ */

div[data-testid="stMetric"] {
    background: #1A1D27; border-radius: 8px;
    padding: .75rem 1rem;
    border: 1px solid rgba(255,255,255,.07);
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size: .9rem !important;
    font-weight: 500 !important;
    padding: .6rem 1.5rem !important;
}
div[data-testid="stDataFrame"] { border-radius: 6px; overflow: hidden; }

/* ══ 12. Scrollbar ══ */

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0F1117; }
::-webkit-scrollbar-thumb { background: rgba(217,119,6,.25); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(217,119,6,.45); }

</style>
""", unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "") -> str:
    return (
        f'<div class="kpi-card">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{"<div class=kpi-sub>" + sub + "</div>" if sub else ""}'
        f"</div>"
    )


def kpi_row(cards: list[tuple]) -> None:
    html = '<div class="kpi-grid">'
    for label, value, *rest in cards:
        html += kpi_card(label, value, rest[0] if rest else "")
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "") -> None:
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f'<div class="sec-header"><h3>{title}</h3>{sub}</div>', unsafe_allow_html=True)


def insight_box(text: str) -> None:
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def warning_box(text: str) -> None:
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)


def no_data_msg(filename: str) -> None:
    st.warning(
        f"Fichier `{filename}` introuvable dans `data/`. "
        "Lancez d'abord `export_for_streamlit.R` depuis R pour générer les données.",
        icon="⚠️",
    )
