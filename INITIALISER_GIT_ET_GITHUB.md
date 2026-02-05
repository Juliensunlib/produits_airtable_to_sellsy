# Comment initialiser Git et pousser vers GitHub

## Votre situation actuelle

Votre projet n'est **pas encore sur GitHub**. C'est pour ça que vous ne voyez pas le bouton "Run workflow" dans Actions.

Ce guide vous explique comment :
1. Initialiser Git localement
2. Créer un dépôt sur GitHub
3. Pousser votre code vers GitHub
4. Lancer le workflow pour récupérer les codes comptables

---

## Étape 1 : Initialiser Git localement

Dans le dossier de votre projet, exécutez :

```bash
# Initialiser le dépôt git
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Premier commit - Projet de synchronisation Airtable vers Sellsy"
```

**Résultat attendu :**
```
Initialized empty Git repository in /votre/chemin/.git/
[master (root-commit) abc1234] Premier commit - Projet de synchronisation Airtable vers Sellsy
 XX files changed, XXX insertions(+)
```

---

## Étape 2 : Créer un dépôt sur GitHub

### Option A : Via l'interface web (Recommandé)

1. **Allez sur https://github.com**
2. **Connectez-vous** à votre compte
3. **Cliquez sur le "+" en haut à droite** → "New repository"
4. **Remplissez le formulaire :**
   - Repository name : `airtable-sellsy-sync` (ou autre nom)
   - Description : "Synchronisation automatique Airtable vers Sellsy"
   - Visibilité : **Private** (recommandé pour les secrets)
   - **NE COCHEZ PAS** "Initialize with README" (vous avez déjà le code)
   - **NE COCHEZ PAS** "Add .gitignore" (vous l'avez déjà)
   - **NE COCHEZ PAS** "Choose a license" (optionnel)
5. **Cliquez sur "Create repository"**

### Option B : Via GitHub CLI

Si vous avez installé GitHub CLI (`gh`) :

```bash
gh repo create airtable-sellsy-sync --private --source=. --remote=origin
```

---

## Étape 3 : Lier votre projet local à GitHub

Après avoir créé le dépôt sur GitHub, GitHub vous affiche des commandes. **Utilisez la section "…or push an existing repository from the command line"** :

```bash
# Remplacez VOTRE_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git

# Renommer la branche en 'main' (si nécessaire)
git branch -M main

# Pousser le code vers GitHub
git push -u origin main
```

**Exemple concret :**
```bash
git remote add origin https://github.com/johndoe/airtable-sellsy-sync.git
git branch -M main
git push -u origin main
```

**Si Git vous demande de vous authentifier :**

Vous avez 2 options :

### Option 1 : Personal Access Token (Recommandé)

1. Allez sur https://github.com/settings/tokens
2. Cliquez sur "Generate new token" → "Generate new token (classic)"
3. Cochez au minimum :
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
4. Cliquez sur "Generate token"
5. **COPIEZ le token** (vous ne pourrez plus le voir après !)
6. Quand Git demande le mot de passe, **collez le token** au lieu de votre mot de passe

### Option 2 : GitHub CLI (Plus simple)

```bash
# Installer GitHub CLI si ce n'est pas fait
# Sur macOS : brew install gh
# Sur Ubuntu : sudo apt install gh

# S'authentifier
gh auth login

# Suivez les instructions interactives
```

---

## Étape 4 : Configurer les secrets GitHub

Maintenant que votre code est sur GitHub, configurez les secrets :

1. **Allez sur votre dépôt GitHub**
2. **Cliquez sur "Settings"** (en haut)
3. **Dans le menu de gauche : "Secrets and variables" → "Actions"**
4. **Cliquez sur "New repository secret"**

**Ajoutez ces 4 secrets un par un :**

| Nom du secret | Où trouver la valeur |
|---------------|----------------------|
| `SELLSY_CONSUMER_TOKEN` | Sellsy → Paramètres → API |
| `SELLSY_CONSUMER_SECRET` | Sellsy → Paramètres → API |
| `SELLSY_USER_TOKEN` | Sellsy → Paramètres → API |
| `SELLSY_USER_SECRET` | Sellsy → Paramètres → API |

Pour chaque secret :
1. Name : Copiez exactement le nom (sensible à la casse !)
2. Secret : Collez la valeur depuis votre fichier `.env` local
3. Cliquez sur "Add secret"

**📖 Guide détaillé :** [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)

---

## Étape 5 : Vérifier que GitHub Actions est activé

1. **Toujours dans Settings**
2. **Allez dans "Actions" → "General"** (menu de gauche)
3. **Vérifiez que "Allow all actions and reusable workflows" est coché**
4. Si ce n'est pas le cas, cochez-le et cliquez sur "Save"

---

## Étape 6 : Lancer le workflow

**Maintenant vous pouvez lancer le workflow !**

1. **Allez sur votre dépôt GitHub**
2. **Cliquez sur l'onglet "Actions"** (en haut)
3. **Dans la liste de gauche, cliquez sur "Récupération des codes comptables Sellsy"**
4. **À droite, cliquez sur "Run workflow"**
5. **Cliquez sur le bouton vert "Run workflow"**
6. **Attendez 1 minute** que le workflow s'exécute
7. **Cliquez sur le workflow** pour voir les résultats

---

## Vérification rapide

Pour vérifier que tout est prêt avant de pousser :

```bash
# Vérifier que Git est initialisé
git status

# Vérifier les fichiers qui seront poussés
git log --oneline

# Vérifier le remote GitHub
git remote -v
```

**Résultat attendu :**
```
origin  https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git (fetch)
origin  https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git (push)
```

---

## Commandes récapitulatives

Voici toutes les commandes dans l'ordre :

```bash
# 1. Initialiser Git
git init
git add .
git commit -m "Premier commit"

# 2. Lier à GitHub (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git
git branch -M main
git push -u origin main

# 3. Vérifier que tout est OK
git status
```

Ensuite, allez sur GitHub pour configurer les secrets et lancer le workflow.

---

## Problèmes courants

### Erreur : "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git
```

### Erreur : "Permission denied"

Vous devez vous authentifier avec un Personal Access Token (voir Étape 3).

### Erreur : "Updates were rejected"

Forcez le push (attention, cela écrasera le dépôt distant) :

```bash
git push -u origin main --force
```

### Le workflow n'apparaît pas dans Actions

Attendez 30 secondes après le push, puis rafraîchissez la page GitHub.

Si ça ne fonctionne toujours pas :
1. Vérifiez que le fichier `.github/workflows/get_accounting_codes.yml` existe
2. Vérifiez qu'il a bien été poussé : `git ls-files .github/workflows/`
3. Vérifiez la syntaxe YAML sur https://www.yamllint.com/

---

## Alternative : Exécution locale

Si vous ne voulez pas utiliser GitHub Actions, vous pouvez exécuter le script en local :

```bash
bash setup_and_get_codes.sh
```

**📖 Guide :** [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md)

---

## Besoin d'aide ?

- **Problèmes Git :** https://docs.github.com/en/get-started
- **Problèmes GitHub Actions :** [TROUBLESHOOTING_WORKFLOW.md](TROUBLESHOOTING_WORKFLOW.md)
- **Problèmes de secrets :** [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)
- **Documentation complète :** [README.md](README.md)

---

## Et après ?

Une fois le workflow lancé avec succès :

1. Récupérez l'ID du code 628000 dans le résumé
2. Configurez `config.py` avec cet ID
3. Décommentez les lignes dans `airtable_client.py`
4. Committez et pushez les changements
5. Lancez le workflow de synchronisation

**📖 Guide complet :** [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)
