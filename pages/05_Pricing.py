"""Page 5 — Pricing & Scénarios (MPR, S1/S2/S3)."""
import streamlit as st
import pandas as pd

from utils.styles import inject_css, section_header, insight_box, no_data_msg, warning_box
from utils.sidebar import render_sidebar
from utils.data_loader import load_mpr, load_seuils, load_etats

st.set_page_config(page_title="Pricing & Scénarios", page_icon="💰", layout="wide")
inject_css()
render_sidebar()

st.title("Pricing & Scénarios")

mpr    = load_mpr()
seuils = load_seuils()

tab_comm, tab_tech = st.tabs(["👔  Vue Commerciale", "🔬  Vue Technique"])

# ── COMMERCIAL ─────────────────────────────────────────────────────────────────
with tab_comm:
    section_header("Les trois scénarios du bond belge",
                   "Quel prix juste pour le bond selon le contexte de risque ?")

    p_s1 = mpr.get("P0_S1", 100.0) if mpr else 100.0
    p_s2 = mpr.get("P0_S2", "N/A")   if mpr else "N/A"
    p_s3 = mpr.get("P0_S3", 100.0) if mpr else 100.0

    st.markdown(f"""
<div class="scenario-row">
  <div class="scenario-card">
    <div class="scenario-title">S1 — Scénario de référence</div>
    <div class="scenario-price">P₀ = {p_s1:.1f}</div>
    <div class="scenario-desc">
      <b>Dynamiques post-COVID + Seuils post-COVID</b><br>
      Le bond est <em>au pair</em> : le coupon de 6 % compense exactement le
      risque de surmortalité post-pandémique. C'est le prix juste d'émission
      pour un investisseur conscient du nouveau régime de risque.
    </div>
  </div>
  <div class="scenario-card s2">
    <div class="scenario-title">S2 — Monde pré-COVID</div>
    <div class="scenario-price s2">P₀ &gt; 100</div>
    <div class="scenario-desc">
      <b>Dynamiques pré-COVID + Seuils pré-COVID</b><br>
      Counterfactuel : sans la pandémie, le même coupon de 6 % serait
      généreux pour le risque réel — le bond se négocierait <em>au-dessus du pair</em>.
      La prime de risque demandée dépasserait la réalité pré-COVID.
    </div>
  </div>
  <div class="scenario-card s3">
    <div class="scenario-title">S3 — Désalignement post-COVID</div>
    <div class="scenario-price s3">P₀ = {p_s3:.1f}</div>
    <div class="scenario-desc">
      <b>Dynamiques post-COVID + Seuils pré-COVID</b><br>
      Scénario de risque sous-estimé : si l'émetteur utilisait des seuils
      obsolètes (pré-COVID) avec une dynamique post-pandémique, le vecteur
      MPR ζ_S3 serait différent de ζ_S1, signalant un bond <em>mal calibré</em>.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns([2, 3])
    with col1:
        section_header("Primes de risque MPR ζ",
                       "Li et al. (2023) vs Belgique — Scénario S1")
        li_et_al = {"γ₁": 0.100, "γ₂": 0.212, "κ₁": 0.178, "κ₂": 0.253, "χ": 0.021}
        if mpr:
            be_vals = {
                "γ₁": mpr.get("gamma1"), "γ₂": mpr.get("gamma2"),
                "κ₁": mpr.get("kappa1"), "κ₂": mpr.get("kappa2"),
                "χ": mpr.get("chi"),
            }
            rows = []
            for k in li_et_al:
                li_v = li_et_al[k]
                be_v = be_vals.get(k)
                rows.append({
                    "Composante": k, "Li et al. (S1)": f"{li_v:.3f}",
                    "Belgique": f"{be_v:.3f}" if be_v is not None else "—",
                    "Δ": f"{be_v - li_v:+.3f}" if be_v is not None else "—",
                })
            st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        else:
            st.dataframe(pd.DataFrame({
                "Composante": list(li_et_al), "Li et al. (S1)": [f"{v:.3f}" for v in li_et_al.values()],
                "Belgique": ["—"] * 5,
            }), hide_index=True)
            no_data_msg("mpr.json")

    with col2:
        section_header("Recommandations stratégiques")
        insight_box("""
<b>💡 Message clé pour les assureurs belges</b><br><br>
1. <b>Le risque post-COVID est durablement plus élevé</b> — les paramètres
   dynamiques ont fondamentalement changé. Les seuils doivent être recalibrés
   régulièrement avec les nouvelles données.<br><br>
2. <b>Le coupon de 6 % est le spread juste</b> dans le contexte actuel (S1).
   Un spread inférieur sous-rémunèrerait les investisseurs pour le risque réel.<br><br>
3. <b>Le scénario S3 est un signal d'alerte</b> : si les seuils n'ont pas été
   mis à jour depuis 2019, l'émetteur transfère implicitement plus de risque
   qu'il ne le croit — le vecteur ζ_S3 révèle cette asymétrie.
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
