# Guide de démarrage rapide 🚀

Configuration en 5 minutes pour commencer à synchroniser vos services Airtable vers Sellsy.

## ⚡ Configuration rapide

### 1. Cloner et installer

```bash
# Cloner le projet
git clone [votre-repo]
cd [nom-du-projet]

# Installer les dépendances
pip3 install -r requirements.txt
```

### 2. Configurer les clés API

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer avec vos clés
nano .env  # ou votre éditeur préféré
```

Remplissez avec vos vraies clés :
```bash
# Airtable
AIRTABLE_API_KEY=keyXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX
AIRTABLE_TABLE_NAME=Services

# Sellsy
SELLSY_CONSUMER_TOKEN=XXXXXXXX
SELLSY_CONSUMER_SECRET=XXXXXXXX
SELLSY_USER_TOKEN=XXXXXXXX
SELLSY_USER_SECRET=XXXXXXXX
```

### 3. Récupérer les codes comptables

```bash
python3 get_all_accounting_codes.py
```

Ce script va :
- ✅ Afficher tous vos codes comptables Sellsy
- ✅ Trouver automatiquement le code 628000
- ✅ Vous donner la ligne exacte à copier dans `config.py`

### 4. Configurer config.py

Ouvrez `config.py` et ajoutez l'ID trouvé :

```python
ACCOUNTING_CODE_MAPPING = {
    '628000': 'ID_TROUVE',  # Remplacez par l'ID trouvé à l'étape 3
}
```

### 5. Activer les codes comptables

Décommentez les lignes 120-122 dans `airtable_client.py` :

```python
# Avant
# if fields['Catégorie'].lower() == 'abonnement':
#     sellsy_data['accountingCode'] = '628000'
#     print(f"Code comptable 628000 ajouté pour l'abonnement")

# Après
if fields['Catégorie'].lower() == 'abonnement':
    sellsy_data['accountingCode'] = '628000'
    print(f"Code comptable 628000 ajouté pour l'abonnement")
```

### 6. Premier test

```bash
python3 main.py
```

Si tout fonctionne, vous verrez :
```
[2026-02-05 15:30:00] Démarrage de la synchronisation Airtable -> Sellsy
[2026-02-05 15:30:01] ✓ Service "Mon service" synchronisé avec succès
[2026-02-05 15:30:02] Synchronisation terminée avec succès
```

## 🔧 Configuration GitHub Actions

Pour automatiser la synchronisation toutes les 6 heures :

### 1. Configurer les secrets GitHub

Dans votre repo GitHub : **Settings → Secrets → Actions**

Ajoutez ces secrets :
- `AIRTABLE_API_KEY`
- `AIRTABLE_BASE_ID`
- `AIRTABLE_TABLE_NAME`
- `SELLSY_CONSUMER_TOKEN`
- `SELLSY_CONSUMER_SECRET`
- `SELLSY_USER_TOKEN`
- `SELLSY_USER_SECRET`

### 2. Activer GitHub Actions

Le fichier `.github/workflows/sync.yml` est déjà configuré. Il s'exécute automatiquement toutes les 6 heures.

### 3. Lancement manuel

Allez dans l'onglet **Actions** → **Synchronisation Airtable vers Sellsy** → **Run workflow**

## 📋 Structure Airtable requise

Votre table Airtable doit avoir ces champs :

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| Nom du service | Texte | ✅ | Titre du service |
| Référence | Texte | ✅ | Code unique |
| Catégorie | Sélection | ✅ | ex: Abonnement |
| Prix HT | Monétaire | ✅ | Tarif |
| Description | Texte long | ⚪ | Description complète |
| Description courte | Texte | ⚪ | Résumé |
| Taux TVA | Nombre | ⚪ | % de TVA |
| Unité | Sélection | ⚪ | Heure, jour, etc. |
| Actif | Case à cocher | ⚪ | Service actif |
| À synchroniser | Case à cocher | ✅ | Pour déclencher la sync |
| ID Sellsy | Texte | Auto | Rempli automatiquement |
| Statut de synchronisation | Sélection | Auto | Statut |
| Dernière synchronisation | Date/Heure | Auto | Date |

## 🎯 Utilisation quotidienne

1. **Dans Airtable** : Cochez "À synchroniser" sur le service
2. **Attendez** : La synchronisation automatique s'exécute toutes les 6 heures
3. **Vérifiez** : Le statut passe à "Synchronisé" dans Airtable
4. **Confirmez** : Le service apparaît dans Sellsy avec le bon code comptable

## ❓ Problèmes fréquents

### "Code comptable non trouvé"
```bash
python3 get_all_accounting_codes.py
```

### "Erreur d'authentification"
Vérifiez vos clés dans `.env`

### "Service non créé dans Sellsy"
1. Vérifiez les logs : `python3 main.py`
2. Consultez le statut dans Airtable
3. Vérifiez que tous les champs obligatoires sont remplis

### "La catégorie n'existe pas"
Vérifiez que la catégorie dans Airtable correspond exactement au nom dans Sellsy (sensible à la casse).

## 📚 Documentation complète

- [README.md](README.md) - Documentation complète du projet
- [SCRIPTS.md](SCRIPTS.md) - Documentation de tous les scripts
- [CONFIGURATION_CODES_COMPTABLES.md](CONFIGURATION_CODES_COMPTABLES.md) - Guide détaillé des codes comptables

## 🆘 Besoin d'aide ?

1. Consultez les logs : GitHub Actions ou exécution locale
2. Vérifiez les fichiers de documentation
3. Ouvrez une issue sur GitHub

---

**✨ Félicitations !** Votre synchronisation Airtable → Sellsy est maintenant opérationnelle !
