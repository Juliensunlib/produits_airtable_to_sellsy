from dotenv import load_dotenv
from sellsy_client import SellsyClient

load_dotenv()

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: MISE À JOUR AVEC accountingcodeid = 75")
print("=" * 80)
print()

params = {
    'type': 'service',
    'id': '1709',
    'service': {
        'name': 'ABO-PV-ANT-2026-recVyLSUFkVwooLoJ',
        'tradename': 'Anthony RAEZ / 5 kWc / 25 ans',
        'notes': 'Abonnement mensuel - Installation photovoltaïque 5 kWc - Durée 25 ans',
        'unitAmount': 79.79,
        'unit': 'unité',
        'actif': 'Y',
        'unitAmountIsTaxesFree': 'Y',
        'qt': 1,
        'taxrate': 20.0,
        'accountingcodeid': 75
    }
}

print("📤 Envoi avec accountingcodeid = 75")
print()

try:
    response = sellsy.call_api('Catalogue.update', params)
    if response:
        print("✅ SUCCÈS! Service 1709 mis à jour avec ID comptable 75")
        print()
        print("👉 Vérifiez dans Sellsy si le code 706000 apparaît maintenant.")
    else:
        print("❌ Échec")
except Exception as e:
    print(f"❌ Erreur: {e}")

print()
print("=" * 80)
