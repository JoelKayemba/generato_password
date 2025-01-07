import hashlib

def generer_mot_de_passe(question1: str, reponse1: str, question2: str, reponse2: str, longueur: int = 16) -> str:
    """
    Génère un mot de passe stable et reproductible à partir de deux questions et leurs réponses.
    
    Args:
    question1 (str): Première question personnelle.
    reponse1 (str): Réponse à la première question.
    question2 (str): Deuxième question personnelle.
    reponse2 (str): Réponse à la deuxième question.
    longueur (int): Longueur souhaitée du mot de passe. Par défaut 16 caractères.
    
    Returns:
    str: Un mot de passe sécurisé unique et stable.
    """
    # Combiner les entrées utilisateur pour créer une graine unique
    graine = f"{question1.lower()}|{reponse1.lower()}|{question2.lower()}|{reponse2.lower()}"
    
    # Hacher la graine avec SHA-256
    hash_graine = hashlib.sha256(graine.encode('utf-8')).hexdigest()
    
    # Extraire les caractères nécessaires pour le mot de passe
    mot_de_passe = hash_graine[:longueur]  # Utilise les premiers caractères du hash
    return mot_de_passe

# Fonction principale pour tester
def main():
    print("Bienvenue dans le générateur de mot de passe stable et reproductible !")
    
    # Entrée des informations utilisateur
    question1 = input("Entrez votre première question personnelle : ")
    reponse1 = input("Entrez votre première réponse : ")
    question2 = input("Entrez votre deuxième question personnelle : ")
    reponse2 = input("Entrez votre deuxième réponse : ")
    
    # Générer le mot de passe
    mot_de_passe = generer_mot_de_passe(question1, reponse1, question2, reponse2)
    print(f"\nVotre mot de passe généré est : {mot_de_passe}")
    print("Astuce : Retenez simplement vos questions et réponses pour recréer ce mot de passe.")

# Lancer le programme
if __name__ == "__main__":
    main()
