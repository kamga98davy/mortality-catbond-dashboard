"""Page 4 — Simulation Monte Carlo & Courbe d'exceedance."""
import streamlit as st
import plotly.graph_objects as go

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.sidebar import render_sidebar
from utils.data_loader import load_exceedance, load_seuils
from utils.charts import exceedance_chart

st.set_page_config(page_title="Monte Carlo", page_icon="📈", layout="wide")
inject_css()

IS_EXEC = render_sidebar() == "Executive"
badge = '<span class="badge-exec">Executive</span>' if IS_EXEC else '<span class="badge-tech">Technique</span>'
st.markdown(f"{badge}", unsafe_allow_html=True)
st.title("Simulation Monte Carlo — Courbe d'exceedance")

seuils = load_seuils()
df_exc = load_exceedance()


def _dummy_exec():
    """Show a placeholder exceedance chart with synthetic data when data unavailable."""
    import numpy as np
    s_range = np.linspace(0.01, 0.06, 300)
    prob = 2.5 * np.exp(-60 * s_range)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s_range, y=prob, mode="lines",
        line=dict(color="#F4A926", width=2), name="P(μ* > s) [simulation]",
    ))
    a_demo, b_demo, p_a, p_b = 0.025, 0.038, 1.16, 0.74
    fig.add_hline(y=p_a, line=dict(color="#4FC3F7", dash="dash"))
    fig.add_hline(y=p_b, line=dict(color="#FF6B6B", dash="dash"))
    fig.add_vline(x=a_demo, line=dict(color="#4FC3F7", dash="dot"))
    fig.add_vline(x=b_demo, line=dict(color="#FF6B6B", dash="dot"))
    fig.update_layout(
        title="Courbe d'exceedance [aperçu — données simulées à titre illustratif]",
        xaxis_title="Seuil s", yaxis_title="P(μ* > s)  [%]",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
        font=dict(color="#CCD6F6"),
    )
    st.plotly_chart(fig, use_container_width=True, key="mc_dummy_exec")
    st.caption("⚠️ Graphique illustratif — remplacé par les vraies données après export R.")


# ── EXECUTIVE VIEW ─────────────────────────────────────────────────────────────
if IS_EXEC:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("La courbe d'exceedance : lire le risque de catastrophe",
                       "Probabilité que la surmortalité dépasse un seuil donné sur 5,25 ans")

        if df_exc is not None and seuils is not None:
            st.plotly_chart(
                exceedance_chart(df_exc, seuils, executive=True),
                use_container_width=True,
                key="mc_exc_exec",
            )
        else:
            st.info(
                "La courbe d'exceedance sera affichée ici une fois les données exportées "
                "via `export_for_streamlit.R`.",
                icon="📊",
            )
            _dummy_exec()

    with col2:
        section_header("Comment lire ce graphique ?")
        st.markdown("""
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;'>
  <b style='color:#4FC3F7;'>Zone blanche (droite du graphique)</b><br>
  <span style='color:#8892B0;'>
    Surmortalité normale — le bond n'est pas activé.
    L'investisseur reçoit tous ses coupons.
  </span>
</div>
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;
            border-left:3px solid #F4A926;'>
  <b style='color:#F4A926;'>Zone orange (entre a_BE et b_BE)</b><br>
  <span style='color:#8892B0;'>
    Surmortalité extrême — perte <em>partielle</em> du principal.
    L'investisseur perd entre 0% et 100% de son capital selon l'intensité.
  </span>
</div>
<div style='background:#112240; border-radius:10px; padding:1.2rem; margin:.5rem 0;
            border-left:3px solid #FF6B6B;'>
  <b style='color:#FF6B6B;'>Au-delà de b_BE</b><br>
  <span style='color:#8892B0;'>
    Catastrophe totale — perte intégrale du principal.
    Probabilité : <b>0,74%</b>.
  </span>
</div>
""", unsafe_allow_html=True)

        if seuils:
            a_BE = seuils.get("a_BE", seuils.get("a", "—"))
            b_BE = seuils.get("b_BE", seuils.get("b", "—"))
            st.markdown(f"""
---
| | Valeur |
|:---|---:|
| Seuil attachment **a_BE** | `{a_BE:.5f}` |
| Seuil exhaustion **b_BE** | `{b_BE:.5f}` |
| P(μ* > a_BE) | **1,16 %** |
| P(μ* > b_BE) | **0,74 %** |
| Perte attendue | **≈ 0,92 %** |
""")

