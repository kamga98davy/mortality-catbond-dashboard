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

        st.markdown("""
<style>
.li-badge {
    display:flex;align-items:center;gap:.55rem;
    margin-top:.9rem;padding:.55rem .8rem;
    background:#1A1D27;
    border:1px solid rgba(10,102,194,.35);
    border-radius:6px;
    text-decoration:none !important;
    transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.li-badge:hover {
    transform:translateY(-2px);
    border-color:#0A66C2;
    box-shadow:0 6px 18px rgba(0,0,0,.4);
}
.li-badge svg { flex-shrink:0; }
.li-badge .li-name { color:#E5E7EB;font-size:.72rem;font-weight:600;line-height:1.2; }
.li-badge .li-handle { color:#6B7280;font-size:.62rem; }
</style>
<a class="li-badge" href="https://www.linkedin.com/in/kamgabopda/"
   target="_blank" rel="noopener noreferrer">
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18"
       viewBox="0 0 24 24" fill="#0A66C2">
    <path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86
             0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9
             1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34
             7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0
             4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0
             .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0
             1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/>
  </svg>
  <div>
    <div class="li-name">Davy Kamga Bopda</div>
    <div class="li-handle">linkedin.com/in/kamgabopda</div>
  </div>
</a>
""", unsafe_allow_html=True)
