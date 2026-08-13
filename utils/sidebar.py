"""Sidebar component — branding et contexte de navigation."""
import streamlit as st


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("""
<div style='padding:.4rem 0 1rem 0;'>
  <div style='font-size:.75rem;font-weight:700;letter-spacing:.1em;
              text-transform:uppercase;color:#D97706;margin-bottom:.3rem;'>
    CAT Bond Mortalite
  </div>
  <div style='color:#6B7280;font-size:.66rem;'>Belgique · Post-COVID · UCL 2024</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.06);margin:.3rem 0 .8rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#6B7280;font-size:.69rem;line-height:1.8;'>
  <span style='color:#D97706;font-weight:600;font-size:.62rem;
               letter-spacing:.08em;text-transform:uppercase;'>Navigation</span><br>
  Utilisez les onglets<br>
  <strong style='color:#D1D5DB;'>L'essentiel</strong> ou
  <strong style='color:#D1D5DB;'>Analyse technique</strong><br>
  en haut de chaque page.
</div>
""", unsafe_allow_html=True)

        st.markdown(
            "<hr style='border:none;border-top:1px solid rgba(255,255,255,.06);margin:.8rem 0;'>",
            unsafe_allow_html=True,
        )
        st.markdown("""
<div style='color:#6B7280;font-size:.64rem;line-height:1.8;'>
  Memoire actuariat · UCL<br>
  Li et al. (2023, IME 85)<br>
  Statbel 2013–2024
</div>
""", unsafe_allow_html=True)
