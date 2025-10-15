# 📖 Guide d'Installation - Projet VPN-DNAC

**Version:** 1.0  
**Date:** 2024

---

## 🎯 Objectif

Ce guide vous accompagne étape par étape dans l'installation et la configuration du projet de réseau hybride sécurisé avec VPN IPsec et automatisation Cisco DNA Center.

---

## 📋 Prérequis

### Matériel Requis
- **Machine virtuelle** ou serveur avec minimum 8GB RAM
- **4 CPU cores** minimum
- **50GB d'espace disque** libre
- **Accès Internet** stable

### Logiciels Requis
- **EVE-NG Pro** ou **Cisco CML** (version récente)
- **Python 3.8+** avec pip
- **Navigateur web** moderne
- **Client SSH** (PuTTY, OpenSSH, etc.)

### Accès Requis
- **Cisco DevNet Account** (gratuit)
- **Accès à la sandbox** Catalyst Center Always-On

---

## 🚀 Installation Étape par Étape

### Étape 1: Préparation de l'Environnement

#### 1.1 Vérification du Système

```bash
# Vérifier la version de Python
python3 --version
# Résultat attendu: Python 3.8.x ou supérieur

# Vérifier pip
pip3 --version
# Résultat attendu: pip 21.x.x ou supérieur

# Vérifier Git (optionnel)
git --version
```

#### 1.2 Création du Répertoire de Travail

```bash
# Créer le répertoire principal
mkdir -p ~/projets_plan/vpn-dnac-hybrid-network
cd ~/projets_plan/vpn-dnac-hybrid-network

# Vérifier la structure
ls -la
```

### Étape 2: Configuration EVE-NG

#### 2.1 Accès à EVE-NG

```bash
# Tester la connectivité EVE-NG
ping <IP_EVE_NG>
# Remplacez <IP_EVE_NG> par l'adresse IP de votre serveur EVE-NG

# Connexion SSH (optionnel)
ssh root@<IP_EVE_NG>
```

#### 2.2 Création du Projet

1. **Ouvrir EVE-NG** dans votre navigateur
2. **Se connecter** avec vos identifiants
3. **Créer un nouveau laboratoire:**
   - Nom: `Projet_VPN_DNAC`
   - Description: `Réseau hybride sécurisé avec VPN IPsec`
   - Type: `Network`

#### 2.3 Ajout des Équipements

Ajoutez les équipements suivants dans l'ordre:

| Équipement | Type | Nom | Image Requise |
|------------|------|-----|---------------|
| Routeur 1 | CSR1000v | HQ-Router | csr1000v |
| Routeur 2 | CSR1000v | Branch-Router | csr1000v |
| Routeur 3 | CSR1000v | Internet-Router | csr1000v |
| Switch 1 | vIOS-L2 | HQ-Switch | viosl2 |
| Switch 2 | vIOS-L2 | Branch-Switch | viosl2 |
| PC 1 | vPC | HQ-PC | vpc |
| PC 2 | vPC | Branch-PC | vpc |

#### 2.4 Câblage de la Topologie

Connectez les équipements selon le schéma:

```
HQ-Router:Gi0/0 ←→ Internet-Router:Gi0/0
HQ-Router:Gi0/1 ←→ HQ-Switch:Gi0/1
Branch-Router:Gi0/0 ←→ Internet-Router:Gi0/1
Branch-Router:Gi0/1 ←→ Branch-Switch:Gi0/1
HQ-PC:Eth0 ←→ HQ-Switch:Gi0/2
Branch-PC:Eth0 ←→ Branch-Switch:Gi0/2
```

### Étape 3: Configuration Automatique

#### 3.1 Lancement des Scripts

```bash
# Rendre les scripts exécutables
chmod +x scripts/*.sh

# Configuration initiale
./scripts/setup-lab.sh
```

#### 3.2 Installation des Dépendances

```bash
# Installation automatique des dépendances Python
pip3 install -r requirements.txt

# Vérification de l'installation
python3 -c "import requests, colorama; print('Dépendances installées avec succès')"
```

### Étape 4: Configuration Réseau

#### 4.1 Application des Configurations

```bash
# Générer les configurations
./scripts/configure-network.sh

# Vérifier la création des fichiers
ls -la configurations/routers/
ls -la configurations/switches/
```

#### 4.2 Application Manuelle aux Équipements

1. **Démarrer tous les équipements** dans EVE-NG
2. **Se connecter à chaque équipement** via console
3. **Appliquer les configurations** fichier par fichier:

```bash
# Pour HQ-Router
copy tftp://<IP_SERVEUR>/hq-router.cfg running-config

# Pour Branch-Router
copy tftp://<IP_SERVEUR>/branch-router.cfg running-config

# Pour Internet-Router
copy tftp://<IP_SERVEUR>/internet-router.cfg running-config
```

### Étape 5: Validation Réseau de Base

#### 5.1 Tests de Connectivité

