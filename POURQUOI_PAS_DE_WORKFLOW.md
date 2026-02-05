# Pourquoi je ne vois pas le workflow dans GitHub Actions ?

## Le problème

Vous allez sur GitHub Actions et vous ne voyez **PAS** le bouton "Run workflow" pour lancer la récupération des codes comptables.

## La raison

**Votre projet n'est pas encore sur GitHub !**

Le workflow ne peut exister dans GitHub Actions que si :
1. ✅ Votre code est dans un dépôt Git local
2. ✅ Ce dépôt est lié à un dépôt GitHub
3. ✅ Le code a été poussé vers GitHub

Si l'une de ces conditions n'est pas remplie, le workflow n'apparaîtra pas.

---

## Solution automatique (RECOMMANDÉE)

J'ai créé un script qui fait TOUT automatiquement pour vous :

```bash
bash setup_git_github.sh
```

**Ce script va :**
1. ✅ Initialiser Git dans votre projet
2. ✅ Créer le premier commit
3. ✅ Vous demander l'URL de votre dépôt GitHub
4. ✅ Lier votre projet à GitHub
5. ✅ Pousser tout le code vers GitHub
6. ✅ Vous donner les prochaines étapes

**Temps estimé : 2-3 minutes**

---

## Solution manuelle (Si vous préférez comprendre)

### Étape 1 : Créer le dépôt sur GitHub

1. **Allez sur https://github.com/new**
2. **Remplissez :**
   - Repository name : `airtable-sellsy-sync`
   - Description : "Synchronisation Airtable vers Sellsy"
   - Visibilité : **Private** (recommandé)
3. **NE COCHEZ RIEN** (pas de README, pas de .gitignore, pas de licence)
4. **Cliquez sur "Create repository"**

GitHub vous affiche maintenant des commandes. **Gardez cette page ouverte.**

### Étape 2 : Initialiser Git localement

Dans votre terminal, dans le dossier du projet :

```bash
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Premier commit"

# Renommer la branche en main
git branch -M main
```

### Étape 3 : Lier à GitHub et pousser

**Copiez l'URL de votre dépôt depuis la page GitHub** (format : https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git)

```bash
# Remplacez l'URL par la vôtre
git remote add origin https://github.com/VOTRE_USERNAME/airtable-sellsy-sync.git

# Pousser le code
git push -u origin main
```

**Si Git demande un mot de passe :**
- N'utilisez PAS votre mot de passe GitHub
- Utilisez un **Personal Access Token**
- Créez-en un ici : https://github.com/settings/tokens

### Étape 4 : Attendre et rafraîchir

1. **Attendez 30 secondes**
2. **Allez sur votre dépôt GitHub** (https://github.com/VOTRE_USERNAME/airtable-sellsy-sync)
3. **Rafraîchissez la page**
4. **Cliquez sur l'onglet "Actions"**
5. **Le workflow devrait maintenant apparaître !**

---

## Vérification rapide

Pour vérifier si votre projet est déjà un dépôt Git :

```bash
# Dans le dossier du projet
git status
```

**Résultats possibles :**

### ✅ Si vous voyez :
```
On branch main
nothing to commit, working tree clean
```
→ Votre projet est déjà un dépôt Git. Vérifiez le remote :
```bash
git remote -v
```

Si vous voyez une URL GitHub, votre projet est lié. Il faut juste pousser :
```bash
git push origin main
```

### ❌ Si vous voyez :
```
fatal: not a git repository
```
→ Votre projet n'est PAS un dépôt Git. Utilisez `bash setup_git_github.sh`

---

## Checklist complète

Cochez au fur et à mesure :

- [ ] J'ai créé un dépôt sur GitHub (https://github.com/new)
- [ ] J'ai initialisé Git localement (`git init`)
- [ ] J'ai créé le premier commit (`git add . && git commit -m "Premier commit"`)
- [ ] J'ai lié mon projet à GitHub (`git remote add origin URL`)
- [ ] J'ai poussé le code vers GitHub (`git push -u origin main`)
- [ ] J'ai attendu 30 secondes et rafraîchi la page GitHub
- [ ] Je vois l'onglet "Actions" sur GitHub
- [ ] Je vois le workflow "Récupération des codes comptables Sellsy" dans la liste

Si tout est coché, le bouton "Run workflow" devrait apparaître !

---

## Alternative : GitHub CLI (Plus rapide)

Si vous avez installé GitHub CLI (`gh`) :

```bash
# S'authentifier
gh auth login

# Créer le dépôt et pousser en une commande
gh repo create airtable-sellsy-sync --private --source=. --remote=origin --push
```

C'est tout ! Le dépôt est créé et le code est poussé automatiquement.

---

## Après avoir poussé vers GitHub

Une fois que votre code est sur GitHub :

### 1. Configurer les secrets (OBLIGATOIRE)

Sans les secrets, le workflow ne pourra pas fonctionner.

1. GitHub → Settings → Secrets and variables → Actions
2. Ajoutez ces 4 secrets :
   - `SELLSY_CONSUMER_TOKEN`
   - `SELLSY_CONSUMER_SECRET`
   - `SELLSY_USER_TOKEN`
   - `SELLSY_USER_SECRET`

**📖 Guide complet :** [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)

### 2. Lancer le workflow

1. Actions → "Récupération des codes comptables Sellsy"
2. "Run workflow" → "Run workflow"
3. Attendez 1 minute
4. Récupérez l'ID du code 628000

**📖 Guide complet :** [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)

---

## Besoin d'aide ?

**Guides disponibles :**
- [setup_git_github.sh](setup_git_github.sh) - **Script automatique** ⭐
- [INITIALISER_GIT_ET_GITHUB.md](INITIALISER_GIT_ET_GITHUB.md) - Guide complet étape par étape
- [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) - Démarrage rapide une fois sur GitHub
- [TROUBLESHOOTING_WORKFLOW.md](TROUBLESHOOTING_WORKFLOW.md) - Dépannage

**Je préfère exécuter en local sans GitHub :**
- [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md)
- `bash setup_and_get_codes.sh`

---

## Récapitulatif visuel

```
❌ SITUATION ACTUELLE
┌─────────────────────────────────┐
│  Votre ordinateur               │
│  ┌───────────────────────────┐  │
│  │  Projet (pas de Git)      │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘

       Pas de lien avec GitHub
       → Workflow invisible


✅ SITUATION APRÈS SETUP
┌─────────────────────────────────┐
│  Votre ordinateur               │
│  ┌───────────────────────────┐  │
│  │  Projet (avec Git)        │  │
│  └───────────┬───────────────┘  │
└──────────────┼──────────────────┘
               │
               │ git push
               ▼
┌─────────────────────────────────┐
│  GitHub                         │
│  ┌───────────────────────────┐  │
│  │  Dépôt                    │  │
│  │  + Workflow Actions       │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘

       → Workflow visible !
       → Bouton "Run workflow" ✅
```

---

**Prêt ?** Lancez le script :

```bash
bash setup_git_github.sh
```
