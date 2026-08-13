"""Belgian Mortality CAT Bond Dashboard."""
import streamlit as st

from utils.styles import inject_css, kpi_row, insight_box, section_header, warning_box
from utils.sidebar import render_sidebar
from utils.icons import icon

st.set_page_config(
    page_title="CAT Bond Mortalite · Belgique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
render_sidebar()

# ── Styles specifiques a cette page ──────────────────────────────────────────
st.markdown("""
<style>
.page-label {
    font-size:.67rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
    color:#D97706;margin-bottom:.5rem;
}
.page-title {
    font-size:1.85rem;font-weight:700;color:#E5E7EB;line-height:1.25;margin-bottom:.4rem;
}
.page-title em { color:#D97706; font-style:normal; }
.problem-block {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-left:3px solid #EF4444;border-radius:6px;
    padding:1.1rem 1.3rem;margin:.4rem 0;
}
.solution-block {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-left:3px solid #22C55E;border-radius:6px;
    padding:1.1rem 1.3rem;margin:.4rem 0;
}
.result-block {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-left:3px solid #D97706;border-radius:6px;
    padding:1.1rem 1.3rem;margin:.4rem 0;
}
.block-eyebrow {
    font-size:.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
    margin-bottom:.4rem;
}
.block-title { font-size:.95rem;font-weight:600;color:#E5E7EB;margin-bottom:.4rem; }
.block-body  { color:#9CA3AF;font-size:.83rem;line-height:1.7; }
.audience-card {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-radius:8px;padding:1rem 1.1rem;
}
.audience-title { font-weight:600;color:#E5E7EB;font-size:.88rem;margin:.35rem 0 .4rem 0; }
.audience-list  { color:#9CA3AF;font-size:.77rem;line-height:1.8; }
.nav-card {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-radius:8px;padding:.9rem 1.1rem;
    display:flex;align-items:flex-start;gap:.8rem;
}
.nav-card-icon { flex-shrink:0;margin-top:.1rem; }
.nav-card-title { font-weight:600;color:#E5E7EB;font-size:.84rem;margin-bottom:.15rem; }
.nav-card-desc  { color:#6B7280;font-size:.75rem;line-height:1.5; }
.scenario-indicator {
    display:flex;align-items:center;gap:.6rem;
    padding:.7rem 1rem;background:#1A1D27;
    border:1px solid rgba(255,255,255,.07);border-radius:6px;margin:.3rem 0;
}
.si-dot { width:8px;height:8px;border-radius:50%;flex-shrink:0; }
.si-name { font-size:.82rem;font-weight:600;color:#E5E7EB; }
.si-desc { font-size:.74rem;color:#6B7280; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-label">Memoire de fin d\'etudes · Actuariat · UCL · 2024</div>',
            unsafe_allow_html=True)
st.markdown("""
<h1 class="page-title">
  Tarification du risque de surmortalite catastrophique<br>
  <em>Application a la Belgique post-COVID</em>
</h1>
""", unsafe_allow_html=True)

tab_comm, tab_tech = st.tabs([
    "  Vue Commerciale — Investisseurs et Management  ",
    "  Vue Technique — Jury academique  ",
])

# ══════════════════════════════════════════════════════════════════════════════
# VUE COMMERCIALE
# ══════════════════════════════════════════════════════════════════════════════
with tab_comm:

    # ── 1. La problematique ────────────────────────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    section_header("La problematique")

    col_prob, col_sol, col_res = st.columns(3, gap="large")

    with col_prob:
        st.markdown(f"""
<div class="problem-block">
  <div class="block-eyebrow" style="color:#EF4444">
    {icon("alert-triangle", 13, "#EF4444")} Le constat
  </div>
  <div class="block-title">Un choc que les modeles n'avaient pas prevu</div>
  <div class="block-body">
    En 2020, la Belgique a enregistre plus de <strong style='color:#E5E7EB'>16 000 deces
    au-dessus des previsions</strong> actuarielles standard. Les modeles classiques
    etaient calibres sur un regime de risque qui n'existait plus.
    Pour les assureurs, cela s'est traduit par des sinistres imprevisibles et
    du capital SCR supplementaire sous Solvency II.
  </div>
</div>
""", unsafe_allow_html=True)

    with col_sol:
        st.markdown(f"""
<div class="solution-block">
  <div class="block-eyebrow" style="color:#22C55E">
    {icon("zap", 13, "#22C55E")} L'approche
  </div>
  <div class="block-title">Un instrument financier pour transferer ce risque</div>
  <div class="block-body">
    Ce memoire calibre un <strong style='color:#E5E7EB'>CAT bond sur la mortalite belge</strong>
    — un instrument qui transfère le risque de surmortalite catastrophique
    aux marches des capitaux. Le modele AJD bivariate (Li et al., 2023)
    capture simultanement le risque de mortalite et le risque de taux,
    avec leur correlation en periode de crise.
  </div>
</div>
""", unsafe_allow_html=True)

    with col_res:
        st.markdown(f"""
<div class="result-block">
  <div class="block-eyebrow" style="color:#D97706">
    {icon("check-circle", 13, "#D97706")} Le resultat
  </div>
  <div class="block-title">Un prix d'equilibre quantifie rigoureusement</div>
  <div class="block-body">
    Un bond de maturite <strong style='color:#E5E7EB'>5,25 ans</strong>, coupon trimestriel de
    <strong style='color:#E5E7EB'>6%/an</strong>, calibre sur les donnees belges 2013-2022.
    La probabilite de perte totale est de <strong style='color:#E5E7EB'>0,74%</strong>.
    Le coupon represente <strong style='color:#E5E7EB'>6,5 fois la perte attendue</strong>,
    comparable aux references du marche ILS.
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── 2. Ce que ce dashboard presente ───────────────────────────────────────
    section_header("Ce que ce tableau de bord presente",
                   "Quatre etapes, du recueil des donnees au prix du bond")

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    for col, ico, num, title, desc in [
        (c1, "database",  "01", "Donnees",
         "Mortalite hebdomadaire Statbel 2013-2024 et EURIBOR 3M. "
         "Le modele GLM Poisson calcule les deces attendus chaque semaine "
         "et en deduit la surmortalite residuelle."),
        (c2, "cpu",       "02", "Modele AJD",
         "Le modele AJD bivariate decrit comment le taux d'interet et "
         "la surmortalite evoluent conjointement, avec des sauts soudains "
         "qui capturent les chocs type COVID."),
        (c3, "activity",  "03", "Calibration",
         "Les 13 parametres du modele sont estimes par MCMC "
         "Metropolis-Hastings sur deux periodes distinctes : "
         "avant et apres la pandemie."),
        (c4, "target",    "04", "Pricing",
         "100 000 trajectoires Monte Carlo sous la mesure risque-neutre Q "
         "donnent le prix du bond et les probabilites d'activation "
         "pour trois scenarios de risque."),
    ]:
        with col:
            st.markdown(f"""
<div class="nav-card">
  <div class="nav-card-icon">{icon(ico, 18, "#D97706")}</div>
  <div>
    <div style='font-size:.6rem;color:#6B7280;font-weight:600;
                text-transform:uppercase;letter-spacing:.08em;margin-bottom:.1rem;'>
      Etape {num}
    </div>
    <div class="nav-card-title">{title}</div>
    <div class="nav-card-desc">{desc}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── 3. Les resultats cles ──────────────────────────────────────────────────
    section_header("Les resultats cles")

    col_kpi, col_scen = st.columns([2, 1], gap="large")

    with col_kpi:
        kpi_row([
            ("Coupon annuel", "6,0%",   "Trimestriel · 5,25 ans"),
            ("Prob. activation", "1,16%", "P(surmortalite > seuil bas)"),
            ("Prob. perte totale", "0,74%", "P(surmortalite > seuil haut)"),
            ("Perte attendue", "0,92%",  "E[1 - PRF] par Monte Carlo"),
            ("Ratio coupon / perte", "6,5x", "6,0% divise par 0,92%"),
        ])
        insight_box("""
<strong>Comment lire ces chiffres ?</strong><br>
Le coupon de 6% est la remuneration versee chaque trimestre a l'investisseur.
La perte attendue de 0,92% represente ce que l'investisseur risque statistiquement de perdre en capital.
Le ratio 6,5x signifie que la remuneration est 6,5 fois superieure au risque statistique — c'est le prix
d'equilibre entre ce que l'investisseur demande et ce que l'assureur accepte de payer.
""")

    with col_scen:
        section_header("Trois scenarios testes")
        for dot_col, s_name, s_desc in [
            ("#D97706", "S1 — Reference",
             "Post-COVID + seuils post-COVID. Prix au pair."),
            ("#0D9488", "S2 — Sans COVID",
             "Pre-COVID + seuils pre-COVID. Coupon trop genereux pour le risque reel."),
            ("#EF4444", "S3 — Desalignement",
             "Post-COVID + seuils obsoletes. Risque sous-estime par l'emetteur."),
        ]:
            st.markdown(f"""
<div class="scenario-indicator">
  <div class="si-dot" style="background:{dot_col}"></div>
  <div>
    <div class="si-name">{s_name}</div>
    <div class="si-desc">{s_desc}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── 4. Pour qui ────────────────────────────────────────────────────────────
    section_header("A qui s'adresse ce travail")

    a1, a2, a3 = st.columns(3, gap="large")
    for col, ico, tag_cls, label, title, items in [
        (a1, "landmark", "",      "Assureurs et Reassureurs",
         "Transferer le risque de queue",
         ["Couverture des scenarios de surmortalite catastrophique",
          "Capital SCR libere sous Solvency II",
          "Complement a la reassurance traditionnelle"]),
        (a2, "trending-up", "teal", "Gestionnaires d'actifs",
         "Alpha non correle aux marches",
         ["6% annuel sur un actif decorele du MSCI Europe",
          "Beta proche de zero en periode normale",
          "Eligible ILS, coupon trimestriel"]),
        (a3, "users",    "blue", "Fonds de pension",
         "Couvrir le risque longevite",
         ["Protection des regimes a prestations definies",
          "Complement aux longevity swaps",
          "Outil de diversification ALM"]),
    ]:
        with col:
            st.markdown(f"""
<div class="audience-card">
  {icon(ico, 20, "#D97706" if tag_cls=="" else ("#0D9488" if tag_cls=="teal" else "#3B82F6"))}
  <div class="audience-title">{title}</div>
  <div style='font-size:.64rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
              color:#6B7280;margin-bottom:.5rem;'>{label}</div>
  <div class="audience-list">{'<br>'.join("· " + i for i in items)}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<p style='color:#4B5563;font-size:.69rem;text-align:center;margin-top:1.2rem;'>
Support de memoire academique — pas un prospectus d'investissement.
Modele de reference : Li, Liu, Tang & Yuan (2023, Insurance: Mathematics and Economics, 85, 84-106).
</p>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# VUE TECHNIQUE
# ══════════════════════════════════════════════════════════════════════════════
with tab_tech:

    st.markdown("""
<p style='color:#6B7280;font-size:.85rem;margin:.3rem 0 1rem 0;'>
  Reproduction et adaptation belge — Li, Liu, Tang &amp; Yuan (2023,
  <em>Insurance: Mathematics and Economics</em>, 85, 84-106)
</p>""", unsafe_allow_html=True)

    kpi_row([
        ("Attachment P(mu*>a)", "1,16%", "Seuil a_BE"),
        ("Exhaustion P(mu*>b)", "0,74%", "Seuil b_BE"),
        ("Perte attendue",      "0,92%", "E[1-PRF] numerique"),
        ("Coupon c*",           "6,0%",  "Annuel, Delta=0,25"),
        ("Maturite T",          "5,25 ans", "21 paiements"),
        ("Simulations N",       "100 000",  "Sous mesure Q"),
    ])

    st.markdown("---")
    section_header("Pipeline methodologique",
                   "10 etapes de l'acquisition des donnees au prix du bond")

    pipe_cols = st.columns(2, gap="large")
    pipeline = [
        ("Donnees",      "Mortalite hebdomadaire Statbel 2013-2024, EURIBOR 3M"),
        ("GLM Poisson",  "Deces attendus E[D_{t,w}], harmoniques saisonnieres (eq. 4.1)"),
        ("Surmortalite", "mu_t = (D_obs - E[D]) / pop * 100 — residu standardise"),
        ("AJD sous P",   "Bivariate (r_t, mu_t), 13 parametres theta, SDE eq. 2.8"),
        ("MCMC MH",      "30 000 iterations, deux periodes : pre-COVID et post-COVID"),
        ("Mesure Q",     "MPR zeta = (gamma1, gamma2; kappa1, kappa2; chi), eq. 2.11"),
        ("Monte Carlo",  "Algorithme A.5 exact, 100 000 trajectoires, mu* = max mu_t"),
        ("Seuils",       "Inversion P(mu*>a)=1,16% et P(mu*>b)=0,74% -> a_BE, b_BE"),
        ("Calibration",  "Moindres carres sur 10 spreads Vita Capital IV D-5 (2011-2015)"),
        ("Pricing",      "P0 = E^Q[coupons + K*PRF_T] actualises, scenarios S1/S2/S3"),
    ]
    for i, (step, desc) in enumerate(pipeline, start=1):
        with pipe_cols[0 if i <= 5 else 1]:
            st.markdown(f"""
<div style='display:flex;gap:.7rem;margin:.25rem 0;align-items:flex-start;'>
  <span style='color:#D97706;font-weight:700;font-size:.75rem;
              min-width:1.4rem;margin-top:.08rem;'>{i:02d}</span>
  <div>
    <span style='color:#E5E7EB;font-weight:600;font-size:.81rem;'>{step}</span>
    <span style='color:#6B7280;font-size:.75rem;'> — {desc}</span>
  </div>
</div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    eq1, eq2 = st.columns(2, gap="large")
    with eq1:
        section_header("Modele AJD bivariate (eq. 2.8)")
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
        section_header("Formule de pricing (eq. 3.1)")
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
        ("bar-chart",   "Donnees",          "GLM Poisson, mu_t, EURIBOR 3M, EDA"),
        ("layers",      "Modele AJD",        "SDE bivariate, correlation eq. 2.10, mesure Q"),
        ("cpu",         "Calibration MCMC",  "MH 30k iter., traces, ESS, delta pre/post-COVID"),
        ("activity",    "Monte Carlo",       "Algorithme A.5, courbe P(mu*>s), seuils"),
        ("target",      "Pricing",           "Vecteur MPR zeta, scenarios S1/S2/S3"),
        ("sliders",     "Sensibilite",       "Impact +/-20% de zeta sur P0, elasticite chi"),
    ]
    cols = st.columns(3)
    for i, (ico, title, desc) in enumerate(page_info):
        with cols[i % 3]:
            st.markdown(f"""
<div style='background:#1A1D27;border-radius:6px;padding:.75rem .9rem;
            margin:.25rem 0;border-left:2px solid #D97706;'>
  <div style='display:flex;align-items:center;gap:.5rem;margin-bottom:.2rem;'>
    {icon(ico, 14, "#D97706")}
    <span style='font-weight:600;color:#E5E7EB;font-size:.83rem;'>{title}</span>
  </div>
  <div style='color:#6B7280;font-size:.73rem;'>{desc}</div>
</div>""", unsafe_allow_html=True)
