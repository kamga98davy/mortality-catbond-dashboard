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
#MainMenu, footer, header {visibility: hidden;}

.main .block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1400px;
}

/* ── KPI cards ── */
.kpi-grid {display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;}
.kpi-card {
    flex: 1; min-width: 160px;
    background: #112240;
    border: 1px solid rgba(244,169,38,.25);
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    text-align: center;
}
.kpi-label {
    color: #8892B0; font-size: .72rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem;
}
.kpi-value {color: #F4A926; font-size: 2rem; font-weight: 700; line-height: 1.1;}
.kpi-sub   {color: #8892B0; font-size: .7rem; margin-top: .2rem;}

/* ── Section divider ── */
.sec-header {
    border-left: 3px solid #F4A926;
    padding-left: .9rem; margin: 1.6rem 0 .8rem 0;
}
.sec-header h3 {margin: 0; color: #CCD6F6; font-weight: 500;}

/* ── Info / Insight boxes ── */
.insight-box {
    background: rgba(100,255,218,.05);
    border: 1px solid rgba(100,255,218,.2);
    border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;
}
.warning-box {
    background: rgba(244,169,38,.07);
    border: 1px solid rgba(244,169,38,.25);
    border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;
}

/* ── Scenario cards ── */
.scenario-row {display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;}
.scenario-card {
    flex: 1; min-width: 180px;
    background: #112240;
    border-radius: 12px;
    padding: 1.2rem;
    border-top: 3px solid #F4A926;
}
.scenario-card.s2 {border-top-color: #64FFDA;}
.scenario-card.s3 {border-top-color: #FF6B6B;}
.scenario-title {font-weight: 600; margin-bottom: .4rem; color: #CCD6F6;}
.scenario-price {font-size: 1.8rem; font-weight: 700; color: #F4A926; line-height: 1.1;}
.scenario-price.s2 {color: #64FFDA;}
.scenario-price.s3 {color: #FF6B6B;}
.scenario-desc  {color: #8892B0; font-size: .78rem; margin-top: .4rem; line-height: 1.4;}

/* ── Mode badge ── */
.badge-exec {
    display: inline-block; padding: .2rem .7rem; border-radius: 20px;
    font-size: .7rem; font-weight: 600; letter-spacing: .05em;
    background: rgba(100,255,218,.1); color: #64FFDA;
    border: 1px solid rgba(100,255,218,.3);
}
.badge-tech {
    display: inline-block; padding: .2rem .7rem; border-radius: 20px;
    font-size: .7rem; font-weight: 600; letter-spacing: .05em;
    background: rgba(244,169,38,.1); color: #F4A926;
    border: 1px solid rgba(244,169,38,.3);
}

/* ── Streamlit element tweaks ── */
div[data-testid="stMetric"] {
    background: #112240;
    border-radius: 10px;
    padding: .8rem 1rem;
    border: 1px solid rgba(244,169,38,.15);
}
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size: .85rem;
}
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
    sub_html = f"<p style='margin:.2rem 0 0 0; color:#8892B0; font-size:.85rem;'>{subtitle}</p>" if subtitle else ""
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
        icon="⚠️"
    )
