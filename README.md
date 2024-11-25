# HR Management System

Un système de gestion des ressources humaines (RH) permettant aux administrateurs et employés de gérer efficacement les informations et les demandes de congés.

## Fonctionnalités

### Administrateur
- **Gestion des employés :**
  - Afficher les informations des employés.
  - Ajouter un nouvel employé avec des détails comme le nom, le poste, le département, etc.
  - Mettre à jour les informations d'un employé.
- **Gestion des demandes de congés :**
  - Afficher toutes les demandes de congés.
  - Accepter ou refuser une demande, avec mise à jour automatique du solde de congés.
- **Système de sécurité :**
  - Connexion sécurisée avec hachage des mots de passe.

### Employé
- **Gestion personnelle :**
  - Voir ses informations personnelles.
  - Soumettre une nouvelle demande de congé.
  - Suivre l'état de ses demandes de congés.
- **Connexion sécurisée :**
  - Accès protégé par email et mot de passe.

### Automatisation
- **Mise à jour mensuelle des congés :**
  - Chaque mois, tous les employés reçoivent automatiquement 2.5 jours de congés supplémentaires (avec vérification pour éviter les doublons).

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/n1motv/HR_Management.git
   cd HR_Management
   ```
2. Installez les dépendances nécessaires :
 ```bash
   pip install -r requirements.txt
   ```
3. Configurez la base de données :
   ```bash
   python db_setup.py
   ```

## Utilisation
1. Lancer l'application :

  ```bash
Copier le code
python main.py
  ```
2. Connexion :

Les administrateurs peuvent se connecter avec l'email admin.
Les employés doivent utiliser leur adresse email et leur mot de passe.

3. Gestion des rôles :

Une fois connecté, un administrateur ou un employé sera redirigé vers le menu approprié.

## Contributions:

Les contributions sont les bienvenues ! Veuillez soumettre vos suggestions via des issues ou des pull requests.

## Auteurs:

n1motv - Développeur principal.
