"""
Vérifie le service ID 1709 dans Sellsy et affiche tous ses codes comptables
"""
from dotenv import load_dotenv
from sellsy_client import SellsyClient
import json

load_dotenv()

sellsy = SellsyClient()

print("=" * 80)
print("  VÉRIFICATION DU SERVICE ID 1709")
print("=" * 80)
print()

# Récupérer le service
params = {'type': 'service', 'id': '1709'}
response = sellsy.call_api('Catalogue.getOne', params)

if response:
    print("✅ Service trouvé")
    print()

    # Afficher les informations de base
    print(f"Nom: {response.get('tradename', 'N/A')}")
    print(f"Prix HT: {response.get('unitAmount', 'N/A')}")
    print()

    # Afficher TOUS les champs liés aux codes comptables
    print("📊 CODES COMPTABLES:")
    print("-" * 80)

    accounting_fields = {}
    for key, value in response.items():
        if 'accounting' in key.lower() or 'code' in key.lower():
            accounting_fields[key] = value
            print(f"  {key:<30} = {value}")

    print()
    print("=" * 80)
    print()

    # Vérifier si des codes sont présents
    achat_code = response.get('accountingPurchaseCode', '')
    vente_code = response.get('accountingCode', '')

    print(f"Code comptable de VENTE  : {vente_code if vente_code else '(vide)'}")
    print(f"Code comptable d'ACHAT   : {achat_code if achat_code else '(vide)'}")
    print()

    # Afficher tous les champs pour debug
    print("=" * 80)
    print("  TOUS LES CHAMPS DU SERVICE (pour debug)")
    print("=" * 80)
    print()
    print(json.dumps(response, indent=2, ensure_ascii=False))

else:
    print("❌ Impossible de récupérer le service")
