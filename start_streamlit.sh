#!/bin/bash

# Script de lancement Streamlit - Projet VPN-DNAC
# Description: Lancement du dashboard web interactif

set -e

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Vérifier si Python est installé
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 n'est pas installé"
        exit 1
    fi
    
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version détecté"
}

# Vérifier si Streamlit est installé
check_streamlit() {
    if ! python3 -c "import streamlit" 2>/dev/null; then
        print_warning "Streamlit n'est pas installé. Installation en cours..."
        pip3 install -r requirements.txt
    else
        print_success "Streamlit est installé"
    fi
}

# Vérifier la configuration
check_config() {
    if [ ! -f "config.env" ]; then
        print_warning "Fichier config.env non trouvé. Création d'un fichier par défaut..."
        cat > config.env << 'EOF'
# Configuration du Projet VPN-DNAC
HQ_PUBLIC_IP=203.0.113.10
BRANCH_PUBLIC_IP=203.0.113.20
INTERNET_ROUTER_IP=203.0.113.1
HQ_LOCAL_NETWORK=192.168.1.0/24
BRANCH_LOCAL_NETWORK=192.168.2.0/24
IKEV2_PSK=VpnSecretKey2024!
IKEV2_ENCRYPTION=aes256
IKEV2_HASH=sha256
IKEV2_DH_GROUP=14
DNAC_URL=https://sandboxdnac2.cisco.com
DNAC_USERNAME=devnetuser
DNAC_PASSWORD=Cisco123!
SSH_PORT=22
HTTP_PORT=80
HTTPS_PORT=443
EOF
        print_success "Fichier config.env créé"
    else
        print_success "Configuration trouvée"
    fi
}

# Lancer Streamlit
launch_streamlit() {
    print_status "Lancement du dashboard Streamlit..."
    print_status "URL d'accès: http://localhost:8501"
    print_status "Appuyez sur Ctrl+C pour arrêter le serveur"
    echo
    
    # Lancer Streamlit
    streamlit run streamlit_app/app.py \
        --server.port 8501 \
        --server.address localhost \
        --browser.gatherUsageStats false \
        --theme.base light \
        --theme.primaryColor "#1f77b4" \
        --theme.backgroundColor "#ffffff" \
        --theme.secondaryBackgroundColor "#f0f2f6"
}

# Fonction principale
main() {
    echo "=========================================="
    echo "  DASHBOARD STREAMLIT - Projet VPN-DNAC"
    echo "=========================================="
    echo
    
    check_python
    check_streamlit
    check_config
    
    echo
    print_success "Préparation terminée !"
    print_status "Fonctionnalités disponibles:"
    echo "  📊 Dashboard principal avec métriques en temps réel"
    echo "  🔐 Monitoring VPN avec visualisations"
    echo "  🤖 Interface DNA Center interactive"
    echo "  ⚙️ Gestionnaire de configurations"
    echo "  📈 Analytics et rapports"
    echo
    
    launch_streamlit
}

# Gestion des signaux
trap 'echo; print_status "Arrêt du serveur Streamlit..."; exit 0' INT

# Exécution du script
main "$@"

