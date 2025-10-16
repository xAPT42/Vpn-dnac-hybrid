#!/usr/bin/env python3
"""
Application Streamlit - Dashboard VPN-DNAC
Description: Interface web interactive pour le projet de réseau hybride sécurisé
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import sys
import requests
from dotenv import load_dotenv

# Configuration de la page
st.set_page_config(
    page_title="VPN-DNAC Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-status {
        color: #28a745;
        font-weight: bold;
    }
    .warning-status {
        color: #ffc107;
        font-weight: bold;
    }
    .error-status {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données de configuration
@st.cache_data
def load_config():
    """Charger la configuration depuis config.env"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.env')
    if os.path.exists(config_path):
        load_dotenv(config_path)
        return {
            'HQ_PUBLIC_IP': os.getenv('HQ_PUBLIC_IP', '203.0.113.10'),
            'BRANCH_PUBLIC_IP': os.getenv('BRANCH_PUBLIC_IP', '203.0.113.20'),
            'HQ_LOCAL_NETWORK': os.getenv('HQ_LOCAL_NETWORK', '192.168.1.0/24'),
            'BRANCH_LOCAL_NETWORK': os.getenv('BRANCH_LOCAL_NETWORK', '192.168.2.0/24'),
            'DNAC_URL': os.getenv('DNAC_URL', 'https://sandboxdnac2.cisco.com'),
            'DNAC_USERNAME': os.getenv('DNAC_USERNAME', 'devnetuser'),
            'DNAC_PASSWORD': os.getenv('DNAC_PASSWORD', 'Cisco123!')
        }
    return {}

# Fonction pour simuler les données VPN
@st.cache_data(ttl=30)
def get_vpn_status():
    """Simuler l'état du tunnel VPN"""
    return {
        'status': 'active',
        'tunnel_up': True,
        'encryption': 'AES-256',
        'integrity': 'SHA-256',
        'traffic_bytes': 1250000,
        'uptime': '2 days, 14 hours',
        'last_rekey': '2024-01-15 14:30:00'
    }

# Fonction pour simuler les données réseau
@st.cache_data(ttl=60)
def get_network_data():
    """Simuler les données du réseau"""
    return {
        'devices': [
            {'name': 'HQ-Router', 'type': 'Routeur', 'ip': '203.0.113.2', 'status': 'active', 'uptime': '99.9%'},
            {'name': 'Branch-Router', 'type': 'Routeur', 'ip': '203.0.113.6', 'status': 'active', 'uptime': '99.8%'},
            {'name': 'Internet-Router', 'type': 'Routeur', 'ip': '203.0.113.1', 'status': 'active', 'uptime': '99.9%'},
            {'name': 'HQ-Switch', 'type': 'Switch', 'ip': '192.168.1.1', 'status': 'active', 'uptime': '99.7%'},
            {'name': 'Branch-Switch', 'type': 'Switch', 'ip': '192.168.2.1', 'status': 'active', 'uptime': '99.6%'},
            {'name': 'HQ-PC', 'type': 'PC', 'ip': '192.168.1.10', 'status': 'active', 'uptime': '98.5%'},
            {'name': 'Branch-PC', 'type': 'PC', 'ip': '192.168.2.10', 'status': 'active', 'uptime': '98.2%'}
        ],
        'traffic_data': generate_traffic_data()
    }

def generate_traffic_data():
    """Générer des données de trafic simulées"""
    import numpy as np
    hours = 24
    timestamps = [datetime.now() - timedelta(hours=h) for h in range(hours, 0, -1)]
    
    # Simulation de trafic VPN
    vpn_traffic = np.random.normal(100, 20, hours)
    vpn_traffic = np.maximum(vpn_traffic, 0)  # Pas de valeurs négatives
    
    # Simulation de trafic Internet
    internet_traffic = np.random.normal(150, 30, hours)
    internet_traffic = np.maximum(internet_traffic, 0)
    
    return {
        'timestamps': timestamps,
        'vpn_traffic': vpn_traffic,
        'internet_traffic': internet_traffic
    }

# Fonction principale
def main():
    """Fonction principale de l'application"""
    
    # Header principal
    st.markdown('<h1 class="main-header">🌐 VPN-DNAC Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Charger la configuration
    config = load_config()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choisir une page",
        ["📊 Dashboard Principal", "🔐 Monitoring VPN", "🤖 DNA Center", "⚙️ Gestion Configs", "📈 Analytics"]
    )
    
    # Affichage de la page sélectionnée
    if page == "📊 Dashboard Principal":
        show_dashboard(config)
    elif page == "🔐 Monitoring VPN":
        show_vpn_monitoring(config)
    elif page == "🤖 DNA Center":
        show_dnac_interface(config)
    elif page == "⚙️ Gestion Configs":
        show_config_manager(config)
    elif page == "📈 Analytics":
        show_analytics(config)

