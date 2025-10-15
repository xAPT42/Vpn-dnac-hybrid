# 🏗️ Architecture du Projet VPN-DNAC

## Diagramme d'Architecture

```mermaid
graph TB
    subgraph "🏢 HQ - Siège Social"
        HQR["`**HQ-Router**
        IP: 203.0.113.2
        Local: 192.168.1.1`"]
        HQS["`**HQ-Switch**
        VLAN: 10
        Users: HQ-Users`"]
        HQP["`**HQ-PC**
        IP: 192.168.1.10
        Gateway: 192.168.1.1`"]
    end
    
    subgraph "🌐 Internet (Simulé)"
        IR["`**Internet-Router**
        IP: 203.0.113.1
        Routes vers HQ/Branch`"]
    end
    
    subgraph "🏪 Branch - Succursale"
        BRR["`**Branch-Router**
        IP: 203.0.113.6
        Local: 192.168.2.1`"]
        BRS["`**Branch-Switch**
        VLAN: 20
        Users: Branch-Users`"]
        BRP["`**Branch-PC**
        IP: 192.168.2.10
        Gateway: 192.168.2.1`"]
    end
    
    subgraph "🔒 Tunnel VPN IPsec"
        TUN["`**Interface Tunnel0**
        HQ: 10.0.0.1/30
        Branch: 10.0.0.2/30
        Chiffrement: AES-256`"]
    end
    
    subgraph "🤖 Automatisation"
        DNA["`**Cisco DNA Center**
        API REST
        Monitoring
        Santé Réseau`"]
        STREAM["`**Dashboard Streamlit**
        Interface Web
        Métriques Temps Réel
        Analytics`"]
    end
    
    %% Connexions réseau
    HQR -.->|"🔒 Tunnel VPN<br/>IPsec IKEv2"| BRR
    HQR -->|"Route Internet"| IR
    BRR -->|"Route Internet"| IR
    HQR -->|"VLAN 10"| HQS
    BRR -->|"VLAN 20"| BRS
    HQS --> HQP
    BRS --> BRP
    
    %% Connexions tunnel
    HQR -.-> TUN
    BRR -.-> TUN
    
    %% Connexions automatisation
    DNA --> HQR
    DNA --> BRR
    DNA --> HQS
    DNA --> BRS
    STREAM --> DNA
    
    %% Styles
    classDef routerStyle fill:#e1f5fe,stroke:#0277bd,stroke-width:2px
    classDef switchStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef pcStyle fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef tunnelStyle fill:#fff3e0,stroke:#f57c00,stroke-width:3px
    classDef autoStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class HQR,BRR,IR routerStyle
    class HQS,BRS switchStyle
    class HQP,BRP pcStyle
    class TUN tunnelStyle
    class DNA,STREAM autoStyle
```

## Flux de Données

```mermaid
sequenceDiagram
    participant HQ as 🏢 HQ-PC
    participant HQR as HQ-Router
    participant BRR as Branch-Router
    participant BR as 🏪 Branch-PC
    participant DNA as 🤖 DNA Center
    participant DASH as 📊 Dashboard
    
    Note over HQ,BR: Communication Inter-Sites
    
    HQ->>HQR: Ping 192.168.2.10
    HQR->>HQR: Chiffrement IPsec
    HQR->>BRR: Tunnel VPN (chiffré)
    BRR->>BRR: Déchiffrement IPsec
    BRR->>BR: Ping vers 192.168.2.10
    BR->>BRR: Réponse
    BRR->>BRR: Chiffrement IPsec
    BRR->>HQR: Tunnel VPN (chiffré)
    HQR->>HQR: Déchiffrement IPsec
    HQR->>HQ: Réponse
    
    Note over DNA,DASH: Monitoring et Analytics
    
    DNA->>HQR: Collecte métriques
    DNA->>BRR: Collecte métriques
    DNA->>DNA: Analyse santé réseau
    DASH->>DNA: API calls
    DNA->>DASH: Données temps réel
    DASH->>DASH: Visualisation graphiques
```

## Technologies par Couche

```mermaid
graph TD
    subgraph "🎨 Couche Présentation"
        UI["`**Streamlit Dashboard**
        Interface Web Interactive
        Graphiques Plotly
        Métriques Temps Réel`"]
    end
    
    subgraph "🔧 Couche Application"
        API["`**APIs Python**
        DNA Center Client
        VPN Checker
        Data Processor`"]
    end
    
    subgraph "🌐 Couche Intégration"
        REST["`**Cisco DNA Center API**
        Authentification
        Collecte Données
        Monitoring`"]
    end
    
    subgraph "🔐 Couche Sécurité"
        VPN["`**VPN IPsec**
        IKEv2 (Phase 1)
        ESP (Phase 2)
        AES-256 + SHA-256`"]
    end
    
    subgraph "🏗️ Couche Infrastructure"
        NET["`**Réseau Cisco**
        Routeurs CSR1000v
        Switches vIOS-L2
        PC Virtuels`"]
    end
    
    UI --> API
    API --> REST
    REST --> VPN
    VPN --> NET
    
    classDef presentationStyle fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef applicationStyle fill:#f1f8e9,stroke:#388e3c,stroke-width:2px
    classDef integrationStyle fill:#fff8e1,stroke:#f57c00,stroke-width:2px
    classDef securityStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    classDef infrastructureStyle fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    
    class UI presentationStyle
    class API applicationStyle
    class REST integrationStyle
    class VPN securityStyle
    class NET infrastructureStyle
```

## Composants du Système

| Composant | Rôle | Technologies |
|-----------|------|-------------|
| **🏢 HQ-Router** | Routeur principal du siège | Cisco CSR1000v, IKEv2, IPsec |
| **🏪 Branch-Router** | Routeur de la succursale | Cisco CSR1000v, IKEv2, IPsec |
| **🌐 Internet-Router** | Simulation d'Internet | Cisco CSR1000v, Routage statique |
| **🔌 Switches** | Gestion des VLANs locaux | Cisco vIOS-L2, VLANs |
| **💻 PC Virtuels** | Stations de travail | vPC, Configuration réseau |
| **🤖 DNA Center** | Automatisation et monitoring | API REST, Collecte métriques |
| **📊 Dashboard** | Interface utilisateur | Streamlit, Plotly, Pandas |

## Sécurité et Chiffrement

```mermaid
graph LR
    subgraph "🔐 Phase 1 - IKEv2"
        IKE1["`**Authentification**
        PSK (Pre-Shared Key)
        Diffie-Hellman Group 14`"]
        IKE2["`**Chiffrement**
        AES-256
        SHA-256`"]
    end
    
    subgraph "🛡️ Phase 2 - IPsec"
        IPS1["`**ESP (Encapsulation)**
        AES-256
        SHA-256`"]
        IPS2["`**Mode Tunnel**
        Chiffrement complet
        Authentification`"]
    end
    
    subgraph "📊 Trafic Protégé"
        TRAF["`**Données d'Entreprise**
        HQ ↔ Branch
        192.168.1.0/24 ↔ 192.168.2.0/24`"]
    end
    
    IKE1 --> IKE2
    IKE2 --> IPS1
    IPS1 --> IPS2
    IPS2 --> TRAF
    
    classDef ikeStyle fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px
    classDef ipsecStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef trafficStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class IKE1,IKE2 ikeStyle
    class IPS1,IPS2 ipsecStyle
    class TRAF trafficStyle
```

