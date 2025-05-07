import requests
import json
import random
import hashlib
import hmac
import time
import urllib.parse
from config import (
    SELLSY_API_URL,
    SELLSY_CONSUMER_TOKEN,
    SELLSY_CONSUMER_SECRET,
    SELLSY_USER_TOKEN,
    SELLSY_USER_SECRET
)

class SellsyClient:
    def __init__(self):
        """Initialise le client Sellsy API v1"""
        self.api_url = SELLSY_API_URL
        self.consumer_token = SELLSY_CONSUMER_TOKEN
        self.consumer_secret = SELLSY_CONSUMER_SECRET
        self.user_token = SELLSY_USER_TOKEN
        self.user_secret = SELLSY_USER_SECRET
    
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
        """Prépare les données de la requête"""
        request_data = {
            'method': method,
            'params': params
        }
        
        # Convertir en JSON encodé pour l'API Sellsy
        encoded_request = urllib.parse.quote(json.dumps(request_data))
        
        return {
            'request': encoded_request,
            'io_mode': 'json'
        }
    
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
            
            # Combiner les données OAuth et les données de requête
            data = {**oauth_params, **request_data}
            
            # Envoyer la requête POST
            response = requests.post(self.api_url, data=data)
            
            # Vérifier le statut de la réponse
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    return result.get('response')
                else:
                    error_msg = result.get('error', 'Unknown error')
                    print(f"Erreur API Sellsy: {error_msg}")
                    raise Exception(f"Erreur API Sellsy: {error_msg}")
            else:
                print(f"Erreur HTTP: {response.status_code}")
                raise Exception(f"Erreur HTTP: {response.status_code}")
        
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API Sellsy: {e}")
            raise
    
    def create_service(self, service_data):
        """
        Crée un nouveau service dans Sellsy
        
        Args:
            service_data: Données du service à créer
            
        Returns:
            str: ID du service créé
        """
        method = 'Catalogue.create'
        params = {
            'type': 'service',
            'service': service_data
        }
        
        try:
            response = self.call_api(method, params)
            if response and 'service_id' in response:
                return response['service_id']
            else:
                print("L'ID du service n'a pas été retourné par l'API Sellsy")
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
        
        # S'assurer que l'ID est inclus dans les données
        service_data['id'] = service_id
        
        params = {
            'type': 'service',
            'id': service_id,
            'service': service_data
        }
        
        try:
            response = self.call_api(method, params)
            if response and 'service_id' in response:
                return True
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
