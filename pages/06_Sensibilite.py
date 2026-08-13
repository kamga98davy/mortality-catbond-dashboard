"""Page 6 — Analyse de sensibilité aux primes de risque MPR (±20%)."""
from __future__ import annotations

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy import interpolate

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.sidebar import render_sidebar
from utils.data_loader import load_sensitivity, load_mpr
from utils.icons import icon
from utils.charts import sensitivity_bar, sensitivity_line

st.set_page_config(page_title="Sensibilité MPR", page_icon="🎯", layout="wide")
inject_css()
render_sidebar()

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


tab_comm, tab_tech = st.tabs(["  L'essentiel  ", "  Analyse technique  "])

# ── COMMERCIAL ─────────────────────────────────────────────────────────────────
with tab_comm:
    section_header("A quoi sert cette page ?",
                   "Tester la robustesse du prix calcule")

    st.markdown("""
<div class="prose" style="margin-bottom:1rem;">
  Une fois le prix de 6%/an calculé, une question naturelle se pose :
  <strong style="color:#E5E7EB">ce prix est-il fiable si certaines hypothèses changent légèrement ?</strong><br><br>
  Pour calibrer le prix sous la mesure risque-neutre Q, il faut estimer 5 "primes de risque" —
  notées ζ — qui représentent la rémunération exigée par le marché pour chaque source de risque
  (risque continu de taux, risque continu de mortalité, intensité des chocs, fréquence des chocs).
  Ces 5 primes sont calibrées sur 10 observations de marché : elles sont donc estimées avec une
  certaine incertitude.<br><br>
  Cette page teste : si chaque prime de risque varie de ±20% autour de sa valeur calibrée,
  le prix du bond change-t-il beaucoup ? Un bond bien construit reste proche de 100 même
  sous ces perturbations.
</div>
""", unsafe_allow_html=True)

    col_intro, col_legend = st.columns([1, 1], gap="large")
    with col_intro:
        section_header("Les 5 primes de risque testées")
        for sym, name, desc in [
            ("γ₁", "Prime risque de taux (continu)",
             "Rémunération pour le risque que le taux d'intérêt fluctue de façon continue"),
            ("γ₂", "Prime risque de mortalité (continu)",
             "Rémunération pour la volatilité quotidienne de la surmortalité"),
            ("κ₁", "Prime intensité des chocs (taux)",
             "Rémunération pour l'ampleur des sauts sur le taux d'intérêt"),
            ("κ₂", "Prime intensité des chocs (mortalité)",
             "Rémunération pour l'ampleur des chocs de mortalité — le plus important"),
            ("χ",  "Prime fréquence des chocs",
             "Rémunération pour la probabilité qu'un événement extrême survienne"),
        ]:
            st.markdown(f"""
<div style='display:flex;gap:.7rem;margin:.35rem 0;align-items:flex-start;'>
  <span style='color:#D97706;font-weight:700;font-size:.8rem;min-width:1.5rem;margin-top:.05rem;'>{sym}</span>
  <div>
    <span style='color:#E5E7EB;font-weight:600;font-size:.8rem;'>{name}</span><br>
    <span style='color:#6B7280;font-size:.73rem;'>{desc}</span>
  </div>
</div>
""", unsafe_allow_html=True)

    with col_legend:
        section_header("Résultat attendu")
        insight_box("""
<strong>Hiérarchie des primes de risque</strong><br><br>
Sur la base de Li et al. (2023), la prime de fréquence des chocs
<strong style="color:#E5E7EB">χ</strong> est généralement la plus influente :
changer la probabilité qu'un événement extrême survienne a le plus grand impact
sur le prix du bond.<br><br>
La prime <strong style="color:#E5E7EB">κ₂</strong> (intensité des chocs de mortalité)
arrive en second. Les primes de risque continu γ₁ et γ₂ ont un impact plus faible —
elles gouvernent le risque ordinaire, pas les scénarios catastrophes.
""")

    st.markdown("---")
    col_chart, col_read = st.columns([3, 1], gap="large")
    with col_chart:
        section_header("Amplitude de variation du prix selon la prime perturbée")
        if sens_df is not None:
            summary = (
                sens_df.groupby("param")["price"]
                .apply(lambda x: x.max() - x.min())
                .reset_index()
                .rename(columns={"price": "amplitude"})
            )
            summary["param_label"] = summary["param"].map(
                lambda p: PARAM_META.get(p, (p, p, "#D97706"))[0]
            )
            st.plotly_chart(sensitivity_bar(summary), use_container_width=True, key="sens_bar_exec")
        else:
            _placeholder_bar()

    with col_read:
        st.markdown("""
<div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
            border-radius:6px;padding:.9rem 1rem;margin-top:1.5rem;'>
  <div style='font-weight:600;color:#E5E7EB;font-size:.84rem;margin-bottom:.5rem;'>
    Lire ce graphique
  </div>
  <div style='color:#9CA3AF;font-size:.77rem;line-height:1.7;'>
    Chaque barre = variation maximale du prix quand une prime de risque varie de &plusmn;20%,
    toutes les autres primes restant fixes.<br><br>
    Barre haute = ce paramètre est déterminant.<br>
    Barre basse = le prix est robuste à ce paramètre.
  </div>
</div>
""", unsafe_allow_html=True)

# ── TECHNIQUE ──────────────────────────────────────────────────────────────────
with tab_tech:
    sub1, sub2 = st.tabs(["🎛️ Explorateur interactif", "📊 Tableau de synthèse"])

    with sub1:
        section_header("Sensibilité interactive du prix P₀",
                       "Sélectionne une composante MPR et explore son impact")

        if sens_df is None or mpr is None:
            st.info(
                "Les données de sensibilité ne sont pas encore générées. "
                "Lancez `source('export_for_streamlit.R')` dans R pour les produire. "
                "En attendant, le graphique indicatif dans l'onglet L'essentiel illustre la structure attendue.",
                icon="ℹ️",
            )
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
                    fig.add_trace(go.Scatter(
                        x=df_p["param_value"], y=df_p["price"],
                        mode="lines+markers", name=f"P₀({symbol})",
                        line=dict(color=color, width=2),
                        marker=dict(size=5, color=color),
                    ))
                    x_fine = np.linspace(lo, hi, 200)
                    y_fine = interp_fn(x_fine)
                    fig.add_trace(go.Scatter(
                        x=x_fine, y=y_fine, mode="lines", name="Interpolation cubic",
                        line=dict(color=color, width=1, dash="dot"),
                        showlegend=False,
                    ))
                    fig.add_trace(go.Scatter(
                        x=[selected], y=[est_price], mode="markers",
                        marker=dict(size=12, color="#FFFFFF", symbol="star"),
                        name="Valeur sélectionnée",
                    ))
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

    with sub2:
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
