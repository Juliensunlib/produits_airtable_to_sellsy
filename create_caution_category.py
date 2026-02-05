"""
Création de la catégorie Caution dans Sellsy
"""
from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("=" * 80)
print("  CRÉATION DE LA CATÉGORIE CAUTION")
print("=" * 80)
print()

# Vérifier si la catégorie existe déjà
print("🔍 Vérification des catégories existantes...")
print()

try:
    categories = sellsy.call_api('Catalogue.getCategories', {})

    if categories and isinstance(categories, list):
        print(f"✅ {len(categories)} catégories trouvées")

        # Chercher si Caution existe déjà
        caution_found = False
        for cat in categories:
            if isinstance(cat, dict):
                name = cat.get('name', cat.get('label', ''))
                cat_id = cat.get('id', '')

                if name.lower() == 'caution':
                    caution_found = True
                    print(f"⚠️  La catégorie 'Caution' existe déjà avec l'ID: {cat_id}")
                    print()
                    print(f"📝 Ajoutez cette ligne dans config.py:")
                    print(f"   'Caution': '{cat_id}',")
                    break

        if not caution_found:
            print("ℹ️  La catégorie 'Caution' n'existe pas encore")
            print()
    else:
        print(f"ℹ️  Format de réponse différent: {type(categories)}")
        print()

except Exception as e:
    print(f"⚠️  Erreur lors de la récupération: {e}")
    print()

# Créer la catégorie Caution
print("-" * 80)
print("📝 Création de la catégorie 'Caution'...")
print()

try:
    params = {
        'category': {
            'name': 'Caution',
            'type': 'service'
        }
    }

    response = sellsy.call_api('Catalogue.createCategory', params)

    if response:
        cat_id = response.get('id', response.get('category_id', 'N/A'))
        print(f"✅ Catégorie 'Caution' créée avec succès!")
        print(f"   ID: {cat_id}")
        print()
        print("=" * 80)
        print("  MISE À JOUR DE LA CONFIGURATION")
        print("=" * 80)
        print()
        print(f"📝 Ajoutez cette ligne dans config.py -> CATEGORY_MAPPING:")
        print()
        print(f"   'Caution': '{cat_id}',")
        print()
    else:
        print("❌ Échec de la création")

except Exception as e:
    error_msg = str(e)
    if 'already exists' in error_msg.lower() or 'E_CATEGORY_EXISTS' in error_msg:
        print("⚠️  La catégorie 'Caution' existe déjà")
        print()
        print("🔍 Relancez le script pour obtenir l'ID existant")
    else:
        print(f"❌ Erreur: {error_msg}")

print()
print("=" * 80)
