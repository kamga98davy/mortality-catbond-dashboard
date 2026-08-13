"""Page 7 — À propos de l'auteur."""
import streamlit as st

from utils.styles import inject_css, section_header
from utils.sidebar import render_sidebar
from utils.icons import icon

st.set_page_config(page_title="À propos de l'auteur", page_icon="👤", layout="wide")
inject_css()
render_sidebar()

st.markdown("""
<style>
.about-fact {
    background:#1A1D27;border:1px solid rgba(255,255,255,.07);
    border-radius:8px;padding:1rem 1.15rem;margin-bottom:.7rem;
}
.about-fact-title {
    font-size:.64rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;
    color:#D97706;margin-bottom:.55rem;display:flex;align-items:center;gap:.45rem;
}
.about-fact-body { color:#9CA3AF;font-size:.78rem;line-height:1.8; }
.about-fact-body strong { color:#E5E7EB;font-weight:600; }
.timeline-item { display:flex;gap:.9rem;margin:.65rem 0;align-items:flex-start; }
.timeline-date {
    min-width:5.2rem;color:#D97706;font-weight:600;font-size:.72rem;
    margin-top:.15rem;text-align:right;
}
.timeline-body { border-left:2px solid rgba(255,255,255,.08);padding-left:.9rem; }
.timeline-role { color:#E5E7EB;font-weight:600;font-size:.84rem; }
.timeline-org  { color:#6B7280;font-size:.74rem;margin-bottom:.15rem; }
.timeline-desc { color:#9CA3AF;font-size:.77rem;line-height:1.6; }
</style>
""", unsafe_allow_html=True)

st.title("À propos de l'auteur")

col_story, col_facts = st.columns([5, 3], gap="large")

