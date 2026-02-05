# 🚀 COMMENCEZ ICI

## Votre situation

Vous voulez récupérer les codes comptables Sellsy directement depuis GitHub Actions, mais **le workflow n'apparaît pas** dans Actions.

## Pourquoi ?

**Votre projet n'est pas encore sur GitHub.** C'est tout !

## Solution en 3 étapes

### Étape 1 : Pousser votre projet vers GitHub

**Option A : Automatique (RECOMMANDÉE)**

```bash
bash setup_git_github.sh
```

Ce script fait tout pour vous en 2 minutes.

**Option B : Manuelle**

```bash
# Créer un dépôt sur https://github.com/new
# Puis exécuter :

git init
git add .
git commit -m "Premier commit"
git remote add origin https://github.com/VOTRE_USERNAME/nom-du-depot.git
git branch -M main
git push -u origin main
```

📖 Guide détaillé : [INITIALISER_GIT_ET_GITHUB.md](INITIALISER_GIT_ET_GITHUB.md)

### Étape 2 : Configurer les secrets GitHub

1. Allez sur GitHub → Settings → Secrets and variables → Actions
2. Ajoutez 4 secrets :
   - `SELLSY_CONSUMER_TOKEN`
   - `SELLSY_CONSUMER_SECRET`
   - `SELLSY_USER_TOKEN`
   - `SELLSY_USER_SECRET`

📖 Guide détaillé : [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)

### Étape 3 : Lancer le workflow

1. GitHub → Actions
2. "Récupération des codes comptables Sellsy"
3. "Run workflow"
4. Attendez 1 minute
5. Récupérez l'ID du code 628000

📖 Guide détaillé : [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)

---

## Alternative : Exécution locale

Si vous ne voulez pas utiliser GitHub :

```bash
bash setup_and_get_codes.sh
```

📖 Guide détaillé : [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md)

---

## Tous les guides disponibles

| Guide | Description |
|-------|-------------|
| **START_HERE.md** ← Vous êtes ici | Point de départ |
| [POURQUOI_PAS_DE_WORKFLOW.md](POURQUOI_PAS_DE_WORKFLOW.md) | Explication du problème |
| [INITIALISER_GIT_ET_GITHUB.md](INITIALISER_GIT_ET_GITHUB.md) | Pousser vers GitHub |
| [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md) | Configurer les secrets |
| [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) | Lancer le workflow |
| [TROUBLESHOOTING_WORKFLOW.md](TROUBLESHOOTING_WORKFLOW.md) | Résoudre les problèmes |
| [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md) | Alternative locale |

---

## Récapitulatif visuel

```
1. Pousser vers GitHub
   │
   ├─ Option A : bash setup_git_github.sh
   └─ Option B : Commandes manuelles
   │
   ▼
2. Configurer les secrets
   │
   └─ Settings > Secrets > Ajouter 4 secrets
   │
   ▼
3. Lancer le workflow
   │
   └─ Actions > Run workflow
   │
   ▼
4. Récupérer l'ID du code 628000
   │
   └─ Copier depuis le résumé
   │
   ▼
5. Configurer config.py
   │
   └─ Ajouter l'ID dans ACCOUNTING_CODE_MAPPING
   │
   ▼
6. Synchroniser
   │
   └─ Lancer le workflow de synchronisation
```

---

**Prêt ?** Commencez par :

```bash
bash setup_git_github.sh
```
