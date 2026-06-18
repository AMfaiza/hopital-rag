import streamlit as st
import requests

st.set_page_config(
    page_title="Assistant IA — Hôpital Robert-Debré",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* Header bleu comme le site */
    .header-box {
        background-color: #003d82;
        padding: 20px 40px;
        border-radius: 0px;
        color: white;
        margin-bottom: 30px;
    }
    
    /* Boutons verts comme le site */
    .stButton>button {
        background-color: #c8d400;
        color: #003d82;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        width: 100%;
        height: auto;
        white-space: normal;
    }
    .stButton>button:hover {
        background-color: #a8b400;
        color: #003d82;
    }
    
    /* Bouton principal */
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #003d82;
        color: white;
        border-radius: 25px;
        padding: 12px 30px;
    }
    
    /* Cards */
    .card {
        background-color: #f0f4ff;
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #003d82;
        margin-bottom: 10px;
        color: #003d82 !important;
    }
    .card b {
        color: #003d82 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-box">
        <h2 style="margin:0; color:white;">🏥 Hôpital Universitaire Robert-Debré — AP-HP</h2>
        <p style="margin:5px 0 0 0; color:#c8d400; font-size:14px;">
        Assistant IA préopératoire · Hôpital mère-enfant du nord-est parisien
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Base de connaissances médicales pédiatriques")
st.markdown("Réponses basées sur les **guidelines OMS** et protocoles pédiatriques internationaux.")
st.markdown("---")

# 3 cas cliniques
st.markdown("### 💡 Cas cliniques fréquents")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""<div class="card">
        <b>🫁 Urgences pédiatriques</b>
    </div>""", unsafe_allow_html=True)
    if st.button("Enfant asthmatique\nen urgence chirurgicale"):
        st.session_state.question = "Quelles sont les précautions anesthésiques pour un enfant asthmatique nécessitant une chirurgie en urgence ?"

with col2:
    st.markdown("""<div class="card">
        <b>🫀 Cardiopathie congénitale</b>
    </div>""", unsafe_allow_html=True)
    if st.button("Nourrisson avec\ncardiopathie et allergie latex"):
        st.session_state.question = "Quel protocole suivre pour opérer un nourrisson atteint de cardiopathie congénitale avec allergie au latex ?"

with col3:
    st.markdown("""<div class="card">
        <b>💉 Diabète type 1</b>
    </div>""", unsafe_allow_html=True)
    if st.button("Gestion insuline\navant appendicectomie urgente"):
        st.session_state.question = "Comment gérer l'insulinothérapie d'un enfant diabétique de type 1 avant une appendicectomie en urgence ?"

st.markdown("---")

question = st.text_area(
    "📝 Votre question clinique :",
    value=st.session_state.get("question", ""),
    placeholder="Ex: Quelles précautions pour un enfant de 4 ans allergique au latex avant une chirurgie cardiaque ?",
    height=120
)

if st.button("🔍 Consulter la base de connaissances", type="primary"):
    if question:
        with st.spinner("Consultation des guidelines OMS en cours..."):
            try:
                response = requests.post(
                    "http://localhost:8001/query",
                    json={"question": question}
                )
                data = response.json()

                st.markdown("""<div class="card">
                    <b>📋 Recommandations cliniques</b>
                </div>""", unsafe_allow_html=True)
                st.write(data["answer"])

                if data["sources"]:
                    st.markdown("---")
                    st.markdown("**📂 Sources consultées :**")
                    for source in data["sources"]:
                        st.markdown(f"- {source}")

                st.markdown("---")
                st.warning("⚠️ Cet outil est une aide à la décision médicale. Le médecin reste seul responsable de la décision thérapeutique finale — conformément à la Charte de l'enfant hospitalisé de l'AP-HP.")

            except Exception as e:
                st.error(f"Erreur de connexion : {str(e)}")
    else:
        st.warning("Veuillez entrer une question clinique.")

# Footer
st.markdown("---")
st.markdown("""
    <p style="text-align:center; color:#003d82; font-size:12px;">
    🏥 Hôpital Robert-Debré · AP-HP · 48 Boulevard Sérurier, 75019 Paris
    </p>
""", unsafe_allow_html=True)