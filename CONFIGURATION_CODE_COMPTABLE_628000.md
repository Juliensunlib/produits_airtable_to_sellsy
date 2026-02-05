# ✅ Configuration du Code Comptable 628000 - Abonnement

## 🎯 Objectif

Ajouter automatiquement le code comptable **628000** (Abonnement) lors de la création de services de catégorie "Abonnement" dans Sellsy depuis Airtable.

## 📝 Configuration réalisée

### 1. Récupération des codes comptables Sellsy

✅ **Script exécuté**: `get_all_accounting_codes.py`
- **Méthode API utilisée**: `Accounting.getList`
- **Code comptable trouvé**: 628000 - Abonnement
- **ID Sellsy**: **76**
- **Total**: 47 codes comptables récupérés

### 2. Configuration du mapping dans `config.py`

```python
ACCOUNTING_CODE_MAPPING = {
    '628000': '76',  # Abonnement ← CONFIGURÉ
    '706000': '2',   # Prestations de services
    '601000': '12',  # Achats stockés - Matières premières
    '411000': '1',   # Clients
    '401000': '3',   # Fournisseurs
}
```

### 3. Activation dans `airtable_client.py`

✅ **Code activé** (lignes 119-121):

```python
# Ajout automatique du code comptable 628000 pour les abonnements
if fields['Catégorie'].lower() == 'abonnement':
    sellsy_data['accountingCode'] = '628000'
    print(f"Code comptable 628000 (ID: 76) ajouté pour l'abonnement")
```

## 🧪 Tests effectués

✅ **Test 1**: Configuration du mapping
- Le code 628000 est bien mappé à l'ID 76

✅ **Test 2**: Mapping Airtable → Sellsy
- Les services de catégorie "Abonnement" reçoivent automatiquement le code 628000

✅ **Test 3**: Conversion code → ID
- Le code 628000 est bien converti en ID 76 pour l'API Sellsy

## 🚀 Utilisation

### Créer un service avec code comptable automatique:

1. **Dans Airtable**, créez un nouveau service:
   - **Catégorie**: `Abonnement` (respectez la casse)
   - Remplissez les autres champs (Nom, Prix, etc.)
   - **Statut**: Marquez-le "À synchroniser"

2. **Lancez la synchronisation**:
   ```bash
   python3 main.py
   ```

3. **Résultat**:
   - Le service sera créé dans Sellsy
   - Le code comptable 628000 (ID: 76) sera automatiquement ajouté
   - Vous verrez le message: `Code comptable '628000' associé à l'ID: 76`

## 📊 Flux de données

```
Airtable
  ↓
  Catégorie = "Abonnement"
  ↓
airtable_client.py
  ↓
  Ajoute accountingCode = '628000'
  ↓
sellsy_client.py
  ↓
  Convertit '628000' → ID: 76
  ↓
  Envoie accountingcodeid = 76
  ↓
Sellsy API
```

## 📋 Liste complète des codes comptables

Le fichier `accounting_codes_sellsy.json` contient tous les 47 codes comptables disponibles.

Codes principaux:
- **628000** - Abonnement → ID: **76**
- 706000 - Prestations de services → ID: 2
- 701000 - Ventes de produits finis → ID: 30
- 707000 - Ventes de marchandises → ID: 31
- 411000 - Clients → ID: 1
- 401000 - Fournisseurs → ID: 3

## 🔧 Ajouter d'autres codes comptables

Pour ajouter d'autres codes automatiques:

1. Consultez `accounting_codes_sellsy.json` pour les IDs
2. Ajoutez le mapping dans `config.py`:
   ```python
   ACCOUNTING_CODE_MAPPING = {
       '628000': '76',
       'VOTRE_CODE': 'ID_SELLSY',
   }
   ```
3. Modifiez `airtable_client.py` pour ajouter la logique:
   ```python
   if fields['Catégorie'].lower() == 'votre_categorie':
       sellsy_data['accountingCode'] = 'VOTRE_CODE'
   ```

## ✅ État actuel

- ✅ Code comptable 628000 configuré
- ✅ ID Sellsy 76 récupéré
- ✅ Mapping configuré dans config.py
- ✅ Code activé dans airtable_client.py
- ✅ Tests réussis
- ✅ Prêt à l'utilisation

## 🎯 Date de configuration

05 février 2026
