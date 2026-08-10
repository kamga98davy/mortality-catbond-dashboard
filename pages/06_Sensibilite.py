"""Page 6 — Analyse de sensibilité aux primes de risque MPR (±20%)."""
from __future__ import annotations

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy import interpolate

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.data_loader import load_sensitivity, load_mpr
from utils.charts import sensitivity_bar, sensitivity_line

st.set_page_config(page_title="Sensibilité MPR", page_icon="🎯", layout="wide")
inject_css()

IS_EXEC = st.session_state.get("view", "Executive") == "Executive"
badge = '<span class="badge-exec">Executive</span>' if IS_EXEC else '<span class="badge-tech">Technique</span>'
st.markdown(f"{badge}", unsafe_allow_html=True)
st.title("Analyse de sensibilité — Primes de risque MPR")

sens_df = load_sensitivity()
mpr     = load_mpr()

PARAM_META = {
    "gamma1": ("γ₁", "MPR brownien taux",     "#F4A926"),
    "gamma2": ("γ₂", "MPR brownien mortalité","#64FFDA"),
    "kappa1": ("κ₁", "MPR saut taux",          "#4FC3F7"),
    "kappa2": ("κ₂", "MPR saut mortalité",      "#FF6B6B"),
    "chi":    ("χ",  "MPR fréquence sauts",     "#A78BFA"),
}


def _placeholder_bar() -> None:
    """Placeholder when no sensitivity data is available."""
    import pandas as pd
    dummy = pd.DataFrame({
        "param_label": ["γ₁", "γ₂", "κ₁", "κ₂", "χ"],
        "amplitude":   [1.5,  2.1,  3.2,  4.8,  6.1],
    })
    fig = go.Figure(go.Bar(
        x=dummy["param_label"], y=dummy["amplitude"],
        marker_color=["#F4A926", "#64FFDA", "#4FC3F7", "#FF6B6B", "#A78BFA"],
        text=[f"{v:.1f}" for v in dummy["amplitude"]], textposition="outside",
    ))
    fig.update_layout(
        title="Sensibilité indicative [données illustratives — export R requis]",
        xaxis_title="Composante MPR", yaxis_title="Amplitude ΔP₀ (indicative)",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
        font=dict(color="#CCD6F6"),
    )
    st.plotly_chart(fig, use_container_width=True, key="sens_placeholder_exec")
    st.caption("⚠️ Valeurs indicatives — remplacées par les résultats réels après export R.")

# ── EXECUTIVE VIEW ─────────────────────────────────────────────────────────────
if IS_EXEC:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Quelle prime de risque impacte le plus le prix du bond ?",
                       "Variation de ±20% autour de la valeur de référence ζ_S1")

        if sens_df is not None:
            summary = (
                sens_df.groupby("param")["price"]
                .apply(lambda x: x.max() - x.min())
                .reset_index()
                .rename(columns={"price": "amplitude"})
            )
            summary["param_label"] = summary["param"].map(
                lambda p: PARAM_META.get(p, (p, p, "#F4A926"))[0]
            )
            st.plotly_chart(sensitivity_bar(summary), use_container_width=True, key="sens_bar_exec")
        else:
            _placeholder_bar()

    with col2:
        section_header("Lecture du graphique")
        st.markdown("""
Chaque barre montre de **combien le prix P₀ varie** quand
on modifie une composante de la prime de risque de ±20%.

**Plus la barre est haute, plus ce facteur de risque
est déterminant pour le prix du bond.**
""")
        insight_box("""
<b>📊 Résultat attendu (analogue Li et al., Figs 5.8–5.10)</b><br><br>
• <b>χ (fréquence des sauts)</b> est généralement la composante
  la plus influente — changer la probabilité d'un événement extrême
  change fondamentalement la valeur du bond.<br><br>
• <b>κ₂ (saut mortalité)</b> est le second facteur — il capture
  l'intensité des chocs de mortalité extrêmes.<br><br>
• <b>γ₁, γ₂ (Browniens)</b> ont un impact plus faible —
  ils affectent le risque continu, pas les chocs extrêmes.
""")

