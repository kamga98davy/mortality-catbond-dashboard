"""Page 2 — Modèle AJD bivarié (Li et al., éq. 2.8–2.11)."""
import streamlit as st

from utils.styles import inject_css, section_header, insight_box
from utils.sidebar import render_sidebar
from utils.icons import icon
from utils.data_loader import load_params_postC, load_params_preC, corr_instantanee

st.set_page_config(page_title="Modèle AJD", page_icon="🔬", layout="wide")
inject_css()
render_sidebar()

st.title("Modèle AJD bivarié")

tab_comm, tab_tech = st.tabs(["👔  Vue Commerciale", "🔬  Vue Technique"])

# ── COMMERCIAL ─────────────────────────────────────────────────────────────────
with tab_comm:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Qu'est-ce qu'un modèle AJD ?",
                       "Affine Jump-Diffusion — modéliser le risque extrême de mortalité")
        st.markdown("""
Le **modèle AJD bivarié** décrit simultanément l'évolution de deux variables :

- **rₜ** — le taux d'intérêt (EURIBOR 3M)
- **μₜ** — la surmortalité hebdomadaire belge

Ces deux variables sont liées car une pandémie peut simultanément
faire monter la mortalité **et** perturber les marchés financiers.

Le modèle comporte **trois sources de risque** :

| Source | Description | Impact |
|:---|:---|:---|
| **Diffusion brownienne** | Fluctuations normales et continues | Risque ordinaire quotidien |
| **Sauts communs** | Chocs soudains, simultanés sur les deux variables | COVID, crises |
| **Corrélation** | Les deux variables bougent ensemble | Dépendance risque-taux |
""")

        insight_box("""
<strong>Intuition clé</strong><br>
Sans COVID, le risque de mortalité est bien séparé du risque financier.
Avec COVID, les deux explosent simultanément — c'est précisément ce que
le terme de saut capture.
La fréquence des sauts λ a fortement augmenté dans les estimations post-COVID.
""")

    with col2:
        section_header("Les 3 mécanismes du modèle")
        st.markdown("""
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;
            border-left:3px solid #4FC3F7;'>
  <b style='color:#4FC3F7;'>1 · Tendance de long terme (drift)</b><br>
  <span style='color:#8892B0; font-size:.85rem;'>
  Les variables reviennent lentement vers leur moyenne d'équilibre.
  Vitesse contrôlée par d₁ et d₂.
  </span>
</div>
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;
            border-left:3px solid #F4A926;'>
  <b style='color:#F4A926;'>2 · Bruit aléatoire (diffusion)</b><br>
  <span style='color:#8892B0; font-size:.85rem;'>
  Variations continues et graduelles — "bruit normal" du marché.
  Corrélées via ρ₁ entre le taux et la mortalité.
  </span>
</div>
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;
            border-left:3px solid #FF6B6B;'>
  <b style='color:#FF6B6B;'>3 · Sauts soudains (Poisson)</b><br>
  <span style='color:#8892B0; font-size:.85rem;'>
  Chocs extrêmes rares mais violents. Fréquence λ sauts/an.
  Taille du saut : distribution normale bivariée (ν₁, ν₂, φ₁, φ₂, ρ₂).
  </span>
</div>
""", unsafe_allow_html=True)

