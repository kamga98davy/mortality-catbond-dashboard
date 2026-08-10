"""Belgian Mortality CAT Bond Dashboard — Home / Accueil."""
import streamlit as st
from streamlit_option_menu import option_menu

from utils.styles import inject_css, kpi_row, insight_box, section_header

st.set_page_config(
    page_title="Belgian Mortality CAT Bond",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Session state ──────────────────────────────────────────────────────────────
if "view" not in st.session_state:
    st.session_state["view"] = "Executive"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style='text-align:center; margin-bottom:1rem;'>
  <span style='font-size:2rem;'>📊</span><br>
  <span style='color:#F4A926; font-weight:700; font-size:1.1rem;'>CAT Bond Mortalité</span><br>
  <span style='color:#8892B0; font-size:.75rem;'>Belgique — Post-COVID</span>
</div>""", unsafe_allow_html=True)

    view = st.radio(
        "Vue",
        ["👔 Executive", "🔬 Technique"],
        index=0 if st.session_state["view"] == "Executive" else 1,
        label_visibility="collapsed",
    )
    st.session_state["view"] = "Executive" if view.startswith("👔") else "Technique"

    st.markdown("---")
    st.markdown(
        "<p style='color:#8892B0; font-size:.75rem;'>Navigation via le menu en haut à gauche.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("""
<div style='margin-top:2rem; color:#8892B0; font-size:.72rem; line-height:1.6;'>
  📄 <b>Mémoire :</b> Pricing Extreme Mortality Risk — Application belge<br>
  🗓️ Données : Statbel 2013–2024<br>
  📐 Modèle : AJD bivarié (Li et al., 2023)<br>
  ⚙️ Calibration : MCMC Metropolis-Hastings
</div>""", unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────────────────────
IS_EXEC = st.session_state["view"] == "Executive"

# Hero
badge = '<span class="badge-exec">Executive</span>' if IS_EXEC else '<span class="badge-tech">Technique</span>'
st.markdown(f"""
<div style='margin-bottom:1.5rem;'>
  {badge}
  <h1 style='margin:.4rem 0 .3rem 0; font-size:2rem; font-weight:700; color:#CCD6F6;'>
    Tarification du Risque de Mortalité Extrême
  </h1>
  <p style='color:#8892B0; font-size:1rem; margin:0;'>
    Application au contexte belge post-COVID · Reproduction de Li, Liu, Tang &amp; Yuan (2023, <em>IME</em>)
  </p>
</div>
""", unsafe_allow_html=True)

# KPI cards — identical in both views
kpi_row([
    ("Probabilité d'attachment", "1.16%", "P(μ* > a_BE)"),
    ("Probabilité d'exhaustion", "0.74%", "P(μ* > b_BE)"),
    ("Perte attendue", "0.92%", "Moyenne pondérée"),
    ("Coupon (spread)", "6.0%", "c* annuel"),
    ("Maturité bond", "5.25 ans", "T = 5.25, Δ = 0.25"),
])

st.markdown("---")

# ── Executive view ─────────────────────────────────────────────────────────────
if IS_EXEC:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Contexte & Enjeu", "Pourquoi un CAT bond sur la mortalité ?")
        st.markdown("""
Les **obligations catastrophe (CAT bonds) sur mortalité** permettent aux
assureurs-vie de transférer au marché le risque d'une surmortalité soudaine
et massive — épidémie, pandémie, catastrophe naturelle.

**La pandémie COVID-19** a brutalement rappelé que ce risque est réel :
la Belgique a enregistré des pics de mortalité hebdomadaire **jusqu'à 3×
supérieurs** aux niveaux habituels durant le printemps 2020.

Cette étude répond à une question centrale pour les assureurs belges :

> *À quel prix juste faut-il émettre un CAT bond sur la mortalité belge
> dans un monde post-pandémique ?*
""")

        insight_box("""
<b>💡 Résultat principal</b><br>
Un CAT bond sur la mortalité belge, calibré sur les données 2017–2022,
devrait offrir un coupon de <b>6 %</b> pour être émis à la valeur nominale (P₀ = 100).
Le risque post-COVID justifie une prime plus élevée qu'un contexte pré-pandémique.
""")

    with col2:
        section_header("Structure du bond (référence)")
        st.markdown("""
| Caractéristique | Valeur |
|:---|---:|
| Indice de référence | Surmortalité belge μ* |
| Seuil d'activation (*attachment*) | a_BE |
| Seuil de perte totale (*exhaustion*) | b_BE |
| Probabilité d'activation | **1,16 %** |
| Probabilité d'exhaustion | **0,74 %** |
| Perte attendue | **0,92 %** |
| Maturité | **5,25 ans** |
| Coupon annuel | **6,0 %** |
| Principal | 100 (pair) |

*Analogue à l'obligation Atlas IX Capital — Li et al. (2023)*
""")

    st.markdown("---")
    section_header("Les 3 scénarios analysés")
    st.markdown("""
<div class="scenario-row">
  <div class="scenario-card">
    <div class="scenario-title">Scénario S1</div>
    <div class="scenario-price">P₀ = 100</div>
    <div class="scenario-desc">
      <b>Dynamiques post-COVID + Seuils post-COVID</b><br>
      Scénario de référence : le marché est calibré sur le contexte actuel.
      Investisseurs conscients du risque pandémique.
    </div>
  </div>
  <div class="scenario-card s2">
    <div class="scenario-title">Scénario S2</div>
    <div class="scenario-price s2">P₀ &gt; 100</div>
    <div class="scenario-desc">
      <b>Dynamiques pré-COVID + Seuils pré-COVID</b><br>
      Counterfactuel : que se serait-il passé sans pandémie ?
      Le bond serait valorisé plus cher (risque perçu plus faible).
    </div>
  </div>
  <div class="scenario-card s3">
    <div class="scenario-title">Scénario S3</div>
    <div class="scenario-price s3">P₀ = 100</div>
    <div class="scenario-desc">
      <b>Dynamiques post-COVID + Seuils pré-COVID</b><br>
      Scénario de désalignement : risque sous-estimé si les seuils
      n'ont pas été mis à jour après la pandémie.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Technical view ─────────────────────────────────────────────────────────────
else:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Résumé technique")
        st.markdown("""
Ce travail reproduit et adapte **Li, Liu, Tang & Yuan (2023)** —
*"Pricing extreme mortality risk in the wake of the COVID-19 pandemic"*,
*Insurance: Mathematics and Economics*, 85, 84–106.

**Méthodologie :**
1. **Données** : mortalité hebdomadaire belge (Statbel, 2013–2024),
   EURIBOR 3M comme taux sans risque
2. **Surmortalité** : GLM Poisson avec harmoniques saisonnières → résidu μₜ
3. **Modèle** : processus AJD bivarié (rₜ, μₜ) — équation (2.8)
4. **Calibration** : MCMC Metropolis-Hastings (30 000 itérations)
   sur deux fenêtres : 2017–2019 (pré-COVID) et 2017–2022 (post-COVID)
5. **Mesure risque-neutre** : changement de mesure P → Q via le vecteur MPR ζ = (γ₁, γ₂; κ₁, κ₂; χ)
6. **Prix** : simulation Monte Carlo (100 000 trajectoires) — algorithme A.5
7. **Calibration MPR** : moindres carrés sur 10 observations trimestrielles
   des spreads du Vita Capital IV D-5 (Lane Financial LLC, 2011–2015)
""")

    with col2:
        section_header("Référence")
        st.markdown("""
**Li, Z., Liu, X., Tang, Q., & Yuan, Z. (2023)**<br>
Pricing extreme mortality risk in the wake of the COVID-19 pandemic.<br>
*Insurance: Mathematics and Economics*, 85, 84–106.<br>
DOI: 10.1016/j.insmatheco.2022.09.006

---

**Modèle AJD (équation 2.8) :**
""")
        st.latex(r"""
\begin{cases}
dr_t = (m_1 - d_1 r_t)\,dt + \sigma_1\,dW_{1,t} + d\!\sum_{i=1}^{N_t} X_{1,i} \\[6pt]
d\mu_t = (m_2 - d_2 \mu_t)\,dt + \sigma_2(\rho_1 dW_{1,t} + \sqrt{1-\rho_1^2}\,dW_{2,t})
+ d\!\sum_{i=1}^{N_t} X_{2,i}
\end{cases}
""")
        st.markdown("""
où $(X_{1,j}, X_{2,j}) \\sim \\mathcal{N}(\\nu_1, \\nu_2;\\, \\phi_1^2, \\phi_2^2;\\, \\rho_2)$
et $N_t \\sim \\text{Poisson}(\\lambda t)$.
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

st.markdown("---")
st.markdown(
    "<p style='color:#8892B0; font-size:.72rem; text-align:center;'>"
    "Mémoire de fin d'études · Belgique · 2024–2025 · "
    "Modèle : AJD bivarié · Calibration : MCMC · Tarification : Monte Carlo"
    "</p>",
    unsafe_allow_html=True,
)
