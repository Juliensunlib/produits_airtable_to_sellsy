# Guide d'Utilisation - Synchronisation Airtable → Sellsy

## Configuration Terminée ✅

Les catégories suivantes sont maintenant configurées :

| Catégorie Airtable | → | ID Sellsy | Code Comptable |
|-------------------|---|-----------|----------------|
| **Abonnement** | → | 57 | 706000 (à configurer dans Sellsy) |
| **Caution** | → | 58 | (à définir selon vos besoins) |

## Dernière Étape Requise

### Configurer le Code Comptable dans Sellsy

Le code comptable **706000** doit être configuré sur la **catégorie Abonnement** dans Sellsy :

1. **Connectez-vous à Sellsy**
2. **Paramètres** → **Catalogue** → **Catégories**
3. Trouvez **"Abonnement"** (ID: 57)
4. Cliquez sur **Modifier**
5. **Code comptable de vente** : Remplacez `275500` par `706000`
6. **Enregistrez**

### Vérifier la Configuration

Après avoir modifié dans Sellsy, lancez :

```bash
python3 verifier_configuration.py
```

Vous devriez voir :
```
🎉 TOUT EST CORRECT!
```

## Utilisation

### 1. Préparer les Services dans Airtable

Dans votre table Airtable, assurez-vous que chaque service a :

| Champ | Description | Valeur Exemple |
|-------|-------------|----------------|
| **Référence** | Code unique | `ABO-PV-CLI-2026-001` |
| **Nom du service** | Nom affiché | `Client X / 5 kWc / 25 ans` |
| **Description** | Description détaillée | `Abonnement mensuel...` |
| **Prix HT** | Prix hors taxes | `99.99` |
| **Unité** | Unité (forfait, mois, etc.) | `unité` |
| **Taux TVA** | Taux de TVA en % | `20` |
| **Quantité** | Quantité | `1` |
| **Catégorie** | **Abonnement** ou **Caution** | `Abonnement` |
| **Statut de synchronisation** | Statut | `À synchroniser` |

### 2. Lancer la Synchronisation

```bash
python3 main.py
```

Le script va :
1. Récupérer tous les services avec `Statut = "À synchroniser"`
2. Pour chaque service :
   - Si **Catégorie = "Abonnement"** → Crée/met à jour avec `categoryid: 57`
   - Si **Catégorie = "Caution"** → Crée/met à jour avec `categoryid: 58`
3. Le code comptable est **automatiquement hérité** de la catégorie
4. Marquer le service comme `Synchronisé` dans Airtable

### 3. Vérifier dans Sellsy

Allez dans **Sellsy** → **Catalogue** → **Services** et vérifiez que :
- Les services sont créés/mis à jour
- La catégorie est correcte
- Le code comptable est **706000** (pour les abonnements)

## Scripts Disponibles

| Script | Description |
|--------|-------------|
| `python3 main.py` | Synchronisation complète Airtable → Sellsy |
| `python3 verifier_configuration.py` | Vérifier que tout est bien configuré |
| `python3 check_service_1709.py` | Vérifier l'état du service de test 1709 |
| `python3 test_final_categories.py` | Créer des services de test avec les catégories |

## Fonctionnement des Codes Comptables

### Principe

Les codes comptables **ne sont PAS envoyés via l'API**. Ils sont **hérités de la catégorie** Sellsy.

```
Service Airtable (Catégorie = "Abonnement")
    ↓
Synchronisation via API
    ↓
Service Sellsy (categoryid = 57)
    ↓
Héritage automatique du code comptable de la catégorie 57
    ↓
Service avec code comptable 706000 ✅
```

### Pourquoi ?

L'API Sellsy v1 ne permet pas de :
- Définir les codes comptables au niveau du service
- Modifier les codes comptables via l'API
- Récupérer les codes comptables via `Catalogue.getOne`

**Solution** : Configurer les codes comptables au niveau de la **catégorie** dans l'interface Sellsy.

## Ajouter d'Autres Catégories

Pour ajouter une nouvelle catégorie (ex: "Installation") :

1. **Créer la catégorie dans Sellsy** (ou via script)
2. **Récupérer son ID**
3. **Modifier `config.py`** :

```python
CATEGORY_MAPPING = {
    'Abonnement': '57',
    'Caution': '58',
    'Installation': '59',  # Nouvelle catégorie
}
```

4. **Configurer le code comptable** dans Sellsy
5. **Utiliser** : Les services avec `Catégorie = "Installation"` dans Airtable utiliseront automatiquement l'ID 59

## Dépannage

### Service non synchronisé

Vérifiez que :
- Le statut est bien `"À synchroniser"` dans Airtable
- La catégorie est bien `"Abonnement"` ou `"Caution"`
- Les champs obligatoires sont remplis (Référence, Nom, Prix HT, TVA)

### Code comptable incorrect

Le code comptable vient de la **catégorie** dans Sellsy, pas du service.

Vérifiez dans **Sellsy** → **Paramètres** → **Catalogue** → **Catégories** → **Abonnement** → Code comptable de vente

### Erreur "Catégorie non trouvée"

Si vous voyez :
```
⚠️ Catégorie non trouvée: 'MaCategorie'
```

Ajoutez le mapping dans `config.py` :
```python
CATEGORY_MAPPING = {
    'MaCategorie': 'ID_SELLSY',
}
```

## Support

Consultez :
- `CONFIGURATION_CATEGORIES.md` - Documentation détaillée
- `RESUME_CONFIGURATION.md` - Résumé de la configuration
- Logs de synchronisation dans la console

---

**Prêt à synchroniser !** 🚀

Une fois le code comptable configuré dans Sellsy, lancez simplement :
```bash
python3 main.py
```
