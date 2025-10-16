#!/usr/bin/env python3
"""
Page Interface DNA Center - Gestion des équipements Cisco
"""

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

def get_dnac_credentials():
    """Récupérer les identifiants DNA Center"""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.env')
    if os.path.exists(config_path):
        load_dotenv(config_path)
        return {
            'url': os.getenv('DNAC_URL', 'https://sandboxdnac2.cisco.com'),
            'username': os.getenv('DNAC_USERNAME', 'devnetuser'),
            'password': os.getenv('DNAC_PASSWORD', 'Cisco123!')
        }
    return None

def simulate_dnac_data():
    """Simuler les données DNA Center"""
    return {
        'devices': [
            {
                'name': 'HQ-Router',
                'type': 'CSR1000v',
                'ip': '203.0.113.2',
                'status': 'Reachable',
                'version': '16.12.04',
                'uptime': '99.9%',
                'last_seen': '2024-01-15 14:30:00'
            },
            {
                'name': 'Branch-Router',
                'type': 'CSR1000v',
                'ip': '203.0.113.6',
                'status': 'Reachable',
                'version': '16.12.04',
                'uptime': '99.8%',
                'last_seen': '2024-01-15 14:29:00'
            },
            {
                'name': 'Internet-Router',
                'type': 'CSR1000v',
                'ip': '203.0.113.1',
                'status': 'Reachable',
                'version': '16.12.04',
                'uptime': '99.9%',
                'last_seen': '2024-01-15 14:30:00'
            },
            {
                'name': 'HQ-Switch',
                'type': 'vIOS-L2',
                'ip': '192.168.1.1',
                'status': 'Reachable',
                'version': '15.2(4)S',
                'uptime': '99.7%',
                'last_seen': '2024-01-15 14:28:00'
            },
            {
                'name': 'Branch-Switch',
                'type': 'vIOS-L2',
                'ip': '192.168.2.1',
                'status': 'Reachable',
                'version': '15.2(4)S',
                'uptime': '99.6%',
                'last_seen': '2024-01-15 14:27:00'
            }
        ],
        'network_health': {
            'connectivity': 98.5,
            'performance': 95.2,
            'security': 99.1,
            'availability': 99.8
        }
    }

def show_dnac_interface():
    """Afficher l'interface DNA Center"""
    st.title("🤖 Interface DNA Center")
    
    # Informations de connexion
    credentials = get_dnac_credentials()
    if credentials:
        st.info(f"🔗 Connexion: {credentials['url']}")
    
    # Actions principales
    st.subheader("🎮 Actions Principales")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Actualiser Données", use_container_width=True):
            st.success("✅ Données actualisées depuis DNA Center")
            st.rerun()
    
    with col2:
        if st.button("🔍 Scanner Réseau", use_container_width=True):
            st.success("✅ Scan des équipements terminé")
            st.info("📋 5 équipements découverts")
    
    with col3:
        if st.button("📊 Générer Rapport", use_container_width=True):
            st.success("✅ Rapport généré")
            st.download_button(
                "📥 Télécharger Rapport",
                data="Rapport DNA Center généré",
                file_name=f"dnac_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    
    # Équipements découverts
    st.subheader("📋 Équipements Découverts")
    
    dnac_data = simulate_dnac_data()
    devices_df = pd.DataFrame(dnac_data['devices'])
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        device_type = st.selectbox("Type d'équipement", ["Tous"] + list(devices_df['type'].unique()))
    with col2:
        device_status = st.selectbox("Statut", ["Tous"] + list(devices_df['status'].unique()))
    
    # Filtrer les données
    filtered_df = devices_df.copy()
    if device_type != "Tous":
        filtered_df = filtered_df[filtered_df['type'] == device_type]
    if device_status != "Tous":
        filtered_df = filtered_df[filtered_df['status'] == device_status]
    
    # Afficher le tableau
    st.dataframe(
        filtered_df[['name', 'type', 'ip', 'status', 'version', 'uptime', 'last_seen']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Santé du réseau
    st.subheader("💚 Santé du Réseau")
    
    health_data = dnac_data['network_health']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Connectivité", f"{health_data['connectivity']}%")
    
    with col2:
        st.metric("Performance", f"{health_data['performance']}%")
    
    with col3:
        st.metric("Sécurité", f"{health_data['security']}%")
    
    with col4:
        st.metric("Disponibilité", f"{health_data['availability']}%")
    
    # Graphique de santé
    st.subheader("📈 Évolution de la Santé")
    
    import plotly.graph_objects as go
    
    # Simulation de données temporelles
    import numpy as np
    dates = pd.date_range(start='2024-01-08', periods=7, freq='D')
    
    fig = go.Figure()
    
    for metric, value in health_data.items():
        # Simulation de variation autour de la valeur
        values = np.random.normal(value, 2, 7)
        values = np.clip(values, 90, 100)
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=metric.capitalize(),
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title="Évolution de la Santé du Réseau",
        xaxis_title="Date",
        yaxis_title="Score (%)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Actions sur les équipements
    st.subheader("⚙️ Actions sur les Équipements")
    
    selected_device = st.selectbox(
        "Sélectionner un équipement",
        [f"{d['name']} ({d['ip']})" for d in dnac_data['devices']]
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Redémarrer", use_container_width=True):
            st.warning(f"⚠️ Redémarrage de {selected_device} en cours...")
    
    with col2:
        if st.button("📋 Configurer", use_container_width=True):
            st.info(f"ℹ️ Ouverture de l'interface de configuration pour {selected_device}")
    
    with col3:
        if st.button("📊 Monitoring", use_container_width=True):
            st.info(f"ℹ️ Ouverture du monitoring pour {selected_device}")
    
    # Logs DNA Center
    st.subheader("📝 Logs DNA Center")
    
    logs = [
        {"Time": "14:30:15", "Level": "INFO", "Message": "Device HQ-Router discovered"},
        {"Time": "14:29:45", "Level": "INFO", "Message": "VPN tunnel established between HQ and Branch"},
        {"Time": "14:28:30", "Level": "WARN", "Message": "High CPU usage detected on Branch-Router"},
        {"Time": "14:27:12", "Level": "INFO", "Message": "Configuration backup completed"},
        {"Time": "14:25:55", "Level": "INFO", "Message": "Network scan completed successfully"}
    ]
    
    logs_df = pd.DataFrame(logs)
    st.dataframe(logs_df, use_container_width=True, hide_index=True)

if __name__ == "__main__":
    show_dnac_interface()