def show_dashboard(config):
    """Afficher le dashboard principal"""
    st.title("📊 Dashboard Principal")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    vpn_status = get_vpn_status()
    network_data = get_network_data()
    
    with col1:
        status_color = "🟢" if vpn_status['tunnel_up'] else "🔴"
        st.metric(
            "État VPN",
            f"{status_color} {'Actif' if vpn_status['tunnel_up'] else 'Inactif'}",
            "100%"
        )
    
    with col2:
        active_devices = len([d for d in network_data['devices'] if d['status'] == 'active'])
        st.metric(
            "Équipements",
            f"{active_devices}/{len(network_data['devices'])}",
            f"+{len(network_data['devices'])}"
        )
    
    with col3:
        traffic_mb = vpn_status['traffic_bytes'] / (1024 * 1024)
        st.metric(
            "Trafic VPN",
            f"{traffic_mb:.1f} MB",
            "+15%"
        )
    
    with col4:
        avg_uptime = sum(float(d['uptime'].replace('%', '')) for d in network_data['devices']) / len(network_data['devices'])
        st.metric(
            "Uptime Moyen",
            f"{avg_uptime:.1f}%",
            "+0.1%"
        )
    
    st.markdown("---")
    
    # Graphique de trafic en temps réel
    st.subheader("📈 Trafic Réseau en Temps Réel")
    
    traffic_data = network_data['traffic_data']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=traffic_data['timestamps'],
        y=traffic_data['vpn_traffic'],
        mode='lines+markers',
        name='Trafic VPN',
        line=dict(color='#1f77b4', width=3)
    ))
    fig.add_trace(go.Scatter(
        x=traffic_data['timestamps'],
        y=traffic_data['internet_traffic'],
        mode='lines+markers',
        name='Trafic Internet',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    fig.update_layout(
        title="Trafic Réseau (MB/h)",
        xaxis_title="Heure",
        yaxis_title="Trafic (MB)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des équipements
    st.subheader("🖥️ État des Équipements")
    
    devices_df = pd.DataFrame(network_data['devices'])
    devices_df['Status'] = devices_df['status'].apply(lambda x: f"🟢 {x}" if x == 'active' else f"🔴 {x}")
    
    st.dataframe(
        devices_df[['name', 'type', 'ip', 'Status', 'uptime']],
        use_container_width=True,
        hide_index=True
    )

def show_vpn_monitoring(config):
    """Afficher le monitoring VPN"""
    st.title("🔐 Monitoring VPN")
    
    vpn_status = get_vpn_status()
    
    # État du tunnel
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔒 État du Tunnel IPsec")
        
        status_color = "success" if vpn_status['tunnel_up'] else "error"
        st.markdown(f"""
        <div class="metric-card">
            <h4>État du Tunnel</h4>
            <p class="{status_color}-status">
                {'🟢 Actif' if vpn_status['tunnel_up'] else '🔴 Inactif'}
            </p>
            <p><strong>Chiffrement:</strong> {vpn_status['encryption']}</p>
            <p><strong>Intégrité:</strong> {vpn_status['integrity']}</p>
            <p><strong>Uptime:</strong> {vpn_status['uptime']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Statistiques VPN")
        
        traffic_mb = vpn_status['traffic_bytes'] / (1024 * 1024)
        st.metric("Trafic Total", f"{traffic_mb:.1f} MB")
        st.metric("Dernier Rekey", vpn_status['last_rekey'])
        st.metric("Sessions Actives", "2")
    
    st.markdown("---")
    
    # Test de connectivité
    st.subheader("🧪 Test de Connectivité")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Test HQ → Branch", use_container_width=True):
            st.success("✅ Ping réussi: 192.168.1.10 → 192.168.2.10 (5ms)")
    
    with col2:
        if st.button("🔄 Test Branch → HQ", use_container_width=True):
            st.success("✅ Ping réussi: 192.168.2.10 → 192.168.1.10 (4ms)")
    
    with col3:
        if st.button("🔄 Test Tunnel", use_container_width=True):
            st.success("✅ Tunnel actif: 10.0.0.1 ↔ 10.0.0.2")

def show_dnac_interface(config):
    """Afficher l'interface DNA Center"""
    st.title("🤖 Interface DNA Center")
    
    st.info("🔗 Connexion à la sandbox Cisco DevNet: sandboxdnac2.cisco.com")
    
    # Bouton d'actualisation
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.success("✅ Données actualisées depuis DNA Center")
    
    with col2:
        if st.button("🔍 Scanner", use_container_width=True):
            st.success("✅ Scan des équipements terminé")
    
    # Simulation des données DNA Center
    st.subheader("📋 Équipements Découverts")
    
    dnac_devices = [
        {'name': 'HQ-Router', 'type': 'CSR1000v', 'ip': '203.0.113.2', 'status': 'Reachable', 'version': '16.12.04'},
        {'name': 'Branch-Router', 'type': 'CSR1000v', 'ip': '203.0.113.6', 'status': 'Reachable', 'version': '16.12.04'},
        {'name': 'HQ-Switch', 'type': 'vIOS-L2', 'ip': '192.168.1.1', 'status': 'Reachable', 'version': '15.2(4)S'},
        {'name': 'Branch-Switch', 'type': 'vIOS-L2', 'ip': '192.168.2.1', 'status': 'Reachable', 'version': '15.2(4)S'}
    ]
    
    dnac_df = pd.DataFrame(dnac_devices)
    st.dataframe(dnac_df, use_container_width=True, hide_index=True)
    
    # Santé du réseau
    st.subheader("💚 Santé du Réseau")
    
    health_metrics = {
        'Connectivité': '98.5%',
        'Performance': '95.2%',
        'Sécurité': '99.1%',
        'Disponibilité': '99.8%'
    }
    
    cols = st.columns(4)
    for i, (metric, value) in enumerate(health_metrics.items()):
        with cols[i]:
            st.metric(metric, value)

def show_config_manager(config):
    """Afficher le gestionnaire de configurations"""
    st.title("⚙️ Gestionnaire de Configurations")
    
    # Upload de configuration
    st.subheader("📤 Upload de Configuration")
    uploaded_file = st.file_uploader(
        "Choisir un fichier de configuration (.cfg, .txt)",
        type=['cfg', 'txt', 'conf']
    )
    
    if uploaded_file:
        st.success(f"✅ Fichier {uploaded_file.name} uploadé avec succès")
        
        # Aperçu du fichier
        if st.checkbox("Aperçu du fichier"):
            content = uploaded_file.read().decode('utf-8')
            st.code(content, language='bash')
    
    st.markdown("---")
    
    # Téléchargement de configurations
    st.subheader("📥 Télécharger des Configurations")
    
    configs = [
        "HQ-Router.cfg",
        "Branch-Router.cfg", 
        "Internet-Router.cfg",
        "HQ-Switch.cfg",
        "Branch-Switch.cfg",
        "VPN-Configs.zip"
    ]
    
    selected_config = st.selectbox("Sélectionner une configuration", configs)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Télécharger", use_container_width=True):
            st.success(f"✅ Configuration {selected_config} téléchargée")
    
    with col2:
        if st.button("📋 Copier", use_container_width=True):
            st.success("✅ Configuration copiée dans le presse-papiers")
    
    # Historique des modifications
    st.subheader("📝 Historique des Modifications")
    
    history_data = [
        {'Date': '2024-01-15 14:30', 'Fichier': 'HQ-Router.cfg', 'Action': 'Modification VPN', 'Utilisateur': 'admin'},
        {'Date': '2024-01-15 10:15', 'Fichier': 'Branch-Router.cfg', 'Action': 'Ajout route', 'Utilisateur': 'admin'},
        {'Date': '2024-01-14 16:45', 'Fichier': 'HQ-Switch.cfg', 'Action': 'Configuration VLAN', 'Utilisateur': 'admin'}
    ]
    
    history_df = pd.DataFrame(history_data)
    st.dataframe(history_df, use_container_width=True, hide_index=True)

def show_analytics(config):
    """Afficher les analytics"""
    st.title("📈 Analytics et Rapports")
    
    # Sélection de la période
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date de début", value=datetime.now().date() - timedelta(days=7))
    with col2:
        end_date = st.date_input("Date de fin", value=datetime.now().date())
    
    # Graphiques d'analytics
    st.subheader("📊 Performance du Réseau")
    
    # Simulation de données d'analytics
    import numpy as np
    
    # Graphique de performance
    days = 7
    dates = [datetime.now().date() - timedelta(days=d) for d in range(days, 0, -1)]
    
    performance_data = np.random.normal(95, 5, days)
    performance_data = np.clip(performance_data, 80, 100)
    
    fig_perf = px.line(
        x=dates,
        y=performance_data,
        title="Performance du Réseau (%)",
        labels={'x': 'Date', 'y': 'Performance (%)'}
    )
    
    st.plotly_chart(fig_perf, use_container_width=True)
    
    # Graphique de trafic
    st.subheader("🌐 Analyse du Trafic")
    
    traffic_hours = list(range(24))
    vpn_traffic = np.random.normal(100, 20, 24)
    internet_traffic = np.random.normal(150, 30, 24)
    
    fig_traffic = go.Figure()
    fig_traffic.add_trace(go.Bar(x=traffic_hours, y=vpn_traffic, name='Trafic VPN', marker_color='#1f77b4'))
    fig_traffic.add_trace(go.Bar(x=traffic_hours, y=internet_traffic, name='Trafic Internet', marker_color='#ff7f0e'))
    
    fig_traffic.update_layout(
        title="Distribution du Trafic par Heure",
        xaxis_title="Heure",
        yaxis_title="Trafic (MB)",
        barmode='group'
    )
    
    st.plotly_chart(fig_traffic, use_container_width=True)
    
    # Métriques clés
    st.subheader("🎯 Métriques Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Uptime Moyen", "99.7%", "+0.2%")
    
    with col2:
        st.metric("Latence Moyenne", "12ms", "-2ms")
    
    with col3:
        st.metric("Débit Moyen", "45 Mbps", "+5 Mbps")
    
    with col4:
        st.metric("Erreurs", "0.1%", "-0.05%")

if __name__ == "__main__":
    main()


