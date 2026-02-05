"""
Script de vérification rapide de la configuration des catégories
"""
from sellsy_client import SellsyClient
from config import CATEGORY_MAPPING

sellsy = SellsyClient()

print("\n" + "=" * 80)
print("  VÉRIFICATION DE LA CONFIGURATION")
print("=" * 80 + "\n")

# 1. Vérifier la configuration dans config.py
print("1️⃣  Configuration dans config.py")
print("-" * 80)

all_configured = True
for cat_name, cat_id in CATEGORY_MAPPING.items():
    if cat_id:
        print(f"   ✅ {cat_name:<15} → ID Sellsy: {cat_id}")
    else:
        print(f"   ❌ {cat_name:<15} → Non configuré")
        all_configured = False

print()

if not all_configured:
    print("⚠️  Certaines catégories ne sont pas configurées dans config.py")
    print()

# 2. Vérifier le service 1709
print("2️⃣  Service de test (ID 1709)")
print("-" * 80)

try:
    service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': '1709'})

    if service:
        nom = service.get('tradename', 'N/A')
        cat_id = service.get('categoryid', '(vide)')
        code_vente = service.get('accountingCode', '(vide)')

        print(f"   Nom            : {nom}")
        print(f"   Catégorie ID   : {cat_id}")
        print(f"   Code VENTE     : {code_vente}")
        print()

        # Vérifications
        if cat_id == CATEGORY_MAPPING.get('Abonnement'):
            print("   ✅ Catégorie Abonnement correctement associée")
        else:
            print(f"   ⚠️  Catégorie attendue: {CATEGORY_MAPPING.get('Abonnement')}, actuelle: {cat_id}")

        if code_vente == '706000':
            print("   ✅ Code comptable 706000 correctement appliqué")
        elif code_vente == '275500':
            print("   ⚠️  Code actuel: 275500")
            print("   👉 Modifiez la catégorie Abonnement dans Sellsy (275500 → 706000)")
        else:
            print(f"   ⚠️  Code comptable: {code_vente}")

except Exception as e:
    print(f"   ❌ Erreur: {str(e)[:100]}")

print()

# 3. Résumé
print("=" * 80)
print("  RÉSUMÉ")
print("=" * 80)
print()

if all_configured:
    print("✅ Toutes les catégories sont configurées dans config.py")
else:
    print("⚠️  Certaines catégories manquent dans config.py")

print()

try:
    service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': '1709'})
    if service:
        code_vente = service.get('accountingCode', '(vide)')

        if code_vente == '706000':
            print("🎉 TOUT EST CORRECT!")
            print()
            print("Votre configuration est prête. Vous pouvez lancer:")
            print("   python3 main.py")
            print()
        else:
            print("📝 ACTION REQUISE:")
            print()
            print("   Modifiez la catégorie Abonnement dans Sellsy:")
            print("   Paramètres > Catalogue > Catégories > Abonnement")
            print(f"   Code comptable de vente: {code_vente} → 706000")
            print()
except:
    pass

print("=" * 80 + "\n")