# ── TECHNICAL VIEW ─────────────────────────────────────────────────────────────
else:
    tab1, tab2 = st.tabs(["🎛️ Explorateur interactif", "📊 Tableau de synthèse"])

    with tab1:
        section_header("Sensibilité interactive du prix P₀",
                       "Sélectionne une composante MPR et explore son impact")

        if sens_df is None or mpr is None:
            no_data_msg("sensitivity.csv / mpr.json")
            st.markdown("""
**Pour générer les données de sensibilité, exécute dans R :**
```r
source("export_for_streamlit.R")
```
L'export inclut les résultats précalculés de la section 5.3 (Rmd).
""")
        else:
            param_choice = st.selectbox(
                "Composante MPR à explorer",
                list(PARAM_META.keys()),
                format_func=lambda p: f"{PARAM_META[p][0]} — {PARAM_META[p][1]}",
            )
            symbol, desc, color = PARAM_META[param_choice]

            df_p = sens_df[sens_df["param"] == param_choice].sort_values("param_value")
            if df_p.empty:
                st.warning(f"Aucune donnée pour `{param_choice}` dans sensitivity.csv.")
            else:
                ref_val = mpr.get(param_choice, df_p["param_value"].mean())

                interp_fn = interpolate.interp1d(
                    df_p["param_value"], df_p["price"],
                    kind="cubic", fill_value="extrapolate",
                )

                col_slider, col_chart = st.columns([1, 3])
                with col_slider:
                    pct_range = 0.20
                    lo = float(df_p["param_value"].min())
                    hi = float(df_p["param_value"].max())
                    selected = st.slider(
                        f"{symbol} ({desc})",
                        min_value=lo, max_value=hi,
                        value=float(ref_val), step=(hi - lo) / 100,
                        format="%.4f",
                    )
                    est_price = float(interp_fn(selected))
                    delta_pct = (est_price - 100) / 100 * 100
                    st.metric("P₀ estimé", f"{est_price:.3f}",
                              delta=f"{delta_pct:+.2f}% vs pair",
                              delta_color="inverse")
                    st.metric("Valeur de référence", f"{ref_val:.4f}")
                    st.metric("Écart relatif", f"{(selected - ref_val) / abs(ref_val) * 100:+.1f}%")

                with col_chart:
                    fig = go.Figure()
                    # Pre-computed curve
                    fig.add_trace(go.Scatter(
                        x=df_p["param_value"], y=df_p["price"],
                        mode="lines+markers", name=f"P₀({symbol})",
                        line=dict(color=color, width=2),
                        marker=dict(size=5, color=color),
                    ))
                    # Smooth interpolation
                    x_fine = np.linspace(lo, hi, 200)
                    y_fine = interp_fn(x_fine)
                    fig.add_trace(go.Scatter(
                        x=x_fine, y=y_fine, mode="lines", name="Interpolation cubic",
                        line=dict(color=color, width=1, dash="dot"),
                        showlegend=False,
                    ))
                    # Selected point
                    fig.add_trace(go.Scatter(
                        x=[selected], y=[est_price], mode="markers",
                        marker=dict(size=12, color="#FFFFFF", symbol="star"),
                        name=f"Valeur sélectionnée",
                    ))
                    # Reference lines
                    fig.add_vline(x=ref_val,
                                  line=dict(color="#64FFDA", dash="dash", width=1.5),
                                  annotation_text=f"Réf. = {ref_val:.4f}",
                                  annotation_position="top right")
                    fig.add_hline(y=100,
                                  line=dict(color="#8892B0", dash="dot", width=1),
                                  annotation_text="Par (100)",
                                  annotation_position="bottom right")
                    fig.update_layout(
                        title=f"Sensibilité de P₀ à {symbol} (±20% autour de la référence)",
                        xaxis_title=f"{symbol} — {desc}",
                        yaxis_title="Prix du bond P₀",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0A1628",
                        font=dict(color="#CCD6F6"),
                        hovermode="x unified",
                        legend=dict(bgcolor="rgba(0,0,0,0)"),
                    )
                    st.plotly_chart(fig, use_container_width=True, key="sens_interactive_tech")

        st.markdown("---")
        section_header("Méthode (Section 5.3 de Li et al.)")
        st.markdown("""
**Protocole CRN (Common Random Numbers) :**

Pour chaque composante $\\zeta_j \\in \\{\\gamma_1, \\gamma_2, \\kappa_1, \\kappa_2, \\chi\\}$,
on fait varier $\\zeta_j$ de $\\pm 20\\%$ autour de $\\zeta_{j}^{S1}$ en 10 points,
**toutes les autres composantes fixes**, avec $N = 20\\,000$ trajectoires Monte Carlo.

$$P_0(\\zeta_j) = \\hat{\\mathbb{E}}^Q\\!\\left[\\sum_{k} e^{-\\int_0^{t_k} r_s ds} c^* \\Delta \\mathrm{PRF}_{t_k} + e^{-\\int_0^T r_s ds} K \\mathrm{PRF}_T\\right]$$

**Élasticité de $\\chi$ :**
$$\\text{Elasticité}(\\chi) = \\frac{\\Delta P_0 / P_0}{\\Delta \\chi / |\\chi|}$$
""")

    with tab2:
        section_header("Tableau de synthèse des amplitudes",
                       "Analogue Table 5.x — variation ±20% de chaque composante MPR")

        if sens_df is not None:
            rows = []
            for param, (sym, desc, _) in PARAM_META.items():
                df_p = sens_df[sens_df["param"] == param]
                if df_p.empty:
                    continue
                amp   = df_p["price"].max() - df_p["price"].min()
                pmin  = df_p["price"].min()
                pmax  = df_p["price"].max()
                p_ref = mpr.get(param) if mpr else None
                rows.append({
                    "Composante": sym, "Description": desc,
                    "Valeur réf.": f"{p_ref:.4f}" if p_ref else "—",
                    "P₀ min": f"{pmin:.3f}",
                    "P₀ max": f"{pmax:.3f}",
                    "Amplitude ΔP₀": f"{amp:.3f}",
                    "Plage testée": f"[{df_p['param_value'].min():.4f}, {df_p['param_value'].max():.4f}]",
                })
            if rows:
                st.dataframe(
                    __import__("pandas").DataFrame(rows),
                    hide_index=True, use_container_width=True,
                )
        else:
            no_data_msg("sensitivity.csv")


