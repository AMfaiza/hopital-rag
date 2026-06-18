# 🏥 Assistant IA Préopératoire — Hôpital Robert-Debré AP-HP

Un assistant médical intelligent basé sur le RAG (Retrieval-Augmented Generation) pour aider les médecins et chirurgiens de l'Hôpital Robert-Debré avant les opérations pédiatriques.

## Le problème qu'on résout

Avant chaque opération, le chirurgien doit consulter les guidelines internationaux, vérifier les protocoles anesthésiques, et adapter les recommandations au profil du patient. Notre solution permet au médecin de poser une question en langage naturel et recevoir en quelques secondes des recommandations basées sur les guidelines officiels de l'OMS.

## Architecture
Question du médecin

↓

Interface Streamlit (http://localhost:8501)

↓

API FastAPI (http://localhost:8001)

↓

Qdrant — recherche sémantique dans la base de connaissances

↓

Groq / LLaMA 3.3 — génère les recommandations

↓

Réponse structurée au médecin

## Base de connaissances

Le système intègre deux sources de données :

**Guidelines officiels OMS** (dossier `data/base_connaissance/`) :
- Documents médicaux pédiatriques internationaux
- Protocoles anesthésiques
- Recommandations chirurgicales

**Valeur ajoutée — Données fictives** (dossier `data/donnees_fictives/`) :
- Dossiers patients pédiatriques types
- Protocoles chirurgicaux pédiatriques
- Fiches interactions médicamenteuses

> 💡 L'hôpital peut enrichir le système en ajoutant ses propres protocoles internes dans `data/base_connaissance/` — le système devient automatiquement plus précis et personnalisé.

## Technologies utilisées

| Outil | Rôle |
|---|---|
| **Qdrant** | Base de données vectorielle |
| **Sentence Transformers** | Embeddings (all-MiniLM-L6-v2) |
| **Groq + LLaMA 3.3** | Génération des recommandations |
| **FastAPI** | API REST |
| **Streamlit** | Interface web médecin |
| **Docker** | Conteneurisation Qdrant |

## Prérequis

- Python 3.9+
- Docker
- Clé API Groq gratuite sur [console.groq.com](https://console.groq.com)

## Installation

### 1. Cloner le repository
```bash
git clone https://github.com/AMfaiza/hopital-rag.git
cd hopital-rag
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurer la clé API
Créer un fichier `.env` :
API_KEY=ta_clé_groq_ici

### 4. Lancer Qdrant avec Docker
```bash
cd docker
docker-compose up -d
cd ..
```

### 5. Ingérer la base de connaissances
```bash
cd src
python 02_ingest.py
```

### 6. Lancer l'API
```bash
python 03_api.py
```

### 7. Lancer l'interface
Ouvrir un nouveau terminal :
```bash
source venv/bin/activate
streamlit run src/04_ui.py
```

Ouvrir **http://localhost:8501** dans le navigateur.

## Structure du projet
hopital-rag/

├── src/

│   ├── patients_data.py    # Données fictives patients et protocoles

│   ├── 02_ingest.py        # Ingestion dans Qdrant

│   ├── 03_api.py           # API FastAPI

│   └── 04_ui.py            # Interface Streamlit

├── data/

│   ├── base_connaissance/  # Guidelines OMS (PDFs)

│   └── donnees_fictives/   # Données patients fictifs

├── docker/

│   └── docker-compose.yml

├── requirements.txt

├── .env

└── README.md

## Exemple d'utilisation

```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelles précautions pour un enfant asthmatique avant une chirurgie en urgence ?"}'
```

## Cas cliniques supportés

- 🫁 **Urgences pédiatriques** — enfant asthmatique en urgence chirurgicale
- 🫀 **Cardiopathie congénitale** — nourrisson avec allergie au latex
- 💉 **Diabète type 1** — gestion insuline avant appendicectomie
- 🧬 **Maladies rares** — protocoles spécifiques
- 💊 **Interactions médicamenteuses** — alertes préopératoires

## Disclaimer

⚠️ Cet outil est une aide à la décision médicale. Le médecin reste seul responsable de la décision thérapeutique finale — conformément à la Charte de l'enfant hospitalisé de l'AP-HP.
