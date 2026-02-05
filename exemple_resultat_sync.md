# 📊 Exemple de Synchronisation avec Code Comptable

## 🔍 Avant la synchronisation

### Dans Airtable:
```
┌─────────────────────────────────────────────────────────┐
│ Service: Abonnement Premium                             │
├─────────────────────────────────────────────────────────┤
│ Référence:       ABO-2024-001                           │
│ Nom:             Abonnement Premium                     │
│ Description:     Service d'abonnement mensuel           │
│ Prix HT:         99.99 €                                │
│ Unité:           mois                                   │
│ Catégorie:       Abonnement ← Important!                │
│ Taux TVA:        20%                                    │
│ Statut:          À synchroniser ✓                       │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Pendant la synchronisation

### Terminal:
```bash
$ python3 main.py

================================================================================
  SYNCHRONISATION AIRTABLE → SELLSY
================================================================================

✅ Connexion à Airtable établie
✅ Connexion à Sellsy établie

🔍 Recherche des services à synchroniser...
   ✓ 1 service(s) trouvé(s)

📦 Service 1/1: Abonnement Premium
   Mapping du service: Abonnement Premium
   Ajout de la catégorie: Abonnement
   Code comptable 628000 (ID: 76) ajouté pour l'abonnement  ← Automatique!

   Données formatées pour Sellsy: {
     'name': 'ABO-2024-001',
     'tradename': 'Abonnement Premium',
     'notes': 'Service d\'abonnement mensuel',
     'unitAmount': 99.99,
     'unit': 'mois',
     'actif': 'Y',
     'taxrate': 20.0,
     'categoryName': 'Abonnement',
     'accountingCode': '628000'  ← Code ajouté
   }

   Code comptable '628000' mappé via configuration à l'ID: 76  ← Conversion
   Code comptable '628000' associé à l'ID: 76

   Création du service dans Sellsy...

   ✅ Service créé avec succès! ID Sellsy: 123456
   ✅ Statut Airtable mis à jour: Synchronisé

================================================================================
  SYNCHRONISATION TERMINÉE
================================================================================

✅ 1 service(s) synchronisé(s) avec succès
   0 erreur(s)
```

## ✅ Après la synchronisation

### Dans Sellsy:
```
┌─────────────────────────────────────────────────────────┐
│ Service créé dans Sellsy                                │
├─────────────────────────────────────────────────────────┤
│ ID:              123456                                 │
│ Référence:       ABO-2024-001                           │
│ Nom:             Abonnement Premium                     │
│ Description:     Service d'abonnement mensuel           │
│ Prix HT:         99.99 €                                │
│ Unité:           mois                                   │
│ TVA:             20%                                    │
│ Code comptable:  628000 - Abonnement ✓ Automatique!    │
│ ID comptable:    76                                     │
│ Statut:          Actif                                  │
└─────────────────────────────────────────────────────────┘
```

### Dans Airtable (mis à jour):
```
┌─────────────────────────────────────────────────────────┐
│ Service: Abonnement Premium                             │
├─────────────────────────────────────────────────────────┤
│ Référence:       ABO-2024-001                           │
│ Nom:             Abonnement Premium                     │
│ ID Sellsy:       123456 ← Nouveau!                      │
│ Statut:          Synchronisé ✓                          │
│ Date sync:       2026-02-05 14:30:00                    │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Points clés

1. **Détection automatique**: Si la catégorie = "Abonnement"
2. **Code ajouté**: accountingCode = '628000'
3. **Conversion**: '628000' → ID: 76
4. **Envoi API**: accountingcodeid = 76
5. **Résultat**: Le service dans Sellsy a le bon code comptable!

## 🔄 Autres catégories

Pour les services qui ne sont PAS des abonnements:

```
Catégorie = "Formation"
→ Pas de code comptable automatique
→ Vous pouvez ajouter d'autres règles dans airtable_client.py
```

## 💡 Astuce

Si vous voulez ajouter un code comptable pour d'autres catégories:

1. Trouvez le code et son ID dans `accounting_codes_sellsy.json`
2. Ajoutez-le dans `config.py` → `ACCOUNTING_CODE_MAPPING`
3. Ajoutez la règle dans `airtable_client.py`:

```python
if fields['Catégorie'].lower() == 'formation':
    sellsy_data['accountingCode'] = '706000'  # Prestations de services
```
