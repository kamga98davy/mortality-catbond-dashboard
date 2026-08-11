"""Belgian Mortality CAT Bond Dashboard — Page d'accueil."""
import streamlit as st

from utils.styles import inject_css, kpi_row, insight_box, section_header, warning_box
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="CAT Bond Mortalité · Belgique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
render_sidebar()

# ── CSS spécifique à cette page ────────────────────────────────────────────────
st.markdown("""
<style>
.hero-eyebrow {
    font-size:.7rem;font-weight:700;letter-spacing:.12em;
    text-transform:uppercase;color:#F4A926;margin-bottom:.4rem;
}
.hero-title {
    font-size:2rem;font-weight:700;color:#CCD6F6;
    line-height:1.22;margin-bottom:.55rem;
}
.hero-title span{color:#F4A926;}
.hero-sub{color:#8892B0;font-size:.92rem;line-height:1.6;margin-bottom:1.2rem;max-width:660px;}
.arg-card{background:#112240;border-radius:12px;padding:1.2rem 1.3rem;border-top:3px solid #F4A926;}
.arg-card.teal{border-top-color:#64FFDA;}
.arg-card.blue{border-top-color:#4FC3F7;}
.arg-icon{font-size:1.4rem;margin-bottom:.4rem;}
.arg-title{font-weight:600;color:#CCD6F6;font-size:.9rem;margin-bottom:.3rem;}
.arg-body{color:#8892B0;font-size:.78rem;line-height:1.6;}
.arg-num{font-size:1.2rem;font-weight:700;color:#F4A926;}
.aud-card{background:#112240;border-radius:12px;padding:1.2rem 1.3rem;border:1px solid rgba(255,255,255,.06);}
.aud-badge{font-size:.62rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
           margin-bottom:.5rem;display:inline-block;padding:.12rem .55rem;border-radius:10px;}
.aud-title{font-size:.92rem;font-weight:600;color:#CCD6F6;margin-bottom:.6rem;}
.aud-list{color:#8892B0;font-size:.78rem;line-height:1.8;}
.divider{border-top:1px solid rgba(255,255,255,.07);margin:1.3rem 0;}
.stat-big{font-size:2.3rem;font-weight:700;color:#F4A926;line-height:1;}
.stat-lbl{color:#8892B0;font-size:.7rem;margin-top:.2rem;line-height:1.4;}
.stat-cell{text-align:center;padding:.4rem 0;}
.note{color:#8892B0;font-size:.7rem;font-style:italic;}
/* Tab selector proéminent */
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    font-size:.95rem !important;
    font-weight:600 !important;
    padding:.65rem 1.8rem !important;
    letter-spacing:.02em !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header au-dessus des onglets ───────────────────────────────────────────────
st.markdown('<div class="hero-eyebrow">Mémoire actuariat · UCL · Belgique · 2024</div>',
            unsafe_allow_html=True)
st.markdown("""
<h1 class="hero-title">
  CAT Bond sur la mortalité belge<br>
  <span>post-COVID — Modèle AJD bivarié</span>
</h1>
""", unsafe_allow_html=True)

# ── LES DEUX ONGLETS — pivot principal ────────────────────────────────────────
tab_comm, tab_tech = st.tabs(["👔  Vue Commerciale — Investisseurs & Management",
                               "🔬  Vue Technique — Jury académique"])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET COMMERCIAL
# ══════════════════════════════════════════════════════════════════════════════
with tab_comm:

    st.markdown("""
<p class="hero-sub">
  Ce mémoire calibre un CAT bond sur la mortalité belge — le bond transfère le risque
  de surmortalité catastrophique aux marchés des capitaux.
  Maturité 5,25 ans · Coupon trimestriel · 100 000 simulations Monte Carlo sous mesure Q.
</p>
""", unsafe_allow_html=True)

    kpi_row([
        ("Coupon annuel c*",     "6,0 %",  "Trimestriel · sur 5,25 ans"),
        ("Prob. activation",     "1,16 %", "P(μ* > a_BE) · 1/86"),
        ("Prob. perte totale",   "0,74 %", "P(μ* > b_BE) · 1/135"),
        ("Perte attendue",       "0,92 %", "E[1−PRF] · réf. Atlas IX"),
        ("Ratio coupon / perte", "6,5×",   "6,0 % / 0,92 %"),
    ])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    col_prob, col_sol = st.columns([1, 1], gap="large")

    with col_prob:
        section_header("Pourquoi ce bond existe",
                       "Le COVID-19 a cassé les modèles de tarification du risque de mortalité")
        st.markdown("""
Le GLM Poisson calibré sur 2013–2019 sous-estimait de **plus de 3 000 décès**
les semaines de mars–avril 2020 en Belgique. Ce n'est pas un problème de modèle —
c'est un régime de risque fondamentalement différent.
""")
        for icon, point, detail in [
            ("🔴", "σ₂ quadruplé post-COVID",
             "Volatilité de μₜ : ~0,002 (pré) → ~0,008 (post). Estimations MCMC sur deux fenêtres."),
            ("🔴", "Fréquence des sauts λ en hausse",
             "Chocs simultanés (rₜ, μₜ) — marché + mortalité — plus fréquents après 2020."),
            ("🟡", "Solvency II durcit les exigences SCR-mortalité",
             "Les assureurs belges ont besoin d'instruments calibrés sur le nouveau régime."),
        ]:
            st.markdown(f"""
<div style='display:flex;gap:.7rem;margin:.55rem 0;align-items:flex-start;'>
  <span style='font-size:.9rem;margin-top:.05rem;'>{icon}</span>
  <div>
    <span style='color:#CCD6F6;font-weight:600;font-size:.85rem;'>{point}</span><br>
    <span style='color:#8892B0;font-size:.76rem;'>{detail}</span>
  </div>
</div>""", unsafe_allow_html=True)

    with col_sol:
        section_header("Ce que propose ce travail",
                       "Un cadre quantitatif complet, reproductible, calibré sur la Belgique")
        st.markdown("""
<div class="arg-card" style="margin-bottom:.7rem;">
  <div class="arg-icon">🛡️</div>
  <div class="arg-title">Pour l'assureur (émetteur)</div>
  <div class="arg-body">
    Couverture des scénarios catastrophiques post-pandémiques.<br>
    Capital libéré sous Solvency II — SCR-mortalité réduit.<br>
    Instrument complémentaire à la réassurance traditionnelle.
  </div>
</div>
<div class="arg-card teal">
  <div class="arg-icon">📈</div>
  <div class="arg-title">Pour l'investisseur (acheteur)</div>
  <div class="arg-body">
    6 % annuel non corrélé aux marchés actions et obligataires.<br>
    β ≈ 0 en période normale — diversification réelle du portefeuille.<br>
    Modèle entièrement auditable, zéro boîte noire.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    section_header("Trois raisons concrètes d'investir",
                   "Les chiffres font le travail")
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown("""
<div class="arg-card">
  <div class="arg-icon">💰</div><div class="arg-num">6,5×</div>
  <div class="arg-title">Rendement / risque réel</div>
  <div class="arg-body">6 % de coupon pour 0,92 % de perte attendue.
  Vita Capital IV D-5 (Li et al., 2011–2015) a servi de référence
  pour calibrer le vecteur MPR ζ.</div>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="arg-card teal">
  <div class="arg-icon">📊</div><div class="arg-num">β ≈ 0</div>
  <div class="arg-title">Décorrélation réelle</div>
  <div class="arg-body">La mortalité belge n'a pas de corrélation structurelle avec
  le MSCI Europe. Le seul scénario de corrélation — pandémie + crise financière —
  est modélisé via le saut commun λ.</div>
</div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="arg-card blue">
  <div class="arg-icon">🔬</div><div class="arg-num">100 k</div>
  <div class="arg-title">Trajectoires, pas d'intuition</div>
  <div class="arg-body">100 000 trajectoires Monte Carlo sous mesure Q
  (Algorithme A.5 exact — Pienaar &amp; Varughese, 2016).
  Chaque probabilité vient de la distribution empirique.</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    section_header("Pour qui, concrètement",
                   "Trois profils institutionnels")
    a1, a2, a3 = st.columns(3, gap="large")
    with a1:
        st.markdown("""
<div class="aud-card">
  <div class="aud-badge" style="background:rgba(244,169,38,.12);color:#F4A926;
       border:1px solid rgba(244,169,38,.3);">🏦 Assureurs & Réassureurs</div>
  <div class="aud-title">Transférer le risque de queue</div>
  <div class="aud-list">✅ Couverture pandémie / vague de chaleur<br>
    ✅ SCR-mortalité réduit (Solvency II)<br>
    ✅ Diversification hors réassurance classique<br>
    ✅ Éligibilité IFRS 17</div>
</div>""", unsafe_allow_html=True)
    with a2:
        st.markdown("""
<div class="aud-card">
  <div class="aud-badge" style="background:rgba(100,255,218,.08);color:#64FFDA;
       border:1px solid rgba(100,255,218,.25);">📈 Gestionnaires d'actifs</div>
  <div class="aud-title">Alpha non corrélé</div>
  <div class="aud-list">✅ 6 % sur actif décorrélé des marchés<br>
    ✅ Améliore le ratio Sharpe<br>
    ✅ Éligible ILS<br>
    ✅ Coupon trimestriel</div>
</div>""", unsafe_allow_html=True)
    with a3:
        st.markdown("""
<div class="aud-card">
  <div class="aud-badge" style="background:rgba(79,195,247,.08);color:#4FC3F7;
       border:1px solid rgba(79,195,247,.25);">🏢 Fonds de pension</div>
  <div class="aud-title">Couvrir le risque longevité</div>
  <div class="aud-list">✅ Protection régimes prestations définies<br>
    ✅ Complément aux longevity swaps<br>
    ✅ Outil de diversification ALM<br>
    ✅ Documentation auditée trustees</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    section_header("Ce que les trois scénarios disent",
                   "S1 = référence · S2 = counterfactuel pré-COVID · S3 = seuils obsolètes")
    st.markdown("""
<div class="scenario-row">
  <div class="scenario-card">
    <div class="scenario-title">S1 — Scénario central</div>
    <div class="scenario-price">P₀ = 100</div>
    <div class="scenario-desc">Dynamiques et seuils recalibrés 2017–2022.
    Le spread de 6 % est le prix d'équilibre. Prix d'émission recommandé.</div>
  </div>
  <div class="scenario-card s2">
    <div class="scenario-title">S2 — Monde sans COVID</div>
    <div class="scenario-price s2">P₀ &gt; 100</div>
    <div class="scenario-desc">Calibration pré-COVID : λ et σ₂ plus faibles.
    Le 6 % surcompenserait le risque. Quantifie la valeur du COVID dans le spread.</div>
  </div>
  <div class="scenario-card s3">
    <div class="scenario-title">S3 — Seuils obsolètes</div>
    <div class="scenario-price s3">P₀ = 100*</div>
    <div class="scenario-desc">Seuils pré-COVID + dynamiques post-COVID.
    ζ_S3 ≠ ζ_S1 : les investisseurs prennent plus de risque qu'ils ne croient.</div>
  </div>
</div>""", unsafe_allow_html=True)

    insight_box("""
<b>Message pour le comité de risque :</b> le scénario S3 n'est pas hypothétique.
Tout assureur qui n'a pas recalibré ses seuils depuis 2019 est structurellement en S3.
Le vecteur ζ le détecte — c'est l'un des apports opérationnels de ce travail.
""")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    section_header("Les chiffres qui structurent le modèle")
    cols = st.columns(6)
    for col, (big, lbl, sub) in zip(cols, [
        ("6,0 %",   "Coupon annuel",        "c* trimestriel"),
        ("5,25 ans","Maturité",             "21 paiements Δ=0,25"),
        ("1,16 %",  "Prob. activation",     "Seuil a_BE"),
        ("0,74 %",  "Prob. perte totale",   "Seuil b_BE"),
        ("0,92 %",  "Perte attendue",       "≈ (1,16+0,74)/2"),
        ("13",      "Paramètres sous P",    "Calibrés MCMC MH"),
    ]):
        with col:
            st.markdown(f"""
<div class="stat-cell">
  <div class="stat-big">{big}</div>
  <div class="stat-lbl"><b style="color:#CCD6F6">{lbl}</b><br>{sub}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("""
<p class="note" style="text-align:center;margin-top:1rem;">
⚠️ Support de mémoire de fin d'études — pas un prospectus d'investissement.
Modèle académique · Li et al. (2023, <em>Insurance: Mathematics and Economics</em>, 85, 84–106).
</p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET TECHNIQUE
# ══════════════════════════════════════════════════════════════════════════════
with tab_tech:

    st.markdown("""
<p style='color:#8892B0;font-size:.88rem;margin:.4rem 0 1rem 0;'>
  Reproduction et adaptation belge · Li, Liu, Tang &amp; Yuan (2023,
  <em>Insurance: Mathematics and Economics</em>, 85, 84–106)
</p>""", unsafe_allow_html=True)

    kpi_row([
        ("Attachment P(μ*>a)", "1,16 %", "Seuil a_BE"),
        ("Exhaustion P(μ*>b)", "0,74 %", "Seuil b_BE"),
        ("Perte attendue",     "0,92 %", "E[1−PRF] numérique"),
        ("Coupon c*",          "6,0 %",  "Annuel · Δ=0,25"),
        ("Maturité T",         "5,25 ans","21 paiements"),
        ("Simulations N",      "100 000", "Sous mesure Q"),
    ])

    st.markdown("---")
    section_header("Pipeline méthodologique")
    pipe_cols = st.columns(2, gap="large")
    pipeline = [
        ("Données",      "Mortalité hebdomadaire Statbel 2013–2024 · EURIBOR 3M"),
        ("GLM Poisson",  "Décès attendus E[D_{t,w}] avec harmoniques saisonnières (éq. 4.1)"),
        ("Surmortalité", "μₜ = (D_obs − E[D]) / pop × 100 — résidu standardisé"),
        ("AJD sous P",   "Bivarié (rₜ, μₜ) — 13 paramètres θ — SDE éq. 2.8"),
        ("MCMC MH",      "30 000 itérations · 2 fenêtres : pré-COVID & post-COVID"),
        ("Mesure Q",     "MPR ζ = (γ₁,γ₂;κ₁,κ₂;χ) · changement de mesure éq. 2.11"),
        ("Monte Carlo",  "Algorithme A.5 exact · 100 000 trajectoires · μ* = max μₜ"),
        ("Seuils",       "Inversion P(μ*>a)=1,16% et P(μ*>b)=0,74% → a_BE, b_BE"),
        ("Calibration ζ","Moindres carrés sur 10 spreads Vita Capital IV D-5 (2011–2015)"),
        ("Pricing",      "P₀ = E^Q[coupons + K·PRF_T] actualisés → S1/S2/S3"),
    ]
    for i, (step, desc) in enumerate(pipeline, start=1):
        with pipe_cols[0 if i <= 5 else 1]:
            st.markdown(f"""
<div style='display:flex;gap:.8rem;margin:.3rem 0;align-items:flex-start;'>
  <span style='color:#F4A926;font-weight:700;font-size:.78rem;
              min-width:1.4rem;margin-top:.1rem;'>{i:02d}</span>
  <div>
    <span style='color:#CCD6F6;font-weight:600;font-size:.83rem;'>{step}</span>
    <span style='color:#8892B0;font-size:.76rem;'> — {desc}</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    eq1, eq2 = st.columns(2, gap="large")
    with eq1:
        section_header("Modèle AJD bivarié (éq. 2.8)")
        st.latex(r"""
\begin{cases}
dr_t = (m_1 - d_1\,r_t)\,dt + \sigma_1\,dW_{1,t}
       + d\!\displaystyle\sum_{i=1}^{N_t} X_{1,i}\\[10pt]
d\mu_t = (m_2 - d_2\,\mu_t)\,dt
         + \sigma_2\!\left(\rho_1\,dW_{1,t}
         + \sqrt{1-\rho_1^2}\,dW_{2,t}\right)
         + d\!\displaystyle\sum_{i=1}^{N_t} X_{2,i}
\end{cases}
""")
    with eq2:
        section_header("Formule de pricing (éq. 3.1)")
        st.latex(r"""
P_0 = \mathbb{E}^Q\!\left[
  \sum_{k=1}^{T/\Delta}
    e^{-\int_0^{t_k}\!r_s\,ds}\,c^*\Delta\,\mathrm{PRF}_{t_k}
  + e^{-\int_0^{T}\!r_s\,ds}\,K\,\mathrm{PRF}_T
\right]
""")
        st.latex(r"""
\mathrm{PRF}_{t_k} = 1 -
\frac{(\mu^* - a)_+ - (\mu^* - b)_+}{b - a},\quad
\mu^* = \max_{0\le t\le T}\mu_t
""")

    st.markdown("---")
    section_header("Structure du document")
    page_info = [
        ("📊", "Données",         "GLM Poisson, μₜ, EURIBOR 3M, EDA"),
        ("🔬", "Modèle AJD",      "SDE bivarié, corrélation éq. 2.10, mesure Q"),
        ("⚙️", "Calibration MCMC","MH 30k iter., traces, ESS, Δ pré/post-COVID"),
        ("📈", "Monte Carlo",     "Algorithme A.5, courbe P(μ*>s), seuils"),
        ("💰", "Pricing",         "Vecteur MPR ζ, scénarios S1/S2/S3"),
        ("🎯", "Sensibilité",     "Impact ±20% de ζ sur P₀ — élasticité χ"),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(page_info):
        with cols[i % 3]:
            st.markdown(f"""
<div style='background:#112240;border-radius:8px;padding:.8rem 1rem;
            margin:.3rem 0;border-left:3px solid #F4A926;'>
  <b style='color:#CCD6F6;font-size:.86rem;'>{icon} {title}</b><br>
  <span style='color:#8892B0;font-size:.74rem;'>{desc}</span>
</div>""", unsafe_allow_html=True)
