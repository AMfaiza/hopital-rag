import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Initialisation
qdrant = QdrantClient(url="http://localhost:6333", check_compatibility=False)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key=os.getenv("API_KEY"))
COLLECTION_NAME = "hopital_pediatrique"

app = FastAPI(title="🏥 Hôpital Pédiatrique AI Assistant")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.get("/")
def root():
    return {"status": "Hôpital Pédiatrique AI Assistant opérationnel !"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        # Recherche sémantique dans Qdrant
        query_vector = embedder.encode(request.question).tolist()
        results = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=4
        )

        if not results.points:
            return QueryResponse(
                answer="Aucune information trouvée dans la base de données.",
                sources=[]
            )

        # Prépare le contexte
        context = ""
        sources = []
        for hit in results.points:
            context += f"\n---\n{hit.payload['text']}\n"
            if hit.payload['type'] == 'patient':
                sources.append(f"Dossier patient: {hit.payload['nom']}")
            elif hit.payload['type'] == 'protocole':
                sources.append(f"Protocole: {hit.payload['titre']}")
            else:
                sources.append(f"Guideline OMS: {hit.payload.get('source', 'Document OMS')}")

        # Groq génère la réponse
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": """Tu es un assistant médical pour un hôpital pédiatrique.
Tu aides les médecins et chirurgiens avant les opérations.
Réponds en français, de manière claire et structurée.
Mets en évidence les alertes importantes (allergies, interactions médicamenteuses).
IMPORTANT: Tu es un outil d'aide à la décision — le médecin prend toujours la décision finale."""},
                {"role": "user", "content": f"Contexte médical:\n{context}\n\nQuestion: {request.question}"}
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        return QueryResponse(
            answer=f"Erreur: {str(e)}",
            sources=[]
        )

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)