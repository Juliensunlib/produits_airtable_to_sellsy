from sellsy_client import SellsyClient

sellsy = SellsyClient()

print("\n" + "=" * 80)
print("  VÉRIFICATION FINALE")
print("=" * 80 + "\n")

service = sellsy.call_api('Catalogue.getOne', {'type': 'service', 'id': '1709'})

if service:
    print(f"Service      : {service.get('tradename', 'N/A')}")
    print(f"Catégorie ID : {service.get('categoryid', 'N/A')}")
    print(f"Code VENTE   : {service.get('accountingCode', '(vide)')}")
    print(f"Code ACHAT   : {service.get('accountingPurchaseCode', '(vide)')}")
    print()

    vente = service.get('accountingCode', '')
    if vente == '706000':
        print("✅ PARFAIT! Le code 706000 est bien appliqué!")
    elif vente:
        print(f"⚠️  Code actuel: {vente} (attendu: 706000)")
        print()
        print("👉 Configurez le code 706000 sur la catégorie Abonnement dans Sellsy")
    else:
        print("❌ Aucun code comptable")
        print()
        print("👉 Configurez le code 706000 sur la catégorie Abonnement dans Sellsy")

print("\n" + "=" * 80)
