# Synchronisation Airtable vers Sellsy

Ce projet automatise la synchronisation des services entre Airtable et Sellsy en utilisant GitHub Actions. Les services sont récupérés depuis une table Airtable et synchronisés vers Sellsy toutes les 6 heures.

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

Dans votre dépôt GitHub, allez dans Settings > Secrets > Actions et ajoutez les secrets suivants:

- `AIRTABLE_API_KEY`: Votre clé API Airtable
- `AIRTABLE_BASE_ID`: L'ID de votre base Airtable
- `AIRTABLE_TABLE_NAME`: Le nom de votre table Airtable contenant les services
- `SELLSY_CONSUMER_TOKEN`: Votre token consommateur Sellsy API V1
- `SELLSY_CONSUMER_SECRET`: Votre secret de consommateur Sellsy API V1
- `SELLSY_USER_TOKEN`: Votre token utilisateur Sellsy API V1
- `SELLSY_USER_SECRET`: Votre secret utilisateur Sellsy API V1

### 2. Structure de la table Airtable

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

## Support

Pour tout problème ou question, veuillez ouvrir une issue sur ce dépôt GitHub.
