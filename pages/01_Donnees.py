"""Page 1 — Données : mortalité belge, GLM Poisson, surmortalité, taux d'intérêt."""
import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, insight_box, no_data_msg
from utils.sidebar import render_sidebar
from utils.icons import icon
from utils.data_loader import (
    load_mortality, load_interest_rate, compute_stats,
)
from utils.charts import (
    deaths_chart, glm_fit_chart, excess_mortality_chart,
    boxplot_covid, joint_chart, interest_rate_chart,
)

st.set_page_config(page_title="Données", page_icon="📊", layout="wide")
inject_css()
render_sidebar()

st.title("Données — Mortalité belge & Taux d'intérêt")

with st.spinner("Chargement des données et calibration GLM…"):
    df = load_mortality()
    df_taux = load_interest_rate()

if df is None:
    no_data_msg("mortalite_final.xlsx")
    st.stop()

tab_comm, tab_tech = st.tabs(["👔  Vue Commerciale", "🔬  Vue Technique"])

# ── COMMERCIAL ─────────────────────────────────────────────────────────────────
with tab_comm:
    pre  = df[df["periode"] == "Pré-COVID"]
    post = df[df["periode"] == "Post-COVID"]

    section_header("Pourquoi ces données ?",
                   "Tout le modèle repose sur deux séries : la mortalité et les taux d'intérêt")

    st.markdown(f"""
<div class="prose" style="margin-bottom:1rem;">
  Pour tarifer un CAT bond sur la mortalité, il faut répondre à deux questions :
  <strong style="color:#E5E7EB">"Que s'est-il passé ?"</strong> (les décès observés) et
  <strong style="color:#E5E7EB">"Que devait-il se passer ?"</strong> (les décès attendus selon un modèle statistique).
  La différence entre les deux — la <em>surmortalité</em> — est la variable centrale du modèle.
  Les taux d'intérêt (EURIBOR 3M) servent à actualiser les flux futurs du bond.
</div>
""", unsafe_allow_html=True)

    col_chart, col_key = st.columns([3, 1], gap="large")
    with col_chart:
        st.plotly_chart(deaths_chart(df), use_container_width=True, key="d1_deaths_exec")
    with col_key:
        st.markdown(f"""
<div style='display:flex;flex-direction:column;gap:.6rem;margin-top:.5rem;'>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.75rem .9rem;'>
    <div style='font-size:1.4rem;font-weight:700;color:#D97706;'>
      {pre['deces'].mean():.0f}
    </div>
    <div style='color:#6B7280;font-size:.71rem;'>Décès/sem. (pré-COVID)</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.75rem .9rem;border-left:2px solid #EF4444;'>
    <div style='font-size:1.4rem;font-weight:700;color:#EF4444;'>
      {post['deces'].mean():.0f}
    </div>
    <div style='color:#6B7280;font-size:.71rem;'>Décès/sem. (post-COVID)</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.75rem .9rem;border-left:2px solid #D97706;'>
    <div style='font-size:1.4rem;font-weight:700;color:#D97706;'>
      {df["deces"].max():,.0f}
    </div>
    <div style='color:#6B7280;font-size:.71rem;'>Pic COVID (semaine la plus mortelle)</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    section_header("La surmortalité : mesurer le choc COVID")

    st.markdown("""
<div class="prose" style="margin-bottom:.8rem;">
  La surmortalité hebdomadaire <strong style="color:#E5E7EB">μₜ</strong> est calculée
  en soustrayant les décès attendus (GLM Poisson) des décès observés, rapporté à la population.
  C'est la variable que le CAT bond protège : si elle dépasse un seuil prédéfini pendant
  la durée du bond, l'investisseur perd une partie de son capital.
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(excess_mortality_chart(df), use_container_width=True, key="d1_mu_exec")
    with col2:
        insight_box(f"""
<strong>Comment lire ce graphique</strong><br><br>
<strong style="color:#E5E7EB">μₜ &gt; 0</strong> : plus de décès que prévu.<br>
Les barres hautes de mars-mai 2020 représentent les premières vagues COVID.<br><br>
<strong>Écart-type avant/après :</strong><br>
Pré-COVID : {pre['mu_t'].std():.4f}<br>
Post-COVID : {post['mu_t'].std():.4f}<br><br>
La volatilité de μₜ a nettement augmenté après 2020, justifiant une recalibration du modèle.
""")

# ── TECHNIQUE ──────────────────────────────────────────────────────────────────
with tab_tech:
    sub1, sub2, sub3, sub4 = st.tabs(
        ["📈 Séries temporelles", "🔬 GLM Poisson & μₜ",
         "📊 Statistiques", "💹 Taux d'intérêt"])

    with sub1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(deaths_chart(df, show_mean=True), use_container_width=True, key="d1_deaths_t1")
        with col2:
            st.plotly_chart(excess_mortality_chart(df), use_container_width=True, key="d1_mu_t1")

        if df_taux is not None:
            st.plotly_chart(joint_chart(df, df_taux), use_container_width=True, key="d1_joint_t1")
        else:
            no_data_msg("taux_journalier.xlsx")

    with sub2:
        section_header("GLM Poisson — Décès attendus",
                       "Équation (Li et al. éq. 4.1) : E[D_{t,w}] = exp(log e_{t,w} + β₀ + β₁t + Σ harmoniques)")

        st.latex(r"""
\log \mathbb{E}[D_{t,w}] = \log(e_{t,w}) + \beta_0 + \beta_1 t
+ \sum_{k=1}^{2}\!\left[a_k \sin\!\tfrac{2\pi k w}{52} + b_k\cos\!\tfrac{2\pi k w}{52}\right]
""")
        st.markdown(
            f"**Corrélation décès observés / attendus :** "
            f"`{df['deces'].corr(df['deces_attendus']):.4f}`"
        )
        st.plotly_chart(glm_fit_chart(df), use_container_width=True, key="d1_glm_t2")

        st.markdown("---")
        section_header("Surmortalité μₜ",
                       "μₜ = (d_t − E[d_t]) / e_t × 100  (équation 4.1)")
        st.plotly_chart(excess_mortality_chart(df), use_container_width=True, key="d1_mu_t2")

        section_header("Distribution de μₜ par période")
        col1, col2 = st.columns([3, 2])
        with col1:
            st.plotly_chart(boxplot_covid(df), use_container_width=True, key="d1_box_t2")
        with col2:
            from scipy import stats as scipy_stats
            pre  = df[df["periode"] == "Pré-COVID"]["mu_t"].dropna()
            post = df[df["periode"] == "Post-COVID"]["mu_t"].dropna()
            t_stat, p_val = scipy_stats.ttest_ind(pre, post, equal_var=False)
            st.markdown("##### Test de Welch (H₀ : moyennes égales)")
            st.markdown(f"""
| | Valeur |
|:---|---:|
| t-statistique | `{t_stat:.4f}` |
| p-valeur | `{p_val:.2e}` |
| Conclusion | {"**Rejet de H₀** à 5%" if p_val < 0.05 else "Non-rejet"} |
""")
            st.info(
                "La p-valeur confirme une différence hautement significative "
                "entre les moyennes pré- et post-COVID.",
                icon="📐"
            )

    with sub3:
        section_header("Statistiques descriptives de μₜ")
        pre  = df[df["periode"] == "Pré-COVID"]["mu_t"].dropna()
        post = df[df["periode"] == "Post-COVID"]["mu_t"].dropna()
        stats_pre  = compute_stats(pre)
        stats_post = compute_stats(post)

        stats_df = pd.DataFrame({
            "Statistique": list(stats_pre.keys()),
            "Pré-COVID":   [str(v) for v in stats_pre.values()],
            "Post-COVID":  [str(v) for v in stats_post.values()],
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)

        st.markdown("---")
        section_header("Distribution complète de μₜ")
        import plotly.graph_objects as go
        fig = go.Figure()
        for label, serie, color in [
            ("Pré-COVID", pre, "#4FC3F7"),
            ("Post-COVID", post, "#F4A926"),
        ]:
            fig.add_trace(go.Histogram(
                x=serie, name=label, opacity=0.7,
                marker_color=color, histnorm="probability density",
                nbinsx=60,
            ))
        fig.update_layout(
            barmode="overlay", title="Distribution de μₜ",
            xaxis_title="μₜ (%)", yaxis_title="Densité",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
            font=dict(color="#CCD6F6"),
        )
        st.plotly_chart(fig, use_container_width=True, key="d1_hist_t3")

    with sub4:
        if df_taux is None:
            no_data_msg("taux_journalier.xlsx")
        else:
            section_header("EURIBOR 3M hebdomadaire",
                           "Proxy du taux sans risque rₜ — Source : Banque nationale de Belgique")
            st.plotly_chart(interest_rate_chart(df_taux), use_container_width=True, key="d1_rate_t4")

            col1, col2, col3 = st.columns(3)
            col1.metric("Taux moyen", f"{df_taux['taux_clot'].mean():.3f}%")
            col2.metric("Taux min", f"{df_taux['taux_clot'].min():.3f}%")
            col3.metric("Taux max", f"{df_taux['taux_clot'].max():.3f}%")

            st.markdown("---")
            st.markdown("##### Aperçu des données")
            st.dataframe(
                df_taux[["Date", "Year", "Semaine", "taux_clot"]]
                .tail(20)
                .rename(columns={"taux_clot": "EURIBOR 3M (%)"}),
                hide_index=True, use_container_width=True,
            )
