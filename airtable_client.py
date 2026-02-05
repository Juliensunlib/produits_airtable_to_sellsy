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
                
            # Utilisons un champ dédié pour stocker les erreurs de synchronisation
            # sans modifier la description originale du service
            if error_message and status == "Erreur":
                # Supposons qu'il existe un champ "Message d'erreur" ou créons-le
                fields_to_update["Message d'erreur"] = f"ERREUR DE SYNC: {error_message}"
            
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
            'actif': 'Y' if fields.get('Actif', True) else 'N',  # Utilisation du paramètre 'actif' conformément à la documentation
            'unitAmountIsTaxesFree': 'Y'  # Indique explicitement que le prix est HT (sans taxes)
        }
        
        # Ajout de la quantité si présente
        if 'Quantité' in fields:
            try:
                quantity = int(fields.get('Quantité', 1))
                sellsy_data['qt'] = quantity
            except (ValueError, TypeError):
                print(f"Erreur de conversion de la quantité pour le service {fields.get('Nom du service')}")
                # Valeur par défaut si la conversion échoue
                sellsy_data['qt'] = 1
        else:
            # Valeur par défaut selon la documentation Sellsy
            sellsy_data['qt'] = 1
        
        # Ajout conditionnel du taux de TVA si présent
        if 'Taux TVA' in fields:
            try:
                # Assumons que le taux est stocké comme un nombre
                tax_rate = float(fields.get('Taux TVA', 0))
                sellsy_data['taxrate'] = tax_rate
            except (ValueError, TypeError):
                print(f"Erreur de conversion du taux TVA pour le service {fields.get('Nom du service')}")
        
        # Ajout de la catégorie si elle est présente
        # CORRECTION: Utiliser 'categoryid' directement comme clé pour que SellsyClient ne la modifie pas
        if 'Catégorie' in fields and fields['Catégorie']:
            print(f"Ajout de la catégorie: {fields['Catégorie']}")
            # La valeur sera utilisée pour rechercher l'ID de catégorie dans SellsyClient
            sellsy_data['categoryName'] = fields['Catégorie']  # On stocke le nom pour la conversion ultérieure

            # Ajout automatique du code comptable 628000 pour les abonnements
            if fields['Catégorie'].lower() == 'abonnement':
                sellsy_data['accountingCode'] = '628000'
                print(f"Code comptable 628000 ajouté pour l'abonnement")

        # Vérifier si on a déjà un ID Sellsy (pour mise à jour)
        if 'ID Sellsy' in fields and fields['ID Sellsy']:
            sellsy_data['id'] = fields['ID Sellsy']
        
        print(f"Données formatées pour Sellsy: {sellsy_data}")
        return sellsy_data
