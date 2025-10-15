# 🔧 Guide de Dépannage - Projet VPN-DNAC

**Version:** 1.0  
**Date:** 2024

---

## 🎯 Objectif

Ce guide vous aide à diagnostiquer et résoudre les problèmes courants rencontrés lors de l'implémentation du projet de réseau hybride sécurisé.

---

## 📊 Matrice de Diagnostic

| Symptôme | Cause Probable | Solution | Priorité |
|----------|----------------|----------|----------|
| Équipements ne démarrent pas | Ressources insuffisantes | Augmenter RAM/CPU | 🔴 Critique |
| Pas de connectivité réseau | Câblage incorrect | Vérifier topologie | 🔴 Critique |
| Tunnel VPN ne se forme pas | Clés/Adresses incorrectes | Vérifier configuration | 🔴 Critique |
| Script Python échoue | Dépendances manquantes | Réinstaller packages | 🟡 Important |
| DNA Center inaccessible | Identifiants incorrects | Vérifier credentials | 🟡 Important |
| Performance dégradée | Charge système élevée | Optimiser ressources | 🟢 Mineur |

---

## 🔴 Problèmes Critiques

### 1. Équipements EVE-NG ne Démarrent Pas

#### Symptômes
- Équipements restent en état "Stopped"
- Messages d'erreur de ressources
- Timeout lors du démarrage

#### Diagnostic
```bash
# Vérifier les ressources système EVE-NG
free -h
df -h
top

# Vérifier les logs EVE-NG
tail -f /opt/unetlab/data/Logs/eve-ng.log
```

#### Solutions
1. **Augmenter les ressources:**
```bash
# Dans EVE-NG, pour chaque équipement:
# RAM: Minimum 1GB par CSR1000v
# CPU: Minimum 2 cores par CSR1000v
# Disque: Minimum 2GB par équipement
```

2. **Redémarrer les services:**
```bash
# Sur le serveur EVE-NG
systemctl restart eve-ng
systemctl restart mysql
```

3. **Nettoyer les ressources:**
```bash
# Arrêter tous les laboratoires inutilisés
# Supprimer les snapshots anciens
# Redémarrer le serveur si nécessaire
```

### 2. Connectivité Réseau Échoue

#### Symptômes
- Ping entre équipements échoue
- Interfaces down
- Pas d'adresses IP

#### Diagnostic
```bash
# Sur chaque routeur
show ip interface brief
show ip route
show arp

# Tester la connectivité
ping <adresse_ip>
traceroute <adresse_ip>
```

#### Solutions
1. **Vérifier le câblage EVE-NG:**
   - Vérifier les connexions physiques
   - S'assurer que les ports sont corrects
   - Redémarrer les équipements après câblage

2. **Vérifier les configurations:**
```bash
# Vérifier les adresses IP
show running-config interface GigabitEthernet0/0

# Vérifier les routes
show ip route

# Vérifier les VLANs (switches)
show vlan brief
```

3. **Configuration manuelle si nécessaire:**
```bash
# Exemple pour un routeur
interface GigabitEthernet0/0
 ip address 203.0.113.2 255.255.255.252
 no shutdown
```

### 3. Tunnel VPN Ne Se Forme Pas

#### Symptômes
- `show crypto ikev2 sa` vide
- `show crypto ipsec sa` vide
- Pas de connectivité inter-sites

#### Diagnostic
```bash
# Vérifier la connectivité publique
ping 203.0.113.2 source 203.0.113.6
ping 203.0.113.6 source 203.0.113.2

# Vérifier la configuration IKEv2
show crypto ikev2 proposal
show crypto ikev2 policy
show crypto ikev2 profile

# Activer les logs de débogage
debug crypto ikev2
debug crypto ipsec
```

#### Solutions
1. **Vérifier la connectivité Internet:**
```bash
# Tester la connectivité entre les routeurs publics
ping 203.0.113.2  # Depuis Branch vers HQ
ping 203.0.113.6  # Depuis HQ vers Branch
```

2. **Vérifier les clés pré-partagées:**
```bash
# Sur HQ-Router
show crypto ikev2 keyring

# Sur Branch-Router
show crypto ikev2 keyring

# Les clés doivent être identiques
```

3. **Vérifier les ACLs:**
```bash
# Vérifier que les ACLs permettent le trafic IKE
show access-lists
show ip access-lists 110
```

4. **Redémarrer le tunnel:**
```bash
# Sur les deux routeurs
clear crypto ikev2 sa
clear crypto ipsec sa

# Le tunnel devrait se reformer automatiquement
```

---

## 🟡 Problèmes Importants

### 4. Script Python d'Automatisation Échoue

#### Symptômes
- Erreur d'importation de modules
- Échec d'authentification DNA Center
- Timeout des requêtes API

#### Diagnostic
```bash
# Vérifier Python et les dépendances
python3 --version
pip3 list | grep requests

# Tester la connectivité DNA Center
curl -k -u devnetuser:Cisco123! https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token
```

#### Solutions
1. **Réinstaller les dépendances:**
```bash
pip3 uninstall requests urllib3 python-dotenv colorama
pip3 install -r requirements.txt
```

