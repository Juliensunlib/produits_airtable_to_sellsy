#!/bin/bash

echo ""
echo "========================================================================="
echo "  RÉCUPÉRATION DES CODES COMPTABLES SELLSY (EN LOCAL)"
echo "========================================================================="
echo ""

# Vérifier si le fichier .env existe
if [ ! -f .env ]; then
    echo "❌ Le fichier .env n'existe pas"
    echo ""
    echo "Création du fichier .env depuis .env.example..."
    cp .env.example .env
    echo "✅ Fichier .env créé"
    echo ""
    echo "⚠️  IMPORTANT: Vous devez maintenant éditer le fichier .env"
    echo "   et ajouter vos vraies clés API Sellsy"
    echo ""
    echo "1. Ouvrez le fichier .env:"
    echo "   nano .env"
    echo ""
    echo "2. Remplacez les valeurs par vos vraies clés Sellsy:"
    echo "   SELLSY_CONSUMER_TOKEN=votre_vraie_clé"
    echo "   SELLSY_CONSUMER_SECRET=votre_vraie_clé"
    echo "   SELLSY_USER_TOKEN=votre_vraie_clé"
    echo "   SELLSY_USER_SECRET=votre_vraie_clé"
    echo ""
    echo "3. Sauvegardez et relancez ce script:"
    echo "   bash setup_and_get_codes.sh"
    echo ""
    exit 1
fi

# Vérifier si les clés Sellsy sont configurées
source .env

if [ -z "$SELLSY_CONSUMER_TOKEN" ] || [ "$SELLSY_CONSUMER_TOKEN" = "votre_consumer_token" ]; then
    echo "❌ Les clés Sellsy ne sont pas configurées dans .env"
    echo ""
    echo "Ouvrez le fichier .env et ajoutez vos vraies clés Sellsy:"
    echo ""
    echo "   SELLSY_CONSUMER_TOKEN=votre_vraie_clé"
    echo "   SELLSY_CONSUMER_SECRET=votre_vraie_clé"
    echo "   SELLSY_USER_TOKEN=votre_vraie_clé"
    echo "   SELLSY_USER_SECRET=votre_vraie_clé"
    echo ""
    echo "Pour obtenir vos clés Sellsy:"
    echo "1. Connectez-vous sur https://www.sellsy.com"
    echo "2. Allez dans Paramètres > API"
    echo "3. Créez une nouvelle clé API"
    echo "4. Copiez les 4 clés générées dans votre .env"
    echo ""
    exit 1
fi

echo "✅ Fichier .env trouvé avec les clés Sellsy"
echo ""

# Vérifier que Python et les dépendances sont installés
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

echo "📦 Vérification des dépendances Python..."
pip3 install -r requirements.txt --quiet

echo ""
echo "🔍 Récupération des codes comptables depuis Sellsy..."
echo ""
echo "========================================================================="
echo ""

# Exécuter le script
python3 get_all_accounting_codes.py

# Vérifier si le script a réussi
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================================="
    echo "  ✅ SUCCÈS!"
    echo "========================================================================="
    echo ""
    echo "📄 Le fichier accounting_codes_sellsy.json a été créé"
    echo ""
    echo "👉 PROCHAINES ÉTAPES:"
    echo ""
    echo "1. Consultez le résumé ci-dessus pour trouver l'ID du code 628000"
    echo ""
    echo "2. Ouvrez config.py et ajoutez l'ID trouvé:"
    echo "   ACCOUNTING_CODE_MAPPING = {"
    echo "       '628000': 'ID_TROUVE',"
    echo "   }"
    echo ""
    echo "3. Décommentez les lignes 120-122 dans airtable_client.py"
    echo ""
    echo "4. Testez la synchronisation:"
    echo "   python3 main.py"
    echo ""
else
    echo ""
    echo "========================================================================="
    echo "  ❌ ÉCHEC"
    echo "========================================================================="
    echo ""
    echo "Consultez les messages d'erreur ci-dessus pour identifier le problème"
    echo ""
    echo "Problèmes courants:"
    echo "- Clés API invalides ou expirées"
    echo "- Problème de connexion à l'API Sellsy"
    echo "- Compte Sellsy sans accès API"
    echo ""
    exit 1
fi
