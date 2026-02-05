# Scripts disponibles

Ce document décrit tous les scripts Python disponibles dans ce projet et comment les utiliser.

## Scripts de synchronisation

### `main.py` - Synchronisation principale
**Usage:** `python3 main.py`

Script principal qui synchronise les services depuis Airtable vers Sellsy.

**Fonctionnalités:**
- Récupère les services marqués "À synchroniser" dans Airtable
- Crée ou met à jour les services dans Sellsy
- Met à jour le statut de synchronisation dans Airtable
- Gère les catégories et les codes comptables

**Quand l'utiliser:**
- Exécution automatique via GitHub Actions (toutes les 6 heures)
- Exécution manuelle pour tester ou forcer une synchronisation

**Prérequis:**
- Fichier `.env` configuré avec les clés API Airtable et Sellsy

---

## Scripts utilitaires

### `get_all_accounting_codes.py` - Récupération des codes comptables ⭐
**Usage:** `python3 get_all_accounting_codes.py`

Script pour récupérer tous les codes comptables depuis votre compte Sellsy via l'API.

**Fonctionnalités:**
- Récupère la liste complète des codes comptables depuis Sellsy
- Affiche les codes avec leurs IDs et libellés
- Recherche automatiquement le code 628000
- Sauvegarde la liste complète dans `accounting_codes_sellsy.json`
- Fournit les instructions pour configurer `config.py`

**Sortie exemple:**
```
Code       Libellé                                                      ID
--------------------------------------------------------------------------------
607000     Achats de marchandises                                       12345
628000     Abonnement                                                   67890
706000     Prestations de services                                      54321
```

**Quand l'utiliser:**
- Première configuration du projet
- Quand vous devez trouver l'ID d'un code comptable
- Pour vérifier les codes comptables disponibles

**Prérequis:**
- Fichier `.env` avec les clés API Sellsy

---

### `find_accounting_code_id.py` - Analyse d'un service existant
**Usage:** `python3 find_accounting_code_id.py [SERVICE_ID]`

Script pour récupérer l'ID du code comptable en analysant un service Sellsy existant.

**Fonctionnalités:**
- Analyse un service Sellsy spécifique pour trouver son code comptable
- Affiche tous les champs liés aux codes comptables
- Utile si vous avez un service avec le bon code comptable configuré
- Accepte un ID de service en paramètre (défaut: 1709)

**Exemples:**
```bash
# Analyser le service ID 1709 (par défaut)
python3 find_accounting_code_id.py

# Analyser un service spécifique
python3 find_accounting_code_id.py 2456
```

**Quand l'utiliser:**
- Si `get_all_accounting_codes.py` ne fonctionne pas
- Pour analyser un service spécifique qui a déjà un code comptable
- Pour vérifier les codes comptables d'un service existant

**Prérequis:**
- Fichier `.env` configuré avec les clés API Sellsy
- Un service existant dans Sellsy avec un code comptable assigné

---

## Modules

### `airtable_client.py`
Module pour interagir avec l'API Airtable.

**Classes:**
- `AirtableClient`: Gestion de la connexion et des opérations Airtable

**Méthodes principales:**
- `get_records_to_sync()`: Récupère les enregistrements à synchroniser
- `update_record()`: Met à jour un enregistrement
- `format_for_sellsy()`: Formate les données pour Sellsy

### `sellsy_client.py`
Module pour interagir avec l'API Sellsy V1.

**Classes:**
- `SellsyClient`: Gestion de l'authentification OAuth et des requêtes API

**Méthodes principales:**
- `call_api()`: Appel générique à l'API
- `create_service()`: Création d'un service
- `update_service()`: Mise à jour d'un service
- `get_category_id()`: Récupération de l'ID d'une catégorie

### `config.py`
Configuration du projet.

**Variables:**
- `ACCOUNTING_CODE_MAPPING`: Mapping entre codes comptables et leurs IDs Sellsy
- `CATEGORY_MAPPING`: Mapping entre noms de catégories et leurs IDs Sellsy

---

## Flux de travail recommandé

### Configuration initiale

1. **Copier le fichier d'exemple:**
   ```bash
   cp .env.example .env
   ```

2. **Éditer `.env`** avec vos vraies clés API

3. **Récupérer les codes comptables:**
   ```bash
   python3 get_all_accounting_codes.py
   ```

4. **Configurer `config.py`** avec les IDs trouvés

5. **Décommenter les lignes** dans `airtable_client.py` (lignes 120-122)

6. **Tester la synchronisation:**
   ```bash
   python3 main.py
   ```

### Utilisation quotidienne

- La synchronisation s'exécute automatiquement via GitHub Actions
- Marquez simplement les services "À synchroniser" dans Airtable
- Consultez les logs dans GitHub Actions pour vérifier

### Dépannage

1. **Problème de codes comptables:**
   ```bash
   python3 get_all_accounting_codes.py
   ```

2. **Problème de catégories:**
   Vérifiez les noms dans Airtable correspondent à ceux dans Sellsy

3. **Erreur d'authentification:**
   Vérifiez les clés API dans le fichier `.env`

4. **Service non synchronisé:**
   - Vérifiez le statut dans Airtable
   - Consultez les logs GitHub Actions
   - Testez en local avec `python3 main.py`

---

## Développement

### Ajouter un nouveau script

1. Créer le fichier `.py` à la racine du projet
2. Importer les modules nécessaires (`airtable_client`, `sellsy_client`, `config`)
3. Ajouter la documentation dans ce fichier
4. Mettre à jour `.gitignore` si nécessaire

### Tester localement

```bash
# Installer les dépendances
pip3 install -r requirements.txt

# Exécuter le script
python3 nom_du_script.py
```

### Contribuer

1. Créer une branche pour vos modifications
2. Tester en local
3. Mettre à jour la documentation
4. Créer une pull request
