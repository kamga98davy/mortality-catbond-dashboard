"""Belgian Mortality CAT Bond Dashboard — Accueil / Pitch investisseur."""
import streamlit as st

from utils.styles import inject_css, kpi_row, insight_box, section_header, warning_box

st.set_page_config(
    page_title="Belgian Mortality CAT Bond",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Extra CSS pour cette page ──────────────────────────────────────────────────
st.markdown("""
<style>
.hero-title {
    font-size: 2.4rem; font-weight: 700; color: #CCD6F6;
    line-height: 1.2; margin: .5rem 0 .4rem 0;
}
.hero-sub {
    font-size: 1.05rem; color: #8892B0; margin-bottom: 1.4rem; line-height: 1.5;
}
.pill {
    display: inline-block; background: rgba(244,169,38,.12);
    color: #F4A926; border: 1px solid rgba(244,169,38,.35);
    border-radius: 20px; padding: .2rem .75rem;
    font-size: .72rem; font-weight: 600; letter-spacing: .06em;
    margin-bottom: .6rem;
}
.arg-card {
    background: #112240; border-radius: 12px;
    padding: 1.2rem 1.3rem; height: 100%;
    border-top: 3px solid #F4A926;
    transition: border-color .2s;
}
.arg-card.teal  { border-top-color: #64FFDA; }
.arg-card.blue  { border-top-color: #4FC3F7; }
.arg-card.red   { border-top-color: #FF6B6B; }
.arg-card.purple{ border-top-color: #A78BFA; }
.arg-icon { font-size: 1.6rem; margin-bottom: .5rem; }
.arg-title { font-weight: 600; color: #CCD6F6; font-size: .95rem; margin-bottom: .35rem; }
.arg-body  { color: #8892B0; font-size: .8rem; line-height: 1.55; }
.audience-card {
    background: #112240; border-radius: 12px; padding: 1.4rem;
    border: 1px solid rgba(255,255,255,.06);
}
.aud-title { font-size: 1rem; font-weight: 600; color: #CCD6F6; margin-bottom: .6rem; }
.aud-tag   { font-size: .7rem; font-weight: 600; letter-spacing: .07em;
             text-transform: uppercase; margin-bottom: .8rem; }
.aud-list  { color: #8892B0; font-size: .82rem; line-height: 1.7; }
.divider   { border-top: 1px solid rgba(255,255,255,.07); margin: 1.5rem 0; }
.stat-big  { font-size: 2.8rem; font-weight: 700; color: #F4A926; line-height: 1; }
.stat-lbl  { color: #8892B0; font-size: .78rem; margin-top: .2rem; }
.stat-cell { text-align: center; padding: .5rem 1rem; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state["view"] = "Executive"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style='text-align:center; padding:.8rem 0 1rem 0;'>
  <span style='font-size:2.2rem;'>📊</span><br>
  <span style='color:#F4A926; font-weight:700; font-size:1.1rem; letter-spacing:.02em;'>
    CAT Bond Mortalité
  </span><br>
  <span style='color:#8892B0; font-size:.72rem;'>Belgique · Post-COVID · 2024</span>
</div>""", unsafe_allow_html=True)

    view = st.radio(
        "Perspective",
        ["👔 Commercial", "🔬 Technique"],
        index=0 if st.session_state["view"] == "Executive" else 1,
        label_visibility="collapsed",
    )
    st.session_state["view"] = "Executive" if view.startswith("👔") else "Technique"

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
<div style='color:#8892B0; font-size:.73rem; line-height:1.7;'>
  <b style='color:#CCD6F6;'>Pages disponibles</b><br>
  📊 Données<br>
  🔬 Modèle AJD<br>
  ⚙️ Calibration MCMC<br>
  📈 Simulation Monte Carlo<br>
  💰 Pricing & Scénarios<br>
  🎯 Sensibilité MPR
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
<div style='color:#8892B0; font-size:.68rem; line-height:1.6;'>
  🎓 Mémoire fin d'études<br>
  Modèle : AJD bivarié<br>
  Réf. : Li et al. (2023, IME)<br>
  Données : Statbel 2013–2024
</div>""", unsafe_allow_html=True)

IS_EXEC = st.session_state["view"] == "Executive"

# ══════════════════════════════════════════════════════════════════════════════
# COMMERCIAL / EXECUTIVE VIEW
# ══════════════════════════════════════════════════════════════════════════════
if IS_EXEC:

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="pill">ÉTUDE D\'INVESTISSEMENT · BELGIQUE · 2024</div>',
                unsafe_allow_html=True)
    st.markdown("""
<h1 class="hero-title">
  Tarifier le risque de mortalité extrême<br>
  <span style="color:#F4A926;">dans un monde post-pandémique</span>
</h1>
<p class="hero-sub">
  Un CAT bond sur la mortalité belge, calibré sur les données 2013–2024 et le
  modèle de référence de Li, Liu, Tang &amp; Yuan (2023).
  Rendement 6 % · Maturité 5,25 ans · Modèle AJD bivarié · MCMC Bayésien.
</p>
""", unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    kpi_row([
        ("Coupon annuel (spread)", "6.0 %",  "c* = 6% sur 5,25 ans"),
        ("Prob. d'activation",    "1.16 %", "P(μ* > a_BE) · Événement rare"),
        ("Prob. perte totale",    "0.74 %", "P(μ* > b_BE) · Catastrophe"),
        ("Perte attendue",        "0.92 %", "E[1-PRF] · Analogue Atlas IX"),
        ("Ratio rendement / perte", "6.5×", "6% / 0.92% · Prima facie attractif"),
    ])

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Le problème ───────────────────────────────────────────────────────────
    col_prob, col_sol = st.columns([1, 1], gap="large")

    with col_prob:
        section_header("Le problème", "Pourquoi le risque de mortalité n'est plus gérable comme avant")
        st.markdown("""
La **pandémie COVID-19** a brisé les hypothèses sur lesquelles reposent les
modèles de mortalité traditionnels des assureurs.

**Ce qui a changé :**
""")
        changes = [
            ("🔴", "Fréquence des chocs", "Des événements à 1-sur-100-ans se sont produits 3 années consécutives"),
            ("🔴", "Amplitude des chocs", "Pics de mortalité 3× supérieurs à la normale en Belgique"),
            ("🔴", "Corrélation inattendue", "La mortalité et les marchés financiers ont chuté simultanément"),
            ("🟡", "Exigences réglementaires", "Solvency II SCR-mortalité en hausse, besoin de couverture accru"),
            ("🟡", "Incertitude résiduelle", "COVID long, variants futurs : la queue de distribution s'est élargie"),
        ]
        for icon, title, desc in changes:
            st.markdown(f"""
<div style='display:flex; gap:.8rem; margin:.5rem 0; align-items:flex-start;'>
  <span style='font-size:1rem; margin-top:.1rem;'>{icon}</span>
  <div>
    <span style='color:#CCD6F6; font-weight:600; font-size:.88rem;'>{title}</span><br>
    <span style='color:#8892B0; font-size:.8rem;'>{desc}</span>
  </div>
</div>""", unsafe_allow_html=True)

    with col_sol:
        section_header("La solution", "Un instrument de transfert de risque innovant et quantifié")
        st.markdown("""
Le **CAT bond sur la mortalité** permet à un assureur de transférer son
risque de surmortalité catastrophique au marché des capitaux.
""")
        st.markdown("""
<div class="arg-card" style="margin-bottom:.8rem;">
  <div class="arg-icon">🛡️</div>
  <div class="arg-title">Pour l'assureur (émetteur)</div>
  <div class="arg-body">
    → Couverture des scénarios catastrophiques (pandemic, guerre, vague de chaleur)<br>
    → Capital libéré sous Solvency II (SCR-mortalité réduit)<br>
    → Diversification des sources de financement du risque
  </div>
</div>
<div class="arg-card teal">
  <div class="arg-icon">📈</div>
  <div class="arg-title">Pour l'investisseur (acheteur)</div>
  <div class="arg-body">
    → Rendement de 6 % non corrélé aux marchés financiers<br>
    → Actif décorrélé (β ≈ 0 vs actions, obligations)<br>
    → Transparence totale du modèle de risque
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Arguments investisseur ─────────────────────────────────────────────────
    section_header("5 raisons d'investir", "Arguments quantitatifs et stratégiques")

    c1, c2, c3, c4, c5 = st.columns(5)
    args = [
        ("c1", "#F4A926", "💰", "Rendement attractif",
         "6 % annuel sur 5,25 ans. Dans un contexte de taux revenants à la normale, une prime de 6 % sur risque non-financier est rare."),
        ("c2", "#64FFDA", "📊", "Décorrélation totale",
         "β ≈ 0 aux marchés actions et obligataires en période normale. La pandémie est le seul risque de corrélation — et il est désormais modélisé."),
        ("c3", "#4FC3F7", "🔬", "Modèle transparent",
         "AJD bivarié calibré MCMC, 100 000 simulations Monte Carlo. Chaque chiffre est auditable. Zéro boîte noire."),
        ("c4", "#A78BFA", "⏱️", "Fenêtre post-COVID",
         "Le marché vient de recalibrer le risque. Le spread de 6 % reflète le nouveau régime — ni sur-ni sous-estimé."),
        ("c5", "#FF6B6B", "🏛️", "Éligibilité Solvency II",
         "Structure conforme aux normes ICS et Solvency II. Les assureurs-acheteurs bénéficient d'un traitement SCR favorable."),
    ]
    cols_ref = [c1, c2, c3, c4, c5]
    css_cls  = ["", "teal", "blue", "purple", "red"]
    for col, (_, color, icon, title, body), cls in zip(cols_ref, args, css_cls):
        with col:
            st.markdown(f"""
<div class="arg-card {cls}" style="border-top-color:{color};">
  <div class="arg-icon">{icon}</div>
  <div class="arg-title">{title}</div>
  <div class="arg-body">{body}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Pour qui ──────────────────────────────────────────────────────────────
    section_header("Pour qui ?", "Trois profils d'investisseurs institutionnels")

    a1, a2, a3 = st.columns(3, gap="large")

    with a1:
        st.markdown("""
<div class="audience-card">
  <div class="aud-tag" style="color:#F4A926;">🏦 Assureurs & Réassureurs</div>
  <div class="aud-title">Transfert de risque réglementaire</div>
  <div class="aud-list">
    ✅ Couverture du risque de pandémie<br>
    ✅ Réduction du SCR-mortalité (Solvency II)<br>
    ✅ Diversification hors réassurance traditionnelle<br>
    ✅ Comptabilisation hors-bilan sous IFRS 17<br>
    ✅ Instrument éprouvé : marché des cat bonds de mortalité >
       $3 Mds depuis 2003
  </div>
</div>""", unsafe_allow_html=True)

    with a2:
        st.markdown("""
<div class="audience-card">
  <div class="aud-tag" style="color:#64FFDA;">📈 Gestionnaires d'actifs & Fonds</div>
  <div class="aud-title">Alpha non corrélé</div>
  <div class="aud-list">
    ✅ Rendement 6 % sur actif décorrélé des marchés<br>
    ✅ Diversification de portefeuille (Sharpe amélioré)<br>
    ✅ Duration 5,25 ans — horizon intermédiaire<br>
    ✅ Éligible en portefeuilles ILS (Insurance-Linked Securities)<br>
    ✅ Coupon trimestriel en espèces (liquidité partielle)
  </div>
</div>""", unsafe_allow_html=True)

    with a3:
        st.markdown("""
<div class="audience-card">
  <div class="aud-tag" style="color:#4FC3F7;">🏢 Entreprises & Fonds de pension</div>
  <div class="aud-title">Protection des engagements longs</div>
  <div class="aud-list">
    ✅ Couverture du risque de mortalité des retraités<br>
    ✅ Protection des régimes de pension à prestations définies<br>
    ✅ Complément aux contrats longevity swap<br>
    ✅ Instrument de diversification pour un comité ALM<br>
    ✅ Documentation de risque complète pour les trustees
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Chiffres clés ─────────────────────────────────────────────────────────
    section_header("Les chiffres qui comptent", "Résultats du modèle AJD calibré sur la Belgique")

    cols = st.columns(6)
    stats = [
        ("1.16 %", "Probabilité d'activation", "1 chance sur 86"),
        ("0.74 %", "Probabilité de perte totale", "1 chance sur 135"),
        ("0.92 %", "Perte attendue annualisée", "Historiquement faible"),
        ("6.0 %", "Coupon annuel", "Prime / perte = 6,5×"),
        ("100 k", "Trajectoires simulées", "Monte Carlo sous Q"),
        ("13", "Paramètres MCMC", "Modèle AJD bivarié"),
    ]
    for col, (big, lbl, sub) in zip(cols, stats):
        with col:
            st.markdown(f"""
<div class="stat-cell">
  <div class="stat-big">{big}</div>
  <div class="stat-lbl"><b style="color:#CCD6F6;">{lbl}</b><br>{sub}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Scénarios ─────────────────────────────────────────────────────────────
    section_header("Analyse de scénarios", "Impact du contexte pandémique sur la valeur du bond")
    st.markdown("""
<div class="scenario-row">
  <div class="scenario-card">
    <div class="scenario-title">S1 · Scénario central (post-COVID)</div>
    <div class="scenario-price">P₀ = 100</div>
    <div class="scenario-desc">
      <b>Dynamiques et seuils recalibrés sur 2017–2022.</b><br>
      Le spread de 6 % est <em>juste</em> : l'investisseur est correctement
      rémunéré pour le risque pandémique actuel. Prix d'émission recommandé.
    </div>
  </div>
  <div class="scenario-card s2">
    <div class="scenario-title">S2 · Counterfactuel (pré-COVID)</div>
    <div class="scenario-price s2">P₀ &gt; 100</div>
    <div class="scenario-desc">
      <b>Si la pandémie n'avait pas eu lieu</b>, le risque modélisé serait
      inférieur → le bond se négocierait au-dessus du pair. Le 6 % serait
      <em>généreux</em> dans ce monde. Delta = valeur de la pandémie.
    </div>
  </div>
  <div class="scenario-card s3">
    <div class="scenario-title">S3 · Désalignement (risque sous-estimé)</div>
    <div class="scenario-price s3">P₀ = 100*</div>
    <div class="scenario-desc">
      <b>Seuils pré-COVID avec dynamiques post-COVID :</b> l'émetteur
      utilise des paramètres obsolètes. Le vecteur ζ_S3 ≠ ζ_S1 révèle un
      désalignement — le risque réel est sous-facturé à l'investisseur.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    insight_box("""
<b>📌 Message pour le comité d'investissement</b><br>
Le modèle montre que la pandémie a durablement augmenté la probabilité d'activation
(pré-COVID : inférieure à 1,16 %). Un bond émis aujourd'hui avec un spread de <b>6 %</b>
et des seuils recalibrés sur les données 2017–2022 offre un <b>rapport rendement/risque
de 6,5×</b> — comparable aux meilleures émissions de cat bonds de mortalité observées
sur le marché ILS (Swiss Re Mortality Pool, Vita Capital IV).
""")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
<p style='color:#8892B0; font-size:.68rem; line-height:1.6; text-align:center;'>
⚠️ <b>Avertissement académique :</b> Ce tableau de bord est un support de mémoire de fin d'études.
Il ne constitue pas un prospectus d'investissement, une offre de souscription ou un conseil financier.
Les résultats sont basés sur un modèle académique (Li et al., 2023) adapté au contexte belge.
Toute décision d'investissement doit être précédée d'une due diligence complète.
</p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TECHNICAL VIEW
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.markdown('<span class="badge-tech">Technique</span>', unsafe_allow_html=True)
    st.markdown("""
<h2 style='margin:.3rem 0 .2rem 0; color:#CCD6F6;'>
  Pricing Extreme Mortality Risk in the Wake of the COVID-19 Pandemic
</h2>
<p style='color:#8892B0; font-size:.9rem;'>
  Reproduction et adaptation de Li, Liu, Tang &amp; Yuan (2023, <em>Insurance: Mathematics and Economics</em>, 85, 84–106)
</p>
""", unsafe_allow_html=True)

    kpi_row([
        ("Prob. attachment", "1.16%", "P(μ* > a_BE)"),
        ("Prob. exhaustion", "0.74%", "P(μ* > b_BE)"),
        ("Perte attendue",   "0.92%", "≈ (1.16+0.74)/2"),
        ("Coupon c*",        "6.0%",  "Annuel, trimestriel"),
        ("Maturité T",       "5.25 ans", "Δ = 0.25"),
    ])

    st.markdown("---")

    col1, col2 = st.columns([3, 2], gap="large")
    with col1:
        section_header("Méthodologie")
        st.markdown("""
1. **Données** : mortalité hebdomadaire belge (Statbel, 2013–2024), EURIBOR 3M
2. **Surmortalité** : GLM Poisson saisonnier → résidu $\\mu_t$ (éq. 4.1)
3. **Modèle** : AJD bivarié $(r_t, \\mu_t)$ — éq. (2.8), 13 paramètres
4. **Calibration** : MCMC Metropolis-Hastings (30 000 iter.) — 2 fenêtres : pré/post-COVID
5. **Mesure Q** : changement de mesure via MPR $\\zeta = (\\gamma_1, \\gamma_2; \\kappa_1, \\kappa_2; \\chi)$
6. **Simulation** : Algorithme A.5 exact, 100 000 trajectoires → courbe d'exceedance → seuils $a^{BE}$, $b^{BE}$
7. **Calibration MPR** : moindres carrés sur 10 spreads Vita Capital IV D-5 (2011–2015)
8. **Scénarios** : S1 (post-COVID), S2 (pré-COVID), S3 (désalignement)
""")

    with col2:
        section_header("Équation principale (2.8)")
        st.latex(r"""
\begin{cases}
dr_t = (m_1 - d_1 r_t)\,dt + \sigma_1\,dW_{1,t} + d\!\sum X_{1,i}\\[6pt]
d\mu_t = (m_2 - d_2\mu_t)\,dt + \sigma_2(\rho_1 dW_{1,t}\\
\quad + \sqrt{1-\rho_1^2}\,dW_{2,t}) + d\!\sum X_{2,i}
\end{cases}
""")
        section_header("Formule de pricing (3.1)")
        st.latex(r"""
P_0 = \mathbb{E}^Q\!\left[\sum_k e^{-\int_0^{t_k}r_s ds}
c^*\!\Delta\,\text{PRF}_{t_k} + e^{-\int_0^T r_s ds} K\,\text{PRF}_T\right]
""")

    st.markdown("---")
    section_header("Structure du document")
    cols = st.columns(3)
    pages_info = [
        ("📊 Données", "Mortalité belge, GLM Poisson, surmortalité μₜ, EURIBOR"),
        ("🔬 Modèle AJD", "Spécification SDE, mesure Q, paramétrage"),
        ("⚙️ Calibration MCMC", "Résultats MH, ESS, comparaison pré/post-COVID"),
        ("📈 Monte Carlo", "Courbe d'exceedance, seuils a_BE et b_BE"),
        ("💰 Pricing", "Vecteur MPR ζ, scénarios S1/S2/S3"),
        ("🎯 Sensibilité", "Impact de ζ sur le prix P₀ (±20%)"),
    ]
    for i, (title, desc) in enumerate(pages_info):
        with cols[i % 3]:
            st.markdown(f"""
<div style='background:#112240; border-radius:8px; padding:.9rem; margin:.4rem 0;
            border-left:3px solid #F4A926;'>
  <b style='color:#CCD6F6;'>{title}</b><br>
  <span style='color:#8892B0; font-size:.78rem;'>{desc}</span>
</div>""", unsafe_allow_html=True)
