from pyairtable import Table
from config import AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME
from datetime import datetime

class AirtableClient:
    def __init__(self):
        """Initialise le client Airtable"""
        self.table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    
    def get_all_services(self):
        """Récupère tous les services depuis Airtable"""
        try:
            return self.table.all()
        except Exception as e:
            print(f"Erreur lors de la récupération des services depuis Airtable: {e}")
            return []
    
    def get_services_to_sync(self):
        """
        Récupère les services marqués 'À synchroniser'
        """
        try:
            # Utilisation de la formule simplifiée pour éviter les problèmes d'encodage
            formula = "{Statut de synchronisation} = 'À synchroniser'"
            print(f"Formule utilisée: {formula}")
            records = self.table.all(formula=formula)
            print(f"Services à synchroniser récupérés: {len(records)}")
            return records
        except Exception as e:
            print(f"Erreur lors de la récupération des services à synchroniser: {e}")
            print(f"Détails de l'erreur: {str(e)}")
            return []
    
    def update_service_status(self, record_id, sellsy_id=None, status="Synchronisé", error_message=None):
        """
        Met à jour le statut d'un service après synchronisation
        
        Args:
            record_id: ID de l'enregistrement Airtable
            sellsy_id: ID du service dans Sellsy (si création réussie)
            status: Statut de synchronisation ("Synchronisé" ou "Erreur")
            error_message: Message d'erreur en cas d'échec
        """
        try:
            fields_to_update = {
                "Statut de synchronisation": status,
                "Dernière synchronisation": datetime.now().isoformat()
            }
            
            if sellsy_id:
                fields_to_update["ID Sellsy"] = str(sellsy_id)  # Conversion explicite en string
                
            # Suppression du champ "Erreur de synchronisation" qui n'existe pas dans Airtable
            # Au lieu d'utiliser un champ séparé, on peut ajouter le message d'erreur dans un champ de notes existant
            if error_message and status == "Erreur":
                # Utilisons un champ existant pour stocker l'erreur, par exemple "Description" ou créez un champ "Notes"
                fields_to_update["Description"] = f"ERREUR DE SYNC: {error_message}"
            
            print(f"Mise à jour du statut du service {record_id} avec les champs: {fields_to_update}")    
            self.table.update(record_id, fields_to_update)
            print(f"Statut du service {record_id} mis à jour: {status}")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut du service: {e}")
            
    def map_to_sellsy_format(self, airtable_record):
        """
        Transforme un enregistrement Airtable au format attendu par l'API Sellsy
        
        Args:
            airtable_record: Enregistrement récupéré depuis Airtable
            
        Returns:
            dict: Données formatées pour l'API Sellsy
        """
        fields = airtable_record['fields']
        print(f"Mapping du service: {fields.get('Nom du service', 'Service sans nom')}")
        
        # Création du mapping selon la structure de votre table Airtable
        sellsy_data = {
            'name': fields.get('Référence', ''),
            'tradename': fields.get('Nom du service', ''),
            'notes': fields.get('Description', ''),
            'unitAmount': float(fields.get('Prix HT', 0)),
            'unit': fields.get('Unité', 'forfait'),  # Valeur par défaut si non spécifiée
            'active': 'Y' if fields.get('Actif', True) else 'N',  # Corrigé: 'active' au lieu de 'actif'
        }
        
        # Ajout conditionnel du taux de TVA si présent
        if 'Taux TVA' in fields:
            try:
                # Assumons que le taux est stocké comme un nombre
                tax_rate = float(fields.get('Taux TVA', 0))
                sellsy_data['taxrate'] = tax_rate
            except (ValueError, TypeError):
                print(f"Erreur de conversion du taux TVA pour le service {fields.get('Nom du service')}")
        
        # Vérifier si on a déjà un ID Sellsy (pour mise à jour)
        if 'ID Sellsy' in fields and fields['ID Sellsy']:
            sellsy_data['id'] = fields['ID Sellsy']
        
        print(f"Données formatées pour Sellsy: {sellsy_data}")
        return sellsy_data
