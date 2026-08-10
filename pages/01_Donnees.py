"""Page 1 — Données : mortalité belge, GLM Poisson, surmortalité, taux d'intérêt."""
import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, insight_box, no_data_msg
from utils.sidebar import render_sidebar
from utils.data_loader import (
    load_mortality, load_interest_rate, compute_stats,
)
from utils.charts import (
    deaths_chart, glm_fit_chart, excess_mortality_chart,
    boxplot_covid, joint_chart, interest_rate_chart,
)

st.set_page_config(page_title="Données", page_icon="📊", layout="wide")
inject_css()

IS_EXEC = render_sidebar() == "Executive"
badge = '<span class="badge-exec">Executive</span>' if IS_EXEC else '<span class="badge-tech">Technique</span>'
st.markdown(f"{badge}", unsafe_allow_html=True)
st.title("Données — Mortalité belge & Taux d'intérêt")

# ── Load data ──────────────────────────────────────────────────────────────────
with st.spinner("Chargement des données et calibration GLM…"):
    df = load_mortality()
    df_taux = load_interest_rate()

if df is None:
    no_data_msg("mortalite_final.xlsx")
    st.stop()

# ── EXECUTIVE VIEW ─────────────────────────────────────────────────────────────
if IS_EXEC:
    section_header("La mortalité belge en chiffres",
                   "Évolution hebdomadaire des décès 2013–2024")

    st.plotly_chart(deaths_chart(df), use_container_width=True, key="d1_deaths_exec")

    pre  = df[df["periode"] == "Pré-COVID"]
    post = df[df["periode"] == "Post-COVID"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Décès/sem. moyen (pré-COVID)",
                f"{pre['deces'].mean():.0f}", help="Semaines 2013–2019")
    col2.metric("Décès/sem. moyen (post-COVID)",
                f"{post['deces'].mean():.0f}",
                delta=f"+{post['deces'].mean() - pre['deces'].mean():.0f}")
    col3.metric("Pic COVID (max hebdo)",
                f"{df['deces'].max():,.0f}", help="Printemps 2020")
    col4.metric("Semaines avec surmortalité > 0",
                f"{(df['mu_t'] > 0).mean() * 100:.1f}%")

    st.markdown("---")
    section_header("Impact COVID-19 sur la surmortalité",
                   "μₜ = (décès observés − décès attendus) / population × 100")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(excess_mortality_chart(df), use_container_width=True, key="d1_mu_exec")
    with col2:
        insight_box("""
<b>📌 Lecture du graphique</b><br><br>
<b>μₜ > 0</b> = plus de décès qu'attendu → surmortalité<br>
<b>μₜ < 0</b> = moins de décès qu'attendu<br><br>
Les pics de mars–mai 2020 et automne 2020 correspondent
aux premières vagues COVID, avec une surmortalité sans
précédent dans la période observée.
""")
        st.markdown("##### Comparaison pré/post-COVID")
        st.markdown(f"""
| | Pré-COVID | Post-COVID |
|---|---:|---:|
| Moyenne μₜ | `{pre['mu_t'].mean():.4f}` | `{post['mu_t'].mean():.4f}` |
| Écart-type | `{pre['mu_t'].std():.4f}` | `{post['mu_t'].std():.4f}` |
| Max μₜ | `{pre['mu_t'].max():.4f}` | `{post['mu_t'].max():.4f}` |
""")

# ── TECHNICAL VIEW ─────────────────────────────────────────────────────────────
else:
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Séries temporelles", "🔬 GLM Poisson & μₜ",
         "📊 Statistiques", "💹 Taux d'intérêt"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(deaths_chart(df, show_mean=True), use_container_width=True, key="d1_deaths_t1")
        with col2:
            st.plotly_chart(excess_mortality_chart(df), use_container_width=True, key="d1_mu_t1")

        if df_taux is not None:
            st.plotly_chart(joint_chart(df, df_taux), use_container_width=True, key="d1_joint_t1")
        else:
            no_data_msg("taux_journalier.xlsx")

    with tab2:
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

    with tab3:
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

    with tab4:
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