2. **Vérifier les identifiants DNA Center:**
```bash
# Éditer config.env
nano config.env

# Vérifier les valeurs:
DNAC_URL=https://sandboxdnac2.cisco.com
DNAC_USERNAME=devnetuser
DNAC_PASSWORD=Cisco123!
```

3. **Tester manuellement l'API:**
```bash
# Test d'authentification
curl -k -X POST \
  https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token \
  -u devnetuser:Cisco123! \
  -H 'Content-Type: application/json'
```

### 5. DNA Center Inaccessible

#### Symptômes
- Timeout de connexion
- Erreur 401 (Non autorisé)
- Erreur 404 (Non trouvé)

#### Diagnostic
```bash
# Tester la connectivité de base
ping sandboxdnac2.cisco.com

# Tester HTTPS
curl -k https://sandboxdnac2.cisco.com

# Vérifier les identifiants
curl -k -u devnetuser:Cisco123! https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token
```

#### Solutions
1. **Vérifier l'accès à la sandbox:**
   - Se reconnecter à Cisco DevNet
   - Relancer la sandbox Catalyst Center
   - Vérifier que la sandbox est active

2. **Mettre à jour les identifiants:**
   - Les identifiants peuvent changer
   - Vérifier dans l'interface DevNet
   - Mettre à jour `config.env`

3. **Vérifier la connectivité réseau:**
```bash
# Tester DNS
nslookup sandboxdnac2.cisco.com

# Tester le port HTTPS
telnet sandboxdnac2.cisco.com 443
```

---

## 🟢 Problèmes Mineurs

### 6. Performance Dégradée

#### Symptômes
- Latence élevée
- Débit réduit
- CPU élevé sur les routeurs

#### Diagnostic
```bash
# Vérifier les performances système
show processes cpu | include crypto
show memory | include crypto
show crypto engine statistics
```

#### Solutions
1. **Optimiser les ressources EVE-NG:**
   - Augmenter la RAM allouée
   - Augmenter le nombre de CPU cores
   - Fermer les applications inutiles

2. **Optimiser les algorithmes VPN:**
```bash
# Utiliser des algorithmes plus légers si nécessaire
crypto ikev2 proposal IKEV2-PROPOSAL
 encryption aes128  # Au lieu de aes256
 integrity sha1     # Au lieu de sha256
```

### 7. Logs Excessifs

#### Symptômes
- Disque plein
- Logs très volumineux
- Performance dégradée

#### Solutions
```bash
# Nettoyer les logs sur EVE-NG
rm -f /opt/unetlab/data/Logs/*.log

# Configurer la rotation des logs
echo "logrotate /opt/unetlab/data/Logs/*.log" >> /etc/logrotate.conf
```

---

## 🔍 Commandes de Diagnostic Avancées

### Diagnostic Réseau Complet
```bash
# Script de diagnostic automatique
#!/bin/bash
echo "=== DIAGNOSTIC RÉSEAU COMPLET ==="

echo "1. État des interfaces:"
show ip interface brief

echo "2. Table de routage:"
show ip route

echo "3. ARP Table:"
show arp

echo "4. Connectivité:"
ping 8.8.8.8
ping 192.168.1.1
ping 192.168.2.1

echo "5. État VPN:"
show crypto ikev2 sa
show crypto ipsec sa
```

### Diagnostic VPN Détaillé
```bash
# Script de diagnostic VPN
#!/bin/bash
echo "=== DIAGNOSTIC VPN DÉTAILLÉ ==="

echo "1. État IKEv2:"
show crypto ikev2 sa detail

echo "2. État IPsec:"
show crypto ipsec sa detail

echo "3. Statistiques:"
show crypto engine statistics
show crypto ikev2 stats

echo "4. Configuration:"
show crypto ikev2 proposal
show crypto ikev2 policy
show crypto ikev2 profile
```

### Diagnostic DNA Center
```bash
# Script de diagnostic DNA Center
#!/bin/bash
echo "=== DIAGNOSTIC DNA CENTER ==="

echo "1. Connectivité:"
curl -k -s -o /dev/null -w "%{http_code}" https://sandboxdnac2.cisco.com

echo "2. Authentification:"
curl -k -u devnetuser:Cisco123! https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token

echo "3. API Test:"
curl -k -H "X-Auth-Token: $TOKEN" https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-device
```

---

## 📞 Support et Ressources

### Ressources Officielles
- **Cisco DevNet:** https://developer.cisco.com/
- **EVE-NG Documentation:** https://www.eve-ng.net/
- **DNA Center API:** https://developer.cisco.com/docs/dna-center/

### Communautés
- **Cisco Learning Network:** https://learningnetwork.cisco.com/
- **EVE-NG Community:** https://www.eve-ng.net/community/
- **Stack Overflow:** Tag `cisco`, `eve-ng`, `vpn`

### Contact Support
- **Cisco DevNet Support:** Via le portail DevNet
- **EVE-NG Support:** Via leur forum communautaire

---

## 📝 Journal de Dépannage

Tenez un journal des problèmes rencontrés et des solutions appliquées:

```
Date: 2024-XX-XX
Problème: Tunnel VPN ne se forme pas
Cause: Clé pré-partagée incorrecte
Solution: Vérification et correction de la clé dans config.env
Résultat: Tunnel opérationnel
Temps de résolution: 30 minutes
```

---

*Guide de dépannage technique - 2024*
