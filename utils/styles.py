import streamlit as st

GOLD   = "#F4A926"
TEAL   = "#64FFDA"
BLUE   = "#4FC3F7"
MUTED  = "#8892B0"
BG     = "#0A1628"
CARD   = "#112240"
RED    = "#FF6B6B"
GREEN  = "#69DB7C"
WHITE  = "#CCD6F6"


def inject_css() -> None:
    st.markdown("""
<style>

/* ══ 1. Masquer le chrome Streamlit sans tuer la sidebar ══ */

#MainMenu { visibility: hidden !important; }
footer    { visibility: hidden !important; }

[data-testid="stDeployButton"]   { display: none !important; }
[data-testid="stToolbarActions"] { display: none !important; }
[data-testid="stDecoration"]     { display: none !important; }
[data-testid="stStatusWidget"]   { display: none !important; }

/* Rendre le header transparent — SANS le cacher (le collapse button y est rattaché) */
[data-testid="stHeader"] {
    background-color: transparent !important;
    border-bottom: none !important;
    box-shadow: none !important;
}

/* ══ 2. Boutons collapse sidebar — visibilité SANS override de position ══ */

/* Bouton ← fermer la sidebar */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapseButton"] button {
    display:        flex    !important;
    visibility:     visible !important;
    opacity:        1       !important;
    pointer-events: auto    !important;
}

/* Bouton > rouvrir la sidebar — NE PAS forcer position, laisser Streamlit placer */
[data-testid="collapsedControl"],
[data-testid="collapsedControl"] button {
    display:        flex    !important;
    visibility:     visible !important;
    opacity:        1       !important;
    pointer-events: auto    !important;
    cursor:         pointer !important;
}

/* ══ 3. Sidebar ══ */

[data-testid="stSidebar"] {
    background: linear-gradient(170deg, #0d1f3c 0%, #0a1628 100%) !important;
    border-right: 1px solid rgba(244,169,38,.12) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.2rem !important;
}

/* ══ 4. Layout principal ══ */

.main .block-container {
    padding-top: 1.4rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

/* ══ 5. KPI cards ══ */

.kpi-grid {
    display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.1rem 0;
}
.kpi-card {
    flex: 1; min-width: 150px;
    background: #112240;
    border: 1px solid rgba(244,169,38,.2);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    text-align: center;
    transition: border-color .2s, transform .15s;
}
.kpi-card:hover {
    border-color: rgba(244,169,38,.45);
    transform: translateY(-2px);
}
.kpi-label {
    color: #8892B0; font-size: .69rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .09em; margin-bottom: .3rem;
}
.kpi-value { color: #F4A926; font-size: 1.9rem; font-weight: 700; line-height: 1.1; }
.kpi-sub   { color: #8892B0; font-size: .67rem; margin-top: .25rem; }

/* ══ 6. Section headers ══ */

.sec-header {
    border-left: 3px solid #F4A926;
    padding-left: .85rem;
    margin: 1.5rem 0 .75rem 0;
}
.sec-header h3 { margin: 0; color: #CCD6F6; font-size: 1.05rem; font-weight: 600; }
.sec-header p  { margin: .15rem 0 0 0; color: #8892B0; font-size: .8rem; line-height: 1.45; }

/* ══ 7. Info boxes ══ */

.insight-box {
    background: rgba(100,255,218,.04);
    border: 1px solid rgba(100,255,218,.18);
    border-radius: 9px;
    padding: 1rem 1.15rem;
    margin: .9rem 0;
    line-height: 1.6;
    font-size: .85rem;
}
.warning-box {
    background: rgba(244,169,38,.06);
    border: 1px solid rgba(244,169,38,.22);
    border-radius: 9px;
    padding: 1rem 1.15rem;
    margin: .9rem 0;
    font-size: .85rem;
}

/* ══ 8. Scenario cards ══ */

.scenario-row { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0; }
.scenario-card {
    flex: 1; min-width: 200px;
    background: #112240;
    border-radius: 12px;
    padding: 1.25rem 1.3rem;
    border-top: 3px solid #F4A926;
    transition: transform .15s;
}
.scenario-card:hover { transform: translateY(-2px); }
.scenario-card.s2  { border-top-color: #64FFDA; }
.scenario-card.s3  { border-top-color: #FF6B6B; }
.scenario-title {
    font-weight: 600; font-size: .88rem;
    margin-bottom: .4rem; color: #CCD6F6;
}
.scenario-price {
    font-size: 2rem; font-weight: 700;
    color: #F4A926; line-height: 1;
    margin-bottom: .4rem;
}
.scenario-price.s2 { color: #64FFDA; }
.scenario-price.s3 { color: #FF6B6B; }
.scenario-desc { color: #8892B0; font-size: .78rem; line-height: 1.5; }

/* ══ 9. View badges ══ */

.badge-exec {
    display: inline-block; padding: .18rem .65rem; border-radius: 20px;
    font-size: .68rem; font-weight: 600; letter-spacing: .06em;
    background: rgba(100,255,218,.08); color: #64FFDA;
    border: 1px solid rgba(100,255,218,.28);
    margin-bottom: .5rem;
}
.badge-tech {
    display: inline-block; padding: .18rem .65rem; border-radius: 20px;
    font-size: .68rem; font-weight: 600; letter-spacing: .06em;
    background: rgba(244,169,38,.08); color: #F4A926;
    border: 1px solid rgba(244,169,38,.28);
    margin-bottom: .5rem;
}

/* ══ 10. Streamlit widget overrides ══ */

div[data-testid="stMetric"] {
    background: #112240;
    border-radius: 10px;
    padding: .8rem 1rem;
    border: 1px solid rgba(244,169,38,.12);
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(244,169,38,.3);
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size: .84rem;
    padding-bottom: .6rem;
}
div[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
}
div[data-testid="stRadio"] > label {
    font-size: .82rem !important;
}
div[data-testid="stRadio"] {
    gap: .3rem;
}

/* ══ 11. Scrollbar custom ══ */

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0A1628; }
::-webkit-scrollbar-thumb { background: rgba(244,169,38,.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(244,169,38,.55); }

</style>
""", unsafe_allow_html=True)


def kpi_card(label: str, value: str, sub: str = "") -> str:
    return f"""
<div class="kpi-card">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    {'<div class="kpi-sub">' + sub + '</div>' if sub else ''}
</div>"""


def kpi_row(cards: list[tuple]) -> None:
    html = '<div class="kpi-grid">'
    for label, value, *rest in cards:
        sub = rest[0] if rest else ""
        html += kpi_card(label, value, sub)
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "") -> None:
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
<div class="sec-header">
  <h3>{title}</h3>
  {sub_html}
</div>""", unsafe_allow_html=True)


def insight_box(text: str) -> None:
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def warning_box(text: str) -> None:
    st.markdown(f'<div class="warning-box">{text}</div>', unsafe_allow_html=True)


def no_data_msg(filename: str) -> None:
    st.warning(
        f"Fichier `{filename}` introuvable dans `data/`. "
        "Lance d'abord `export_for_streamlit.R` depuis R pour générer les données.",
        icon="⚠️",
    )
