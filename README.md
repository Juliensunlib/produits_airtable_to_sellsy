# Synchronisation Airtable vers Sellsy

Ce projet automatise la synchronisation des services entre Airtable et Sellsy en utilisant GitHub Actions. Les services sont récupérés depuis une table Airtable et synchronisés vers Sellsy toutes les 6 heures.

---

## ⚠️ VOTRE PROJET N'EST PAS ENCORE SUR GITHUB

**Vous ne voyez pas le workflow dans GitHub Actions ?** C'est normal !

**Solution automatique en 1 commande :**
```bash
bash setup_git_github.sh
```

**📖 Pourquoi et comment ?** [POURQUOI_PAS_DE_WORKFLOW.md](POURQUOI_PAS_DE_WORKFLOW.md)

---

## 🚀 Guides de démarrage rapide

**Une fois sur GitHub :**
- **Récupérer les codes comptables** : [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) ⭐ Recommandé
- **Configuration complète** : [QUICKSTART.md](QUICKSTART.md)

**Alternative locale (sans GitHub) :**
- **Récupérer les codes en local** : [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md)
- Commande : `bash setup_and_get_codes.sh`

## Fonctionnalités

- Récupération automatique des services à synchroniser dans Airtable
- Création, mise à jour de services dans Sellsy
- Statut de synchronisation mis à jour dans Airtable
- Exécution automatique toutes les 6 heures via GitHub Actions
- Possibilité de lancer manuellement la synchronisation

## Prérequis

- Un compte GitHub
- Un compte Airtable avec une base de données de services
- Un compte Sellsy avec un accès API

## Configuration

### 1. Configurer les secrets GitHub

**📖 Guide complet : [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)**

Le guide détaillé vous explique :
- Comment obtenir vos clés API Sellsy et Airtable
- Comment configurer chaque secret dans GitHub
- Comment tester que tout fonctionne
- Dépannage des problèmes courants

**Secrets requis :**

Dans votre dépôt GitHub, allez dans Settings > Secrets and variables > Actions et ajoutez :

- `AIRTABLE_API_KEY`: Votre clé API Airtable
- `AIRTABLE_BASE_ID`: L'ID de votre base Airtable
- `AIRTABLE_TABLE_NAME`: Le nom de votre table Airtable contenant les services
- `SELLSY_CONSUMER_TOKEN`: Votre token consommateur Sellsy API V1
- `SELLSY_CONSUMER_SECRET`: Votre secret de consommateur Sellsy API V1
- `SELLSY_USER_TOKEN`: Votre token utilisateur Sellsy API V1
- `SELLSY_USER_SECRET`: Votre secret utilisateur Sellsy API V1

### 2. Configuration des codes comptables

Pour que les codes comptables soient correctement assignés aux services, vous devez configurer le mapping dans le fichier `config.py`.

#### Méthode recommandée : Workflow GitHub 🚀

**📖 Guide complet : [LANCER_WORKFLOW_GITHUB.md](LANCER_WORKFLOW_GITHUB.md)**

Lancez le workflow directement depuis GitHub Actions :
1. Onglet **Actions** > **"Récupération des codes comptables Sellsy"**
2. Cliquez sur **"Run workflow"** > **"Run workflow"**
3. Attendez 1 minute
4. Récupérez l'ID du code 628000 dans le résumé

Avantages : Pas d'installation locale, secrets déjà configurés dans GitHub, résultats en 1 minute !

#### Alternative : Exécution locale

**📖 Guide complet : [OBTENIR_IDS_LOCALEMENT.md](OBTENIR_IDS_LOCALEMENT.md)

**Option 1 : Script automatique**

```bash
bash setup_and_get_codes.sh
```

**Option 2 : Script Python direct**

```bash
python3 get_all_accounting_codes.py
```

Ce script va :
- Récupérer tous les codes comptables depuis votre compte Sellsy
- Afficher une liste complète avec les IDs
- Chercher automatiquement le code 628000
- Sauvegarder la liste dans `accounting_codes_sellsy.json`
- Vous donner les instructions exactes pour configurer `config.py`