# ── TECHNIQUE ──────────────────────────────────────────────────────────────────
with tab_tech:
    sub1, sub2, sub3 = st.tabs(
        ["📐 Spécification mathématique", "🔄 Mesure risque-neutre Q", "📊 Paramètres"])

    with sub1:
        section_header("Processus AJD bivarié sous P",
                       "Équation (2.8) de Li, Liu, Tang & Yuan (2023)")
        st.latex(r"""
Y_t = \begin{pmatrix} r_t \\ \mu_t \end{pmatrix}, \qquad
\begin{cases}
dr_t = (m_1 - d_1 r_t)\,dt + \sigma_1\,dW_{1,t}
       + d\!\displaystyle\sum_{i=1}^{N_t} X_{1,i}\\[10pt]
d\mu_t = (m_2 - d_2 \mu_t)\,dt
         + \sigma_2\!\left(\rho_1\,dW_{1,t} + \sqrt{1-\rho_1^2}\,dW_{2,t}\right)
         + d\!\displaystyle\sum_{i=1}^{N_t} X_{2,i}
\end{cases}
""")
        st.markdown("""
**Notation :**
- $(W_{1,t}, W_{2,t})$ : mouvements browniens standard indépendants
- $\\{N_t\\}$ : processus de Poisson d'intensité $\\lambda$ (sauts/an)
- $(X_{1,j}, X_{2,j}) \\sim \\mathcal{N}(\\nu_1, \\nu_2;\\, \\phi_1^2, \\phi_2^2;\\, \\rho_2)$ : taille des sauts i.i.d.
- Vecteur de paramètres : $\\theta = (m_1, d_1, \\sigma_1, m_2, d_2, \\sigma_2, \\rho_1, \\lambda, \\nu_1, \\nu_2, \\phi_1, \\phi_2, \\rho_2) \\in \\mathbb{R}^{13}$
""")

        st.markdown("---")
        section_header("Corrélation instantanée",
                       "Équation (2.10) — Mesure la dépendance entre dr_t et dμ_t")
        st.latex(r"""
\mathrm{corr}(dr_t,\,d\mu_t) =
\frac{\rho_1\sigma_1\sigma_2 + \lambda(\rho_2\phi_1\phi_2 + \nu_1\nu_2)}
     {\sqrt{(\sigma_1^2 + \lambda(\phi_1^2+\nu_1^2))
            (\sigma_2^2 + \lambda(\phi_2^2+\nu_2^2))}}
""")
        st.markdown("""
La corrélation provient de **deux contributions** :
- **Diffusion** : $\\rho_1 \\sigma_1 \\sigma_2$ — lien brownien continu
- **Sauts** : $\\lambda(\\rho_2\\phi_1\\phi_2 + \\nu_1\\nu_2)$ — lien via les chocs communs
""")

        params = load_params_postC()
        if params:
            rho = corr_instantanee(params)
            st.success(f"**Corrélation instantanée estimée (post-COVID) :** `{rho:.4f}`")

    with sub2:
        section_header("Changement de mesure P → Q",
                       "Équation (2.11) — Market Prices of Risk (MPR) ζ = (γ₁, γ₂; κ₁, κ₂; χ)")
        st.latex(r"""
\begin{aligned}
m_1^* &= m_1 + \gamma_1\sigma_1\\
m_2^* &= m_2 + \gamma_1\sigma_2\rho_1 + \gamma_2\sigma_2\sqrt{1-\rho_1^2}\\
\nu_1^* &= \nu_1 + \phi_1\kappa_1\\
\nu_2^* &= \nu_2 + \phi_2\kappa_2\\
\lambda^* &= \lambda(1+\chi)
\end{aligned}
""")
        st.markdown("""
**Interprétation du vecteur MPR ζ :**

| Composante | Nom | Interprétation économique |
|:---|:---|:---|
| $\\gamma_1$ | MPR brownien (taux) | Prime pour le risque continu du taux d'intérêt |
| $\\gamma_2$ | MPR brownien (mortalité) | Prime pour le risque continu de mortalité |
| $\\kappa_1$ | MPR taille saut (taux) | Prime pour la taille des chocs sur le taux |
| $\\kappa_2$ | MPR taille saut (mort.) | Prime pour la taille des chocs de mortalité |
| $\\chi$ | MPR fréquence des sauts | Prime pour la fréquence des événements extrêmes |

Le vecteur ζ est calibré sur les **spreads observés du marché secondaire**
(Vita Capital IV D-5, 10 observations trimestrielles 2011–2015).
""")

        section_header("Formule de pricing (équation 3.1)")
        st.latex(r"""
P_0 = \mathbb{E}^Q\!\left[
\sum_{k=1}^{T/\Delta} e^{-\int_0^{t_k} r_s\,ds}\,
c^*\,\Delta\,\mathrm{PRF}_{t_k}
+ e^{-\int_0^T r_s\,ds}\,K\,\mathrm{PRF}_T
\right]
""")
        st.latex(r"""
\text{PRF}_{t_k} = 1 - \frac{(\mu^* - a)_+ - (\mu^* - b)_+}{b - a}, \qquad
\mu^* = \max_{0 \leq t \leq T} \mu_t
""")

    with sub3:
        section_header("Paramètres du modèle",
                       "13 paramètres sous P — vecteur θ")
        import pandas as pd
        params_info = pd.DataFrame([
            ("m₁", "m1",    "Drift moyen (taux)",                "ℝ",       "Tendance de long terme du taux"),
            ("d₁", "d1",    "Vitesse de retour (taux)",          "ℝ₊",      "Vitesse de mean-reversion du taux"),
            ("σ₁", "sigma1","Volatilité diffusion (taux)",       "ℝ₊",      "Amplitude des chocs continus (taux)"),
            ("m₂", "m2",    "Drift moyen (mortalité)",           "ℝ",       "Tendance de long terme de μₜ"),
            ("d₂", "d2",    "Vitesse de retour (mortalité)",     "ℝ₊",      "Vitesse de mean-reversion de μₜ"),
            ("σ₂", "sigma2","Volatilité diffusion (mortalité)", "ℝ₊",       "Amplitude des chocs continus (μₜ)"),
            ("ρ₁", "rho1",  "Corrélation brownienne",            "[-1,1]",  "Lien continu entre rₜ et μₜ"),
            ("λ",  "lambda","Fréquence des sauts",               "ℝ₊",      "Sauts par année (processus Poisson)"),
            ("ν₁", "v1",    "Taille moyenne saut (taux)",        "ℝ",       "Saut moyen sur rₜ"),
            ("ν₂", "v2",    "Taille moyenne saut (mortalité)",   "ℝ",       "Saut moyen sur μₜ"),
            ("φ₁", "phi1",  "Écart-type saut (taux)",            "ℝ₊",      "Variabilité des sauts sur rₜ"),
            ("φ₂", "phi2",  "Écart-type saut (mortalité)",       "ℝ₊",      "Variabilité des sauts sur μₜ"),
            ("ρ₂", "rho2",  "Corrélation des sauts",             "[-1,1]",  "Lien entre les sauts (rₜ, μₜ)"),
        ], columns=["Symbole", "Code R", "Description", "Espace", "Interprétation"])

        params = load_params_postC()
        if params:
            def _fmt_param(k: str) -> str:
                v = params.get(k)
                return f"{v:.5f}" if v is not None else "—"
            params_info["Valeur (post-COVID)"] = params_info["Code R"].map(_fmt_param)

        st.dataframe(params_info, hide_index=True, use_container_width=True)
