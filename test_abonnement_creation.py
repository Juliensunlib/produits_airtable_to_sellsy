"""
Script de test pour vérifier la création d'un service abonnement avec le code comptable 628000
"""
from airtable_client import AirtableClient
from sellsy_client import SellsyClient
from config import ACCOUNTING_CODE_MAPPING

def test_accounting_code_mapping():
    """Teste que le mapping du code comptable 628000 est bien configuré"""
    print("=" * 80)
    print("  TEST DE CONFIGURATION DU CODE COMPTABLE")
    print("=" * 80)
    print()

    print("📋 Vérification du mapping des codes comptables:")
    print()

    for code, code_id in ACCOUNTING_CODE_MAPPING.items():
        status = "✅" if code_id else "❌"
        print(f"  {status} {code}: {code_id}")

    print()

    if ACCOUNTING_CODE_MAPPING.get('628000'):
        print("✅ Le code comptable 628000 est bien configuré avec l'ID:", ACCOUNTING_CODE_MAPPING['628000'])
        print()
        return True
    else:
        print("❌ Le code comptable 628000 n'est pas configuré!")
        print()
        return False

def test_airtable_mapping():
    """Teste le mapping d'un service abonnement depuis Airtable"""
    print("=" * 80)
    print("  TEST DE MAPPING AIRTABLE → SELLSY")
    print("=" * 80)
    print()

    # Simuler un enregistrement Airtable avec catégorie Abonnement
    fake_airtable_record = {
        'id': 'rec_test_123',
        'fields': {
            'Référence': 'ABO-TEST-001',
            'Nom du service': 'Test Abonnement Premium',
            'Description': 'Service de test pour vérifier le code comptable',
            'Prix HT': 99.99,
            'Unité': 'mois',
            'Actif': True,
            'Catégorie': 'Abonnement',  # ← Catégorie "Abonnement"
            'Taux TVA': 20.0,
            'Quantité': 1,
        }
    }

    print("📦 Enregistrement Airtable simulé:")
    print(f"  - Nom: {fake_airtable_record['fields']['Nom du service']}")
    print(f"  - Catégorie: {fake_airtable_record['fields']['Catégorie']}")
    print()

    # Tester le mapping
    airtable_client = AirtableClient()
    sellsy_data = airtable_client.map_to_sellsy_format(fake_airtable_record)

    print()
    print("📤 Données formatées pour Sellsy:")
    print()

    for key, value in sellsy_data.items():
        print(f"  • {key}: {value}")

    print()

    if 'accountingCode' in sellsy_data and sellsy_data['accountingCode'] == '628000':
        print("✅ Le code comptable 628000 a bien été ajouté automatiquement!")
        print()
        return True
    else:
        print("❌ Le code comptable 628000 n'a pas été ajouté!")
        print()
        return False

def test_sellsy_client_conversion():
    """Teste la conversion du code comptable vers l'ID Sellsy"""
    print("=" * 80)
    print("  TEST DE CONVERSION CODE COMPTABLE → ID SELLSY")
    print("=" * 80)
    print()

    sellsy_client = SellsyClient()

    print("🔄 Test de conversion du code 628000 vers ID Sellsy:")
    print()

    accounting_code_id = sellsy_client.get_accounting_code_id('628000')

    print()

    if accounting_code_id == '76':
        print(f"✅ Conversion réussie: 628000 → ID: {accounting_code_id}")
        print()
        return True
    else:
        print(f"❌ Conversion échouée! ID retourné: {accounting_code_id}")
        print()
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print()
    print("🧪 DÉBUT DES TESTS")
    print()

    results = []

    # Test 1: Configuration
    results.append(("Configuration du mapping", test_accounting_code_mapping()))

    # Test 2: Mapping Airtable
    results.append(("Mapping Airtable → Sellsy", test_airtable_mapping()))

    # Test 3: Conversion dans SellsyClient
    results.append(("Conversion code → ID", test_sellsy_client_conversion()))

    # Résultats finaux
    print("=" * 80)
    print("  RÉSULTATS DES TESTS")
    print("=" * 80)
    print()

    all_passed = True
    for test_name, passed in results:
        status = "✅ RÉUSSI" if passed else "❌ ÉCHOUÉ"
        print(f"  {status} - {test_name}")
        if not passed:
            all_passed = False

    print()
    print("=" * 80)

    if all_passed:
        print("  🎉 TOUS LES TESTS SONT PASSÉS!")
        print("=" * 80)
        print()
        print("✅ Votre configuration est prête!")
        print()
        print("📝 Prochaines étapes:")
        print("   1. Créez un service de catégorie 'Abonnement' dans Airtable")
        print("   2. Marquez-le 'À synchroniser'")
        print("   3. Lancez: python3 main.py")
        print("   4. Le code comptable 628000 (ID: 76) sera automatiquement ajouté!")
        print()
    else:
        print("  ⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("=" * 80)
        print()
        print("Vérifiez la configuration et réessayez.")
        print()

    return all_passed

if __name__ == "__main__":
    run_all_tests()
