import requests
import json
import random
import time
from config import (
    SELLSY_CONSUMER_TOKEN,
    SELLSY_CONSUMER_SECRET,
    SELLSY_USER_TOKEN,
    SELLSY_USER_SECRET
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
            
            # CORRECTION: Structure correcte selon la documentation Sellsy
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
            
            # Mettre en cache
            self._categories_cache = categories
            return categories
        
        except Exception as e:
            print(f"Erreur lors de la récupération des catégories: {e}")
            return {}
    
    def get_category_id(self, category_name):
        """
        Obtient l'ID d'une catégorie à partir de son nom
        
        Args:
            category_name: Nom de la catégorie
            
        Returns:
            str: ID de la catégorie ou None si non trouvée
        """
        categories = self.get_categories()
        
        # Recherche exacte
        if category_name in categories:
            return categories[category_name]
        
        # Recherche insensible à la casse
        for name, cat_id in categories.items():
            if name.lower() == category_name.lower():
                return cat_id
        
        print(f"Catégorie non trouvée: {category_name}")
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
        
        # Traiter la catégorie si présente
        if 'category' in service_data:
            category_name = service_data.pop('category')
            category_id = self.get_category_id(category_name)
            if category_id:
                service_data['categoryid'] = category_id
                print(f"Catégorie '{category_name}' mappée à l'ID: {category_id}")
            else:
                print(f"Catégorie '{category_name}' non trouvée dans Sellsy")
            
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
        
        # Traiter la catégorie si présente
        if 'category' in service_data:
            category_name = service_data.pop('category')
            category_id = self.get_category_id(category_name)
            if category_id:
                service_data['categoryid'] = category_id
                print(f"Catégorie '{category_name}' mappée à l'ID: {category_id}")
            else:
                print(f"Catégorie '{category_name}' non trouvée dans Sellsy")
        
        # S'assurer que l'ID est inclus dans les données
        service_data['id'] = service_id
        
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
