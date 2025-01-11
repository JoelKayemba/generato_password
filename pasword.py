import hashlib
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import json
import os

# Fichier de sauvegarde
SAVE_FILE = "questions_reponses.enc"
KEY_FILE = "key.key"

# Générer ou charger une clé de chiffrement
def charger_ou_creer_cle():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key

# Initialiser le module Fernet avec la clé
cle = charger_ou_creer_cle()
fernet = Fernet(cle)

def sauvegarder_questions_reponses(data):
    """Sauvegarde les questions et réponses dans un fichier chiffré."""
    data_json = json.dumps(data).encode('utf-8')
    data_chiffree = fernet.encrypt(data_json)
    with open(SAVE_FILE, "wb") as f:
        f.write(data_chiffree)

def charger_questions_reponses():
    """Charge les questions et réponses depuis un fichier chiffré, si disponible."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            data_chiffree = f.read()
        try:
            data_dechiffree = fernet.decrypt(data_chiffree)
            return json.loads(data_dechiffree)
        except Exception as e:
            messagebox.showerror("Erreur", "Impossible de déchiffrer les données sauvegardées.")
            return {}
    return {}

def generer_mot_de_passe(question1, reponse1, question2, reponse2, longueur=16):
    """
    Génère un mot de passe sécurisé et reproductible à partir de deux questions/réponses personnalisées.
    """
    graine = f"{question1.lower().strip()}|{reponse1.lower().strip()}|{question2.lower().strip()}|{reponse2.lower().strip()}"
    salt = "secure-salt-value"  # Sel fixe pour la reproductibilité
    graine_salee = graine + salt
    hash_graine = hashlib.sha256(graine_salee.encode('utf-8')).hexdigest()

    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    mot_de_passe = ''.join(caracteres[int(hash_graine[i:i+2], 16) % len(caracteres)] for i in range(0, longueur * 2, 2))

    return mot_de_passe

def generer_et_afficher():
    """Génère et affiche le mot de passe."""
    question1 = entry_question1.get()
    reponse1 = entry_reponse1.get()
    question2 = entry_question2.get()
    reponse2 = entry_reponse2.get()

    if not (question1 and reponse1 and question2 and reponse2):
        messagebox.showerror("Erreur", "Toutes les questions et réponses doivent être remplies.")
        return

    # Sauvegarder les questions/réponses
    sauvegarder_questions_reponses({
        "question1": question1,
        "question2": question2,
    })

    mot_de_passe = generer_mot_de_passe(question1, reponse1, question2, reponse2)
    messagebox.showinfo("Mot de passe généré", f"Votre mot de passe est :\n{mot_de_passe}")

def charger_et_remplir():
    """Charge les questions/réponses et remplit les champs."""
    data = charger_questions_reponses()
    entry_question1.insert(0, data.get("question1", ""))
    entry_question2.insert(0, data.get("question2", ""))


# Interface Tkinter
app = tk.Tk()
app.title("Générateur de Mot de Passe")
app.geometry("400x350")

# Instructions
tk.Label(app, text="Remplissez les questions et réponses ci-dessous pour générer votre mot de passe.", wraplength=350, justify="center").pack(pady=10)

# Champs pour la première question/réponse
tk.Label(app, text="Question 1 :").pack()
entry_question1 = tk.Entry(app, width=50)
entry_question1.pack()

tk.Label(app, text="Réponse 1 :").pack()
entry_reponse1 = tk.Entry(app, width=50)
entry_reponse1.pack()

# Champs pour la deuxième question/réponse
tk.Label(app, text="Question 2 :").pack()
entry_question2 = tk.Entry(app, width=50)
entry_question2.pack()

tk.Label(app, text="Réponse 2 :").pack()
entry_reponse2 = tk.Entry(app, width=50)
entry_reponse2.pack()

# Bouton pour générer le mot de passe
tk.Button(app, text="Générer le mot de passe", command=generer_et_afficher).pack(pady=10)

# Charger les questions/réponses existantes au démarrage
charger_et_remplir()

# Lancement de l'application
app.mainloop()
