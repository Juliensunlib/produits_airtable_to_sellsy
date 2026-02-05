# Configuration des Catégories et Codes Comptables

## Résumé de la Configuration

### Catégories Sellsy Créées

Les catégories suivantes ont été créées dans Sellsy et configurées dans `config.py` :

| Catégorie Airtable | ID Sellsy | Code Comptable à Configurer |
|-------------------|-----------|----------------------------|
| **Abonnement** | 57 | 706000 (Prestations de services) |
| **Caution** | 58 | À définir selon vos besoins |

### Codes Comptables (dans config.py)

```python
ACCOUNTING_CODE_MAPPING = {
    '706000': '75',  # Prestations de services (code de VENTE pour abonnements)
    '628000': '76',  # Autre prestation
    # Autres codes...
}
```

## Comment ça fonctionne ?

### 1. Synchronisation Airtable → Sellsy

Quand vous synchronisez un service d'Airtable vers Sellsy :

- **Si la catégorie = "Abonnement"** → Le service sera créé dans Sellsy avec `categoryid: 57`
- **Si la catégorie = "Caution"** → Le service sera créé dans Sellsy avec `categoryid: 58`

### 2. Héritage des Codes Comptables

Les codes comptables **ne sont PAS envoyés via l'API**. Ils sont **hérités de la catégorie** Sellsy.

**Important :** L'API Sellsy v1 ne permet pas de modifier les codes comptables des services individuels.

## Configuration Manuelle dans Sellsy

### Étape 1 : Configurer le Code Comptable de la Catégorie Abonnement

1. Connectez-vous à Sellsy
2. Allez dans **Paramètres** → **Catalogue** → **Catégories**
3. Trouvez la catégorie **"Abonnement"** (ID: 57)
4. Cliquez sur **Modifier**
5. Dans **Code comptable de VENTE**, sélectionnez **706000** (Prestations de services)
6. Enregistrez

### Étape 2 : Configurer le Code Comptable de la Catégorie Caution

1. Dans **Paramètres** → **Catalogue** → **Catégories**
2. Trouvez la catégorie **"Caution"** (ID: 58)
3. Cliquez sur **Modifier**
4. Définissez le code comptable de VENTE selon vos besoins
5. Enregistrez

### Étape 3 : Vérifier

1. Tous les services de catégorie **Abonnement** hériteront du code **706000**
2. Tous les services de catégorie **Caution** hériteront du code que vous avez défini

## Test

Pour tester que tout fonctionne :

```bash
python3 test_final_categories.py
```

Ce script crée des services de test avec les catégories Abonnement et Caution et vérifie que les catégories sont correctement associées.

## Synchronisation Complète

Une fois la configuration manuelle terminée dans Sellsy :

```bash
python3 main.py
```

Tous vos services d'Airtable seront synchronisés vers Sellsy avec les bonnes catégories et hériteront automatiquement des codes comptables configurés.

## Limitation de l'API Sellsy v1

⚠️ **Important** : L'API Sellsy v1 (apifeed.sellsy.com) ne permet pas de :
- Définir les codes comptables au niveau du service via l'API
- Récupérer les codes comptables via `Catalogue.getOne` (le champ est vide dans la réponse)

Les codes comptables doivent être configurés **au niveau de la catégorie** dans l'interface Sellsy, et seront ensuite **hérités automatiquement** par tous les services de cette catégorie.

## Codes Disponibles

Pour voir tous les codes comptables disponibles dans Sellsy avec leurs IDs :

```bash
python3 find_accounting_code_id.py 706000
```

(Note : Certaines méthodes API pour récupérer les codes comptables ne sont pas disponibles dans l'API v1)
