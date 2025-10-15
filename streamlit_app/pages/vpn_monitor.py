#!/usr/bin/env python3
"""
Page Monitoring VPN - Surveillance du tunnel IPsec
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

def show_vpn_monitoring():
    """Afficher le monitoring VPN détaillé"""
    st.title("🔐 Monitoring VPN IPsec")
    
    # État du tunnel
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔒 État du Tunnel")
        
        # Simulation de l'état VPN
        tunnel_status = {
            'active': True,
            'encryption': 'AES-256',
            'integrity': 'SHA-256',
            'dh_group': 14,
            'traffic_bytes': 1250000,
            'uptime': '2 days, 14 hours',
            'last_rekey': '2024-01-15 14:30:00'
        }
        
        if tunnel_status['active']:
            st.success("🟢 Tunnel IPsec Actif")
        else:
            st.error("🔴 Tunnel IPsec Inactif")
        
        st.metric("Chiffrement", tunnel_status['encryption'])
        st.metric("Intégrité", tunnel_status['integrity'])
        st.metric("DH Group", tunnel_status['dh_group'])
        st.metric("Uptime", tunnel_status['uptime'])
    
    with col2:
        st.subheader("📊 Statistiques")
        
        traffic_mb = tunnel_status['traffic_bytes'] / (1024 * 1024)
        st.metric("Trafic Total", f"{traffic_mb:.1f} MB")
        st.metric("Dernier Rekey", tunnel_status['last_rekey'])
        st.metric("Sessions IKEv2", "1")
        st.metric("Sessions IPsec", "1")
    
    st.markdown("---")
    
    # Graphique de trafic VPN
    st.subheader("📈 Trafic VPN en Temps Réel")
    
    # Simulation de données de trafic
    hours = list(range(24))
    vpn_traffic = np.random.normal(100, 20, 24)
    vpn_traffic = np.maximum(vpn_traffic, 0)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hours,
        y=vpn_traffic,
        mode='lines+markers',
        name='Trafic VPN (MB/h)',
        line=dict(color='#1f77b4', width=3),
        fill='tonexty'
    ))
    
    fig.update_layout(
        title="Trafic VPN par Heure",
        xaxis_title="Heure",
        yaxis_title="Trafic (MB)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tests de connectivité
    st.subheader("🧪 Tests de Connectivité")
    
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
    
    # Détails techniques
    st.subheader("🔧 Détails Techniques")
    
    with st.expander("Configuration IKEv2"):
        st.code("""
crypto ikev2 proposal IKEV2-PROPOSAL
 encryption aes256
 integrity sha256
 group 14

crypto ikev2 policy IKEV2-POLICY
 proposal IKEV2-PROPOSAL
        """, language='bash')
    
    with st.expander("Configuration IPsec"):
        st.code("""
crypto ipsec transform-set ESP-TRANSFORM-SET esp-aes256 esp-sha256
 mode tunnel

crypto ipsec profile IPSEC-PROFILE
 set transform-set ESP-TRANSFORM-SET
 set ikev2-profile IKEV2-PROFILE
        """, language='bash')
    
    with st.expander("Interface Tunnel"):
        st.code("""
interface Tunnel0
 ip address 10.0.0.1 255.255.255.252
 tunnel source GigabitEthernet0/0
 tunnel destination 203.0.113.6
 tunnel protection ipsec profile IPSEC-PROFILE
        """, language='bash')

if __name__ == "__main__":
    show_vpn_monitoring()

