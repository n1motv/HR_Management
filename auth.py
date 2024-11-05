import sqlite3
from admin_menu import afficher_admin_menu
from employe_menu import afficher_menu_employe
from getpass import getpass

import bcrypt

def connecter_db():
    return sqlite3.connect("rh_data.db")

def verifier_identifiants(email, mot_de_passe):
    connexion = connecter_db()
    if connexion is None:
        return None
    curseur = connexion.cursor()
    curseur.execute("""
        SELECT mot_de_passe FROM users WHERE email = ?
    """, (email,))
    
    resultats = curseur.fetchone()
    
    if resultats:
        mot_de_passe_hache = resultats[0]
        if isinstance(mot_de_passe_hache, str):
            mot_de_passe_hache = mot_de_passe_hache.encode('utf-8')
        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), mot_de_passe_hache):
            return True

    connexion.close()
    return False


def connexion_utilisateur(role):
    email = input("Entrer votre mail :")
    mot_de_passe = getpass("Entrer votre mot de passe : ")

    utilisateur = verifier_identifiants(email,mot_de_passe)

    if utilisateur :
        if role == "admin" and email == "admin" :
            print("Connexion réussi en tant qu'administrateur. ")

            afficher_admin_menu()
        elif role == "employe":
            print("Connection en tant qu'employé.")
            afficher_menu_employe(email)
        else:
            print("Accès refusé : Vous n'avez pas les autorisation nécessaires.")
    else:
        print("Identifiants incorrects, veuillez réessayer.")
        