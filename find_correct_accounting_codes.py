"""
Teste différentes méthodes API pour récupérer les codes comptables
"""
from dotenv import load_dotenv
from sellsy_client import SellsyClient

load_dotenv()

sellsy = SellsyClient()

print("=" * 80)
print("  RECHERCHE DES CODES COMPTABLES")
print("=" * 80)
print()

# Liste des méthodes à tester
methods = [
    ('Accountingcodes.getList', {}),
    ('Accountingcode.getList', {}),
    ('Accountdatas.get', {}),
    ('Accountpreferences.getList', {}),
]

for method_name, params in methods:
    print(f"🔍 Test de: {method_name}")
    print("-" * 80)

    try:
        response = sellsy.call_api(method_name, params)

        if response and isinstance(response, dict):
            print(f"✅ Fonctionne! {len(response)} éléments")

            # Afficher les premiers éléments
            count = 0
            for key, value in response.items():
                if count < 5:
                    if isinstance(value, dict):
                        code = value.get('code', value.get('accountingcode', key))
                        label = value.get('label', value.get('libelle', value.get('name', 'N/A')))
                        print(f"   ID: {key} - Code: {code} - {label}")
                    else:
                        print(f"   {key}: {value}")
                    count += 1

                # Chercher spécifiquement 706000, 275500, 218100
                if isinstance(value, dict):
                    code = str(value.get('code', value.get('accountingcode', '')))
                    if code in ['706000', '275500', '218100', '628000']:
                        print(f"   🎯 TROUVÉ! Code {code} → ID: {key}")

            print()
            print("✅ CETTE MÉTHODE FONCTIONNE!")
            print()
            break
        else:
            print("❌ Pas de données")
            print()

    except Exception as e:
        error_msg = str(e)
        if 'does not exist' in error_msg:
            print("❌ Méthode n'existe pas")
        else:
            print(f"❌ Erreur: {error_msg[:100]}")
        print()

print("=" * 80)
print()

# Test spécifique pour voir si accountingcodeid est bien pris en compte
print("🔍 TEST: Est-ce que accountingcodeid=76 correspond au code 628000 ?")
print("=" * 80)
print()
print("Selon votre configuration:")
print("  628000 → ID 76")
print("  706000 → ID 2")
print()
print("Mais dans la capture Sellsy, on voit:")
print("  Code de vente: 275500")
print("  Code d'achat: 218100")
print()
print("💡 Ces codes (275500, 218100) ne correspondent PAS à notre config.")
print("   Soit ils ont été ajoutés manuellement, soit les IDs sont incorrects.")
print()
