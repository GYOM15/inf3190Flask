# **Gestionnaire d'Adoption d'Animaux de Compagnie**

Ce projet est une application web développée dans le cadre du TP3 du cours INF3190 – Introduction à la programmation web (Automne 2024). L'application permet de gérer l'adoption d'animaux de compagnie. Les utilisateurs peuvent consulter les animaux disponibles, rechercher un animal, et mettre un animal en adoption via un formulaire sécurisé.

---

## **Fonctionnalités**

### **Consultation des Animaux**
- Les utilisateurs peuvent consulter une liste paginée des animaux disponibles pour adoption.
- Chaque animal possède une page dédiée affichant ses détails et l'adresse de son propriétaire.
- Un moteur de recherche permet de trouver des animaux selon leur nom, leur espèce, ou leur description.
- La page d'accueil affiche 5 animaux au hasard avec un lien vers leur page respective.
- Sur la page d'un animal, un lien permet de contacter le propriétaire par courriel pour manifester un intérêt.

### **Mise en Adoption**
- Les utilisateurs peuvent mettre un animal en adoption en remplissant un formulaire contenant les informations suivantes :
  - **Nom de l'animal** (entre 3 et 20 caractères, sans virgule).
  - **Espèce** (ex. chien, chat, poisson).
  - **Race** (ex. Schnauzer).
  - **Âge** (numérique).
  - **Description** (texte court sur l'animal).
  - **Courriel** (doit être un courriel valide).
  - **Adresse complète** (adresse civique, ville, code postal canadien).

- Une fois le formulaire soumis, l'animal est ajouté à la base de données, et l'utilisateur est redirigé vers la page dédiée de l'animal.

---

## **Structure de la Base de Données**

La base de données SQLite contient une table `animals` avec les colonnes suivantes :
- `id` : identifiant unique de l'animal (généré automatiquement).
- `nom` : nom de l'animal.
- `espece` : espèce de l'animal.
- `race` : race de l'animal.
- `age` : âge en années.
- `description` : description textuelle.
- `courriel` : adresse courriel du propriétaire.
- `adresse` : adresse civique où récupérer l'animal.
- `ville` : ville de résidence de l'animal.
- `cp` : code postal.

---

## **Validations**

### **Frontend**
- Tous les champs sont obligatoires.
- Aucun champ ne peut contenir de virgule.
- **Nom** : entre 3 et 20 caractères.
- **Âge** : numérique, entre 0 et 30.
- **Courriel** : doit respecter un format valide.
- **Adresse** : doit inclure une adresse civique, une ville, et un code postal au format canadien.
- Si une validation échoue, un message d'erreur s'affiche à côté du champ concerné.

### **Backend**
- Les mêmes validations sont effectuées côté serveur pour garantir l'intégrité des données.

---

## **Technologies Utilisées**

### **Frontend**
- **HTML5**
- **CSS3**
- **JavaScript**
  - Utilisation de DOM pour la gestion des erreurs et confirmations.
  - Aucun usage de pop-ups (alert, prompt).

### **Backend**
- **Python 3.12+**
- **Flask 3.0+**


---

# Structure du Projet INF3190FLASK

```bash
INF3190FLASK/
├── .venv/                   # Environnement virtuel Python
├── app/                     # Dossier principal de l'application Flask
│   ├── routes/              # Routes de l'application
│   ├── services/            # Services pour la logique métier
│   ├── static/              # Ressources statiques (CSS, JS, etc.)
│   ├── templates/           # Templates HTML (Jinja2)
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── database.py          # Gestion de la base de données
│   ├── forms.py             # Gestion des formulaires
│   ├── models.py            # Modèles de base de données
├── my_env                   # Fichier/dossier lié à l'environnement
├── .env                     # Variables d'environnement
├── .gitignore               # Fichier pour ignorer certains fichiers/dossiers dans Git
├── app.log                  # Fichier de logs pour l'application
├── app.py                   # Point d'entrée de l'application
├── config.py                # Configuration de l'application Flask
├── database.db              # Base de données SQLite
├── README.md                # Documentation du projet
├── requirements.txt         # Dépendances Python du projet
└── script_push.sh           # Script pour le déploiement ou la gestion
```

---

## **Instructions d'Installation**

1. **Cloner le Dépôt :**
   ```bash
   git clone <url-du-depot>
   cd INF3190FLASK
   ```

2. **Configurer l'Environnement Virtuel :**
   ```bash
   python -m venv env
   source env/bin/activate   # Sur Windows : env\Scripts\activate
   ```

3. **Installer les Dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'Application :**
   ```bash
   python run.py
   ```
   L'application sera accessible à l'adresse [http://127.0.0.1:5000](http://127.0.0.1:5000).

## **Problème : Le Module Flask n'est pas Reconnu**

Si vous rencontrez une erreur indiquant que le module Flask n'est pas reconnu dans votre projet, suivez ces étapes pour résoudre le problème en configurant l'interpréteur Python correct :

### **Étapes pour Configurer l'Interpréteur Python :**

1. **Ouvrir la Palette de Commandes :**
   - Appuyez sur `Command + Shift + P` (macOS) ou `Ctrl + Shift + P` (Linux/Windows).

2. **Rechercher l'Interpréteur :**
   - Tapez `Python: Select Interpreter` dans la barre de recherche.

3. **Choisir l'Environnement Virtuel :**
   - Dans la liste des interpréteurs disponibles, sélectionnez celui correspondant à l'environnement virtuel de votre projet (ex. : `INF3190FLASK/.venv/bin/python` ou similaire).

4. **Vérifier que Flask est Installé :**
   - Une fois l'interpréteur sélectionné, assurez-vous que le module Flask est installé :
     ```bash
     pip show flask
     ```
   - Si Flask n'est pas installé, utilisez la commande suivante :
     ```bash
     pip install flask
     ```

### **Remarques pour macOS/Linux et Windows :**

- **Pour macOS/Linux :**
  - Si l'interpréteur n'est pas listé automatiquement, vous pouvez naviguer manuellement jusqu'à votre environnement virtuel (`env/bin/python`).

- **Pour Windows :**
  - Naviguez manuellement jusqu'au fichier `env\Scripts\python.exe` si nécessaire.

---

### **Redémarrer l'Environnement**

Après avoir configuré l'interpréteur, redémarrez Visual Studio Code pour appliquer les modifications.

---

## **Fonctionnalités Clés**

1. **Page d'accueil :** Affiche 5 animaux sélectionnés au hasard.
2. **Recherche :** Permet de trouver des animaux en fonction de mots-clés.
3. **Mise en adoption :** Un formulaire permet d'ajouter un animal.
4. **Administration :** Panneau permettant de gérer les animaux :
   - Modifier leurs informations.
   - Supprimer un animal.

---

## **Règles Spécifiques**

- Respect strict des règles POST-REDIRECT-GET.
- Aucune librairie ou framework Python externe (autre que Flask) n'est autorisé.
- Toutes les validations sont faites à la fois sur le frontend et le backend.

---

### **Exclusion des Dossiers `__pycache__`**

Pour éviter de pousser accidentellement les dossiers `__pycache__` dans votre dépôt, ces derniers doivent être exclus via le fichier `.gitignore`. Voici une commande pour supprimer tous les dossiers `__pycache__` de votre projet :

#### Sous Linux/MacOS :
```bash
find . -type d -name "__pycache__" -exec rm -rf {} +

```
#### Sous Windows (PowerShell) :
```powershell
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```
#### Sous Windows (CMD) :
```cmd
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
```
Ces commandes permettent de supprimer tous les dossiers `__pycache__` de votre projet avant de faire un commit ou un push.
---
## **Licence Académique**
Ce projet a été réalisé dans le cadre du TP3 du cours **INF3190 – Introduction à la programmation web (Automne 2024)**. Il est destiné à un usage académique et pédagogique uniquement.
Toute réutilisation ou redistribution doit être conforme aux règlements académiques en vigueur. Les travaux soumis doivent être le résultat du travail personnel des étudiants. La copie ou le plagiat de ce projet peut entraîner des sanctions disciplinaires conformément au règlement de l'université.
---

"""