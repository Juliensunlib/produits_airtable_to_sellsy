"""
Test pour les codes comptables d'ACHAT
"""
from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: CODES COMPTABLES D'ACHAT")
print("=" * 80)
print()

tests = [
    {
        'name': 'Test 1: accountingPurchaseCodeId (ID)',
        'params': {
            'accountingPurchaseCodeId': 75
        }
    },
    {
        'name': 'Test 2: purchaseAccountingCodeId (ID)',
        'params': {
            'purchaseAccountingCodeId': 75
        }
    },
    {
        'name': 'Test 3: Remettre à 0 (réinitialiser)',
        'params': {
            'accountingcodeid': 0
        }
    }
]

for i, test in enumerate(tests, 1):
    print(f"🧪 {test['name']}")
    print("-" * 80)

    params = {
        'type': 'service',
        'id': '1709',
        'service': {
            'name': 'ABO-PV-ANT-2026-recVyLSUFkVwooLoJ',
            'tradename': 'Anthony RAEZ / 5 kWc / 25 ans',
            'unitAmount': 79.79,
            'unit': 'unité',
            'taxrate': 20.0,
            'qt': 1,
            **test['params']
        }
    }

    try:
        response = sellsy.call_api('Catalogue.update', params)
        if response:
            print(f"✅ Accepté")

            # Vérifier
            service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': '1709'})
            if service:
                vente = service.get('accountingCode', '(vide)')
                achat = service.get('accountingPurchaseCode', '(vide)')
                print(f"   VENTE: {vente}")
                print(f"   ACHAT: {achat}")
        else:
            print("❌ Échec")

    except Exception as e:
        print(f"❌ Erreur: {str(e)[:80]}")

    print()

print("=" * 80)
print()
print("💡 CONCLUSION:")
print()
print("L'API Sellsy v1 (Catalogue.update) ne permet probablement PAS")
print("de modifier les codes comptables via l'API.")
print()
print("Les codes 275500 (vente) et 218100 (achat) sont probablement:")
print("  1. Définis au niveau de la CATÉGORIE (pas du service)")
print("  2. Configurés manuellement dans l'interface Sellsy")
print("  3. Non modifiables via l'API v1")
print()
print("📝 Vérifiez dans Sellsy:")
print("   Paramètres > Comptabilité > Catégories de produits")
print("   Chaque catégorie peut avoir des codes comptables par défaut.")
print()
