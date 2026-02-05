#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║  CONFIGURATION GIT ET GITHUB - Assistant                         ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Fonction pour demander une confirmation
ask_confirmation() {
    while true; do
        read -p "$1 (o/n) : " yn
        case $yn in
            [Oo]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Répondez par o (oui) ou n (non).";;
        esac
    done
}

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé."
    echo ""
    echo "Installez Git :"
    echo "  - macOS : brew install git"
    echo "  - Ubuntu : sudo apt install git"
    echo "  - Windows : https://git-scm.com/download/win"
    exit 1
fi

echo "✅ Git est installé"
echo ""

# Vérifier si c'est déjà un dépôt Git
if [ -d ".git" ]; then
    echo "ℹ️  Ce dossier est déjà un dépôt Git."
    echo ""

    if ask_confirmation "Voulez-vous réinitialiser complètement Git ?"; then
        echo "⚠️  Suppression de .git..."
        rm -rf .git
        echo "✅ Git réinitialisé"
        echo ""
    else
        echo "ℹ️  Conservation du dépôt Git existant"
        echo ""

        # Vérifier s'il y a un remote
        if git remote -v | grep -q "origin"; then
            echo "ℹ️  Remote origin déjà configuré :"
            git remote -v
            echo ""

            if ask_confirmation "Voulez-vous pousser vers GitHub maintenant ?"; then
                echo ""
                echo "🚀 Push vers GitHub..."
                git add .
                git commit -m "Mise à jour du projet" || true
                git push origin main || git push origin master

                if [ $? -eq 0 ]; then
                    echo ""
                    echo "✅ Code poussé vers GitHub avec succès !"
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "🎯 PROCHAINES ÉTAPES"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo ""
                    echo "1. Allez sur GitHub dans votre navigateur"
                    echo "2. Configurez les secrets (si pas déjà fait) :"
                    echo "   Settings > Secrets and variables > Actions"
                    echo "   📖 Guide : GITHUB_SECRETS_SETUP.md"
                    echo ""
                    echo "3. Lancez le workflow :"
                    echo "   Actions > Récupération des codes comptables > Run workflow"
                    echo "   📖 Guide : QUICK_START_GITHUB.md"
                    echo ""
                    exit 0
                else
                    echo ""
                    echo "❌ Erreur lors du push"
                    echo ""
                    echo "Vérifiez :"
                    echo "  - Votre connexion Internet"
                    echo "  - Vos permissions sur le dépôt"
                    echo "  - Votre authentification GitHub"
                    echo ""
                    echo "📖 Guide complet : INITIALISER_GIT_ET_GITHUB.md"
                    exit 1
                fi
            fi

            exit 0
        fi
    fi
fi

# Initialiser Git si nécessaire
if [ ! -d ".git" ]; then
    echo "📦 Initialisation de Git..."
    git init

    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'initialisation de Git"
        exit 1
    fi

    echo "✅ Git initialisé"
    echo ""
fi

# Vérifier la configuration Git
echo "🔍 Vérification de la configuration Git..."
GIT_USER_NAME=$(git config user.name)
GIT_USER_EMAIL=$(git config user.email)

if [ -z "$GIT_USER_NAME" ] || [ -z "$GIT_USER_EMAIL" ]; then
    echo "⚠️  Configuration Git incomplète"
    echo ""

    if [ -z "$GIT_USER_NAME" ]; then
        read -p "Votre nom complet : " user_name
        git config user.name "$user_name"
    fi

    if [ -z "$GIT_USER_EMAIL" ]; then
        read -p "Votre email : " user_email
        git config user.email "$user_email"
    fi

    echo ""
    echo "✅ Configuration Git complétée"
    echo "   Nom : $(git config user.name)"
    echo "   Email : $(git config user.email)"
    echo ""
fi

# Créer le premier commit
echo "📝 Création du commit initial..."

# Vérifier s'il y a déjà des commits
if git rev-parse HEAD &> /dev/null; then
    echo "ℹ️  Des commits existent déjà"
    git add .
    git commit -m "Mise à jour du projet" || echo "ℹ️  Rien à committer"
else
    git add .
    git commit -m "Premier commit - Projet de synchronisation Airtable vers Sellsy"
fi

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du commit"
    exit 1
fi

echo "✅ Commit créé"
echo ""