```bash
# Tester la connectivité publique
ping 203.0.113.2  # Depuis Internet-Router vers HQ-Router
ping 203.0.113.6  # Depuis Internet-Router vers Branch-Router

# Tester la connectivité locale
ping 192.168.1.10  # Depuis HQ-Router vers HQ-PC
ping 192.168.2.10  # Depuis Branch-Router vers Branch-PC
```

#### 5.2 Validation des PC Virtuels

```bash
# Configuration HQ-PC
ip 192.168.1.10 255.255.255.0 192.168.1.1
ip dns 8.8.8.8
save

# Configuration Branch-PC
ip 192.168.2.10 255.255.255.0 192.168.2.1
ip dns 8.8.8.8
save
```

### Étape 6: Configuration VPN

#### 6.1 Génération des Configurations VPN

```bash
# Générer les configurations VPN
./scripts/setup-vpn.sh

# Vérifier la création
ls -la configurations/vpn/
```

#### 6.2 Application des Configurations VPN

1. **Appliquer sur HQ-Router:**
```bash
copy tftp://<IP_SERVEUR>/hq-router-vpn.cfg running-config
```

2. **Appliquer sur Branch-Router:**
```bash
copy tftp://<IP_SERVEUR>/branch-router-vpn.cfg running-config
```

#### 6.3 Validation du Tunnel VPN

```bash
# Vérifier l'état du tunnel
show crypto ikev2 sa
show crypto ipsec sa

# Tester la connectivité inter-sites
ping 192.168.2.10 source 192.168.1.1  # Depuis HQ vers Branch
ping 192.168.1.10 source 192.168.2.1  # Depuis Branch vers HQ
```

### Étape 7: Automatisation DNA Center

#### 7.1 Accès à la Sandbox DevNet

1. **Se connecter à Cisco DevNet:**
   - URL: https://devnetsandbox.cisco.com
   - Créer un compte gratuit si nécessaire

2. **Lancer la sandbox Catalyst Center:**
   - Rechercher: "Catalyst Center Always-On"
   - Cliquer sur "Reserve"
   - Noter les identifiants fournis

#### 7.2 Configuration des Identifiants

```bash
# Éditer le fichier de configuration
nano config.env

# Mettre à jour les identifiants DNA Center
DNAC_URL=https://sandboxdnac2.cisco.com
DNAC_USERNAME=devnetuser
DNAC_PASSWORD=Cisco123!
```

#### 7.3 Exécution de l'Automatisation

```bash
# Exécuter le script d'automatisation
cd automation
python3 dnac_automation.py

# Vérifier les résultats
ls -la ../logs/
```

---

## 🔍 Validation Finale

### Tests Complets

```bash
# Script de validation complet
./scripts/validate-vpn.sh

# Tests manuels
ping 192.168.2.10  # Depuis HQ-PC vers Branch-PC
ping 192.168.1.10  # Depuis Branch-PC vers HQ-PC
```

### Vérifications Système

```bash
# Vérifier l'état de tous les équipements
show version  # Sur chaque routeur
show ip interface brief  # Sur chaque équipement
show vlan brief  # Sur chaque switch
```

---

## 🛠️ Dépannage

### Problèmes Courants

#### 1. Équipements ne démarrent pas
- **Cause:** Ressources insuffisantes
- **Solution:** Augmenter RAM/CPU dans EVE-NG

#### 2. Connectivité réseau échoue
- **Cause:** Câblage incorrect
- **Solution:** Vérifier les connexions dans EVE-NG

#### 3. VPN ne se forme pas
- **Cause:** Clés ou adresses IP incorrectes
- **Solution:** Vérifier `config.env` et reconfigurer

#### 4. Script Python échoue
- **Cause:** Dépendances manquantes
- **Solution:** `pip3 install -r requirements.txt`

### Commandes de Diagnostic

```bash
# Diagnostic réseau
show ip route
show arp
show interfaces status

# Diagnostic VPN
show crypto ikev2 sa
show crypto ipsec sa
debug crypto ikev2

# Diagnostic Python
python3 -c "import sys; print(sys.version)"
python3 -c "import requests; print('OK')"
```

---

## ✅ Checklist de Validation

- [ ] **EVE-NG** accessible et fonctionnel
- [ ] **Tous les équipements** démarrés
- [ ] **Câblage** correct selon la topologie
- [ ] **Configurations réseau** appliquées
- [ ] **Connectivité publique** fonctionnelle
- [ ] **Connectivité locale** fonctionnelle
- [ ] **Tunnel VPN** actif et fonctionnel
- [ ] **Connectivité inter-sites** via VPN
- [ ] **Script DNA Center** exécuté avec succès
- [ ] **Logs** générés et consultables
- [ ] **Documentation** complète et à jour

---

## 🎉 Félicitations !

Si tous les éléments de la checklist sont validés, votre projet de réseau hybride sécurisé est opérationnel !

Vous pouvez maintenant:
- **Documenter** vos résultats avec des captures d'écran
- **Créer un dépôt GitHub** pour votre portfolio
- **Explorer** les fonctionnalités avancées de DNA Center
- **Expérimenter** avec d'autres technologies d'automatisation

---

*Guide technique - 2024*
