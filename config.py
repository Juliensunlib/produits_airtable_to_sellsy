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
    'name': 'Name',              # Nom du service dans Airtable
    'tradename': 'TradeName',    # Nom commercial dans Airtable
    'notes': 'Notes',            # Notes dans Airtable
    'unitAmount': 'UnitAmount',  # Prix unitaire dans Airtable
    'unit': 'Unit',              # Unité dans Airtable
    'taxid': 'TaxID',            # ID de taxe dans Airtable
    # Ajoutez d'autres champs selon vos besoins
}

# ID externe pour suivre les modifications/suppressions
AIRTABLE_ID_FIELD = 'ID'         # Champ ID unique dans Airtable
SELLSY_ID_FIELD = 'SellsyID'     # Champ où stocker l'ID Sellsy dans Airtable
