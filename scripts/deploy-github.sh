#!/bin/bash

# Script de déploiement GitHub - Projet VPN-DNAC
# Description: Automatisation du déploiement sur GitHub avec documentation

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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Vérifier si Git est installé
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "Git n'est pas installé. Installation en cours..."
        sudo apt update && sudo apt install -y git
    fi
    print_success "Git est disponible"
}

# Initialiser le dépôt Git
init_repository() {
    print_status "Initialisation du dépôt Git..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Dépôt Git initialisé"
    else
        print_warning "Dépôt Git déjà initialisé"
    fi
}

# Créer le fichier .gitignore
create_gitignore() {
    print_status "Création du fichier .gitignore..."
    
    cat > .gitignore << 'EOF'
# Fichiers de configuration sensibles
config.env
*.key
*.pem
*.p12

# Fichiers de logs
logs/*.log
logs/*.json
*.log

# Fichiers temporaires
*.tmp
*.temp
.DS_Store
Thumbs.db

# Environnements virtuels Python
venv/
env/
.env

# Fichiers de cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# Système
*.pid
*.seed
*.pid.lock

# Fichiers de sauvegarde
*.bak
*.backup
EOF

    print_success "Fichier .gitignore créé"
}

# Préparer les captures d'écran
prepare_screenshots() {
    print_status "Préparation des captures d'écran..."
    
    # Créer des fichiers de démonstration pour les captures d'écran
    mkdir -p screenshots/{eve-ng,configurations,automation}
    
    # Créer des fichiers de démonstration
    cat > screenshots/eve-ng/README.md << 'EOF'
# Captures d'Écran EVE-NG

## Topologie du Projet
Placez ici la capture d'écran de votre topologie EVE-NG montrant:
- Tous les équipements (routeurs, switches, PC)
- Les connexions entre équipements
- Les adresses IP configurées

## État des Équipements
Placez ici les captures d'écran montrant:
- Tous les équipements démarrés
- Les interfaces actives
- Les configurations appliquées
EOF

    cat > screenshots/configurations/README.md << 'EOF'
# Captures d'Écran Configurations

## Validation du Tunnel VPN
Placez ici les captures d'écran des commandes:
- `show crypto ikev2 sa`
- `show crypto ipsec sa`
- `show interfaces tunnel 0`

## Tests de Connectivité
Placez ici les captures d'écran des tests:
- Ping entre HQ-PC et Branch-PC
- Traceroute via le tunnel VPN
- Validation de la connectivité inter-sites
EOF

    cat > screenshots/automation/README.md << 'EOF'
# Captures d'Écran Automatisation

## Exécution du Script DNA Center
Placez ici les captures d'écran montrant:
- L'exécution du script Python
- Les résultats de l'API DNA Center
- Les données récupérées (équipements, santé réseau)

## Interface DNA Center
Placez ici les captures d'écran de:
- L'interface web DNA Center
- Les équipements découverts
- Les dashboards de santé réseau
EOF

    print_success "Structure des captures d'écran préparée"
}

# Créer le fichier de licence
create_license() {
    print_status "Création du fichier de licence..."
    
    cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 Tudy Gbaguidi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

    print_success "Fichier de licence créé"
}

# Créer le fichier de contribution
create_contributing() {
    print_status "Création du fichier CONTRIBUTING.md..."
    
    cat > CONTRIBUTING.md << 'EOF'
# Guide de Contribution - Projet VPN-DNAC

## Comment Contribuer

Nous accueillons les contributions à ce projet ! Voici comment vous pouvez aider :

### Types de Contributions

1. **Signalement de bugs**
2. **Nouvelles fonctionnalités**
3. **Amélioration de la documentation**
4. **Optimisation des scripts**

### Processus de Contribution

1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commit** vos changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer** une Pull Request

### Standards de Code

- Utilisez des commentaires clairs en français
- Respectez l'indentation existante
- Testez vos modifications avant de soumettre
- Documentez les nouvelles fonctionnalités

### Rapport de Bugs

Lors du signalement d'un bug, incluez :
- Description détaillée du problème
- Étapes pour reproduire
- Résultat attendu vs. résultat obtenu
- Environnement (OS, versions, etc.)

### Contact

Pour toute question, contactez Tudy Gbaguidi.

Merci de votre contribution !
EOF

    print_success "Fichier CONTRIBUTING.md créé"
}

# Créer le fichier de changelog
create_changelog() {
    print_status "Création du fichier CHANGELOG.md..."
    
    cat > CHANGELOG.md << 'EOF'
# Changelog - Projet VPN-DNAC

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-XX-XX

### Ajouté
- Configuration complète du laboratoire EVE-NG
- Scripts de configuration automatique pour routeurs et switches
- Implémentation du tunnel VPN IPsec avec IKEv2
- Script d'automatisation Cisco DNA Center
- Documentation complète avec guides d'installation et de dépannage
- Structure modulaire et organisée du projet
- Scripts de validation et de test
- Support pour la déploiement GitHub automatisé

### Sécurité
- Utilisation d'algorithmes de chiffrement robustes (AES-256, SHA-256)
- Configuration sécurisée des clés pré-partagées
- Validation des connexions VPN

### Documentation
- README.md complet avec architecture et instructions
- Guide d'installation détaillé
- Guide de dépannage avec solutions aux problèmes courants
- Documentation technique pour chaque composant

## [0.1.0] - 2024-XX-XX

### Ajouté
- Structure de base du projet
- Configuration initiale des environnements
- Premiers scripts de configuration
EOF

    print_success "Fichier CHANGELOG.md créé"
}

# Effectuer le commit initial
initial_commit() {
    print_status "Préparation du commit initial..."
    
    git add .
    git commit -m "Initial commit: Projet VPN-DNAC - Réseau Hybride Sécurisé

- Configuration complète du laboratoire EVE-NG
- Scripts de configuration automatique
- Tunnel VPN IPsec avec IKEv2
- Automatisation Cisco DNA Center
- Documentation complète
- Structure modulaire et organisée

Auteur: Tudy Gbaguidi
Date: $(date '+%Y-%m-%d')"
    
    print_success "Commit initial effectué"
}

# Afficher les instructions pour GitHub
show_github_instructions() {
    print_success "Projet prêt pour GitHub !"
    
    echo
    echo "=========================================="
    echo "  INSTRUCTIONS POUR GITHUB"
    echo "=========================================="
    echo
    print_status "Étapes suivantes:"
    echo
    echo "1. Créer un nouveau dépôt sur GitHub:"
    echo "   - Nom: vpn-dnac-hybrid-network"
    echo "   - Description: Déploiement d'un Réseau Hybride Sécurisé avec VPN IPsec et Automatisation Cisco DNA Center"
    echo "   - Visibilité: Public (pour portfolio)"
    echo
    echo "2. Connecter le dépôt local:"
    echo "   git remote add origin https://github.com/VOTRE_USERNAME/vpn-dnac-hybrid-network.git"
    echo
    echo "3. Pousser le code:"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo
    echo "4. Ajouter les captures d'écran:"
    echo "   - Prendre des captures d'écran de votre topologie EVE-NG"
    echo "   - Capturer les résultats des tests VPN"
    echo "   - Capturer l'exécution du script DNA Center"
    echo "   - Les placer dans le dossier screenshots/"
    echo
    echo "5. Mettre à jour la documentation:"
    echo "   - Ajouter les captures d'écran au README.md"
    echo "   - Documenter vos résultats spécifiques"
    echo "   - Mettre à jour les liens et références"
    echo
    print_status "Votre projet sera alors prêt pour votre portfolio !"
}

# Fonction principale
main() {
    echo "=========================================="
    echo "  DÉPLOIEMENT GITHUB - Projet VPN-DNAC"
    echo "=========================================="
    echo
    
    check_git
    init_repository
    create_gitignore
    prepare_screenshots
    create_license
    create_contributing
    create_changelog
    initial_commit
    show_github_instructions
    
    echo
    print_success "Déploiement GitHub préparé avec succès !"
}

# Exécution du script
main "$@"
