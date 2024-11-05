import sqlite3
from tabulate import tabulate
from getpass import getpass
import bcrypt

def connect_db():
    return sqlite3.connect("rh_data.db")

def afficher_admin_menu():

    while True :
        print("\n--- Menu Administrateur ---")
        print("Options d'administration : \n1-Voir les employés \n2-Ajouter un employé \n3-Mettre à jour un employé \n4-Voir les demandes de congés\n5-Répondre au demandes de congés\n6-Se déconnecter.")
        choix = input("Veuillez choisir une option : ")

        if choix =="1":
            voir_employe()
        elif choix =="2":
            ajouter_employe()
        elif choix == "3":
            mettre_a_jour_employe()
        elif choix == "4" :
            voir_demandes_conges()
        elif choix =="5":
            repondre_demande_conge()
        elif choix == "6":        
            se_deconnecter()
            break
        else:
            print("Choix invalide veillez réessayer.")


def voir_employe():
    connexion = connect_db()
    curseur = connexion.cursor()
    while True : 
        choix= input("Taper 1 pour afficher tout les employers ou taper 2 pour choisir l'employé à afficher: ")
        if choix == "1":
            curseur.execute("""
                SELECT nom, prenom, age, poste, email ,mot_de_passe,conge FROM users WHERE id != 1 ORDER BY id
            """)
            resultats = curseur.fetchall()
            print(tabulate(resultats, headers=["Nom", "Prénom", "Âge", "Poste", "Email","mot de passe", "Congés"], tablefmt="grid"))

            connexion.close()
            break
        elif choix == "2":
            id = input("Veuillez entrer l'id de l'employé à afficher : ")
            curseur.execute("""
                SELECT nom, prenom, age, poste, email, mot_de_passe,conge FROM users WHERE id = ? ORDER BY id
            """, (id,))
            resultats = curseur.fetchall()
            if resultats:
                print(tabulate(resultats, headers=["Nom", "Prénom", "Âge", "Poste", "Email", "Mot de Passe","Congés"], tablefmt="grid"))
            else:
                print(f"Aucun employé trouvé avec l'ID {id}.")

            connexion.close()
            break
        else:
            print("Choix invalide veillez réessayer.")
            break
            

