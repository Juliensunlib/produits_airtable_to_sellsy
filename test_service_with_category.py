"""
Test : Associer le service 1709 à la catégorie Abonnement (ID 57)
et vérifier si le code comptable 706000 est appliqué automatiquement
"""
from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: SERVICE AVEC CATÉGORIE ABONNEMENT")
print("=" * 80)
print()

# Étape 1: Mettre à jour le service 1709 avec la catégorie 57
print("📝 Étape 1: Association du service 1709 à la catégorie Abonnement (ID: 57)")
print("-" * 80)

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
        'categoryid': 57  # Catégorie Abonnement
    }
}

try:
    response = sellsy.call_api('Catalogue.update', params)
    if response:
        print("✅ Service mis à jour avec la catégorie Abonnement")
    else:
        print("❌ Échec de la mise à jour")

except Exception as e:
    print(f"❌ Erreur: {e}")

print()

# Étape 2: Vérifier si le code comptable 706000 apparaît
print("🔍 Étape 2: Vérification des codes comptables")
print("-" * 80)

try:
    service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': '1709'})

    if service:
        categoryid = service.get('categoryid', '(vide)')
        vente = service.get('accountingCode', '(vide)')
        achat = service.get('accountingPurchaseCode', '(vide)')

        print(f"Catégorie ID   : {categoryid}")
        print(f"Code de VENTE  : {vente}")
        print(f"Code d'ACHAT   : {achat}")
        print()

        if categoryid == '57':
            print("✅ La catégorie Abonnement est bien associée")

            if vente == '706000':
                print("✅ Le code comptable 706000 est appliqué automatiquement!")
                print()
                print("🎉 SUCCÈS TOTAL!")
            elif vente and vente != '(vide)' and vente != '275500':
                print(f"⚠️  Un code de vente est présent ({vente}), mais ce n'est pas 706000")
            else:
                print("❌ Le code 706000 n'est PAS appliqué automatiquement")
                print()
                print("💡 Solution: Configurez manuellement le code comptable dans Sellsy:")
                print("   Paramètres > Catalogue > Catégories > Abonnement")
                print("   Définissez le code comptable de VENTE à 706000")
        else:
            print(f"❌ La catégorie n'a pas été appliquée correctement (ID: {categoryid})")

except Exception as e:
    print(f"❌ Erreur: {e}")

print()
print("=" * 80)
