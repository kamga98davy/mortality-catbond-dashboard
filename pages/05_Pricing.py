"""Page 5 — Pricing & Scénarios (MPR, S1/S2/S3)."""
import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.sidebar import render_sidebar
from utils.data_loader import load_mpr, load_seuils, load_etats
from utils.icons import icon

st.set_page_config(page_title="Pricing & Scénarios", page_icon="💰", layout="wide")
inject_css()
render_sidebar()

st.title("Pricing & Scénarios")

mpr    = load_mpr()
seuils = load_seuils()

tab_comm, tab_tech = st.tabs(["👔  Vue Commerciale", "🔬  Vue Technique"])

# ── COMMERCIAL ─────────────────────────────────────────────────────────────────
with tab_comm:
    section_header("Qu'est-ce que le pricing ?",
                   "Trouver le coupon d'équilibre entre l'investisseur et l'assureur")

    st.markdown("""
<div class="prose" style="margin-bottom:1.1rem;">
  Le pricing répond à une question simple :
  <strong style="color:#E5E7EB">combien faut-il verser à l'investisseur chaque trimestre
  pour qu'il accepte de porter le risque de surmortalité catastrophique belge ?</strong><br><br>
  La réponse n'est pas arbitraire. Elle sort d'une équation d'équilibre : le prix du bond
  doit être exactement 100 (au pair) quand on actualise tous les flux futurs sous la
  probabilité risque-neutre Q. La valeur du coupon qui satisfait cette condition est 6%/an.
</div>
""", unsafe_allow_html=True)

    col_meca, col_struct = st.columns([1, 1], gap="large")

    with col_meca:
        section_header("Mécanisme du bond en trois cas")
        for dot, case, expl in [
            ("#22C55E", "Scénario normal (probabilité 98,84%)",
             "La surmortalité reste sous le seuil d'activation. L'investisseur reçoit "
             "tous ses coupons trimestriels (6%/an) et récupère 100% de son capital à maturité."),
            ("#D97706", "Activation partielle (entre les deux seuils)",
             "La surmortalité a dépassé le premier seuil mais pas le second. "
             "L'investisseur perd une fraction de son capital — proportionnelle à l'intensité du choc."),
            ("#EF4444", "Perte totale (probabilité 0,74%)",
             "La surmortalité a dépassé le seuil d'exhaustion. L'investisseur perd 100% de son capital. "
             "Pour l'assureur, c'est une couverture totale du scénario catastrophe."),
        ]:
            st.markdown(f"""
<div style='display:flex;gap:.8rem;margin:.5rem 0;align-items:flex-start;'>
  <div style='width:8px;height:8px;border-radius:50%;background:{dot};
              flex-shrink:0;margin-top:.4rem;'></div>
  <div>
    <div style='font-weight:600;color:#E5E7EB;font-size:.84rem;margin-bottom:.2rem;'>{case}</div>
    <div style='color:#9CA3AF;font-size:.78rem;line-height:1.6;'>{expl}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    with col_struct:
        section_header("Structure du bond calibré")
        p_s1 = mpr.get("P0_S1", 100.0) if mpr else 100.0
        st.markdown(f"""
<div style='display:grid;grid-template-columns:1fr 1fr;gap:.6rem;margin-top:.4rem;'>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;'>
    <div style='font-size:1.5rem;font-weight:700;color:#D97706;'>6,0%</div>
    <div style='color:#6B7280;font-size:.69rem;'>Coupon annuel</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;'>
    <div style='font-size:1.5rem;font-weight:700;color:#D97706;'>5,25 ans</div>
    <div style='color:#6B7280;font-size:.69rem;'>Maturité</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;'>
    <div style='font-size:1.5rem;font-weight:700;color:#D97706;'>1,16%</div>
    <div style='color:#6B7280;font-size:.69rem;'>Prob. activation</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;'>
    <div style='font-size:1.5rem;font-weight:700;color:#EF4444;'>0,74%</div>
    <div style='color:#6B7280;font-size:.69rem;'>Prob. perte totale</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;'>
    <div style='font-size:1.5rem;font-weight:700;color:#D97706;'>0,92%</div>
    <div style='color:#6B7280;font-size:.69rem;'>Perte attendue</div>
  </div>
  <div style='background:#1A1D27;border:1px solid rgba(255,255,255,.07);
              border-radius:6px;padding:.7rem .9rem;border-left:2px solid #D97706;'>
    <div style='font-size:1.5rem;font-weight:700;color:#D97706;'>6,5x</div>
    <div style='color:#6B7280;font-size:.69rem;'>Coupon / perte attendue</div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    section_header("Pourquoi trois scénarios ?",
                   "Tester la robustesse du prix selon le contexte de risque")

    st.markdown("""
<div class="prose" style="margin-bottom:.8rem;">
  Le prix du bond dépend des hypothèses sur la dynamique de mortalité (pre ou post-COVID)
  et sur les seuils d'activation (calibrés à quelle période ?). Les trois scénarios
  testent ce que le prix deviendrait si ces hypothèses changeaient.
</div>
""", unsafe_allow_html=True)

    p_s1 = mpr.get("P0_S1", 100.0) if mpr else 100.0
    p_s3 = mpr.get("P0_S3", 100.0) if mpr else 100.0
    st.markdown(f"""
<div class="scenario-row">
  <div class="scenario-card">
    <div class="scenario-title">S1 — Scénario de référence</div>
    <div class="scenario-price">P₀ = {p_s1:.1f}</div>
    <div class="scenario-desc">
      Dynamiques post-COVID + seuils post-COVID.<br>
      Le bond est au pair : le coupon de 6% est le prix juste.
      C'est le scénario recommandé pour une émission aujourd'hui.
    </div>
  </div>
  <div class="scenario-card s2">
    <div class="scenario-title">S2 — Monde sans COVID</div>
    <div class="scenario-price s2">P₀ &gt; 100</div>
    <div class="scenario-desc">
      Dynamiques pré-COVID + seuils pré-COVID.<br>
      Si la pandémie n'avait pas eu lieu, 6%/an serait trop généreux
      — le bond vaudrait plus que 100. Sert de référence contrefactuelle.
    </div>
  </div>
  <div class="scenario-card s3">
    <div class="scenario-title">S3 — Seuils obsolètes</div>
    <div class="scenario-price s3">P₀ = {p_s3:.1f}</div>
    <div class="scenario-desc">
      Dynamiques post-COVID + seuils pré-COVID.<br>
      L'émetteur utilise des seuils non recalibrés depuis 2019.
      L'investisseur porte plus de risque qu'il ne croit : un signal d'alerte.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    insight_box("""
<strong>Le message operationnel du scenario S3</strong><br>
Si un assureur belge n'a pas mis à jour ses seuils de mortalité depuis 2019, il est
structurellement en situation S3. Son CAT bond sous-tarifie le risque réel.
Ce travail fournit la méthodologie pour détecter et corriger cet écart.
""")

# ── TECHNIQUE ──────────────────────────────────────────────────────────────────
with tab_tech:
    sub1, sub2, sub3, sub4 = st.tabs(
        ["💰 Formule de pricing", "🎯 Vecteur MPR ζ", "📋 États de calibration", "📊 Scénarios S1/S2/S3"])

    with sub1:
        section_header("Formule de pricing — Équation (3.1)")
        st.latex(r"""
P_0 = \mathbb{E}^Q\!\left[
\sum_{k=1}^{T/\Delta} e^{-\int_0^{t_k} r_s\,ds}\,c^*\,\Delta\,\mathrm{PRF}_{t_k}
+ e^{-\int_0^T r_s\,ds}\,K\,\mathrm{PRF}_T
\right]
""")
        st.markdown("""
**Paramètres du bond :**

| Paramètre | Valeur |
|:---|---:|
| Coupon annuel $c^*$ | 6% |
| Pas trimestriel $\\Delta$ | 0,25 an |
| Horizon $T$ | 5,25 ans |
| Principal $K$ | 100 |
| Nombre de pas | 21 |

**Principal Recovery Factor (PRF) :**
""")
        st.latex(r"""
\mathrm{PRF}_{t_k} = 1 - \frac{(\mu^* - a)_+ - (\mu^* - b)_+}{b-a},
\qquad \mu^* = \max_{0\leq s \leq t_k} \mu_s
""")
        st.markdown("""
- $\\mu^* \\leq a$ : PRF = 1 → coupon et principal complets
- $a < \\mu^* < b$ : PRF ∈ (0,1) → perte partielle proportionnelle
- $\\mu^* \\geq b$ : PRF = 0 → perte totale du principal

**Estimation Monte Carlo :** $N = 10\\,000$ trajectoires sous $Q$
""")

    with sub2:
        section_header("Calibration du vecteur MPR ζ",
                       "Moindres carrés sur 10 spreads trimestriels Vita Capital IV D-5 (2011–2015)")
        st.latex(r"""
\hat{\zeta} = \arg\min_{\zeta}\;
\sum_{k=1}^{10} \left[P^{\text{model}}_0(t_k;\,\zeta) - 100\right]^2
""")
        st.markdown("""
**Algorithme d'optimisation :** NEWUOA (Li et al.) puis Nelder-Mead
**Point de départ :** ζ₀ = (0,100 ; 0,212 ; 0,178 ; 0,253 ; 0,021)
""")

        if mpr:
            st.markdown("---")
            section_header("Résultats MPR — Vecteur ζ estimé")
            li_vals = [0.100, 0.212, 0.178, 0.253, 0.021]
            be_vals = [mpr.get("gamma1"), mpr.get("gamma2"),
                       mpr.get("kappa1"), mpr.get("kappa2"), mpr.get("chi")]
            s3_vals = [mpr.get("gamma1_S3"), mpr.get("gamma2_S3"),
                       mpr.get("kappa1_S3"), mpr.get("kappa2_S3"), mpr.get("chi_S3")]
            labels = ["γ₁ (Brownien taux)", "γ₂ (Brownien mort.)",
                      "κ₁ (Saut taux)", "κ₂ (Saut mort.)", "χ (Fréq. sauts)"]
            rows = []
            for i, label in enumerate(labels):
                row = {"Composante": label,
                       "Li et al. S1": f"{li_vals[i]:.3f}",
                       "Belgique S1": f"{be_vals[i]:.3f}" if be_vals[i] else "—",
                       "Belgique S3": f"{s3_vals[i]:.3f}" if s3_vals[i] else "—"}
                rows.append(row)
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

            if mpr.get("SSE"):
                st.metric("SSE de calibration (S1)", f"{mpr['SSE']:.6f}")
        else:
            no_data_msg("mpr.json")

    with sub3:
        section_header("États trimestriels de calibration",
                       "Vita Capital IV D-5 — 10 observations 2011–2015 (Lane Financial LLC)")
        etats = load_etats()
        if etats is not None:
            st.dataframe(etats, hide_index=True, use_container_width=True)
        else:
            no_data_msg("etats_calibration.csv")
            st.markdown("""
Le tableau contient 10 observations trimestrielles :
- `date` : date de cotation du spread
- `c_star` : spread observé (%)
- `r_tk` : EURIBOR 3M à la date
- `mu_tk` : surmortalité belge interpolée
- `tenor_restant` : durée résiduelle du bond
""")

    with sub4:
        section_header("Comparaison des scénarios S1 / S2 / S3",
                       "Analogue Table 5.1 de Li et al. (2023)")
        if mpr and seuils:
            a_BE = seuils.get("a_BE", seuils.get("a", "—"))
            b_BE = seuils.get("b_BE", seuils.get("b", "—"))
            a_pre = seuils.get("a_BE_preC", "—")
            b_pre = seuils.get("b_BE_preC", "—")

            scen_df = pd.DataFrame([
                {
                    "Scénario": "S1", "Dynamiques P": "Post-COVID (2017–2022)",
                    "Seuils": "Post-COVID (a_BE, b_BE)",
                    "a": f"{a_BE:.5f}" if isinstance(a_BE, float) else a_BE,
                    "b": f"{b_BE:.5f}" if isinstance(b_BE, float) else b_BE,
                    "P₀": "100 (calibration)",
                },
                {
                    "Scénario": "S2", "Dynamiques P": "Pré-COVID (2017–2019)",
                    "Seuils": "Pré-COVID (a_preC, b_preC)",
                    "a": f"{a_pre:.5f}" if isinstance(a_pre, float) else a_pre,
                    "b": f"{b_pre:.5f}" if isinstance(b_pre, float) else b_pre,
                    "P₀": "> 100 (surévaluation)",
                },
                {
                    "Scénario": "S3", "Dynamiques P": "Post-COVID (2017–2022)",
                    "Seuils": "Pré-COVID (a_preC, b_preC)",
                    "a": f"{a_pre:.5f}" if isinstance(a_pre, float) else a_pre,
                    "b": f"{b_pre:.5f}" if isinstance(b_pre, float) else b_pre,
                    "P₀": "100 (recalibration ζ_S3)",
                },
            ])
            st.dataframe(scen_df, hide_index=True, use_container_width=True)
        else:
            no_data_msg("mpr.json / seuils.json")

        st.markdown("""
---
**Interprétation économique du scénario S3 :**

Le vecteur $\\zeta_{S3}$ est recalibré pour remettre le bond au pair
avec des seuils pré-COVID mais une dynamique post-COVID.
La comparaison $\\zeta_{S1}$ vs $\\zeta_{S3}$ révèle le **désalignement de risque** :
les composantes MPR devront être ajustées — notamment $\\chi$ (fréquence des sauts) —
pour compenser l'utilisation de seuils obsolètes.
""")
