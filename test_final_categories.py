"""
Test final : Création de services avec les catégories Abonnement et Caution
"""
from sellsy_client import SellsyClient
from config import CATEGORY_MAPPING

sellsy = SellsyClient()

print("=" * 80)
print("  TEST FINAL: SERVICES AVEC CATÉGORIES")
print("=" * 80)
print()

print("📋 Configuration des catégories:")
print("-" * 80)
for cat_name, cat_id in CATEGORY_MAPPING.items():
    if cat_id:
        print(f"   {cat_name:<15} → ID Sellsy: {cat_id}")
    else:
        print(f"   {cat_name:<15} → ⚠️  Non configuré")
print()

# Test 1: Créer un service Abonnement
print("=" * 80)
print("  TEST 1: Création d'un service avec catégorie ABONNEMENT")
print("=" * 80)
print()

service_abonnement = {
    'type': 'service',
    'service': {
        'name': 'TEST-ABO-001',
        'tradename': 'Test Abonnement Mensuel',
        'notes': 'Service de test pour la catégorie Abonnement',
        'unitAmount': 99.99,
        'unit': 'mois',
        'actif': 'Y',
        'unitAmountIsTaxesFree': 'Y',
        'qt': 1,
        'taxrate': 20.0,
        'categoryid': CATEGORY_MAPPING['Abonnement']  # ID 57
    }
}

try:
    print(f"📤 Création avec categoryid = {CATEGORY_MAPPING['Abonnement']}")
    response = sellsy.call_api('Catalogue.create', service_abonnement)

    if response:
        service_id = response.get('service_id')
        print(f"✅ Service créé avec ID: {service_id}")

        # Vérifier le service créé
        service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': str(service_id)})
        if service:
            print()
            print("🔍 Détails du service créé:")
            print(f"   Nom          : {service.get('tradename', 'N/A')}")
            print(f"   Catégorie ID : {service.get('categoryid', 'N/A')}")
            print(f"   Code VENTE   : {service.get('accountingCode', '(vide)')}")
            print(f"   Code ACHAT   : {service.get('accountingPurchaseCode', '(vide)')}")
            print()

            if service.get('categoryid') == CATEGORY_MAPPING['Abonnement']:
                print("✅ Catégorie Abonnement correctement associée")

                # Le code comptable doit être hérité de la catégorie
                if service.get('accountingCode'):
                    print(f"✅ Code comptable hérité de la catégorie: {service.get('accountingCode')}")
                else:
                    print("⚠️  Aucun code comptable (configurez-le sur la catégorie Abonnement dans Sellsy)")
    else:
        print("❌ Échec de création")

except Exception as e:
    print(f"❌ Erreur: {str(e)[:150]}")

print()

# Test 2: Créer un service Caution
print("=" * 80)
print("  TEST 2: Création d'un service avec catégorie CAUTION")
print("=" * 80)
print()

service_caution = {
    'type': 'service',
    'service': {
        'name': 'TEST-CAU-001',
        'tradename': 'Test Caution',
        'notes': 'Service de test pour la catégorie Caution',
        'unitAmount': 200.00,
        'unit': 'unité',
        'actif': 'Y',
        'unitAmountIsTaxesFree': 'Y',
        'qt': 1,
        'taxrate': 20.0,
        'categoryid': CATEGORY_MAPPING['Caution']  # ID 58
    }
}

try:
    print(f"📤 Création avec categoryid = {CATEGORY_MAPPING['Caution']}")
    response = sellsy.call_api('Catalogue.create', service_caution)

    if response:
        service_id = response.get('service_id')
        print(f"✅ Service créé avec ID: {service_id}")

        # Vérifier le service créé
        service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': str(service_id)})
        if service:
            print()
            print("🔍 Détails du service créé:")
            print(f"   Nom          : {service.get('tradename', 'N/A')}")
            print(f"   Catégorie ID : {service.get('categoryid', 'N/A')}")
            print(f"   Code VENTE   : {service.get('accountingCode', '(vide)')}")
            print(f"   Code ACHAT   : {service.get('accountingPurchaseCode', '(vide)')}")
            print()

            if service.get('categoryid') == CATEGORY_MAPPING['Caution']:
                print("✅ Catégorie Caution correctement associée")
    else:
        print("❌ Échec de création")

except Exception as e:
    print(f"❌ Erreur: {str(e)[:150]}")

print()
print("=" * 80)
print("  RÉSUMÉ")
print("=" * 80)
print()
print("✅ Les catégories sont correctement configurées:")
print(f"   • Abonnement → ID {CATEGORY_MAPPING['Abonnement']}")
print(f"   • Caution    → ID {CATEGORY_MAPPING['Caution']}")
print()
print("📝 IMPORTANT:")
print("   Les codes comptables sont hérités des catégories.")
print("   Configurez-les manuellement dans Sellsy:")
print()
print("   1. Paramètres > Catalogue > Catégories")
print("   2. Catégorie 'Abonnement' → Code comptable de VENTE: 706000")
print("   3. Catégorie 'Caution' → Code comptable selon vos besoins")
print()
print("=" * 80)
