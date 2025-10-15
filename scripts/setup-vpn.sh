#!/bin/bash

# Script de configuration VPN IPsec
# Auteur: Tudy Gbaguidi
# Description: Configuration automatique du tunnel VPN IPsec entre HQ et Branch

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

# Configuration VPN pour HQ-Router
configure_hq_vpn() {
    print_status "Configuration VPN HQ-Router..."
    
    cat > ../configurations/vpn/hq-router-vpn.cfg << EOF
! Configuration VPN HQ-Router
! Auteur: Tudy Gbaguidi

hostname HQ-Router

! Configuration IKEv2 (Phase 1)
crypto ikev2 proposal IKEV2-PROPOSAL
 encryption $IKEV2_ENCRYPTION
 integrity $IKEV2_HASH
 group $IKEV2_DH_GROUP

crypto ikev2 policy IKEV2-POLICY
 proposal IKEV2-PROPOSAL

crypto ikev2 keyring IKEV2-KEYRING
 peer Branch-Router
  address $BRANCH_PUBLIC_IP
  pre-shared-key $IKEV2_PSK

crypto ikev2 profile IKEV2-PROFILE
 match identity remote address $BRANCH_PUBLIC_IP
 authentication remote pre-share
 authentication local pre-share
 keyring local IKEV2-KEYRING

! Configuration IPsec (Phase 2)
crypto ipsec transform-set ESP-TRANSFORM-SET esp-$IKEV2_ENCRYPTION esp-$IKEV2_HASH
 mode tunnel

crypto ipsec profile IPSEC-PROFILE
 set transform-set ESP-TRANSFORM-SET
 set ikev2-profile IKEV2-PROFILE

! Interface Tunnel
interface Tunnel0
 ip address 10.0.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination $BRANCH_PUBLIC_IP
 tunnel protection ipsec profile IPSEC-PROFILE
 no shutdown

! ACL pour le trafic intéressant
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255

! Routage pour le tunnel
ip route 192.168.2.0 255.255.255.0 Tunnel0

end
EOF

    print_success "Configuration VPN HQ-Router créée"
}

# Configuration VPN pour Branch-Router
configure_branch_vpn() {
    print_status "Configuration VPN Branch-Router..."
    
    cat > ../configurations/vpn/branch-router-vpn.cfg << EOF
! Configuration VPN Branch-Router
! Auteur: Tudy Gbaguidi

hostname Branch-Router

! Configuration IKEv2 (Phase 1)
crypto ikev2 proposal IKEV2-PROPOSAL
 encryption $IKEV2_ENCRYPTION
 integrity $IKEV2_HASH
 group $IKEV2_DH_GROUP

crypto ikev2 policy IKEV2-POLICY
 proposal IKEV2-PROPOSAL

crypto ikev2 keyring IKEV2-KEYRING
 peer HQ-Router
  address $HQ_PUBLIC_IP
  pre-shared-key $IKEV2_PSK

crypto ikev2 profile IKEV2-PROFILE
 match identity remote address $HQ_PUBLIC_IP
 authentication remote pre-share
 authentication local pre-share
 keyring local IKEV2-KEYRING

! Configuration IPsec (Phase 2)
crypto ipsec transform-set ESP-TRANSFORM-SET esp-$IKEV2_ENCRYPTION esp-$IKEV2_HASH
 mode tunnel

crypto ipsec profile IPSEC-PROFILE
 set transform-set ESP-TRANSFORM-SET
 set ikev2-profile IKEV2-PROFILE

! Interface Tunnel
interface Tunnel0
 ip address 10.0.0.2 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination $HQ_PUBLIC_IP
 tunnel protection ipsec profile IPSEC-PROFILE
 no shutdown

! ACL pour le trafic intéressant
access-list 110 permit ip 192.168.2.0 0.0.0.255 192.168.1.0 0.0.0.255

! Routage pour le tunnel
ip route 192.168.1.0 255.255.255.0 Tunnel0

end
EOF

    print_success "Configuration VPN Branch-Router créée"
}

