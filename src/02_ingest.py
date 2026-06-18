import os
import importlib
import sys
import fitz  # pymupdf
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

# Import données fictives
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/donnees_fictives"))
from patients_data import patients, protocoles

# Initialisation
qdrant = QdrantClient(url="http://localhost:6333", check_compatibility=False)
embedder = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "hopital_pediatrique"

def extract_text_from_pdf(filepath, max_pages=20):
    doc = fitz.open(filepath)
    text = ""
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=400, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if len(chunk) > 100:
            chunks.append(chunk)
    return chunks

def main():
    print("Création de la collection Qdrant...")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        )
    )

    points = []
    point_id = 0

    # ============================================
    # 1. Ingestion des PDFs OMS
    # ============================================
    base_connaissance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/base_connaissance")
    print("\n Ingestion des guidelines ...")

    for filename in os.listdir(base_connaissance_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(base_connaissance_path, filename)
            print(f"  → Traitement de {filename}...")

            text = extract_text_from_pdf(filepath)
            chunks = chunk_text(text)
            print(f"  → {len(chunks)} chunks créés")

            for chunk in chunks:
                vector = embedder.encode(chunk).tolist()
                points.append(models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "type": "guideline_oms",
                        "source": filename,
                        "text": chunk
                    }
                ))
                point_id += 1

    # ============================================
    # 2. Ingestion des données fictives patients
    # ============================================
    print("\n👶 Ingestion des dossiers patients fictifs...")
    for patient in patients:
        texte = f"""
        Patient: {patient['nom']}, {patient['age']} ans, {patient['sexe']}
        Poids: {patient['poids']}kg, Taille: {patient['taille']}cm
        Groupe sanguin: {patient['groupe_sanguin']}
        Maladies: {', '.join(patient['maladies'])}
        Allergies: {', '.join(patient['allergies'])}
        Medicaments: {', '.join(patient['medicaments'])}
        Operation prevue: {patient['operation']}
        Antecedents: {patient['antecedents']}
        """
        vector = embedder.encode(texte).tolist()
        points.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "type": "patient",
                "patient_id": patient['patient_id'],
                "nom": patient['nom'],
                "age": patient['age'],
                "operation": patient['operation'],
                "text": texte
            }
        ))
        point_id += 1

    # ============================================
    # 3. Ingestion des protocoles fictifs
    # ============================================
    print("\n Ingestion des protocoles médicaux...")
    for protocole in protocoles:
        vector = embedder.encode(protocole['contenu']).tolist()
        points.append(models.PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "type": "protocole",
                "titre": protocole['type'],
                "text": protocole['contenu']
            }
        ))
        point_id += 1

    # Insertion dans Qdrant
    print(f"\n Insertion de {len(points)} documents dans Qdrant...")
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"\n Ingestion terminée !")
    print(f"   - Guidelines OMS : {point_id - len(patients) - len(protocoles)} chunks")
    print(f"   - Patients fictifs : {len(patients)}")
    print(f"   - Protocoles fictifs : {len(protocoles)}")

if __name__ == "__main__":
    main()