import requests
import json
import random
import time
from config import (
    SELLSY_CONSUMER_TOKEN,
    SELLSY_CONSUMER_SECRET,
    SELLSY_USER_TOKEN,
    SELLSY_USER_SECRET,
    CATEGORY_MAPPING  # Import du mapping de catégories
)

class SellsyClient:
    def __init__(self):
        """Initialise le client Sellsy API v1"""
        # URL correcte pour l'API v1
        self.api_url = 'https://apifeed.sellsy.com/0/'
        self.consumer_token = SELLSY_CONSUMER_TOKEN
        self.consumer_secret = SELLSY_CONSUMER_SECRET
        self.user_token = SELLSY_USER_TOKEN
        self.user_secret = SELLSY_USER_SECRET
        # Cache pour les catégories
        self._categories_cache = None
        # Cache pour les codes comptables
        self._accounting_codes_cache = None
    
    def _get_oauth_params(self):
        """Génère les paramètres OAuth requis pour l'authentification"""
        oauth_params = {
            'oauth_consumer_key': self.consumer_token,
            'oauth_token': self.user_token,
            'oauth_nonce': str(random.getrandbits(64)),
            'oauth_timestamp': str(int(time.time())),
            'oauth_signature_method': 'PLAINTEXT',
            'oauth_version': '1.0',
            'oauth_signature': f"{self.consumer_secret}&{self.user_secret}"
        }
        return oauth_params
    
    def _prepare_request(self, method, params):
        """Prépare les données de la requête selon le format attendu par l'API Sellsy"""
        request_data = {
            'method': method,
            'params': params
        }
        return request_data
    
    def call_api(self, method, params):
        """
        Envoie une requête à l'API Sellsy
        
        Args:
            method: Méthode API Sellsy (ex: 'Catalogue.create')
            params: Paramètres de la méthode
            
        Returns:
            dict: Réponse de l'API Sellsy
        """
        try:
            # Obtenir les paramètres OAuth
            oauth_params = self._get_oauth_params()
            
            # Préparer les données de la requête
            request_data = self._prepare_request(method, params)
            
            # Structure correcte selon la documentation Sellsy
            data = {
                **oauth_params,
                'request': 1,
                'io_mode': 'json',
                'do_in': json.dumps(request_data)
            }
            
            # Envoyer la requête POST avec les paramètres correctement formatés
            print(f"Envoi de la requête à l'API Sellsy: {method}")
            response = requests.post(self.api_url, data=data)
            
            # Afficher les paramètres envoyés pour le débogage (sans les infos sensibles)
            debug_params = {**params}
            print(f"Paramètres envoyés: {json.dumps(debug_params, indent=2, default=str)}")
            
            # Vérifier le statut de la réponse
            if response.status_code == 200:
                result = response.json()
                print(f"Réponse de l'API (status): {result.get('status')}")
                
                if result.get('status') == 'success':
                    return result.get('response')
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"Erreur API Sellsy: {error_msg}")
                    raise Exception(f"Erreur API Sellsy: {error_msg}")
            else:
                print(f"Erreur HTTP: {response.status_code}")
                print(f"Contenu de la réponse: {response.text}")
                raise Exception(f"Erreur HTTP: {response.status_code}")
        
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API Sellsy: {e}")
            raise
    
    def get_categories(self, force_refresh=False):
        """
        Récupère les catégories de produits/services depuis Sellsy
        
        Args:
            force_refresh: Force le rafraîchissement du cache des catégories
            
        Returns:
            dict: Dictionnaire des catégories {nom_catégorie: id_catégorie}
        """
        # Utiliser le cache si disponible et non forcé
        if self._categories_cache is not None and not force_refresh:
            return self._categories_cache
        
        method = 'Catalogue.getCategories'
        params = {}
        
        try:
            response = self.call_api(method, params)
            
            # Créer un dictionnaire pour le mapping nom -> id
            categories = {}
            
            if response and isinstance(response, dict):
                for category_id, category_data in response.items():
                    # S'assurer que la catégorie a un nom
                    if 'name' in category_data:
                        categories[category_data['name']] = category_id
            
            print(f"Catégories récupérées: {categories}")
            
            # Afficher les catégories pour faciliter la mise en place du mapping
            print("\n=== LISTE COMPLÈTE DES CATÉGORIES SELLSY ===")
            for name, cat_id in categories.items():
                print(f"'{name}': '{cat_id}',")
            print("===========================================\n")
            
            # Mettre en cache
            self._categories_cache = categories
            return categories
        
        except Exception as e:
            print(f"Erreur lors de la récupération des catégories: {e}")
            return {}
    
    def map_category(self, airtable_category):
        """
        Mappe une catégorie Airtable vers un ID de catégorie Sellsy
        
        Args:
            airtable_category: Nom de la catégorie dans Airtable
            
        Returns:
            str: ID de la catégorie dans Sellsy ou None si non trouvée
        """
        # D'abord essayer avec le mapping prédéfini
        if CATEGORY_MAPPING and airtable_category in CATEGORY_MAPPING:
            category_id = CATEGORY_MAPPING[airtable_category]
            print(f"Catégorie '{airtable_category}' mappée via configuration à l'ID: {category_id}")
            return category_id
        
        # Ensuite essayer de trouver la catégorie par son nom exact
        categories = self.get_categories()
        
        # Recherche exacte
        if airtable_category in categories:
            return categories[airtable_category]
        
        # Recherche insensible à la casse
        for name, cat_id in categories.items():
            if name.lower() == airtable_category.lower():
                return cat_id
        
        print(f"⚠️ Catégorie non trouvée: '{airtable_category}'. "
              f"Veuillez ajouter ce mapping dans config.py -> CATEGORY_MAPPING")
        return None

    def get_accounting_codes(self, force_refresh=False):
        """
        Récupère les codes comptables depuis Sellsy

        Args:
            force_refresh: Force le rafraîchissement du cache

        Returns:
            dict: Dictionnaire des codes comptables {code: id}
        """
        # Utiliser le cache si disponible et non forcé
        if self._accounting_codes_cache is not None and not force_refresh:
            return self._accounting_codes_cache

        method = 'Accountdatas.getList'
        params = {}

        try:
            response = self.call_api(method, params)

            # Créer un dictionnaire pour le mapping code -> id
            accounting_codes = {}

            if response and isinstance(response, dict):
                for code_id, code_data in response.items():
                    # S'assurer que le code comptable a un numéro
                    if 'code' in code_data:
                        accounting_codes[code_data['code']] = code_id

            print(f"Codes comptables récupérés: {len(accounting_codes)} codes")

            # Afficher quelques exemples pour le débogage
            print("\n=== EXEMPLES DE CODES COMPTABLES SELLSY ===")
            count = 0
            for code, code_id in accounting_codes.items():
                if count < 10 or code in ['628000', '706000', '601000']:
                    print(f"Code '{code}': ID '{code_id}'")
                    count += 1
            print("===========================================\n")

            # Mettre en cache
            self._accounting_codes_cache = accounting_codes
            return accounting_codes

        except Exception as e:
            print(f"Erreur lors de la récupération des codes comptables: {e}")
            return {}

    def get_accounting_code_id(self, code):
        """
        Récupère l'ID d'un code comptable depuis son numéro

        Args:
            code: Numéro du code comptable (ex: '628000')

        Returns:
            str: ID du code comptable ou None si non trouvé
        """
        accounting_codes = self.get_accounting_codes()

        # Recherche exacte
        if code in accounting_codes:
            return accounting_codes[code]

        # Recherche en convertissant en string si nécessaire
        str_code = str(code)
        if str_code in accounting_codes:
            return accounting_codes[str_code]

        print(f"⚠️ Code comptable non trouvé: '{code}'")
        return None

    def create_service(self, service_data):
        """
        Crée un nouveau service dans Sellsy
        
        Args:
            service_data: Données du service à créer
            
        Returns:
            str: ID du service créé
        """
        method = 'Catalogue.create'
        
        # S'assurer que la valeur par défaut pour le taux de TVA est 20% si non spécifié
        if 'taxrate' not in service_data:
            service_data['taxrate'] = 20.0
        
        # S'assurer que la quantité est spécifiée (valeur par défaut = 1)
        if 'qt' not in service_data:
            service_data['qt'] = 1
        
        # Traiter la catégorie avec le système de mapping
        if 'categoryName' in service_data:
            category_name = service_data.pop('categoryName')
            category_id = self.map_category(category_name)
            if category_id:
                service_data['categoryid'] = category_id
                print(f"Catégorie '{category_name}' associée à l'ID: {category_id}")
            else:
                print(f"⚠️ Catégorie '{category_name}' non trouvée, service créé sans catégorie")

        # Traiter le code comptable de vente
        if 'accountingCode' in service_data:
            accounting_code = service_data.pop('accountingCode')
            accounting_code_id = self.get_accounting_code_id(accounting_code)
            if accounting_code_id:
                service_data['accountingcodeid'] = accounting_code_id
                print(f"Code comptable '{accounting_code}' associé à l'ID: {accounting_code_id}")
            else:
                print(f"⚠️ Code comptable '{accounting_code}' non trouvé, service créé sans code comptable")

        params = {
            'type': 'service',
            'service': service_data
        }
        
        try:
            response = self.call_api(method, params)
            # Vérifier si l'ID du service est retourné (peut être 'service_id' ou 'id')
            if response:
                print(f"Réponse de création du service: {json.dumps(response, indent=2, default=str)}")
                if 'service_id' in response:
                    return response['service_id']
                elif 'id' in response:
                    return response['id']
                else:
                    print(f"L'ID du service n'a pas été retourné par l'API Sellsy. Réponse: {response}")
                    return None
            else:
                print("Réponse vide de l'API Sellsy")
                return None
        
        except Exception as e:
            print(f"Erreur lors de la création du service: {e}")
            return None
    
    def update_service(self, service_id, service_data):
        """
        Met à jour un service existant dans Sellsy
        
        Args:
            service_id: ID du service à mettre à jour
            service_data: Nouvelles données du service
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        method = 'Catalogue.update'
        
        # S'assurer que la valeur par défaut pour le taux de TVA est 20% si non spécifié
        if 'taxrate' not in service_data:
            service_data['taxrate'] = 20.0
        
        # S'assurer que la quantité est spécifiée (valeur par défaut = 1)
        if 'qt' not in service_data:
            service_data['qt'] = 1
        
        # Traiter la catégorie avec le système de mapping
        if 'categoryName' in service_data:
            category_name = service_data.pop('categoryName')
            category_id = self.map_category(category_name)
            if category_id:
                service_data['categoryid'] = category_id
                print(f"Catégorie '{category_name}' associée à l'ID: {category_id}")
            else:
                print(f"⚠️ Catégorie '{category_name}' non trouvée, service mis à jour sans catégorie")

        # Traiter le code comptable de vente
        if 'accountingCode' in service_data:
            accounting_code = service_data.pop('accountingCode')
            accounting_code_id = self.get_accounting_code_id(accounting_code)
            if accounting_code_id:
                service_data['accountingcodeId'] = accounting_code_id
                print(f"Code comptable '{accounting_code}' associé à l'ID: {accounting_code_id}")
            else:
                print(f"⚠️ Code comptable '{accounting_code}' non trouvé, service mis à jour sans code comptable")

        params = {
            'type': 'service',
            'id': service_id,
            'service': service_data
        }
        
        try:
            response = self.call_api(method, params)
            print(f"Réponse de mise à jour du service: {json.dumps(response, indent=2, default=str)}")
            
            if response:
                # La mise à jour peut renvoyer différents formats de réponse
                if 'service_id' in response or 'id' in response or response is True:
                    return True
                else:
                    print(f"Format de réponse inattendu lors de la mise à jour du service: {response}")
                    return False
            else:
                print("Erreur lors de la mise à jour du service")
                return False
        
        except Exception as e:
            print(f"Erreur lors de la mise à jour du service: {e}")
            return False
    
    def delete_service(self, service_id):
        """
        Supprime un service de Sellsy
        
        Args:
            service_id: ID du service à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        method = 'Catalogue.delete'
        params = {
            'type': 'service',
            'id': service_id
        }
        
        try:
            response = self.call_api(method, params)
            return True
        
        except Exception as e:
            print(f"Erreur lors de la suppression du service: {e}")
            return False
