# Obtenir les IDs des codes comptables EN LOCAL

Si vous ne pouvez pas exécuter le workflow GitHub Actions, vous pouvez obtenir les IDs des codes comptables directement depuis votre ordinateur.

## Méthode rapide (recommandée)

### Option 1 : Script automatique

```bash
bash setup_and_get_codes.sh
```

Ce script va :
1. Vérifier votre fichier .env
2. Installer les dépendances nécessaires
3. Récupérer tous les codes comptables depuis Sellsy
4. Afficher les résultats et les prochaines étapes

### Option 2 : Étapes manuelles

#### 1. Configurer le fichier .env

```bash
# Copier le fichier exemple si nécessaire
cp .env.example .env

# Éditer le fichier
nano .env  # ou utilisez votre éditeur préféré
```

Ajoutez vos vraies clés Sellsy :

```bash
# Configuration Sellsy API V1
SELLSY_CONSUMER_TOKEN=votre_consumer_token_ici
SELLSY_CONSUMER_SECRET=votre_consumer_secret_ici
SELLSY_USER_TOKEN=votre_user_token_ici
SELLSY_USER_SECRET=votre_user_secret_ici
```

**Comment obtenir ces clés ?**

1. Connectez-vous sur [https://www.sellsy.com](https://www.sellsy.com)
2. Allez dans **Paramètres** > **API** (ou `https://www.sellsy.com/settings/api`)
3. Cliquez sur **"Créer une clé API"** ou **"Nouvelle application"**
4. Donnez un nom (ex: "Synchronisation Airtable")
5. Copiez les 4 clés générées et collez-les dans votre .env

⚠️ **Important** : Sauvegardez ces clés immédiatement, vous ne pourrez plus les voir après !

#### 2. Installer les dépendances Python

```bash
pip3 install -r requirements.txt
```

#### 3. Exécuter le script

```bash
python3 get_all_accounting_codes.py
```

## Résultat attendu

Le script va afficher quelque chose comme :

```
================================================================================
  RÉCUPÉRATION DES CODES COMPTABLES SELLSY
================================================================================

✅ Client Sellsy initialisé

🔍 Récupération des codes comptables...

   Récupération de 0 à 100... ✓ 45 codes récupérés

================================================================================
  TOTAL: 45 codes comptables récupérés
================================================================================

📋 LISTE DES CODES COMPTABLES:

Code       Libellé                                                      ID
--------------------------------------------------------------------------------
607000     Achats de marchandises                                       12345
628000     Abonnement                                                   67890
706000     Prestations de services                                      54321
...

================================================================================
  🎯 CODE COMPTABLE 628000 TROUVÉ!
================================================================================

✅ ID du code comptable 628000: 67890

👉 ÉTAPES SUIVANTES:

1. Ouvrez le fichier config.py

2. Trouvez la section ACCOUNTING_CODE_MAPPING

3. Ajoutez ou modifiez cette ligne:

   ACCOUNTING_CODE_MAPPING = {
       '628000': '67890',
   }

4. Décommentez les lignes dans airtable_client.py (lignes 120-122)

5. Relancez la synchronisation avec: python3 main.py

================================================================================
📁 Liste complète sauvegardée dans: accounting_codes_sellsy.json
================================================================================
```

## Fichier JSON créé

Le script crée aussi un fichier `accounting_codes_sellsy.json` contenant tous vos codes comptables au format JSON. Vous pouvez le consulter pour trouver d'autres codes si nécessaire.

## Que faire ensuite ?

### 1. Configurer config.py

Ouvrez `config.py` et ajoutez l'ID trouvé :

```python
ACCOUNTING_CODE_MAPPING = {
    '628000': '67890',  # Remplacez 67890 par votre ID réel
}
```

### 2. Activer l'ajout automatique des codes

Décommentez les lignes 120-122 dans `airtable_client.py` :

```python
# AVANT (commenté)
# if fields['Catégorie'].lower() == 'abonnement':
#     sellsy_data['accountingCode'] = '628000'
#     print(f"Code comptable 628000 ajouté pour l'abonnement")

# APRÈS (décommenté)
if fields['Catégorie'].lower() == 'abonnement':
    sellsy_data['accountingCode'] = '628000'
    print(f"Code comptable 628000 ajouté pour l'abonnement")
```

### 3. Tester la synchronisation

```bash
python3 main.py
```

## Dépannage

### Erreur : "Variables d'environnement Sellsy manquantes"

→ Vérifiez que votre fichier .env contient les 4 clés Sellsy et qu'elles ne sont pas vides.

### Erreur : "Erreur HTTP: 401"

→ Vos clés API sont invalides ou expirées. Régénérez-les dans Sellsy.

### Erreur : "Aucun code comptable trouvé"

→ Votre compte Sellsy n'a peut-être pas de codes comptables configurés. Vérifiez dans Sellsy > Paramètres > Comptabilité > Plan comptable.

### Le script ne trouve pas le code 628000

→ Le code 628000 n'existe pas dans votre Sellsy. Vous devez le créer :
1. Allez dans Sellsy > Paramètres > Comptabilité > Plan comptable
2. Créez un nouveau code comptable 628000
3. Relancez le script

## Vous avez obtenu les IDs ?

Parfait ! Vous pouvez maintenant :

1. **Configurer les secrets GitHub** (pour les workflows automatiques) : voir [GITHUB_SECRETS_SETUP.md](GITHUB_SECRETS_SETUP.md)
2. **Tester en local** : `python3 main.py`
3. **Consulter la doc complète** : voir [README.md](README.md) et [QUICKSTART.md](QUICKSTART.md)

## Besoin d'aide ?

- Consultez [SCRIPTS.md](SCRIPTS.md) pour tous les scripts disponibles
- Ouvrez une issue sur GitHub avec les détails de votre erreur
