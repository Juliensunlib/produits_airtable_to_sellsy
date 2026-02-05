"""
Test de gestion des catégories via l'API Sellsy
"""
from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("=" * 80)
print("  TEST: GESTION DES CATÉGORIES")
print("=" * 80)
print()

# Test 1: Récupérer les catégories
print("📋 Test 1: Récupération des catégories")
print("-" * 80)

try:
    categories = sellsy.call_api('Catalogue.getCategories', {})
    if categories:
        print(f"✅ {len(categories)} catégories trouvées")
        for cat_id, cat_data in list(categories.items())[:5]:
            name = cat_data.get('name', cat_data.get('label', 'N/A'))
            print(f"   ID: {cat_id} - {name}")
    else:
        print("❌ Aucune catégorie")
except Exception as e:
    print(f"❌ Erreur: {str(e)[:100]}")

print()

# Test 2: Créer une catégorie "Abonnement" avec code comptable
print("📝 Test 2: Création d'une catégorie 'Abonnement'")
print("-" * 80)

try:
    params = {
        'category': {
            'name': 'Abonnement',
            'accountingcodeid': 75,  # Code 706000
            'type': 'service'
        }
    }

    response = sellsy.call_api('Catalogue.createCategory', params)
    if response:
        print(f"✅ Catégorie créée avec succès!")
        print(f"   ID: {response.get('id', 'N/A')}")
    else:
        print("❌ Échec de création")

except Exception as e:
    error_msg = str(e)
    if 'already exists' in error_msg.lower() or 'E_CATEGORY_EXISTS' in error_msg:
        print("⚠️  La catégorie 'Abonnement' existe déjà")
        print()
        print("📝 Test 3: Mise à jour de la catégorie existante")
        print("-" * 80)

        # Chercher l'ID de la catégorie Abonnement
        try:
            categories = sellsy.call_api('Catalogue.getCategories', {})
            if categories:
                for cat_id, cat_data in categories.items():
                    name = cat_data.get('name', cat_data.get('label', ''))
                    if name.lower() == 'abonnement':
                        print(f"   Catégorie trouvée - ID: {cat_id}")

                        # Tenter de mettre à jour
                        update_params = {
                            'id': cat_id,
                            'category': {
                                'accountingcodeid': 75
                            }
                        }

                        update_response = sellsy.call_api('Catalogue.updateCategory', update_params)
                        if update_response:
                            print(f"   ✅ Catégorie mise à jour avec le code comptable ID 75")
                        else:
                            print(f"   ❌ Échec de la mise à jour")
                        break
        except Exception as e2:
            print(f"   ❌ Erreur: {str(e2)[:100]}")
    else:
        print(f"❌ Erreur: {error_msg[:100]}")

print()
print("=" * 80)
print()
print("💡 PROCHAINE ÉTAPE:")
print()
print("1. Si la catégorie 'Abonnement' a été créée/mise à jour avec succès,")
print("   tous les services de cette catégorie hériteront du code 706000")
print()
print("2. Sinon, configurez manuellement dans Sellsy:")
print("   Paramètres > Catalogue > Catégories")
print("   Créez/Modifiez la catégorie 'Abonnement'")
print("   Associez-lui le code comptable 706000 (ID: 75)")
print()
