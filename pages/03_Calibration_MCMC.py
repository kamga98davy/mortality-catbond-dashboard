"""Page 3 — Calibration MCMC Metropolis-Hastings."""
import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.data_loader import (
    load_mcmc_summary, load_mcmc_chains, load_params_postC, load_params_preC,
    corr_instantanee,
)
from utils.charts import trace_plot

st.set_page_config(page_title="Calibration MCMC", page_icon="⚙️", layout="wide")
inject_css()

IS_EXEC = st.session_state.get("view", "Executive") == "Executive"
badge = '<span class="badge-exec">Executive</span>' if IS_EXEC else '<span class="badge-tech">Technique</span>'
st.markdown(f"{badge}", unsafe_allow_html=True)
st.title("Calibration MCMC — Metropolis-Hastings")

# ── EXECUTIVE VIEW ─────────────────────────────────────────────────────────────
if IS_EXEC:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Qu'est-ce que la calibration MCMC ?",
                       "Metropolis-Hastings — Inférence bayésienne sur les paramètres")
        st.markdown("""
Le **MCMC (Monte Carlo par Chaînes de Markov)** est une méthode pour
estimer les 13 paramètres du modèle AJD directement à partir des données
belges observées, sans supposer de distribution a priori.

**Principe :**
1. On part d'un jeu de paramètres initial
2. On propose une petite modification aléatoire
3. On accepte ou rejette selon que les données deviennent plus ou moins vraisemblables
4. Après **30 000 itérations**, la distribution empirique des paramètres retenus
   approche la distribution **posteriori** exacte

**Deux calibrations** ont été réalisées :
- **Pré-COVID (2017–2019)** : comportement "normal" de la mortalité belge
- **Post-COVID (2017–2022)** : dynamiques après la pandémie
""")

    with col2:
        section_header("Résultat clé — Impact de la pandémie")
        insight_box("""
<b>🔴 Avant la pandémie (2017–2019)</b><br>
λ ≈ faible → sauts rares<br>
σ₂ ≈ faible → μₜ peu volatile<br><br>
<b>🟡 Après la pandémie (2017–2022)</b><br>
λ augmente → sauts plus fréquents<br>
σ₂ augmente → μₜ plus volatile<br>
ν₂ augmente → chocs de mortalité plus intenses<br><br>
➡ La pandémie a <b>fondamentalement changé</b> la dynamique
de mortalité belge. Le modèle le capte clairement.
""")

    st.markdown("---")
    section_header("Comparaison pré / post-COVID",
                   "Paramètres de mortalité — Changement structurel")

    params_pre  = load_params_preC()
    params_post = load_params_postC()

    if params_pre and params_post:
        param_labels = {
            "m2": "m₂ (drift mortalité)", "d2": "d₂ (mean-reversion)",
            "sigma2": "σ₂ (volatilité diff.)", "lambda": "λ (fréq. sauts)",
            "v2": "ν₂ (saut moyen mort.)", "phi2": "φ₂ (écart-type saut)",
            "rho1": "ρ₁ (corr. brownienne)", "rho2": "ρ₂ (corr. sauts)",
        }
        rows = []
        for k, label in param_labels.items():
            pre_v  = params_pre.get(k, params_pre.get(k.replace("sigma", "s").replace("lambda", "lam"), None))
            post_v = params_post.get(k, params_post.get(k.replace("sigma", "s").replace("lambda", "lam"), None))
            if pre_v is not None and post_v is not None:
                delta = post_v - pre_v
                pct   = delta / abs(pre_v) * 100 if pre_v != 0 else float("nan")
                rows.append({
                    "Paramètre": label,
                    "Pré-COVID": f"{pre_v:.5f}",
                    "Post-COVID": f"{post_v:.5f}",
                    "Δ": f"{delta:+.5f}",
                    "Δ%": f"{pct:+.1f}%",
                })
        if rows:
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    else:
        no_data_msg("params_postC.json / params_preC.json")

