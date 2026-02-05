"""
Test pour trouver le bon paramètre pour le code comptable de VENTE
"""
from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: CODES COMPTABLES VENTE vs ACHAT")
print("=" * 80)
print()

tests = [
    {
        'name': 'Test 1: accountingSaleCodeId (ID pour code de VENTE)',
        'params': {
            'accountingSaleCodeId': 75
        }
    },
    {
        'name': 'Test 2: accountingSaleCodeId en string',
        'params': {
            'accountingSaleCodeId': '75'
        }
    },
    {
        'name': 'Test 3: accountingcodeid (pour code de vente)',
        'params': {
            'accountingcodeid': 75
        }
    },
    {
        'name': 'Test 4: accountingCode en string (le code lui-même)',
        'params': {
            'accountingCode': '706000'
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
            print(f"✅ Accepté par l'API")

            # Vérifier le résultat
            verify_params = {'type': 'service', 'id': '1709'}
            service = sellsy.call_api('Catalogue.getOne', verify_params)

            if service:
                vente = service.get('accountingCode', '(vide)')
                achat = service.get('accountingPurchaseCode', '(vide)')
                print(f"📊 Code VENTE: {vente}")
                print(f"📊 Code ACHAT: {achat}")

                if vente and vente != '275500':
                    print(f"✅ CODE DE VENTE MODIFIÉ!")
        else:
            print("❌ Échec")

    except Exception as e:
        error_msg = str(e)
        if 'E_PARAM' in error_msg:
            print(f"❌ Paramètre refusé")
        else:
            print(f"❌ Erreur: {error_msg[:100]}")

    print()

    if i < len(tests):
        print("⏳ Attente de 1 seconde...")
        import time
        time.sleep(1)
        print()

print("=" * 80)
