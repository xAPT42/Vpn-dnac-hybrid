#!/usr/bin/env python3
"""
Script d'automatisation Cisco DNA Center
Description: Interaction avec l'API Cisco DNA Center pour la gestion réseau
"""

import requests
import json
import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import colorama
from colorama import Fore, Back, Style

# Supprimer les avertissements SSL pour les environnements de lab
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
colorama.init()

class DNACAutomation:
    """Classe pour l'automatisation Cisco DNA Center"""
    
    def __init__(self, base_url, username, password):
        """
        Initialisation de la classe DNAC
        
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
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Authentification auprès de DNA Center...")
        
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
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Authentification réussie !")
                return True
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Échec de l'authentification: {response.status_code}")
                print(f"Réponse: {response.text}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur lors de l'authentification: {str(e)}")
            return False
    
    def get_network_devices(self):
        """Récupérer la liste des équipements réseau"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Récupération de la liste des équipements...")
        
        url = f"{self.base_url}/dna/intent/api/v1/network-device"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                devices = response.json()['response']
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {len(devices)} équipements trouvés")
                return devices
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur lors de la récupération: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {str(e)}")
            return None
    
    def get_device_details(self, device_id):
        """Récupérer les détails d'un équipement spécifique"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Récupération des détails de l'équipement {device_id}...")
        
        url = f"{self.base_url}/dna/intent/api/v1/network-device/{device_id}"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                device = response.json()['response']
                return device
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {str(e)}")
            return None
    
    def get_network_health(self):
        """Récupérer l'état de santé du réseau"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Récupération de l'état de santé du réseau...")
        
        url = f"{self.base_url}/dna/intent/api/v1/network-health"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                health = response.json()['response']
                return health
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {str(e)}")
            return None
    
    def get_client_health(self):
        """Récupérer l'état de santé des clients"""
        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} Récupération de l'état de santé des clients...")
        
        url = f"{self.base_url}/dna/intent/api/v1/client-health"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 200:
                health = response.json()['response']
                return health
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur: {str(e)}")
            return None
    
    def display_devices(self, devices):
        """Afficher la liste des équipements de manière formatée"""
        if not devices:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Aucun équipement trouvé")
            return
        
        print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}LISTE DES ÉQUIPEMENTS RÉSEAU{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
        
        for i, device in enumerate(devices, 1):
            print(f"\n{Fore.YELLOW}[{i}] {device.get('hostname', 'N/A')}{Style.RESET_ALL}")
            print(f"   Type: {device.get('type', 'N/A')}")
            print(f"   Adresse IP: {device.get('managementIpAddress', 'N/A')}")
            print(f"   MAC: {device.get('macAddress', 'N/A')}")
            print(f"   Statut: {device.get('reachabilityStatus', 'N/A')}")
            print(f"   Version: {device.get('softwareVersion', 'N/A')}")
    
    def save_results(self, data, filename):
        """Sauvegarder les résultats dans un fichier JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = f"../logs/{filename}_{timestamp}.json"
        
        os.makedirs(os.path.dirname(full_filename), exist_ok=True)
        
        with open(full_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Résultats sauvegardés dans {full_filename}")

def main():
    """Fonction principale"""
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    AUTOMATISATION CISCO DNA CENTER{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    
    # Charger les variables d'environnement
    load_dotenv('../config.env')
    
    # Configuration DNA Center (Cisco DevNet Sandbox)
    DNAC_URL = os.getenv('DNAC_URL', 'https://sandboxdnac2.cisco.com')
    DNAC_USERNAME = os.getenv('DNAC_USERNAME', 'devnetuser')
    DNAC_PASSWORD = os.getenv('DNAC_PASSWORD', 'Cisco123!')
    
    print(f"\n{Fore.BLUE}[INFO]{Style.RESET_ALL} Configuration:")
    print(f"   URL: {DNAC_URL}")
    print(f"   Utilisateur: {DNAC_USERNAME}")
    
    # Initialiser l'automatisation DNA Center
    dnac = DNACAutomation(DNAC_URL, DNAC_USERNAME, DNAC_PASSWORD)
    
    # Authentification
    if not dnac.authenticate():
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Impossible de se connecter à DNA Center")
        sys.exit(1)
    
    try:
        # Récupérer et afficher les équipements
        devices = dnac.get_network_devices()
        if devices:
            dnac.display_devices(devices)
            dnac.save_results(devices, 'network_devices')
        
        # Récupérer l'état de santé du réseau
        network_health = dnac.get_network_health()
        if network_health:
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}ÉTAT DE SANTÉ DU RÉSEAU{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(json.dumps(network_health, indent=2))
            dnac.save_results(network_health, 'network_health')
        
        # Récupérer l'état de santé des clients
        client_health = dnac.get_client_health()
        if client_health:
            print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}ÉTAT DE SANTÉ DES CLIENTS{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            print(json.dumps(client_health, indent=2))
            dnac.save_results(client_health, 'client_health')
        
        print(f"\n{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Automatisation DNA Center terminée avec succès !")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Interruption par l'utilisateur")
    except Exception as e:
        print(f"\n{Fore.RED}[ERROR]{Style.RESET_ALL} Erreur inattendue: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
