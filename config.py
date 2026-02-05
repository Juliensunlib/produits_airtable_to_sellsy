import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configuration Airtable
AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

# Configuration Sellsy
SELLSY_CONSUMER_TOKEN = os.getenv('SELLSY_CONSUMER_TOKEN')
SELLSY_CONSUMER_SECRET = os.getenv('SELLSY_CONSUMER_SECRET')
SELLSY_USER_TOKEN = os.getenv('SELLSY_USER_TOKEN')
SELLSY_USER_SECRET = os.getenv('SELLSY_USER_SECRET')

# URL de l'API Sellsy (pour référence)
SELLSY_API_URL = 'https://apifeed.sellsy.com/0/'

# Mapping des catégories Airtable vers les IDs Sellsy
# À remplir après avoir exécuté une première fois le script
# qui affichera toutes les catégories disponibles dans Sellsy
CATEGORY_MAPPING = {
    # Format : 'Nom catégorie dans Airtable': 'ID catégorie dans Sellsy'
    # Exemple :
    'Développement web': '123456',
    'Formation': '234567',
    'Conseil': '345678',
    'Design': '456789',
    # Ajoutez les autres catégories selon vos besoins
}

# Mapping des codes comptables vers leurs IDs Sellsy
# À remplir manuellement en consultant votre interface Sellsy
# (Paramètres > Comptabilité > Plan comptable)
ACCOUNTING_CODE_MAPPING = {
    # Format : 'Code comptable': 'ID du code comptable dans Sellsy'
    '628000': '76',  # Abonnement
    '706000': '2',   # Prestations de services
    '601000': '12',  # Achats stockés - Matières premières
    '411000': '1',   # Clients
    '401000': '3',   # Fournisseurs
    # Ajoutez les autres codes selon vos besoins
}

# Mapping des champs Airtable vers Sellsy
AIRTABLE_TO_SELLSY_MAPPING = {
    'name': 'Référence',         # Code référence dans Airtable
    'tradename': 'Nom du service',  # Nom du service dans Airtable
    'notes': 'Description',      # Description dans Airtable
    'unitAmount': 'Prix HT',     # Prix unitaire dans Airtable
    'unit': 'Unité',             # Unité dans Airtable
    'taxrate': 'Taux TVA',       # Taux de TVA dans Airtable
    'active': 'Actif',           # Si le service est actif
    'categoryid': 'Catégorie',   # Catégorie dans Airtable
    'qt': 'Quantité',            # Quantité dans Airtable
    # Ajoutez d'autres champs selon vos besoins
}
