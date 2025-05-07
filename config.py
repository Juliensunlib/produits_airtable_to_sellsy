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

# URL de l'API Sellsy
SELLSY_API_URL = 'https://api.sellsy.com/v1/api.php'

# Mapping des champs Airtable vers Sellsy
# Modifiez cette section selon votre structure de données dans Airtable
AIRTABLE_TO_SELLSY_MAPPING = {
    'name': 'Référence',         # Code référence dans Airtable
    'tradename': 'Nom du service',  # Nom du service dans Airtable
    'notes': 'Description',      # Description dans Airtable
    'unitAmount': 'Prix HT',     # Prix unitaire dans Airtable
    'unit': 'Unité',             # Unité dans Airtable
    'taxrate': 'Taux TVA',       # Taux de TVA dans Airtable
    'active': 'Actif',           # Si le service est actif
    # Ajoutez d'autres champs selon vos besoins
}
