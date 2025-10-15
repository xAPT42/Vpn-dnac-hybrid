#!/usr/bin/env python3
"""
Page Gestionnaire de Configurations - Upload/Download des configs
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import zipfile
import io

def show_config_manager():
    """Afficher le gestionnaire de configurations"""
    st.title("⚙️ Gestionnaire de Configurations")
    
    # Upload de configurations
    st.subheader("📤 Upload de Configuration")
    
    uploaded_file = st.file_uploader(
        "Choisir un fichier de configuration",
        type=['cfg', 'txt', 'conf', 'zip'],
        help="Formats supportés: .cfg, .txt, .conf, .zip"
    )
    
    if uploaded_file:
        st.success(f"✅ Fichier {uploaded_file.name} uploadé avec succès")
        
        # Détails du fichier
        file_size = len(uploaded_file.getvalue())
        st.info(f"📏 Taille: {file_size} bytes")
        
        # Aperçu du contenu
        if st.checkbox("Aperçu du contenu"):
            if uploaded_file.name.endswith('.zip'):
                st.info("📦 Fichier ZIP détecté")
                try:
                    with zipfile.ZipFile(uploaded_file) as zip_file:
                        file_list = zip_file.namelist()
                        st.write("📋 Contenu de l'archive:")
                        for file in file_list:
                            st.write(f"  - {file}")
                except:
                    st.error("❌ Erreur lors de la lecture du fichier ZIP")
            else:
                content = uploaded_file.read().decode('utf-8')
                st.code(content[:1000] + "..." if len(content) > 1000 else content, language='bash')
        
        # Actions sur le fichier uploadé
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Sauvegarder", use_container_width=True):
                st.success("✅ Configuration sauvegardée")
        
        with col2:
            if st.button("✅ Valider", use_container_width=True):
                st.success("✅ Configuration validée")
        
        with col3:
            if st.button("🚀 Appliquer", use_container_width=True):
                st.warning("⚠️ Application de la configuration en cours...")
    
    st.markdown("---")
    
    # Téléchargement de configurations
    st.subheader("📥 Télécharger des Configurations")
    
    # Liste des configurations disponibles
    configs = [
        {
            'name': 'HQ-Router.cfg',
            'type': 'Configuration Routeur',
            'size': '2.3 KB',
            'modified': '2024-01-15 14:30'
        },
        {
            'name': 'Branch-Router.cfg',
            'type': 'Configuration Routeur',
            'size': '2.1 KB',
            'modified': '2024-01-15 14:30'
        },
        {
            'name': 'Internet-Router.cfg',
            'type': 'Configuration Routeur',
            'size': '1.8 KB',
            'modified': '2024-01-15 14:30'
        },
        {
            'name': 'HQ-Switch.cfg',
            'type': 'Configuration Switch',
            'size': '1.5 KB',
            'modified': '2024-01-15 14:30'
        },
        {
            'name': 'Branch-Switch.cfg',
            'type': 'Configuration Switch',
            'size': '1.4 KB',
            'modified': '2024-01-15 14:30'
        },
        {
            'name': 'VPN-Configs.zip',
            'type': 'Archive VPN',
            'size': '5.2 KB',
            'modified': '2024-01-15 14:30'
        }
    ]
    
    # Tableau des configurations
    configs_df = pd.DataFrame(configs)
    st.dataframe(configs_df, use_container_width=True, hide_index=True)
    
    # Sélection et téléchargement
    selected_config = st.selectbox(
        "Sélectionner une configuration à télécharger",
        [config['name'] for config in configs]
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Télécharger", use_container_width=True):
            # Simulation du téléchargement
            sample_config = """!
! Configuration générée automatiquement
! Date: 2024-01-15 14:30:00
!
hostname HQ-Router
!
interface GigabitEthernet0/0
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
end"""
            
            st.download_button(
                "💾 Télécharger le fichier",
                data=sample_config,
                file_name=selected_config,
                mime="text/plain"
            )
    
    with col2:
        if st.button("📋 Copier", use_container_width=True):
            st.success("✅ Configuration copiée dans le presse-papiers")
    
    with col3:
        if st.button("👁️ Aperçu", use_container_width=True):
            st.info(f"ℹ️ Aperçu de {selected_config}")
            st.code("""
!
! Configuration générée automatiquement
! Date: 2024-01-15 14:30:00
!
hostname HQ-Router
!
interface GigabitEthernet0/0
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
end
            """, language='bash')
    
    st.markdown("---")
    
    # Historique des modifications
    st.subheader("📝 Historique des Modifications")
    
    history_data = [
        {
            'Date': '2024-01-15 14:30:00',
            'Fichier': 'HQ-Router.cfg',
            'Action': 'Modification VPN',
            'Utilisateur': 'admin',
            'Statut': 'Appliqué'
        },
        {
            'Date': '2024-01-15 10:15:00',
            'Fichier': 'Branch-Router.cfg',
            'Action': 'Ajout route',
            'Utilisateur': 'admin',
            'Statut': 'Appliqué'
        },
        {
            'Date': '2024-01-14 16:45:00',
            'Fichier': 'HQ-Switch.cfg',
            'Action': 'Configuration VLAN',
            'Utilisateur': 'admin',
            'Statut': 'En attente'
        },
        {
            'Date': '2024-01-14 14:20:00',
            'Fichier': 'Internet-Router.cfg',
            'Action': 'Modification NAT',
            'Utilisateur': 'admin',
            'Statut': 'Appliqué'
        },
        {
            'Date': '2024-01-14 09:30:00',
            'Fichier': 'Branch-Switch.cfg',
            'Action': 'Configuration port',
            'Utilisateur': 'admin',
            'Statut': 'Appliqué'
        }
    ]
    
    history_df = pd.DataFrame(history_data)
    
    # Filtres pour l'historique
    col1, col2 = st.columns(2)
    with col1:
        filter_file = st.selectbox(
            "Filtrer par fichier",
            ["Tous"] + list(history_df['Fichier'].unique())
        )
    with col2:
        filter_status = st.selectbox(
            "Filtrer par statut",
            ["Tous"] + list(history_df['Statut'].unique())
        )
    
    # Appliquer les filtres
    filtered_history = history_df.copy()
    if filter_file != "Tous":
        filtered_history = filtered_history[filtered_history['Fichier'] == filter_file]
    if filter_status != "Tous":
        filtered_history = filtered_history[filtered_history['Statut'] == filter_status]
    
    st.dataframe(filtered_history, use_container_width=True, hide_index=True)
    
    # Actions sur l'historique
    if st.button("🔄 Actualiser Historique"):
        st.success("✅ Historique actualisé")
        st.rerun()
    
    st.markdown("---")
    
    # Backup et Restore
    st.subheader("💾 Backup et Restore")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sauvegarde**")
        if st.button("📦 Créer Backup Complet", use_container_width=True):
            st.success("✅ Backup créé avec succès")
            st.download_button(
                "📥 Télécharger Backup",
                data="Backup complet des configurations",
                file_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime="application/zip"
            )
    
    with col2:
        st.markdown("**Restauration**")
        backup_file = st.file_uploader(
            "Choisir un fichier de backup",
            type=['zip'],
            key="backup_uploader"
        )
        if backup_file and st.button("🔄 Restaurer Backup", use_container_width=True):
            st.warning("⚠️ Restauration du backup en cours...")
            st.success("✅ Backup restauré avec succès")

if __name__ == "__main__":
    show_config_manager()

