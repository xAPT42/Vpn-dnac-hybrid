#!/bin/bash

# Script de configuration du laboratoire VPN-DNAC
# Description: Configuration automatique de l'environnement de laboratoire

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage avec couleur
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier si EVE-NG est accessible
check_eve_ng() {
    print_status "Vérification de l'accès à EVE-NG..."
    
    if ! command -v telnet &> /dev/null; then
        print_error "Telnet n'est pas installé. Installation en cours..."
        sudo apt update && sudo apt install -y telnet
    fi
    
    # Test de connexion EVE-NG (ajustez l'IP selon votre configuration)
    EVE_NG_IP="192.168.1.100"  # À modifier selon votre environnement
    
    if ping -c 1 $EVE_NG_IP &> /dev/null; then
        print_success "EVE-NG est accessible sur $EVE_NG_IP"
    else
        print_warning "EVE-NG n'est pas accessible sur $EVE_NG_IP"
        print_status "Veuillez ajuster l'IP dans le script ou vérifier la connectivité"
    fi
}

# Créer les répertoires de travail
setup_directories() {
    print_status "Création des répertoires de travail..."
    
    mkdir -p screenshots/{eve-ng,configurations,automation}
    mkdir -p configurations/{routers,switches,validation}
    mkdir -p logs
    
    print_success "Répertoires créés avec succès"
}

# Installer les dépendances Python
install_python_deps() {
    print_status "Installation des dépendances Python..."
    
    if [ ! -f requirements.txt ]; then
        cat > requirements.txt << EOF
requests==2.31.0
urllib3==2.0.7
python-dotenv==1.0.0
colorama==0.4.6
tabulate==0.9.0
EOF
    fi
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
        print_success "Dépendances Python installées"
    else
        print_error "Python3/pip3 n'est pas installé"
        exit 1
    fi
}

# Créer le fichier de configuration pour EVE-NG
create_eve_config() {
    print_status "Création de la configuration EVE-NG..."
    
    cat > configurations/eve-ng-topology.txt << 'EOF'
# Topologie EVE-NG - Projet VPN-DNAC
# 
# Équipements à créer:
# 1. HQ-Router (Cisco CSR1000v)
# 2. Branch-Router (Cisco CSR1000v)  
# 3. Internet-Router (Cisco CSR1000v)
# 4. HQ-Switch (Cisco vIOS-L2)
# 5. Branch-Switch (Cisco vIOS-L2)
# 6. HQ-PC (vPC)
# 7. Branch-PC (vPC)

# Câblage:
# HQ-Router:Gi0/0 <-> Internet-Router:Gi0/0
# Branch-Router:Gi0/0 <-> Internet-Router:Gi0/1
# HQ-Router:Gi0/1 <-> HQ-Switch:Gi0/1
# Branch-Router:Gi0/1 <-> Branch-Switch:Gi0/1
# HQ-PC:Eth0 <-> HQ-Switch:Gi0/2
# Branch-PC:Eth0 <-> Branch-Switch:Gi0/2

# Adresses IP:
# Internet-Router:Gi0/0: 203.0.113.1/30
# Internet-Router:Gi0/1: 203.0.113.5/30
# HQ-Router:Gi0/0: 203.0.113.2/30
# HQ-Router:Gi0/1: 192.168.1.1/24
# Branch-Router:Gi0/0: 203.0.113.6/30
# Branch-Router:Gi0/1: 192.168.2.1/24
# HQ-PC: 192.168.1.10/24 (GW: 192.168.1.1)
# Branch-PC: 192.168.2.10/24 (GW: 192.168.2.1)
EOF

    print_success "Configuration EVE-NG créée dans configurations/eve-ng-topology.txt"
}

# Fonction principale
main() {
    echo "=========================================="
    echo "  Configuration du Laboratoire VPN-DNAC"
    echo "=========================================="
    echo
    
    setup_directories
    install_python_deps
    create_eve_config
    check_eve_ng
    
    echo
    print_success "Configuration du laboratoire terminée !"
    print_status "Prochaines étapes:"
    echo "  1. Ouvrir EVE-NG et créer le projet 'Projet_VPN_DNAC'"
    echo "  2. Placer les équipements selon configurations/eve-ng-topology.txt"
    echo "  3. Exécuter: ./scripts/configure-network.sh"
    echo
}

# Exécution du script
main "$@"
