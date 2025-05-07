#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime
from airtable_client import AirtableClient
from sellsy_client import SellsyClient

def log_message(message):
    """Affiche un message horodaté"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def sync_service(airtable_client, sellsy_client, service_record):
    """
    Synchronise un service entre Airtable et Sellsy
    
    Args:
        airtable_client: Instance d'AirtableClient
        sellsy_client: Instance de SellsyClient
        service_record: Enregistrement du service depuis Airtable
        
    Returns:
        bool: True si la synchronisation a réussi, False sinon
    """
    record_id = service_record['id']
    fields = service_record['fields']
    service_name = fields.get('Nom du service', 'Service sans nom')
    
    log_message(f"Traitement du service: {service_name}")
    
    try:
        # Convertir l'enregistrement Airtable au format Sellsy
        sellsy_data = airtable_client.map_to_sellsy_format(service_record)
        
        # Vérifier si on a déjà un ID Sellsy (mise à jour) ou s'il faut créer
        if 'id' in sellsy_data and sellsy_data['id']:
            # Mise à jour d'un service existant
            service_id = sellsy_data.pop('id')  # Retirer l'ID des données pour éviter une erreur
            log_message(f"Mise à jour du service Sellsy ID: {service_id}")
            
            if sellsy_client.update_service(service_id, sellsy_data):
                log_message(f"Service mis à jour avec succès: {service_name}")
                airtable_client.update_service_status(record_id, service_id)
                return True
            else:
                error_msg = "Échec de la mise à jour du service dans Sellsy"
                log_message(error_msg)
                airtable_client.update_service_status(record_id, status="Erreur", error_message=error_msg)
                return False
        else:
            # Création d'un nouveau service
            log_message(f"Création d'un nouveau service: {service_name}")
            service_id = sellsy_client.create_service(sellsy_data)
            
            if service_id:
                log_message(f"Service créé avec succès, ID Sellsy: {service_id}")
                # Important: Mise à jour de l'ID Sellsy dans Airtable
                airtable_client.update_service_status(record_id, service_id)
                return True
            else:
                error_msg = "Échec de la création du service dans Sellsy"
                log_message(error_msg)
                airtable_client.update_service_status(record_id, status="Erreur", error_message=error_msg)
                return False
    
    except Exception as e:
        error_msg = f"Erreur lors de la synchronisation du service {service_name}: {str(e)}"
        log_message(error_msg)
        airtable_client.update_service_status(record_id, status="Erreur", error_message=error_msg)
        return False

def main():
    """Fonction principale"""
    log_message("Démarrage de la synchronisation Airtable -> Sellsy")
    
    try:
        # Initialiser les clients
        log_message("Initialisation des clients Airtable et Sellsy")
        airtable_client = AirtableClient()
        sellsy_client = SellsyClient()
        
        # Récupérer les services à synchroniser
        log_message("Récupération des services à synchroniser depuis Airtable")
        services_to_sync = airtable_client.get_services_to_sync()
        
        if not services_to_sync:
            log_message("Aucun service à synchroniser")
            return
        
        log_message(f"Nombre de services à synchroniser: {len(services_to_sync)}")
        
        # Synchroniser chaque service
        success_count = 0
        for service_record in services_to_sync:
            if sync_service(airtable_client, sellsy_client, service_record):
                success_count += 1
            
            # Petite pause pour éviter de surcharger les APIs
            time.sleep(1)
        
        log_message(f"Synchronisation terminée. {success_count}/{len(services_to_sync)} services synchronisés avec succès.")
    
    except Exception as e:
        log_message(f"Erreur critique lors de la synchronisation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
