"""
Script simple pour récupérer l'ID du code comptable depuis un service Sellsy
"""
# Copiez vos clés API Sellsy directement ici pour test
SELLSY_CONSUMER_TOKEN = "VOTRE_CONSUMER_TOKEN"
SELLSY_CONSUMER_SECRET = "VOTRE_CONSUMER_SECRET"
SELLSY_USER_TOKEN = "VOTRE_USER_TOKEN"
SELLSY_USER_SECRET = "VOTRE_USER_SECRET"

import requests
import json
import hashlib
import random
import time
import hmac
import urllib.parse

def get_service_details():
    """Récupère les détails du service ID 1709"""

    # OAuth params
    oauth_timestamp = str(int(time.time()))
    oauth_nonce = str(random.randint(1000000, 9999999))

    oauth_params = {
        'oauth_consumer_key': SELLSY_CONSUMER_TOKEN,
        'oauth_token': SELLSY_USER_TOKEN,
        'oauth_nonce': oauth_nonce,
        'oauth_timestamp': oauth_timestamp,
        'oauth_signature_method': 'PLAINTEXT',
        'oauth_version': '1.0',
        'oauth_signature': f"{SELLSY_CONSUMER_SECRET}&{SELLSY_USER_SECRET}"
    }

    # API params
    request_params = {
        'io_mode': 'json',
        'do_in': json.dumps({
            'method': 'Catalogue.getOne',
            'params': {
                'type': 'service',
                'id': '1709'
            }
        })
    }

    # Combine all params
    all_params = {**oauth_params, **request_params}

    # Make request
    response = requests.post(
        'https://apifeed.sellsy.com/0/',
        data=all_params
    )

    if response.status_code == 200:
        data = response.json()

        if 'response' in data:
            service = data['response']

            print("=" * 70)
            print("  SERVICE TROUVÉ")
            print("=" * 70)
            print(f"\nNom: {service.get('tradename', 'N/A')}")
            print(f"Référence: {service.get('name', 'N/A')}")
            print()

            # Chercher le code comptable
            print("🔍 Recherche du code comptable...")
            print()

            found = False
            for key in service.keys():
                if 'account' in key.lower() and 'code' in key.lower():
                    print(f"   ✓ {key}: {service[key]}")
                    found = True

            if found:
                print()
                print("=" * 70)
                print("  COPIEZ CETTE LIGNE DANS config.py:")
                print("=" * 70)
                print()
                accounting_id = service.get('purchaseAccountingcodeid') or service.get('accountingcodeid')
                if accounting_id:
                    print(f"    '628000': '{accounting_id}',")
                print()
            else:
                print("⚠️ Aucun code comptable trouvé")
                print("   Assignez d'abord le code 628000 au service dans Sellsy")

            # Debug: afficher tous les champs
            print()
            print("=" * 70)
            print("  TOUS LES CHAMPS (pour debug)")
            print("=" * 70)
            for key in sorted(service.keys()):
                print(f"{key}: {service[key]}")
        else:
            print("Erreur:", data)
    else:
        print(f"Erreur HTTP {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    print()
    print("=" * 70)
    print("  RÉCUPÉRATION DU CODE COMPTABLE DU SERVICE")
    print("=" * 70)
    print()

    # Vérifier que les clés sont renseignées
    if "VOTRE_" in SELLSY_CONSUMER_TOKEN:
        print("❌ ERREUR: Vous devez d'abord renseigner vos clés API Sellsy")
        print("   dans le fichier get_service_accounting_code.py")
        print()
        print("   Ouvrez le fichier et remplacez:")
        print("   - VOTRE_CONSUMER_TOKEN par votre token")
        print("   - VOTRE_CONSUMER_SECRET par votre secret")
        print("   - VOTRE_USER_TOKEN par votre user token")
        print("   - VOTRE_USER_SECRET par votre user secret")
        print()
    else:
        get_service_details()
        print()
        print("=" * 70)
        print("  FIN")
        print("=" * 70)
        print()
