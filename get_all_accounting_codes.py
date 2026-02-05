"""
Script pour récupérer tous les codes comptables depuis Sellsy
À exécuter manuellement quand nécessaire
"""
import os
import json
from dotenv import load_dotenv
from sellsy_client import SellsyClient

def get_all_accounting_codes():
    """Récupère tous les codes comptables depuis Sellsy avec pagination"""

    print("=" * 80)
    print("  RÉCUPÉRATION DES CODES COMPTABLES SELLSY")
    print("=" * 80)
    print()

    # Charger les variables d'environnement
    load_dotenv()

    # Vérifier les credentials
    if not os.getenv('SELLSY_CONSUMER_TOKEN'):
        print("❌ ERREUR: Variables d'environnement Sellsy manquantes")
        print("   Assurez-vous que votre fichier .env contient:")
        print("   - SELLSY_CONSUMER_TOKEN")
        print("   - SELLSY_CONSUMER_SECRET")
        print("   - SELLSY_USER_TOKEN")
        print("   - SELLSY_USER_SECRET")
        return

    try:
        # Initialiser le client Sellsy
        sellsy_client = SellsyClient()
        print("✅ Client Sellsy initialisé")
        print()

        # Paramètres de récupération
        all_codes = []
        limit = 100  # Maximum autorisé
        offset = 0

        print("🔍 Récupération des codes comptables...")
        print()

        while True:
            # Appeler l'API Sellsy pour obtenir les codes comptables
            params = {
                'pagination': {
                    'limit': limit,
                    'offset': offset
                },
                'order': {
                    'field': 'code',
                    'direction': 'asc'
                }
            }

            print(f"   Récupération de {offset} à {offset + limit}...", end=" ")

            try:
                response = sellsy_client.call_api('Accountdatas.getList', params)

                if response and isinstance(response, dict):
                    # Ajouter les codes à la liste
                    codes = list(response.values()) if response else []
                    all_codes.extend(codes)

                    print(f"✓ {len(codes)} codes récupérés")

                    # Si on a récupéré moins que la limite, c'est la dernière page
                    if len(codes) < limit:
                        break

                    offset += limit
                else:
                    print("✗ Aucune donnée")
                    break

            except Exception as e:
                print(f"✗ Erreur: {e}")
                break

        print()
        print("=" * 80)
        print(f"  TOTAL: {len(all_codes)} codes comptables récupérés")
        print("=" * 80)
        print()

        if not all_codes:
            print("⚠️  Aucun code comptable trouvé")
            print()
            print("💡 Essayez ces méthodes alternatives:")
            print("   1. Accountingcode.getList")
            print("   2. Accountingcodes.getList")
            print("   3. Catalogue.getAccountingCodes")
            return

        # Afficher les codes comptables de manière structurée
        print("📋 LISTE DES CODES COMPTABLES:")
        print()
        print(f"{'Code':<10} {'Libellé':<60} {'ID':<10}")
        print("-" * 80)

        target_code_found = False
        target_code_id = None

        for code_data in all_codes:
            if isinstance(code_data, dict):
                code_num = code_data.get('code', code_data.get('accountingcode', 'N/A'))
                label = code_data.get('label', code_data.get('libelle', code_data.get('name', 'N/A')))
                code_id = code_data.get('id', code_data.get('accountingcodeid', 'N/A'))

                # Tronquer le libellé s'il est trop long
                if len(str(label)) > 60:
                    label = str(label)[:57] + "..."

                print(f"{str(code_num):<10} {str(label):<60} {str(code_id):<10}")

                # Vérifier si c'est le code 628000 recherché
                if str(code_num) == '628000':
                    target_code_found = True
                    target_code_id = code_id

        print()
        print("=" * 80)

        # Si le code 628000 a été trouvé, afficher les instructions
        if target_code_found:
            print("  🎯 CODE COMPTABLE 628000 TROUVÉ!")
            print("=" * 80)
            print()
            print(f"✅ ID du code comptable 628000: {target_code_id}")
            print()
            print("👉 ÉTAPES SUIVANTES:")
            print()
            print("1. Ouvrez le fichier config.py")
            print()
            print("2. Trouvez la section ACCOUNTING_CODE_MAPPING")
            print()
            print("3. Ajoutez ou modifiez cette ligne:")
            print()
            print(f"   ACCOUNTING_CODE_MAPPING = {{")
            print(f"       '628000': '{target_code_id}',")
            print(f"   }}")
            print()
            print("4. Décommentez les lignes dans airtable_client.py (lignes 119-122)")
            print()
            print("5. Relancez la synchronisation avec: python3 main.py")
            print()
        else:
            print("  ⚠️  CODE COMPTABLE 628000 NON TROUVÉ")
            print("=" * 80)
            print()
            print("💡 SOLUTIONS:")
            print()
            print("1. Créez le code comptable 628000 dans Sellsy:")
            print("   - Allez dans Paramètres > Comptabilité > Plan comptable")
            print("   - Ajoutez un nouveau code avec:")
            print("     • Code: 628000")
            print("     • Libellé: Abonnement (ou autre)")
            print()
            print("2. Relancez ce script pour récupérer son ID")
            print()

        # Sauvegarder dans un fichier JSON pour référence
        output_file = 'accounting_codes_sellsy.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_codes, f, indent=2, ensure_ascii=False)

        print("=" * 80)
        print(f"📁 Liste complète sauvegardée dans: {output_file}")
        print("=" * 80)
        print()

    except Exception as e:
        print()
        print("=" * 80)
        print("  ❌ ERREUR")
        print("=" * 80)
        print()
        print(f"Erreur lors de la récupération: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()

def try_alternative_methods():
    """Essaie différentes méthodes API si la première ne fonctionne pas"""

    load_dotenv()

    try:
        sellsy_client = SellsyClient()

        methods = [
            'Accountdatas.getList',
            'Accountingcode.getList',
            'Accountingcodes.getList',
            'Catalogue.getAccountingCodes',
            'Accountpreferences.getList',
        ]

        print()
        print("=" * 80)
        print("  RECHERCHE DE LA BONNE MÉTHODE API")
        print("=" * 80)
        print()

        for method in methods:
            print(f"🔍 Test de: {method}...", end=" ")

            try:
                response = sellsy_client.call_api(method, {'pagination': {'limit': 5}})

                if response and isinstance(response, dict):
                    print("✅ Fonctionne!")
                    print(f"   Exemple de réponse: {json.dumps(response, indent=2)[:200]}...")
                    print()
                    return method
                else:
                    print("❌ Pas de données")
            except Exception as e:
                print(f"❌ Erreur: {str(e)[:50]}")

        print()
        print("⚠️  Aucune méthode ne fonctionne")
        print()

        return None

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    print()
    get_all_accounting_codes()

    # Si la méthode principale échoue, essayer les alternatives
    # Décommentez si nécessaire:
    # print("\n🔄 Essai de méthodes alternatives...")
    # try_alternative_methods()
