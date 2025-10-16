#!/usr/bin/env python3
"""
Utilitaire API DNA Center
Description: Gestion des appels API vers Cisco DNA Center
"""

import requests
import json
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Supprimer les avertissements SSL pour les environnements de lab
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class DNACClient:
    """Client pour l'API Cisco DNA Center"""
    
    def __init__(self, base_url, username, password):
        """
        Initialiser le client DNA Center
        
        Args:
            base_url (str): URL de base du DNA Center
            username (str): Nom d'utilisateur
            password (str): Mot de passe
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.session = requests.Session()
        self.session.verify = False  # Pour les environnements de lab uniquement
    
    def authenticate(self):
        """Authentification auprès du DNA Center"""
        auth_url = f"{self.base_url}/dna/system/api/v1/auth/token"
        
        try:
            response = self.session.post(
                auth_url,
                auth=HTTPBasicAuth(self.username, self.password),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                self.token = response.json()['Token']
                self.session.headers.update({
                    'X-Auth-Token': self.token,
                    'Content-Type': 'application/json'
                })
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Erreur d'authentification: {str(e)}")
            return False
    
    def get_network_devices(self):
        """Récupérer la liste des équipements réseau"""
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération des équipements: {str(e)}")
            return None
    
    def get_network_health(self):
        """Récupérer l'état de santé du réseau"""
        url = f"{self.base_url}/dna/intent/api/v1/network-health"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération de la santé: {str(e)}")
            return None
    
    def get_client_health(self):
        """Récupérer l'état de santé des clients"""
        url = f"{self.base_url}/dna/intent/api/v1/client-health"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()['response']
            else:
                return None
                
        except Exception as e:
            print(f"Erreur lors de la récupération de la santé des clients: {str(e)}")
            return None

def get_dnac_client():
    """Créer et authentifier un client DNA Center"""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.env')
    
    if os.path.exists(config_path):
        load_dotenv(config_path)
        
        base_url = os.getenv('DNAC_URL', 'https://sandboxdnac2.cisco.com')
        username = os.getenv('DNAC_USERNAME', 'devnetuser')
        password = os.getenv('DNAC_PASSWORD', 'Cisco123!')
        
        client = DNACClient(base_url, username, password)
        
        if client.authenticate():
            return client
        else:
            return None
    else:
        return None

def simulate_dnac_data():
    """Simuler les données DNA Center pour les tests"""
    return {
        'devices': [
            {
                'hostname': 'HQ-Router',
                'type': 'Cisco CSR1000v',
                'managementIpAddress': '203.0.113.2',
                'reachabilityStatus': 'Reachable',
                'softwareVersion': '16.12.04',
                'macAddress': '00:50:56:12:34:56'
            },
            {
                'hostname': 'Branch-Router',
                'type': 'Cisco CSR1000v',
                'managementIpAddress': '203.0.113.6',
                'reachabilityStatus': 'Reachable',
                'softwareVersion': '16.12.04',
                'macAddress': '00:50:56:12:34:57'
            },
            {
                'hostname': 'HQ-Switch',
                'type': 'Cisco vIOS-L2',
                'managementIpAddress': '192.168.1.1',
                'reachabilityStatus': 'Reachable',
                'softwareVersion': '15.2(4)S',
                'macAddress': '00:50:56:12:34:58'
            },
            {
                'hostname': 'Branch-Switch',
                'type': 'Cisco vIOS-L2',
                'managementIpAddress': '192.168.2.1',
                'reachabilityStatus': 'Reachable',
                'softwareVersion': '15.2(4)S',
                'macAddress': '00:50:56:12:34:59'
            }
        ],
        'network_health': {
            'overallHealthScore': 98.5,
            'connectivity': 98.5,
            'performance': 95.2,
            'security': 99.1,
            'availability': 99.8
        },
        'client_health': {
            'totalClients': 15,
            'healthyClients': 14,
            'unhealthyClients': 1,
            'healthScore': 93.3
        }
    }


