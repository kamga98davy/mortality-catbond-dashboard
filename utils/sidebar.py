"""Sidebar component partagé entre toutes les pages."""
import streamlit as st


def render_sidebar() -> str:
    """Render the sidebar with view toggle. Returns 'Executive' or 'Technique'."""
    with st.sidebar:
        st.markdown("""
<div style='text-align:center;padding:.6rem 0 1.1rem 0;'>
  <div style='font-size:1.9rem;margin-bottom:.35rem;'>📊</div>
  <div style='color:#F4A926;font-weight:700;font-size:1rem;letter-spacing:.03em;'>
    CAT Bond Mortalité
  </div>
  <div style='color:#8892B0;font-size:.68rem;margin-top:.25rem;'>
    Belgique · Post-COVID · 2024
  </div>
</div>""", unsafe_allow_html=True)

        current = st.session_state.get("view", "Executive")
        choice = st.radio(
            "Perspective",
            ["👔 Commercial", "🔬 Technique"],
            index=0 if current == "Executive" else 1,
            key="view_radio",
            label_visibility="collapsed",
        )
        st.session_state["view"] = "Executive" if choice.startswith("👔") else "Technique"

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.07);margin:.7rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#8892B0;font-size:.71rem;line-height:1.95;'>
  <div style='color:#CCD6F6;font-size:.76rem;font-weight:600;
              margin-bottom:.3rem;letter-spacing:.04em;'>PAGES</div>
  📊 &nbsp;Données<br>
  🔬 &nbsp;Modèle AJD<br>
  ⚙️ &nbsp;Calibration MCMC<br>
  📈 &nbsp;Monte Carlo<br>
  💰 &nbsp;Pricing & Scénarios<br>
  🎯 &nbsp;Sensibilité MPR
</div>""", unsafe_allow_html=True)

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.07);margin:.7rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#8892B0;font-size:.66rem;line-height:1.7;'>
  🎓 Mémoire actuariat · ULB<br>
  📖 Li et al. (2023, IME)<br>
  📂 Statbel 2013–2024
</div>""", unsafe_allow_html=True)

    return st.session_state.get("view", "Executive")
