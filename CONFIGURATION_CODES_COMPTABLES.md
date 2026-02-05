# Configuration des codes comptables dans Sellsy

## Problème actuel

Le code comptable **628000** n'est pas appliqué aux services de catégorie "Abonnement" car l'API Sellsy v1 nécessite l'**ID** du code comptable, pas le code lui-même.

## Solution

Vous devez configurer manuellement le mapping des codes comptables dans le fichier `config.py`.

## Étapes à suivre

### 1. Trouver l'ID du code comptable 628000 dans Sellsy

1. **Connectez-vous** à votre interface Sellsy
2. Allez dans **Paramètres** > **Comptabilité** > **Plan comptable**
3. Trouvez le code comptable **628000** dans la liste
4. **Cliquez** sur le code pour ouvrir ses détails
5. Regardez l'**URL** dans votre navigateur, elle devrait ressembler à :
   ```
   https://votrecompte.sellsy.com/settings/accountdatas/edit/123456
   ```
6. L'ID se trouve à la fin de l'URL (dans cet exemple : `123456`)

### 2. Alternative : Inspecter l'élément via l'API

Si vous ne trouvez pas l'ID dans l'interface, vous pouvez également :

1. Créer un service test dans Sellsy avec le code comptable 628000
2. Récupérer les détails de ce service via l'API (méthode `Catalogue.getOne`)
3. Chercher le champ `accountingcodeid` dans la réponse

### 3. Configurer le mapping dans config.py

Ouvrez le fichier `config.py` et modifiez la section `ACCOUNTING_CODE_MAPPING` :

```python
ACCOUNTING_CODE_MAPPING = {
    '628000': '123456',  # Remplacez 123456 par l'ID réel trouvé
    '706000': None,      # Ajoutez l'ID si vous utilisez ce code
    '601000': None,      # Ajoutez l'ID si vous utilisez ce code
}
```

### 4. Configuration de la catégorie "Abonnement"

N'oubliez pas aussi de configurer le mapping de la catégorie "Abonnement" dans le même fichier :

```python
CATEGORY_MAPPING = {
    'Abonnement': 'ID_CATEGORIE_ABONNEMENT',  # ID à récupérer depuis Sellsy
    # Autres catégories...
}
```

Pour trouver l'ID de la catégorie, exécutez :
```bash
python main.py --list-categories
```

### 5. Tester la synchronisation

Une fois la configuration complétée, relancez la synchronisation :

```bash
python main.py
```

Le code comptable **628000** sera maintenant correctement appliqué à tous les services de catégorie "Abonnement".

## Exemple de configuration complète

```python
# Dans config.py

CATEGORY_MAPPING = {
    'Abonnement': '789',
    'Développement web': '123456',
    'Formation': '234567',
}

ACCOUNTING_CODE_MAPPING = {
    '628000': '45678',  # Code pour les abonnements
    '706000': '45679',  # Code pour les prestations de services
    '601000': '45680',  # Code pour les achats
}
```

## Notes importantes

- Les codes comptables sont **automatiquement appliqués** selon la catégorie :
  - Si la catégorie est "Abonnement" → Code comptable 628000
- Vous pouvez étendre cette logique dans `airtable_client.py` pour d'autres catégories
- Les IDs des codes comptables sont spécifiques à votre compte Sellsy
