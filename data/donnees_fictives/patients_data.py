# Données fictives pour le prototype hôpital pédiatrique
patients = [
    {
        "patient_id": "P001",
        "nom": "Youssef Ben Ali",
        "age": 8,
        "sexe": "Garçon",
        "poids": 25,
        "taille": 128,
        "groupe_sanguin": "A+",
        "maladies": ["Asthme modéré"],
        "allergies": ["Pénicilline"],
        "medicaments": ["Salbutamol spray"],
        "operation": "Ablation des amygdales",
        "antecedents": "3 hospitalisations pour crise d'asthme"
    },
    {
        "patient_id": "P002",
        "nom": "Lina Moussaoui",
        "age": 4,
        "sexe": "Fille",
        "poids": 16,
        "taille": 102,
        "groupe_sanguin": "O-",
        "maladies": ["Cardiopathie congénitale"],
        "allergies": ["Latex"],
        "medicaments": ["Furosémide 10mg", "Captopril 3mg"],
        "operation": "Correction cardiopathie congénitale",
        "antecedents": "Prématurée à 32 semaines"
    },
    {
        "patient_id": "P003",
        "nom": "Adam Idrissi",
        "age": 12,
        "sexe": "Garçon",
        "poids": 40,
        "taille": 152,
        "groupe_sanguin": "B+",
        "maladies": ["Diabète type 1"],
        "allergies": ["Aucune allergie connue"],
        "medicaments": ["Insuline Novorapid", "Insuline Lantus"],
        "operation": "Appendicectomie en urgence",
        "antecedents": "Diabétique depuis l'âge de 6 ans"
    },
    {
        "patient_id": "P004",
        "nom": "Sara Benchekroun",
        "age": 6,
        "sexe": "Fille",
        "poids": 20,
        "taille": 116,
        "groupe_sanguin": "AB+",
        "maladies": ["Aucune maladie chronique"],
        "allergies": ["Iode"],
        "medicaments": ["Aucun médicament régulier"],
        "operation": "Correction hernie inguinale",
        "antecedents": "Aucun antécédent chirurgical"
    },
    {
        "patient_id": "P005",
        "nom": "Hamza Tazi",
        "age": 2,
        "sexe": "Garçon",
        "poids": 12,
        "taille": 88,
        "groupe_sanguin": "A-",
        "maladies": ["Malformation rénale"],
        "allergies": ["Aucune allergie connue"],
        "medicaments": ["Amoxicilline 125mg"],
        "operation": "Correction malformation rénale",
        "antecedents": "Diagnostic prénatal à 6 mois de grossesse"
    }
]

protocoles = [
    {
        "type": "Anesthésie pédiatrique",
        "contenu": """Protocole anesthésie pédiatrique :
        - Doses calculées selon le poids de l'enfant (mg/kg)
        - Jeûne : lait maternel 4h, lait artificiel 6h, solides 8h
        - Pour asthmatiques : éviter AINS, préférer Kétamine
        - Allergie latex : matériel latex-free obligatoire
        - Allergie pénicilline : utiliser Céfazoline ou Clindamycine
        - Allergie iode : remplacer Bétadine par Chlorhexidine
        - Présence parent autorisée jusqu'à l'induction
        - Voie IV difficile : utiliser EMLA cream 1h avant"""
    },
    {
        "type": "Chirurgie cardiaque pédiatrique",
        "contenu": """Protocole chirurgie cardiaque pédiatrique :
        - Durée : 4 à 8h selon la complexité
        - Circulation extracorporelle adaptée au poids
        - Réanimation pédiatrique postopératoire obligatoire
        - Surveillance hémodynamique continue
        - Transfusion selon protocole pédiatrique
        - Parents informés et accompagnés par psychologue"""
    },
    {
        "type": "Chirurgie urgence pédiatrique",
        "contenu": """Protocole urgence pédiatrique :
        - Estomac plein : induction séquence rapide
        - Pour diabétiques : glycémie cible 6-10 mmol/L
        - Surveiller glycémie toutes les 2h en peropératoire
        - Insuline IV selon protocole pédiatrique
        - Réchauffement actif obligatoire (risque hypothermie)
        - Antibioprophylaxie selon poids"""
    },
    {
        "type": "Interactions médicamenteuses pédiatriques",
        "contenu": """Interactions importantes en chirurgie pédiatrique :
        - Insuline : réduire dose de 50% la veille, perfusion glucose peropératoire
        - Furosémide : bilan électrolytes obligatoire avant chirurgie
        - Amoxicilline + allergie pénicilline : CONTRE-INDIQUÉ, remplacer par Azithromycine
        - AINS : éviter chez asthmatiques et moins de 3 mois
        - Captopril : surveiller tension artérielle en peropératoire
        - Salbutamol : continuer jusqu'au jour de l'opération"""
    }
]

if __name__ == "__main__":
    print(f" {len(patients)} patients pédiatriques créés")
    print(f"{len(protocoles)} protocoles pédiatriques créés")
    print("\nDonnées prêtes pour l'ingestion !")