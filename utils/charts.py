"""Plotly chart factory for the mortality CAT bond dashboard."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

GOLD  = "#F4A926"
TEAL  = "#64FFDA"
BLUE  = "#4FC3F7"
RED   = "#FF6B6B"
MUTED = "#8892B0"
BG    = "#0A1628"
GRID  = "rgba(255,255,255,0.06)"

_BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=BG,
    font=dict(family="sans-serif", color="#CCD6F6", size=12),
    margin=dict(l=50, r=30, t=50, b=50),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED)),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED)),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID, borderwidth=1),
    hovermode="x unified",
)


def _fig(**overrides) -> go.Figure:
    layout = {**_BASE_LAYOUT, **overrides}
    return go.Figure(layout=go.Layout(**layout))


# ── Mortality charts ───────────────────────────────────────────────────────────

def deaths_chart(df: pd.DataFrame, *, show_mean: bool = True) -> go.Figure:
    fig = _fig(title="Décès hebdomadaires en Belgique (2013–2024)")
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["deces"], name="Décès observés",
        line=dict(color=BLUE, width=1.2), mode="lines",
    ))
    if show_mean:
        m = df["deces"].mean()
        fig.add_hline(y=m, line=dict(color=MUTED, dash="dash", width=1),
                      annotation_text=f"Moy. = {m:.0f}", annotation_position="bottom right")
    # COVID marker
    fig.add_vline(x="2020-03-11", line=dict(color=RED, dash="dot", width=1.5))
    fig.add_annotation(x="2020-03-11", y=1, yref="paper",
                       text="COVID-19<br>mars 2020", showarrow=False,
                       xanchor="left", xshift=6,
                       font=dict(color=RED, size=10))
    fig.update_layout(xaxis_title="Date", yaxis_title="Décès / semaine")
    return fig


def excess_mortality_chart(df: pd.DataFrame) -> go.Figure:
    pre  = df[df["periode"] == "Pré-COVID"]
    post = df[df["periode"] == "Post-COVID"]
    fig = _fig(title="Surmortalité hebdomadaire μₜ (%)")
    fig.add_trace(go.Scatter(
        x=pre["Date"], y=pre["mu_t"], name="Pré-COVID",
        line=dict(color=BLUE, width=1), mode="lines"))
    fig.add_trace(go.Scatter(
        x=post["Date"], y=post["mu_t"], name="Post-COVID",
        line=dict(color=GOLD, width=1.3), mode="lines"))
    fig.add_hline(y=0, line=dict(color=MUTED, width=0.8))
    fig.add_vline(x="2020-03-11", line=dict(color=RED, dash="dot", width=1.5))
    fig.update_layout(xaxis_title="Date", yaxis_title="μₜ (%)",
                      legend=dict(x=0.01, y=0.99))
    return fig


def glm_fit_chart(df: pd.DataFrame) -> go.Figure:
    fig = _fig(title="Décès observés vs décès attendus (GLM Poisson)")
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["deces"], name="Observés",
        line=dict(color=BLUE, width=1.2), mode="lines"))
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["deces_attendus"], name="Attendus (GLM)",
        line=dict(color=GOLD, dash="dash", width=1.5), mode="lines"))
    fig.add_vline(x="2020-03-11", line=dict(color=RED, dash="dot", width=1.2))
    fig.update_layout(xaxis_title="Date", yaxis_title="Décès / semaine")
    return fig


def boxplot_covid(df: pd.DataFrame) -> go.Figure:
    fig = _fig(title="Distribution de μₜ — Pré vs Post-COVID")
    for periode, color in [("Pré-COVID", BLUE), ("Post-COVID", GOLD)]:
        sub = df[df["periode"] == periode]["mu_t"].dropna()
        fig.add_trace(go.Box(
            y=sub, name=periode, marker_color=color,
            line_color=color, fillcolor=color.replace("#", "#33") if False else "rgba(0,0,0,0)",
            boxmean=True,
        ))
    fig.add_hline(y=0, line=dict(color=MUTED, dash="dash", width=0.8))
    fig.update_layout(yaxis_title="μₜ (%)", showlegend=True)
    return fig


def joint_chart(df_mort: pd.DataFrame, df_taux: pd.DataFrame) -> go.Figure:
    merged = df_mort.merge(df_taux[["Year", "Semaine", "taux_clot"]],
                           on=["Year", "Semaine"], how="inner")
    fig = _fig(title="Surmortalité μₜ et taux EURIBOR 3M (2016–2024)")
    fig.add_trace(go.Scatter(
        x=merged["Date"], y=merged["mu_t"], name="Surmortalité μₜ",
        line=dict(color=RED, width=1.2), mode="lines", yaxis="y"))
    fig.add_trace(go.Scatter(
        x=merged["Date"], y=merged["taux_clot"], name="EURIBOR 3M (%)",
        line=dict(color=BLUE, dash="dot", width=1.2), mode="lines", yaxis="y2"))
    fig.update_layout(
        yaxis=dict(title="μₜ (%)", gridcolor=GRID, tickfont=dict(color=RED)),
        yaxis2=dict(title="Taux (%)", overlaying="y", side="right",
                    gridcolor="rgba(0,0,0,0)", tickfont=dict(color=BLUE)),
        legend=dict(x=0.01, y=0.99),
    )
    return fig


def interest_rate_chart(df: pd.DataFrame) -> go.Figure:
    fig = _fig(title="Taux EURIBOR 3M hebdomadaire (2016–2024)")
    fig.add_trace(go.Scatter(
        x=df["Date"], y=df["taux_clot"], name="EURIBOR 3M",
        line=dict(color=BLUE, width=1.3), mode="lines",
        fill="tozeroy", fillcolor="rgba(79,195,247,0.08)"))
    fig.add_hline(y=0, line=dict(color=MUTED, dash="dash", width=0.8))
    fig.update_layout(xaxis_title="Date", yaxis_title="Taux (%)")
    return fig


# ── Exceedance curve ───────────────────────────────────────────────────────────

def exceedance_chart(df: pd.DataFrame, seuils: dict, *, executive: bool = False) -> go.Figure:
    a_BE = seuils.get("a_BE", seuils.get("a"))
    b_BE = seuils.get("b_BE", seuils.get("b"))
    p_att = seuils.get("p_att", 1.16)
    p_exh = seuils.get("p_exh", 0.74)

    fig = _fig(title="Courbe d'exceedance de μ* — Belgique (analogue Fig. 5.3)")
    fig.add_trace(go.Scatter(
        x=df["seuil"], y=df["prob_pct"], name="P(μ* > s)",
        line=dict(color=WHITE if not executive else GOLD, width=2), mode="lines",
    ))
    # Attachment
    fig.add_hline(y=p_att, line=dict(color=BLUE, dash="dash", width=1.5))
    fig.add_vline(x=a_BE, line=dict(color=BLUE, dash="dot", width=1.2))
    if not executive:
        fig.add_annotation(x=a_BE, y=p_att, xanchor="left", yanchor="bottom",
                           text=f"Attachment<br>a_BE = {a_BE:.4f}<br>P = {p_att:.2f}%",
                           showarrow=False, font=dict(color=BLUE, size=10),
                           bgcolor="rgba(10,22,40,0.8)")
    # Exhaustion
    fig.add_hline(y=p_exh, line=dict(color=RED, dash="dash", width=1.5))
    fig.add_vline(x=b_BE, line=dict(color=RED, dash="dot", width=1.2))
    if not executive:
        fig.add_annotation(x=b_BE, y=p_exh, xanchor="right", yanchor="top",
                           text=f"Exhaustion<br>b_BE = {b_BE:.4f}<br>P = {p_exh:.2f}%",
                           showarrow=False, font=dict(color=RED, size=10),
                           bgcolor="rgba(10,22,40,0.8)")
    # Shaded zone
    df_zone = df[(df["seuil"] >= min(a_BE, b_BE)) & (df["seuil"] <= max(a_BE, b_BE))]
    if len(df_zone) > 0:
        fig.add_trace(go.Scatter(
            x=pd.concat([df_zone["seuil"], df_zone["seuil"][::-1]]),
            y=pd.concat([df_zone["prob_pct"], pd.Series([p_exh] * len(df_zone))]),
            fill="toself", fillcolor="rgba(244,169,38,0.12)",
            line=dict(width=0), name="Zone de perte partielle", showlegend=True,
        ))
    fig.update_layout(xaxis_title="Seuil s", yaxis_title="P(μ* > s)  [%]",
                      legend=dict(x=0.01, y=0.99))
    return fig


# ── MCMC trace plot ────────────────────────────────────────────────────────────

def trace_plot(chains_df: pd.DataFrame, param: str, label: str) -> go.Figure:
    series = chains_df[param]
    fig = _fig(title=f"Trace — {label}")
    fig.add_trace(go.Scatter(
        y=series, mode="lines", name=label,
        line=dict(color=BLUE, width=0.8)))
    fig.add_hline(y=series.mean(), line=dict(color=GOLD, dash="dash", width=1.2),
                  annotation_text=f"Moy. = {series.mean():.5f}",
                  annotation_position="right")
    fig.update_layout(xaxis_title="Itération", yaxis_title=label,
                      margin=dict(l=40, r=40, t=40, b=30))
    return fig


# ── Sensitivity charts ─────────────────────────────────────────────────────────

def sensitivity_bar(summary_df: pd.DataFrame) -> go.Figure:
    colors = [GOLD, TEAL, BLUE, RED, "#A78BFA"]
    fig = _fig(title="Impact des primes de risque MPR sur le prix P₀ (±20%)")
    fig.add_trace(go.Bar(
        x=summary_df["param_label"],
        y=summary_df["amplitude"],
        marker_color=colors[:len(summary_df)],
        text=[f"{v:.3f}" for v in summary_df["amplitude"]],
        textposition="outside",
    ))
    fig.update_layout(xaxis_title="Composante MPR (ζ)",
                      yaxis_title="Amplitude ΔP₀ (variation ±20%)",
                      showlegend=False)
    return fig


def sensitivity_line(df_param: pd.DataFrame, ref_value: float,
                     ref_price: float, label: str) -> go.Figure:
    fig = _fig(title=f"Sensibilité du prix P₀ à {label}")
    fig.add_trace(go.Scatter(
        x=df_param["param_value"], y=df_param["price"],
        mode="lines+markers", name=f"P₀({label})",
        line=dict(color=GOLD, width=2),
        marker=dict(size=5, color=GOLD),
    ))
    fig.add_vline(x=ref_value, line=dict(color=TEAL, dash="dash", width=1.5),
                  annotation_text=f"Référence = {ref_value:.4f}",
                  annotation_position="top right")
    fig.add_hline(y=100, line=dict(color=MUTED, dash="dot", width=1),
                  annotation_text="P₀ = 100 (par)", annotation_position="bottom right")
    fig.update_layout(xaxis_title=label, yaxis_title="Prix P₀")
    return fig


WHITE = "#CCD6F6"
