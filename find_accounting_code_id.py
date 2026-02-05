"""
Script pour trouver l'ID d'un code comptable dans Sellsy en analysant un service existant
"""
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importer après le chargement de .env
from sellsy_client import SellsyClient

def get_service_details(sellsy_client, service_id):
    """Récupère les détails d'un service pour voir son code comptable"""
    print("=" * 70)
    print(f"  ANALYSE DU SERVICE ID {service_id}")
    print("=" * 70)
    print()

    try:
        method = 'Catalogue.getOne'
        params = {
            'type': 'service',
            'id': service_id
        }

        response = sellsy_client.call_api(method, params)

        if response and isinstance(response, dict):
            print("✅ Service récupéré avec succès!\n")
            print(f"📌 Nom: {response.get('tradename', 'N/A')}")
            print(f"📌 Référence: {response.get('name', 'N/A')}")
            print()

            # Chercher tous les champs liés aux codes comptables
            print("🔍 Recherche des champs de code comptable...")
            print()

            accounting_fields_found = {}

            # Liste exhaustive des noms possibles
            possible_fields = [
                'accountingcodeid',
                'accountingcodeId',
                'accountingCodeId',
                'accounting_code_id',
                'purchaseAccountingcodeid',
                'purchaseAccountingcodeId',
                'saleAccountingcodeid',
                'saleAccountingcodeId',
            ]

            # Chercher dans tous les champs du service
            for key, value in response.items():
                # Chercher les champs qui contiennent "account" et "code"
                if 'account' in key.lower() and 'code' in key.lower():
                    accounting_fields_found[key] = value
                    print(f"   ✓ {key}: {value}")

                # Vérifier aussi les champs spécifiques
                if key in possible_fields and value:
                    accounting_fields_found[key] = value
                    print(f"   ✓ {key}: {value}")

            if accounting_fields_found:
                print()
                print("=" * 70)
                print("  ✅ CODE COMPTABLE TROUVÉ!")
                print("=" * 70)
                print()

                # Prendre le premier ID trouvé (probablement le bon)
                accounting_id = list(accounting_fields_found.values())[0]

                print(f"📋 ID du code comptable à utiliser: {accounting_id}")
                print()
                print("👉 AJOUTEZ CETTE LIGNE dans config.py -> ACCOUNTING_CODE_MAPPING:")
                print()
                print(f"    '628000': '{accounting_id}',")
                print()
                print("=" * 70)
            else:
                print()
                print("⚠️ Aucun code comptable trouvé dans ce service")
                print("   Le service n'a probablement pas de code comptable assigné.")
                print()
                print("💡 SOLUTION:")
                print("   1. Allez dans votre interface Sellsy")
                print(f"   2. Éditez le service (ID: {service_id})")
                print("   3. Assignez-lui le code comptable souhaité (ex: 628000)")
                print("   4. Relancez ce script")
                print()

            # Afficher TOUS les champs pour debug
            print()
            print("=" * 70)
            print("  DEBUG: TOUS LES CHAMPS DU SERVICE")
            print("=" * 70)
            print()
            for key, value in sorted(response.items()):
                print(f"{key}: {value}")

            return response
        else:
            print("❌ Aucune réponse de l'API")
            return None

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print()
    print("=" * 70)
    print("  OUTIL DE RECHERCHE D'ID DE CODE COMPTABLE SELLSY")
    print("=" * 70)
    print()

    # Vérifier que les variables d'environnement sont chargées
    if not os.getenv('SELLSY_CONSUMER_TOKEN'):
        print("❌ Erreur: Variables d'environnement Sellsy non trouvées")
        print("   Vérifiez que le fichier .env existe et contient les clés API Sellsy")
        return

    # Initialiser le client Sellsy
    try:
        sellsy_client = SellsyClient()
        print("✅ Client Sellsy initialisé avec succès")
        print()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du client Sellsy: {e}")
        return

    # Récupérer l'ID du service depuis les arguments de ligne de commande
    service_id = '1709'  # Valeur par défaut

    if len(sys.argv) > 1:
        service_id = sys.argv[1]
        print(f"📌 ID de service fourni: {service_id}")
        print()
    else:
        print(f"💡 Utilisation: python3 find_accounting_code_id.py <SERVICE_ID>")
        print(f"   Utilisation de l'ID par défaut: {service_id}")
        print()

    # Analyser le service existant
    service_data = get_service_details(sellsy_client, service_id)

    print()
    print("=" * 70)
    print("  FIN DE L'ANALYSE")
    print("=" * 70)
    print()

if __name__ == "__main__":
    main()