**Prérequis :** Assurez-vous que votre fichier `.env` contient vos clés API Sellsy.

#### Méthode manuelle

Si vous préférez récupérer l'ID manuellement :

1. Connectez-vous à votre interface Sellsy
2. Allez dans **Paramètres** > **Comptabilité** > **Plan comptable**
3. Trouvez le code comptable souhaité (ex: 628000)
4. Cliquez sur le code pour voir ses détails
5. L'ID du code comptable se trouve dans l'URL : `https://votrecompte.sellsy.com/settings/accountdatas/edit/ID`

#### Configuration dans config.py

Une fois l'ID récupéré, ajoutez-le dans `config.py` :

```python
ACCOUNTING_CODE_MAPPING = {
    '628000': 'ID_TROUVE',  # Remplacez ID_TROUVE par l'ID récupéré
    '706000': 'ID_TROUVE',
    '601000': 'ID_TROUVE',
}
```

Puis décommentez les lignes 120-122 dans `airtable_client.py` pour activer l'ajout automatique des codes comptables.

**Note :** Les codes comptables sont automatiquement assignés selon la catégorie du service :
- Catégorie "Abonnement" → Code comptable 628000

### 3. Structure de la table Airtable

Votre table Airtable doit contenir les champs suivants:

- `Nom du service` (Texte): Titre du service
- `Référence` (Texte): Code unique pour identifier le service
- `ID Sellsy` (Texte): ID du service dans Sellsy
- `Statut de synchronisation` (Sélection): "À synchroniser", "Synchronisé", "Erreur"
- `Dernière synchronisation` (Date/Heure): Date de la dernière synchronisation
- `À synchroniser` (Case à cocher): Pour marquer les services à synchroniser
- `Description` (Texte long): Description détaillée du service
- `Description courte` (Texte): Version résumée
- `Catégorie` (Sélection): Type de service
- `Prix HT` (Monétaire): Tarif hors taxes
- `Taux TVA` (Nombre): Pourcentage de TVA
- `Unité` (Sélection): Heure, jour, forfait, etc.
- `Actif` (Case à cocher): Si le service est actuellement proposé

## Utilisation

### Synchronisation automatique

La synchronisation s'exécute automatiquement toutes les 6 heures selon la configuration dans `.github/workflows/sync.yml`.

### Synchronisation manuelle

Vous pouvez également lancer manuellement la synchronisation depuis l'onglet Actions de votre dépôt GitHub:

1. Accédez à l'onglet "Actions"
2. Sélectionnez le workflow "Synchronisation Airtable vers Sellsy"
3. Cliquez sur "Run workflow"

### Marquer un service pour synchronisation

Dans Airtable, pour qu'un service soit synchronisé:
1. Modifiez le service
2. Définissez "Statut de synchronisation" sur "À synchroniser" ou cochez la case "À synchroniser"
3. Attendez la prochaine synchronisation automatique ou lancez-la manuellement

## Dépannage

Si un service n'est pas synchronisé correctement:

1. Vérifiez le "Statut de synchronisation" dans Airtable
2. Si le statut est "Erreur", consultez le message d'erreur dans le champ correspondant
3. Vérifiez les logs d'exécution dans GitHub Actions pour plus de détails

## Scripts utilitaires

Ce projet contient plusieurs scripts utilitaires pour faciliter la configuration et le dépannage.

**📖 Consultez le fichier [SCRIPTS.md](SCRIPTS.md) pour la documentation complète de tous les scripts disponibles.**

Scripts principaux :
- `main.py` - Synchronisation Airtable → Sellsy
- `get_all_accounting_codes.py` - Récupération automatique des codes comptables depuis Sellsy
- `find_accounting_code_id.py` - Analyse d'un service existant pour trouver son code comptable

## Support

Pour tout problème ou question, veuillez ouvrir une issue sur ce dépôt GitHub.