# Script de validation du VPN
create_vpn_validation() {
    print_status "Création du script de validation VPN..."
    
    cat > ../scripts/validate-vpn.sh << 'EOF'
#!/bin/bash

# Script de validation du tunnel VPN
# Auteur: Tudy Gbaguidi

# Couleurs
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

echo "=========================================="
echo "  Validation du Tunnel VPN IPsec"
echo "  Auteur: Tudy Gbaguidi"
echo "=========================================="
echo

print_status "Tests de validation à effectuer:"
echo "1. Ping entre HQ-PC (192.168.1.10) et Branch-PC (192.168.2.10)"
echo "2. Vérification du tunnel avec: show crypto ikev2 sa"
echo "3. Vérification des sessions IPsec avec: show crypto ipsec sa"
echo "4. Vérification de la table de routage avec: show ip route"
echo "5. Test de trafic avec: show crypto engine connections active"
echo

print_status "Commandes de validation sur les routeurs:"
echo "HQ-Router:"
echo "  show crypto ikev2 sa"
echo "  show crypto ipsec sa"
echo "  show ip route"
echo "  ping 192.168.2.10 source 192.168.1.1"
echo
echo "Branch-Router:"
echo "  show crypto ikev2 sa"
echo "  show crypto ipsec sa"
echo "  show ip route"
echo "  ping 192.168.1.10 source 192.168.2.1"
echo

print_success "Script de validation créé !"
EOF

    chmod +x ../scripts/validate-vpn.sh
    print_success "Script de validation VPN créé"
}

# Documentation de la configuration VPN
create_vpn_documentation() {
    print_status "Création de la documentation VPN..."
    
    cat > ../documentation/vpn-setup.md << 'EOF'
# Configuration VPN IPsec - Projet VPN-DNAC


## Vue d'ensemble

Ce document décrit la configuration du tunnel VPN IPsec entre le siège (HQ) et la succursale (Branch) du projet VPN-DNAC.

## Architecture VPN

```
HQ (192.168.1.0/24) <---> Tunnel0 (10.0.0.0/30) <---> Branch (192.168.2.0/24)
     |                                                        |
     v                                                        v
HQ-Router (203.0.113.2)                              Branch-Router (203.0.113.6)
     |                                                        |
     v                                                        v
Internet-Router (203.0.113.1)                    Internet-Router (203.0.113.5)
```

## Paramètres de Configuration

### Phase 1 (IKEv2)
- **Algorithme de chiffrement:** AES-256
- **Algorithme d'intégrité:** SHA-256
- **Groupe Diffie-Hellman:** 14
- **Clé pré-partagée:** VpnSecretKey2024!

### Phase 2 (IPsec)
- **Protocole:** ESP
- **Mode:** Tunnel
- **Chiffrement:** AES-256
- **Intégrité:** SHA-256

## Trafic Intéressant

Le tunnel VPN transporte uniquement le trafic entre les réseaux locaux:
- **Source:** 192.168.1.0/24 (HQ)
- **Destination:** 192.168.2.0/24 (Branch)
- **Vice versa**

## Validation

Pour valider le fonctionnement du VPN:

1. **Connectivité de base:** Ping entre HQ-PC et Branch-PC
2. **État du tunnel:** `show crypto ikev2 sa`
3. **Sessions IPsec:** `show crypto ipsec sa`
4. **Routage:** `show ip route`
5. **Trafic actif:** `show crypto engine connections active`

## Dépannage

### Problèmes courants:

1. **Tunnel ne se forme pas:**
   - Vérifier la connectivité Internet entre les routeurs
   - Vérifier les clés pré-partagées
   - Vérifier les ACLs et le routage

2. **Trafic ne passe pas:**
   - Vérifier les routes dans les tables de routage
   - Vérifier les ACLs de trafic intéressant
   - Vérifier l'état des interfaces Tunnel

3. **Performance dégradée:**
   - Vérifier la charge CPU des routeurs
   - Analyser les statistiques de cryptographie
   - Considérer l'optimisation des algorithmes

## Sécurité

- Utiliser des clés pré-partagées fortes
- Implémenter la rotation des clés
- Surveiller les logs de sécurité
- Maintenir les équipements à jour
EOF

    print_success "Documentation VPN créée"
}

# Fonction principale
main() {
    echo "=========================================="
    echo "  Configuration VPN IPsec - Projet VPN-DNAC"
    echo "  Auteur: Tudy Gbaguidi"
    echo "=========================================="
    echo
    
    # Créer le répertoire VPN
    mkdir -p ../configurations/vpn
    mkdir -p ../configurations/pc-configs
    
    configure_hq_vpn
    configure_branch_vpn
    create_vpn_validation
    create_vpn_documentation
    
    echo
    print_success "Configuration VPN terminée !"
    print_status "Prochaines étapes:"
    echo "  1. Appliquer les configurations VPN aux routeurs"
    echo "  2. Exécuter: ./scripts/validate-vpn.sh"
    echo "  3. Tester la connectivité entre HQ-PC et Branch-PC"
    echo "  4. Exécuter: ./scripts/setup-automation.sh"
    echo
}

# Exécution du script
main "$@"
