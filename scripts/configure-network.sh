#!/bin/bash

# Script de configuration réseau automatique

# Description: Configuration des routeurs et switches pour le projet VPN-DNAC

set -e

# Charger les variables d'environnement
source ../config.env

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

# Configuration du routeur Internet
configure_internet_router() {
    print_status "Configuration du routeur Internet..."
    
    cat > ../configurations/routers/internet-router.cfg << EOF
! Configuration Internet-Router
! Auteur: Tudy Gbaguidi

hostname Internet-Router

! Configuration des interfaces
interface GigabitEthernet0/0
 description Link to HQ-Router
 ip address $INTERNET_ROUTER_IP 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 description Link to Branch-Router
 ip address 203.0.113.5 255.255.255.252
 no shutdown

! Routage statique
ip route 203.0.113.2 255.255.255.255 GigabitEthernet0/0
ip route 203.0.113.6 255.255.255.255 GigabitEthernet0/1

! Configuration SSH
ip domain-name vpn-dnac.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin123
line vty 0 4
 login local
 transport input ssh

! Configuration NTP
ntp server pool.ntp.org

end
EOF

    print_success "Configuration Internet-Router créée"
}

# Configuration du routeur HQ
configure_hq_router() {
    print_status "Configuration du routeur HQ..."
    
    cat > ../configurations/routers/hq-router.cfg << EOF
! Configuration HQ-Router
! Auteur: Tudy Gbaguidi

hostname HQ-Router

! Configuration des interfaces
interface GigabitEthernet0/0
 description Link to Internet-Router
 ip address 203.0.113.2 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 description Link to HQ-Switch (Local Network)
 ip address 192.168.1.1 255.255.255.0
 no shutdown

! Routage de base
ip route 0.0.0.0 0.0.0.0 203.0.113.1

! Configuration NAT pour accès Internet
access-list 100 permit ip 192.168.1.0 0.0.0.255 any
interface GigabitEthernet0/0
 ip nat outside
interface GigabitEthernet0/1
 ip nat inside
ip nat inside source list 100 interface GigabitEthernet0/0 overload

! Configuration SSH
ip domain-name hq.vpn-dnac.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin123
line vty 0 4
 login local
 transport input ssh

! Configuration NTP
ntp server 203.0.113.1

end
EOF

    print_success "Configuration HQ-Router créée"
}

# Configuration du routeur Branch
configure_branch_router() {
    print_status "Configuration du routeur Branch..."
    
    cat > ../configurations/routers/branch-router.cfg << EOF
! Configuration Branch-Router
! Auteur: Tudy Gbaguidi

hostname Branch-Router

! Configuration des interfaces
interface GigabitEthernet0/0
 description Link to Internet-Router
 ip address 203.0.113.6 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 description Link to Branch-Switch (Local Network)
 ip address 192.168.2.1 255.255.255.0
 no shutdown

! Routage de base
ip route 0.0.0.0 0.0.0.0 203.0.113.5

! Configuration NAT pour accès Internet
access-list 100 permit ip 192.168.2.0 0.0.0.255 any
interface GigabitEthernet0/0
 ip nat outside
interface GigabitEthernet0/1
 ip nat inside
ip nat inside source list 100 interface GigabitEthernet0/0 overload

! Configuration SSH
ip domain-name branch.vpn-dnac.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin123
line vty 0 4
 login local
 transport input ssh

! Configuration NTP
ntp server 203.0.113.5

end
EOF

    print_success "Configuration Branch-Router créée"
}

# Configuration des switches
configure_switches() {
    print_status "Configuration des switches..."
    
    # HQ-Switch
    cat > ../configurations/switches/hq-switch.cfg << EOF
! Configuration HQ-Switch
! Auteur: Tudy Gbaguidi

hostname HQ-Switch

! Configuration des VLANs
vlan 10
 name HQ-Users

! Configuration des interfaces
interface GigabitEthernet0/1
 description Uplink to HQ-Router
 switchport mode trunk
 no shutdown

interface GigabitEthernet0/2
 description HQ-PC Connection
 switchport access vlan 10
 no shutdown

interface range GigabitEthernet0/3-10
 description Available ports for HQ users
 switchport access vlan 10
 no shutdown

! Configuration SSH
ip domain-name hq-switch.vpn-dnac.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin123
line vty 0 4
 login local
 transport input ssh

end
EOF

    # Branch-Switch
    cat > ../configurations/switches/branch-switch.cfg << EOF
! Configuration Branch-Switch
! Auteur: Tudy Gbaguidi

hostname Branch-Switch

! Configuration des VLANs
vlan 20
 name Branch-Users

! Configuration des interfaces
interface GigabitEthernet0/1
 description Uplink to Branch-Router
 switchport mode trunk
 no shutdown

interface GigabitEthernet0/2
 description Branch-PC Connection
 switchport access vlan 20
 no shutdown

interface range GigabitEthernet0/3-10
 description Available ports for Branch users
 switchport access vlan 20
 no shutdown

! Configuration SSH
ip domain-name branch-switch.vpn-dnac.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret admin123
line vty 0 4
 login local
 transport input ssh

end
EOF

    print_success "Configurations des switches créées"
}

# Configuration des PC virtuels
configure_pcs() {
    print_status "Configuration des PC virtuels..."
    
    # HQ-PC
    cat > ../configurations/pc-configs/hq-pc.cfg << EOF
# Configuration HQ-PC
# Auteur: Tudy Gbaguidi

# Configuration réseau
ip 192.168.1.10 255.255.255.0 192.168.1.1
ip dns 8.8.8.8
save
EOF

    # Branch-PC
    cat > ../configurations/pc-configs/branch-pc.cfg << EOF
# Configuration Branch-PC
# Auteur: Tudy Gbaguidi

# Configuration réseau
ip 192.168.2.10 255.255.255.0 192.168.2.1
ip dns 8.8.8.8
save
EOF

    print_success "Configurations des PC créées"
}

# Fonction principale
main() {
    echo "=========================================="
    echo "  Configuration Réseau - Projet VPN-DNAC"
    echo "  Auteur: Tudy Gbaguidi"
    echo "=========================================="
    echo
    
    configure_internet_router
    configure_hq_router
    configure_branch_router
    configure_switches
    configure_pcs
    
    echo
    print_success "Toutes les configurations réseau ont été créées !"
    print_status "Prochaines étapes:"
    echo "  1. Appliquer les configurations aux équipements EVE-NG"
    echo "  2. Tester la connectivité de base"
    echo "  3. Exécuter: ./scripts/setup-vpn.sh"
    echo
}

# Exécution du script
main "$@"
