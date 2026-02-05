"""
Test : Envoyer le code comptable directement (pas l'ID)
"""
from dotenv import load_dotenv
from sellsy_client import SellsyClient

load_dotenv()

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: ENVOI DU CODE COMPTABLE DIRECTEMENT")
print("=" * 80)
print()

tests = [
    {
        'name': 'Test 1: accountingCode = "706000" (STRING)',
        'data': {
            'name': 'ABO-PV-ANT-2026-recVyLSUFkVwooLoJ',
            'tradename': 'Anthony RAEZ / 5 kWc / 25 ans',
            'unitAmount': 79.79,
            'unit': 'unité',
            'taxrate': 20.0,
            'qt': 1,
            'accountingCode': '706000'  # CODE en string
        }
    },
    {
        'name': 'Test 2: accountingcodeid = "2" (STRING)',
        'data': {
            'name': 'ABO-PV-ANT-2026-recVyLSUFkVwooLoJ',
            'tradename': 'Anthony RAEZ / 5 kWc / 25 ans',
            'unitAmount': 79.79,
            'unit': 'unité',
            'taxrate': 20.0,
            'qt': 1,
            'accountingcodeid': '2'  # ID en string
        }
    },
    {
        'name': 'Test 3: accountingcodeid = 2 (NUMBER)',
        'data': {
            'name': 'ABO-PV-ANT-2026-recVyLSUFkVwooLoJ',
            'tradename': 'Anthony RAEZ / 5 kWc / 25 ans',
            'unitAmount': 79.79,
            'unit': 'unité',
            'taxrate': 20.0,
            'qt': 1,
            'accountingcodeid': 2  # ID en nombre
        }
    }
]

for test in tests:
    print(f"🧪 {test['name']}")
    print("-" * 80)

    params = {
        'type': 'service',
        'id': '1709',
        'service': test['data']
    }

    try:
        response = sellsy.call_api('Catalogue.update', params)
        if response:
            print("✅ Requête acceptée")
        else:
            print("❌ Échec")
    except Exception as e:
        print(f"❌ Erreur: {str(e)[:100]}")

    print()

print("=" * 80)
print()
print("💡 IMPORTANT:")
print()
print("L'API Sellsy v1 a une limitation :")
print("  - `Catalogue.getOne` ne retourne PAS les codes comptables")
print("  - Vous devez vérifier MANUELLEMENT dans l'interface Sellsy")
print()
print("Vérifiez maintenant dans Sellsy si le code 706000 apparaît.")
print()