# ── Colonne narrative ─────────────────────────────────────────────────────────
with col_story:
    st.markdown("""
<div class="prose">
Je m'appelle <strong style="color:#E5E7EB">Davy Romaric Kamga Bopda</strong>.
Je suis ingénieur statisticien économiste, formé à l'ISSEA de Yaoundé,
et depuis septembre 2024 je poursuis le master en sciences actuarielles
à l'UCLouvain, où je suis aussi chargé de travaux pratiques en statistiques.
</div>
""", unsafe_allow_html=True)

    section_header("Le parcours en deux temps")
    st.markdown("""
<div class="prose">
J'ai commencé par la data science. Chez Orange Cameroun, j'ai d'abord construit
un modèle d'upselling pour Orange Money et un score de satisfaction client à partir
des enquêtes NPS, puis, l'année suivante, des dashboards Power BI pour le pilotage
des revenus Wholesale — avec au passage l'automatisation en Python et VBA des
réconciliations d'infrastructures entre MTN et Orange, un travail ingrat mais qui
a permis de détecter des écarts non contractuels dans les trafics d'interconnexion.
Entre les deux, j'ai projeté le trafic portuaire camerounais 2024-2028 pour
l'Autorité Portuaire Nationale.
<br><br>
L'actuariat est venu après, et c'était un choix délibéré. L'analyse de données
me donnait les outils ; il me manquait le cadre théorique du risque — celui qui
permet de dire non pas seulement <em>ce que les données montrent</em>, mais
<em>combien ce risque doit coûter</em>. C'est exactement la question de ce mémoire.
</div>
""", unsafe_allow_html=True)

    section_header("Pourquoi ce sujet")
    st.markdown("""
<div class="prose">
Les CAT bonds de mortalité sont un sujet où mes deux formations servent en même temps :
il faut du code (le MCMC, les 100 000 simulations, la calibration) et il faut
de la théorie actuarielle (le changement de mesure, les primes de risque, la
structure du bond). En Belgique, le P-score de surmortalité a atteint 17,5 %
au pic de 2020 — un chiffre qui justifie à lui seul de se demander si les
instruments de transfert de risque d'avant la pandémie sont encore bien calibrés.
<br><br>
Ce mémoire est supervisé par Karim Barigou, professeur en sciences actuarielles
à l'UCLouvain. Ce tableau de bord en est le support interactif : tout ce qui y
est montré sort du code R et Python du mémoire, rien n'est décoratif.
</div>
""", unsafe_allow_html=True)

    section_header("Expériences")
    for date, role, org, desc in [
        ("2024 – 2025", "Chargé de travaux pratiques", "UCLouvain",
         "Analyse de données et probabilités (BAC 3), statistique inférentielle pour sciences de gestion."),
        ("2024 – 2025", "Business Analytics", "The POD, Louvain-la-Neuve",
         "Étude de l'écosystème numérique du Brabant wallon : cartographies, interviews, analyse quantitative et qualitative."),
        ("2024", "Data Analyst (stage)", "Orange Cameroun, Douala",
         "Dashboards Power BI Wholesale, automatisation des réconciliations MTN/Orange en Python et VBA."),
        ("2023 – 2024", "Assistant en planification stratégique", "Autorité Portuaire Nationale du Cameroun",
         "Projection du trafic portuaire 2024-2028 par modélisation statistique, diagnostic de l'offre portuaire."),
        ("2023", "Data Scientist (stage)", "Orange Cameroun, Douala",
         "Modèle d'upselling Machine Learning pour Orange Money, score de satisfaction client (drivers NPS)."),
    ]:
        st.markdown(f"""
<div class="timeline-item">
  <div class="timeline-date">{date}</div>
  <div class="timeline-body">
    <div class="timeline-role">{role}</div>
    <div class="timeline-org">{org}</div>
    <div class="timeline-desc">{desc}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Colonne faits ─────────────────────────────────────────────────────────────
with col_facts:
    st.markdown(f"""
<div class="about-fact">
  <div class="about-fact-title">{icon("book-open", 13, "#D97706")} Formation</div>
  <div class="about-fact-body">
    <strong>Master en sciences actuarielles</strong><br>
    UCLouvain · 2024 – 2026<br><br>
    <strong>Ingénieur statisticien économiste</strong><br>
    ISSEA, Yaoundé (grande école CEMAC) · 2020 – 2023<br>
    Spécialisation data science<br><br>
    <strong>Master II Mathématiques (Analyse)</strong><br>
    Université de Yaoundé I · 2017 – 2019
  </div>
</div>

<div class="about-fact">
  <div class="about-fact-title">{icon("sliders", 13, "#D97706")} Compétences</div>
  <div class="about-fact-body">
    <strong>Data</strong> — SQL, Power BI, Excel avancé (Power Query, TCD)<br>
    <strong>Langages</strong> — Python et R orientés analyse de données, SAS, VBA<br>
    <strong>Actuariat</strong> — GLM, modèles de survie, CAT bonds,
    réassurance XL, tarification, Solvency II<br>
    <strong>Méthodes</strong> — modélisation stochastique, simulation
    Monte Carlo, machine learning (RF, XGBoost)
  </div>
</div>

<div class="about-fact">
  <div class="about-fact-title">{icon("check-circle", 13, "#D97706")} Certification</div>
  <div class="about-fact-body">
    <strong>SAS Certified Specialist</strong><br>
    Base Programming Using SAS 9.4
  </div>
</div>

<div class="about-fact">
  <div class="about-fact-title">{icon("file-text", 13, "#D97706")} Projets académiques récents</div>
  <div class="about-fact-body">
    Pricing Monte Carlo GMIB, 1 million de trajectoires (processus de Lévy)<br>
    Tarification d'un traité de réassurance XL (Burning Cost, Poisson-Pareto)<br>
    Best Estimate de passifs actuariels (bootstrapping, Svensson)<br>
    Prédiction de sinistres auto sur 24 774 contrats (AUC 0,701)
  </div>
</div>

<div class="about-fact">
  <div class="about-fact-title">{icon("users", 13, "#D97706")} Contact</div>
  <div class="about-fact-body">
    kamgabopda@gmail.com<br>
    <a href="https://www.linkedin.com/in/kamgabopda/" target="_blank" rel="noopener noreferrer"
       style="color:#D97706;text-decoration:none;">linkedin.com/in/kamgabopda</a><br>
    Louvain-la-Neuve, Belgique
  </div>
</div>
""", unsafe_allow_html=True)
