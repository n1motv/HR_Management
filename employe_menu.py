import sqlite3
from tabulate import tabulate
def connect_db():
    return sqlite3.connect("rh_data.db")

def afficher_menu_employe(email):
    while True:
        print("\n--- Menu Employé ---")
        print("Options pour l'employé :\n1-Voir mes informations\n2-Soumettre une demande de congé\n3-Voir mes demandes de congés\n4-Se déconnecter.")
        choix = input("Veuillez choisir une option : ")
        if choix == "1": 
            voir_mes_info(email)
        elif choix=="2":
            soumettre_demande_conge(email)
        elif choix =="3":
            voir_suivi_demandes_conges(email)
        elif choix == "4":
            se_deconnecter()
            break

def voir_mes_info(email):
    connexion = connect_db()
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT nom, prenom, age, poste, email, mot_de_passe, conge FROM users WHERE email = ? ORDER BY id
                    """, (email,))
    resultats = curseur.fetchall()
    print(tabulate(resultats, headers=["Nom", "Prénom", "Âge", "Poste", "Email", "Mot De Passe" , "Congés"], tablefmt="grid"))
    connexion.close()

def soumettre_demande_conge(email):
    raison = input("Veuillez entrer le motif de la demande de congé : ")
    date_debut = input("Veuillez entrer la date de début (YYYY-MM-DD) : ")
    date_fin = input("Veuillez entrer la date de fin (YYYY-MM-DD) : ")
    plus_infos = input("Veuillez entrer des informations supplémentaires (facultatif) : ")

    connexion = connect_db()
    cur = connexion.cursor()

    cur.execute("""
        INSERT INTO conges (email, raison, date_debut, date_fin, plus_infos)
        VALUES (?, ?, ?, ?, ?)
    """, (email, raison, date_debut, date_fin, plus_infos))
    
    connexion.commit()
    connexion.close()
    print("Demande de congé soumise avec succès.")

def voir_suivi_demandes_conges(email):
    connexion = connect_db()
    cur = connexion.cursor()
    cur.execute("""
        SELECT id, raison, date_debut, date_fin, plus_infos, statut, motif_refus
        FROM conges
        WHERE email = ?
    """, (email,))

    demandes = cur.fetchall()

    if demandes:
        print(tabulate(demandes, headers=["ID", "Raison", "Date de Début", "Date de Fin", "Infos Supplémentaires", "Statut", "Motif de Refus"], tablefmt="grid"))
    else:
        print("Aucune demande de congé trouvée.")

    connexion.close()


def se_deconnecter():
    print("Fermeture de l'application")
    connect_db().close()