# Demander l'URL du dépôt GitHub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 CONFIGURATION DU DÉPÔT GITHUB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Si vous n'avez pas encore créé de dépôt sur GitHub :"
echo "  1. Allez sur https://github.com/new"
echo "  2. Nom : airtable-sellsy-sync (ou autre)"
echo "  3. Visibilité : Private"
echo "  4. NE COCHEZ RIEN d'autre"
echo "  5. Cliquez sur 'Create repository'"
echo ""
echo "Format attendu : https://github.com/VOTRE_USERNAME/nom-du-depot.git"
echo ""

read -p "URL du dépôt GitHub : " github_url

if [ -z "$github_url" ]; then
    echo ""
    echo "❌ URL vide. Opération annulée."
    echo ""
    echo "Vous pouvez toujours configurer le remote plus tard avec :"
    echo "  git remote add origin https://github.com/VOTRE_USERNAME/nom-du-depot.git"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

# Ajouter le remote origin
echo ""
echo "🔗 Configuration du remote GitHub..."

if git remote -v | grep -q "origin"; then
    echo "ℹ️  Remote origin existe déjà, suppression..."
    git remote remove origin
fi

git remote add origin "$github_url"

if [ $? -ne 0 ]; then
    echo "❌ Erreur lors de l'ajout du remote"
    exit 1
fi

echo "✅ Remote configuré : $github_url"
echo ""

# Renommer la branche en main si nécessaire
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 Renommage de la branche en 'main'..."
    git branch -M main
    echo "✅ Branche renommée"
    echo ""
fi

# Pousser vers GitHub
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 PUSH VERS GITHUB"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Git va maintenant pousser votre code vers GitHub."
echo ""
echo "Si Git vous demande un mot de passe :"
echo "  → Utilisez un Personal Access Token (pas votre mot de passe)"
echo "  → Guide : INITIALISER_GIT_ET_GITHUB.md"
echo ""

if ask_confirmation "Pousser le code vers GitHub maintenant ?"; then
    git push -u origin main

    if [ $? -eq 0 ]; then
        echo ""
        echo "╔═══════════════════════════════════════════════════════════════════╗"
        echo "║  ✅ SUCCÈS - CODE POUSSÉ VERS GITHUB                             ║"
        echo "╚═══════════════════════════════════════════════════════════════════╝"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🎯 PROCHAINES ÉTAPES"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "1️⃣  Configurer les secrets GitHub (OBLIGATOIRE)"
        echo ""
        echo "    a. Allez sur votre dépôt GitHub dans le navigateur"
        echo "    b. Settings > Secrets and variables > Actions"
        echo "    c. Cliquez sur 'New repository secret'"
        echo "    d. Ajoutez ces 4 secrets :"
        echo "       - SELLSY_CONSUMER_TOKEN"
        echo "       - SELLSY_CONSUMER_SECRET"
        echo "       - SELLSY_USER_TOKEN"
        echo "       - SELLSY_USER_SECRET"
        echo ""
        echo "    📖 Guide détaillé : GITHUB_SECRETS_SETUP.md"
        echo ""
        echo "2️⃣  Lancer le workflow pour récupérer les codes comptables"
        echo ""
        echo "    a. Onglet Actions > 'Récupération des codes comptables Sellsy'"
        echo "    b. Cliquez sur 'Run workflow' (à droite)"
        echo "    c. Cliquez sur le bouton vert 'Run workflow'"
        echo "    d. Attendez 1 minute"
        echo "    e. Consultez le résumé pour récupérer l'ID du code 628000"
        echo ""
        echo "    📖 Guide détaillé : QUICK_START_GITHUB.md"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
    else
        echo ""
        echo "❌ Erreur lors du push vers GitHub"
        echo ""
        echo "Causes possibles :"
        echo "  - Authentification requise (utilisez un Personal Access Token)"
        echo "  - Problème de connexion Internet"
        echo "  - Permissions insuffisantes sur le dépôt"
        echo ""
        echo "📖 Guide complet : INITIALISER_GIT_ET_GITHUB.md"
        echo ""
        echo "Vous pouvez réessayer avec :"
        echo "  git push -u origin main"
        echo ""
        exit 1
    fi
else
    echo ""
    echo "ℹ️  Push annulé"
    echo ""
    echo "Vous pouvez pousser plus tard avec :"
    echo "  git push -u origin main"
    echo ""
fi
