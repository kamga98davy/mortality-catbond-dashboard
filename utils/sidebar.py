"""Sidebar component — navigation context uniquement (plus de toggle vue)."""
import streamlit as st


def render_sidebar() -> None:
    """Render the sidebar with branding and navigation context."""
    with st.sidebar:
        st.markdown("""
<div style='text-align:center;padding:.5rem 0 1rem 0;'>
  <div style='font-size:1.8rem;margin-bottom:.3rem;'>📊</div>
  <div style='color:#F4A926;font-weight:700;font-size:.95rem;letter-spacing:.03em;'>
    CAT Bond Mortalité
  </div>
  <div style='color:#8892B0;font-size:.66rem;margin-top:.2rem;'>
    Belgique · Post-COVID · 2024
  </div>
</div>""", unsafe_allow_html=True)

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.07);margin:.5rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#8892B0;font-size:.7rem;line-height:1.7;'>
  <span style='color:#64FFDA;font-size:.65rem;font-weight:600;
               letter-spacing:.06em;'>CONSEIL</span><br>
  Utilisez les onglets<br>
  <b style='color:#CCD6F6;'>👔 Commercial</b> ou
  <b style='color:#CCD6F6;'>🔬 Technique</b><br>
  en haut de chaque page.
</div>""", unsafe_allow_html=True)

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.07);margin:.5rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#8892B0;font-size:.65rem;line-height:1.65;'>
  🎓 Mémoire actuariat · UCL<br>
  📖 Li et al. (2023, IME)<br>
  📂 Statbel 2013–2024
</div>""", unsafe_allow_html=True)