def ajouter_employe():

    nom= input("Entre le nom: ")
    prenom= input("Entre le prènom: ")
    age= input("Entre l'âge: ")
    poste= input("Entrer le poste: ")
    email= input("Entrer l'adresse mail: ")
    x=True
    while x:
        mot_de_passe = getpass("Entrer le mot de passe: ")
        re_mot_de_pass =getpass("Re entrer le mot de passe: ")
        if mot_de_passe==re_mot_de_pass:
            x =False
        else:
            print("Les mot de passe ne sont pas identiques! ")
    mot_de_passe_hash =bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
    conge=input("Entrer le solde du congé: ")
    connexion =connect_db()
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO users (nom,prenom,age,poste,email,mot_de_passe,conge)
                    VALUES (?,?,?,?,?,?,?)
                    """,(nom,prenom,age,poste,email,mot_de_passe_hash,conge))
    connexion.commit()
    connexion.close()
    print("Employé ajouté avec succés")

def mettre_a_jour_employe():

    id = input("Veuillez entrer l'id de l'employé à modifier: ")

    connexion = connect_db()
    curseur = connexion.cursor()
    curseur.execute("SELECT nom, prenom, age, poste, email, mot_de_passe,conge FROM users WHERE id = ?", (id,))
    employe = curseur.fetchone()

    if employe is None:
        print("Aucun employé trouvé avec cet ID.")
        return
    
    print("\nInformations actuelles :")
    print(f"Nom : {employe[0]}, Prénom : {employe[1]}, Âge : {employe[2]}, Poste : {employe[3]}, Email : {employe[4]}")

    nom = input(f"Entre le nouveau nom (actuel : {employe[0]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[0]
    prenom = input(f"Entre le nouveau prénom (actuel : {employe[1]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[1]
    age = input(f"Entre le nouveau âge (actuel : {employe[2]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[2]
    poste = input(f"Entre le nouveau poste (actuel : {employe[3]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[3]
    email = input(f"Entre la nouvelle adresse mail (actuel : {employe[4]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[4]
    mot_de_passe = getpass("Entrer le nouveau mot de passe (appuyer sur Entrée pour ne pas changer) : ") or employe[5]
    conge = input(f"Entre le nouveau solde du congé (actuel : {employe[6]} ou appuyer sur Entrée pour ne pas changer) : ") or employe[6]
    mot_de_passe_hash =bcrypt.hashpw(mot_de_passe.encode('utf-8'), bcrypt.gensalt())
    curseur.execute("""
                    UPDATE users
                    SET nom = ?,
                        prenom = ?,
                        age = ?,
                        poste = ?,
                        email = ?,
                        mot_de_passe = ?,
                        conge=?
                    WHERE id = ?;""",
                    (nom, prenom, age, poste, email, mot_de_passe_hash, conge, id))
    
    connexion.commit()
    print("Informations mises à jour avec succès.")

    connexion.close()
def voir_demandes_conges():
    connexion = connect_db()
    cur = connexion.cursor()

    cur.execute("SELECT * FROM conges")
    demandes = cur.fetchall()

    if demandes:
        print(tabulate(demandes, headers=["ID", "Email", "Raison", "Date de Début", "Date de Fin", "Infos Supplémentaires", "Statut", "Motif de Refus"], tablefmt="grid"))
    else:
        print("Aucune demande de congé à afficher.")

    connexion.close()

from datetime import datetime

from datetime import datetime, timedelta

def compter_jours_de_conge(date_debut, date_fin):
    """ Fonction pour compter le nombre de jours de congé en excluant les samedis et dimanches. """
    jours_conge = 0
    date_courante = date_debut

    while date_courante <= date_fin:
        if date_courante.weekday() < 5:
            jours_conge += 1
        date_courante += timedelta(days=1)

    return jours_conge

def repondre_demande_conge():
    while True:
        id_demande = input("Veuillez entrer l'ID de la demande à traiter : ")
        connexion = connect_db()
        curseur = connexion.cursor()
        curseur.execute("""SELECT * FROM conges WHERE id = ?""", (id_demande,))
        resultats = curseur.fetchone()

        if resultats:
            email_employe = resultats[1]
            date_debut = resultats[3]
            date_fin = resultats[4]
            date_debut_dt = datetime.strptime(date_debut, '%Y-%m-%d')
            date_fin_dt = datetime.strptime(date_fin, '%Y-%m-%d')
            nombre_jours = compter_jours_de_conge(date_debut_dt, date_fin_dt)
            curseur.execute("SELECT conge FROM users WHERE email = ?", (email_employe,))
            solde_conge = curseur.fetchone()

            if solde_conge and solde_conge[0] >= nombre_jours:
                statut = input("Accepter ou Refuser la demande ? (entrez 'accepter' ou 'refuser') : ")
                motif_refus = None

                if statut.lower() == 'refuser':
                    motif_refus = input("Veuillez entrer le motif du refus : ")

                if statut.lower() == 'accepter':
                    nouveau_solde = solde_conge[0] - nombre_jours
                    curseur.execute("UPDATE users SET conge = ? WHERE email = ?", (nouveau_solde, email_employe))

                    curseur.execute("""
                        UPDATE conges
                        SET statut = 'accepté'
                        WHERE id = ?
                    """, (id_demande,))
                elif statut.lower() == 'refuser':
                    curseur.execute("""
                        UPDATE conges
                        SET statut = 'refusé', motif_refus = ?
                        WHERE id = ?
                    """, (motif_refus, id_demande))
                else:
                    print("Statut invalide. Veuillez entrer 'accepter' ou 'refuser'.")
                    connexion.close()
                    return

                connexion.commit()
                print("Demande traitée avec succès.")
            else:
                print("L'employé n'a pas suffisamment de jours de congé pour cette demande.")
        else:
            print("Il n'y a pas de demande avec cet ID")
            break
        
        connexion.close()


def se_deconnecter():
    print("Fermeture de l'application")
    connect_db().close()
    