# ── TECHNICAL VIEW ─────────────────────────────────────────────────────────────
else:
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Résultats post-COVID", "📊 Résultats pré-COVID",
         "📈 Traceplots (échantillon)", "🔢 Diagnostics"])

    with tab1:
        section_header("Paramètres estimés — Données 2017–2022",
                       "Médiane a posteriori avec intervalles de crédibilité 95%")
        mcmc_post = load_mcmc_summary("postC")
        if mcmc_post is not None:
            st.dataframe(
                mcmc_post.style.format({
                    "mean": "{:.5f}", "sd": "{:.5f}",
                    "ci_025": "{:.5f}", "ci_975": "{:.5f}",
                    "ESS": "{:.0f}",
                }),
                hide_index=True, use_container_width=True,
            )
            params = load_params_postC()
            if params:
                corr = corr_instantanee(params)
                st.metric("Corrélation instantanée corr(drₜ, dμₜ)", f"{corr:.4f}")
        else:
            no_data_msg("mcmc_summary_postC.csv")

    with tab2:
        section_header("Paramètres estimés — Données pré-COVID 2017–2019",
                       "Analogue Table 4.2 de Li et al. (2023)")
        mcmc_pre = load_mcmc_summary("preC")
        if mcmc_pre is not None:
            st.dataframe(
                mcmc_pre.style.format({
                    "mean": "{:.5f}", "sd": "{:.5f}",
                    "ci_025": "{:.5f}", "ci_975": "{:.5f}",
                    "ESS": "{:.0f}",
                }),
                hide_index=True, use_container_width=True,
            )
        else:
            no_data_msg("mcmc_summary_preC.csv")

        params_pre  = load_params_preC()
        params_post = load_params_postC()
        if params_pre and params_post:
            st.markdown("---")
            section_header("Tableau comparatif complet — Pré vs Post-COVID")
            param_names = [
                ("m1","m₁"), ("d1","d₁"), ("sigma1","σ₁"),
                ("m2","m₂"), ("d2","d₂"), ("sigma2","σ₂"),
                ("rho1","ρ₁"), ("lambda","λ"),
                ("v1","ν₁"), ("v2","ν₂"), ("phi1","φ₁"), ("phi2","φ₂"), ("rho2","ρ₂"),
            ]
            rows = []
            for k, label in param_names:
                pre_v  = params_pre.get(k)
                post_v = params_post.get(k)
                if pre_v is None or post_v is None:
                    continue
                rows.append({
                    "Paramètre": label, "Pré-COVID": f"{pre_v:.5f}",
                    "Post-COVID": f"{post_v:.5f}",
                    "Δ": f"{post_v - pre_v:+.5f}",
                })
            if rows:
                st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    with tab3:
        chains = load_mcmc_chains("postC")
        if chains is not None:
            st.markdown("**Traceplots — Modèle post-COVID (2017–2022) · 1 000 itérations thinned**")
            param_labels = {
                "m1": "m₁", "d1": "d₁", "sigma1": "σ₁",
                "m2": "m₂", "d2": "d₂", "sigma2": "σ₂",
                "rho1": "ρ₁", "lambda": "λ",
                "v1": "ν₁", "v2": "ν₂", "phi1": "φ₁", "phi2": "φ₂", "rho2": "ρ₂",
            }
            cols = st.columns(2)
            for i, (param, label) in enumerate(param_labels.items()):
                if param in chains.columns:
                    with cols[i % 2]:
                        st.plotly_chart(trace_plot(chains, param, label),
                                        use_container_width=True)
        else:
            no_data_msg("mcmc_chains_postC.csv")

    with tab4:
        section_header("Diagnostics de convergence")
        mcmc_post = load_mcmc_summary("postC")
        if mcmc_post is not None and "ESS" in mcmc_post.columns:
            import plotly.graph_objects as go
            fig = go.Figure(go.Bar(
                x=mcmc_post["param"],
                y=mcmc_post["ESS"],
                marker_color=["#F4A926" if v >= 100 else "#FF6B6B"
                              for v in mcmc_post["ESS"]],
                text=[f"{v:.0f}" for v in mcmc_post["ESS"]],
                textposition="outside",
            ))
            fig.add_hline(y=100, line=dict(color="#64FFDA", dash="dash"),
                          annotation_text="ESS minimum recommandé (100)",
                          annotation_position="bottom right")
            fig.update_layout(
                title="Effective Sample Size (ESS) par paramètre",
                xaxis_title="Paramètre", yaxis_title="ESS",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
                font=dict(color="#CCD6F6"),
            )
            st.plotly_chart(fig, use_container_width=True)

            warning_box("""
<b>Rappel :</b> ESS &gt; 100 est considéré acceptable pour l'inférence.
Un ESS élevé indique une bonne exploration de la distribution posteriori par la chaîne.
Paramètres en rouge (ESS &lt; 100) peuvent nécessiter un run plus long ou un tuning des propositions.
""")
        else:
            no_data_msg("mcmc_summary_postC.csv (colonne ESS)")

        st.markdown("""
---
**Paramètres d'implémentation MCMC :**
- Algorithme : Metropolis-Hastings Random Walk
- Itérations : 30 000 (burn-in : 15 000, n_iter effectif : 15 000)
- Propositions : distribution normale multivariée (sds adaptatifs)
- Priors : sur λ et ρ₁ pour assurer l'identifiabilité
- Logiciel : R, implémentation manuelle
""")
