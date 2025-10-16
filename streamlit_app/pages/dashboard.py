#!/usr/bin/env python3
"""
Page Dashboard - Vue d'ensemble du système
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

def show_dashboard():
    """Afficher le dashboard principal"""
    st.title("📊 Dashboard Principal")
    
    # Métriques en temps réel
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("État VPN", "🟢 Actif", "100%")
    
    with col2:
        st.metric("Équipements", "7/7", "+2")
    
    with col3:
        st.metric("Trafic", "1.2 GB", "+15%")
    
    with col4:
        st.metric("Uptime", "99.9%", "0.1%")
    
    st.markdown("---")
    
    # Graphique de performance
    st.subheader("📈 Performance du Système")
    
    # Simulation de données
    hours = list(range(24))
    cpu_usage = np.random.normal(45, 10, 24)
    memory_usage = np.random.normal(60, 8, 24)
    network_usage = np.random.normal(35, 12, 24)
    
    fig = px.line(
        x=hours,
        y=[cpu_usage, memory_usage, network_usage],
        title="Utilisation des Ressources (%)",
        labels={'x': 'Heure', 'y': 'Utilisation (%)'},
        color_discrete_map={0: 'CPU', 1: 'Mémoire', 2: 'Réseau'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alertes système
    st.subheader("🚨 Alertes Système")
    
    alerts = [
        {"Type": "Info", "Message": "Tunnel VPN stable", "Time": "2024-01-15 14:30"},
        {"Type": "Warning", "Message": "Charge CPU élevée sur HQ-Router", "Time": "2024-01-15 14:25"},
        {"Type": "Success", "Message": "Configuration VPN appliquée", "Time": "2024-01-15 14:20"}
    ]
    
    for alert in alerts:
        if alert["Type"] == "Info":
            st.info(f"ℹ️ {alert['Message']} - {alert['Time']}")
        elif alert["Type"] == "Warning":
            st.warning(f"⚠️ {alert['Message']} - {alert['Time']}")
        elif alert["Type"] == "Success":
            st.success(f"✅ {alert['Message']} - {alert['Time']}")

if __name__ == "__main__":
    show_dashboard()