# ── TECHNICAL VIEW ─────────────────────────────────────────────────────────────
else:
    tab1, tab2, tab3 = st.tabs(
        ["📈 Courbe d'exceedance", "⚙️ Algorithme A.5", "📐 Dérivation des seuils"])

    with tab1:
        section_header("Probabilité d'exceedance de μ*",
                       "Analogue Figure 5.3 de Li et al. (2023)")
        st.markdown(r"""
$$\mu^* = \max_{0 \leq t \leq T} \mu_t$$

La variable $\mu^*$ représente le **maximum** de la surmortalité sur l'horizon du bond $T = 5{,}25$ ans.
Les seuils $a^{BE}$ et $b^{BE}$ sont déterminés par inversion :

$$a^{BE} = F_{\mu^*}^{-1}(1 - 0{,}0116), \qquad
  b^{BE} = F_{\mu^*}^{-1}(1 - 0{,}0074)$$
""")
        if df_exc is not None and seuils is not None:
            st.plotly_chart(
                exceedance_chart(df_exc, seuils, executive=False),
                use_container_width=True,
                key="mc_exc_tech",
            )
        else:
            no_data_msg("exceedance.csv / seuils.json")
            st.markdown("""
**Pour générer ces données, exécute dans R :**
```r
source("export_for_streamlit.R")
```
""")

        if seuils:
            a_BE = seuils.get("a_BE", seuils.get("a"))
            b_BE = seuils.get("b_BE", seuils.get("b"))
            col1, col2, col3 = st.columns(3)
            col1.metric("a_BE (attachment)", f"{a_BE:.6f}")
            col2.metric("b_BE (exhaustion)", f"{b_BE:.6f}")
            col3.metric("N simulations", "100 000")

    with tab2:
        section_header("Algorithme de simulation exacte (Appendice A.5)",
                       "Simulation des trajectoires (rₜ, μₜ) sous P")
        st.markdown("""
L'algorithme simule des trajectoires **exactes** (non euler) du processus AJD,
exploitant la structure affine pour intégrer analytiquement les moments.

**Entrées :**
- État initial $(r_0, \\mu_0)$ : derniers points observés (fin 2022)
- Paramètres sous $P$ : `params_postC`
- Pas de temps : $\\Delta = 0{,}25$ an (trimestriel)
- Horizon : $T = 5{,}25$ ans → 21 pas
- $N_{\\text{sim}} = 100\\,000$ trajectoires

**Étapes par pas de temps $[t_k, t_{k+1}]$ :**
""")
        st.code("""
# Pour chaque trajectoire i = 1,...,N_sim :
#   Étape 1 : Simuler les moments jusqu'à l'ordre 4 via RK4 (ODE, eq. 2.9)
moments <- rk4(r[k], mu[k], dt=Delta, mesh=10, par, mv)

#   Étape 2 : Convertir moments → cumulants (ordre 4)
kum <- moments_vers_cumulants(moments)

#   Étape 3 : Générer (r[k+1], mu[k+1]) via approximation saddlepoint bivariée
#             (Pienaar & Varughese, 2016) — Newton-Raphson
(r[k+1], mu[k+1]) <- sample_saddlepoint(kum)

#   Étape 4 : Actualiser mu_star = max(mu_star, mu[k+1])

# mu_star_i = max_{k=0..T} mu_i[k]
""", language="r")

        st.markdown("""
**Sortie :** vecteur `mu_star` de taille $N_{\\text{sim}} = 100\\,000$.

La distribution empirique de `mu_star` donne la courbe d'exceedance.
""")

        warning_box("""
<b>Note de calcul :</b> La simulation complète (100 000 trajectoires × 21 pas)
prend environ 2–4 heures sur un CPU standard en R.
Les résultats sont sauvegardés dans <code>seuils_BE.rds</code> puis exportés
en <code>exceedance.csv</code> via le script R.
""")

    with tab3:
        section_header("Dérivation des seuils a_BE et b_BE",
                       "Scénarios S1 (post-COVID) et S3 (pré-COVID)")
        st.markdown("""
Les seuils sont calibrés de façon à reproduire les probabilités d'exceedance
du bond de référence **Atlas IX Capital** (Li et al., Example 3.1) :

| Scénario | Dynamiques sous P | Conditions initiales | Seuils résultants |
|:---|:---|:---|:---|
| **S1** | Post-COVID (2017–2022) | Fin 2022 | $a^{BE}$, $b^{BE}$ |
| **S3** | Pré-COVID (2017–2019) | Fin 2019 | $a^{BE}_{\\text{preC}}$, $b^{BE}_{\\text{preC}}$ |

**Contraintes d'inversion :**
$$P(\\mu^* > a^{BE}) = 1{,}16\\%\\qquad P(\\mu^* > b^{BE}) = 0{,}74\\%$$

**Perte attendue théorique :**
$$E[1 - \\text{PRF}] = \\frac{1}{b-a}\\int_a^b P(\\mu^*>s)\\,ds \\approx
\\frac{P(a)+P(b)}{2} = \\frac{1{,}16\\% + 0{,}74\\%}{2} = 0{,}95\\%$$

La valeur exacte de **0,92 %** (Li et al.) provient de l'intégrale numérique
sur la courbe d'exceedance réelle (légèrement concave).
""")

        if seuils:
            a_BE = seuils.get("a_BE", seuils.get("a"))
            b_BE = seuils.get("b_BE", seuils.get("b"))
            a_pre = seuils.get("a_BE_preC")
            b_pre = seuils.get("b_BE_preC")
            if a_pre and b_pre:
                st.markdown(f"""
| | S1 (post-COVID) | S3 (pré-COVID) | Variation |
|:---|---:|---:|---:|
| Attachment *a* | `{a_BE:.5f}` | `{a_pre:.5f}` | `{a_BE - a_pre:+.5f}` |
| Exhaustion *b* | `{b_BE:.5f}` | `{b_pre:.5f}` | `{b_BE - b_pre:+.5f}` |
""")
                if a_pre < a_BE:
                    insight_box("""
<b>📌 Interprétation du désalignement (Scénario S3)</b><br>
Les seuils post-COVID sont <b>plus élevés</b> que les seuils pré-COVID :
la surmortalité extrême est devenue plus probable après la pandémie.
Un émetteur qui conserverait les seuils pré-COVID sous-estimerait le risque réel —
c'est précisément le scénario S3.
""")


def _dummy_exec_bottom():  # kept for reference, real one moved above
    s_range = []
    prob = 2.5 * np.exp(-60 * s_range)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=s_range, y=prob, mode="lines",
        line=dict(color="#F4A926", width=2), name="P(μ* > s) [simulation]",
    ))
    a_demo, b_demo, p_a, p_b = 0.025, 0.038, 1.16, 0.74
    fig.add_hline(y=p_a, line=dict(color="#4FC3F7", dash="dash"))
    fig.add_hline(y=p_b, line=dict(color="#FF6B6B", dash="dash"))
    fig.add_vline(x=a_demo, line=dict(color="#4FC3F7", dash="dot"))
    fig.add_vline(x=b_demo, line=dict(color="#FF6B6B", dash="dot"))
    fig.update_layout(
        title="Courbe d'exceedance [aperçu — données simulées à titre illustratif]",
        xaxis_title="Seuil s", yaxis_title="P(μ* > s)  [%]",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
        font=dict(color="#CCD6F6"),
    )
    st.plotly_chart(fig, use_container_width=True, key="mc_dummy_bottom")
    st.caption("⚠️ Graphique illustratif — remplacé par les vraies données après export R.")
