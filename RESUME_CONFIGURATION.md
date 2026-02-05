# ✅ Configuration Complète des Catégories

## Ce qui a été fait

### 1. Catégories créées dans Sellsy

| Catégorie | ID Sellsy | Statut |
|-----------|-----------|--------|
| **Abonnement** | 57 | ✅ Créée et configurée |
| **Caution** | 58 | ✅ Créée et configurée |

### 2. Configuration dans config.py

```python
CATEGORY_MAPPING = {
    'Abonnement': '57',  # ✅
    'Caution': '58',     # ✅
}

ACCOUNTING_CODE_MAPPING = {
    '706000': '75',  # Prestations de services (pour abonnements)
    # Autres codes...
}
```

### 3. Test effectué

Le service **1709** a été mis à jour avec la catégorie **Abonnement (ID: 57)** ✅

**État actuel du service 1709 :**
- Catégorie : 57 (Abonnement) ✅
- Code comptable : 275500 (hérité de la catégorie)

## ⚠️ ACTION REQUISE

Le code comptable **275500** provient de la configuration actuelle de la catégorie Abonnement dans Sellsy.

**Pour que les services utilisent le code 706000**, vous devez :

### Étape 1 : Modifier la Catégorie Abonnement

1. Connectez-vous à **Sellsy**
2. Allez dans **Paramètres** → **Catalogue** → **Catégories**
3. Trouvez la catégorie **"Abonnement"** (ID: 57)
4. Cliquez sur **Modifier**
5. Dans **"Code comptable de vente"**, remplacez **275500** par **706000**
6. Enregistrez

### Étape 2 : (Optionnel) Configurer la Catégorie Caution

1. Dans **Paramètres** → **Catalogue** → **Catégories**
2. Trouvez la catégorie **"Caution"** (ID: 58)
3. Définissez le code comptable de vente selon vos besoins
4. Enregistrez

## Comment utiliser

Désormais, quand vous synchronisez un service d'Airtable :

- **Si Catégorie = "Abonnement"** → Service créé dans Sellsy avec :
  - `categoryid: 57`
  - Code comptable hérité de la catégorie (706000 après votre modification)

- **Si Catégorie = "Caution"** → Service créé dans Sellsy avec :
  - `categoryid: 58`
  - Code comptable hérité de la catégorie (selon votre configuration)

## Synchronisation

Pour synchroniser vos services Airtable → Sellsy :

```bash
python3 main.py
```

Le script :
1. Récupère les services "À synchroniser" d'Airtable
2. Trouve la catégorie correspondante dans `CATEGORY_MAPPING`
3. Crée/met à jour le service dans Sellsy avec la bonne catégorie
4. Le code comptable est automatiquement hérité de la catégorie

## Vérification

Pour vérifier que tout fonctionne après modification dans Sellsy :

```bash
python3 check_service_1709.py
```

Vous devriez voir :
- Code comptable de VENTE : **706000** (au lieu de 275500)

## Documentation complète

Consultez `CONFIGURATION_CATEGORIES.md` pour plus de détails.

---

**Résumé** : La synchronisation est configurée. Il ne reste qu'à modifier le code comptable de la catégorie Abonnement dans l'interface Sellsy (275500 → 706000).
