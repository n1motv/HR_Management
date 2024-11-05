from auth import connexion_utilisateur
from db_setup import cree_table_utilisateurs, cree_compte_admin,cree_table_conges
from fonctionality import ajouter_conge_mensuel
def menu_principale():
    print("Bienvenue dans le gestionnaire de resources humaines! ")
    while True:
        print("\n--- Menu Principal ---")
        print("1. Connexion en tant qu'admin")
        print("2. Connexion en tant qu'employé")
        print("3. Quitter")

        choix = input("Veuillez choisir une option : ")

        if choix== "1" :
            connexion_utilisateur(role="admin")
        elif choix == "2" :
            connexion_utilisateur(role="employe")
        elif choix == "3" :
            print("Fermeture de l'application")
            break
        else:
            print("Choix invalide veillez réessayer.")

if __name__ =="__main__":
    cree_table_utilisateurs()
    cree_compte_admin()
    cree_table_conges()
    ajouter_conge_mensuel()
    menu_principale()
