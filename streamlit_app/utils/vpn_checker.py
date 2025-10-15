#!/usr/bin/env python3
"""
Utilitaire de vérification VPN
Description: Vérification de l'état du tunnel VPN IPsec
"""

import subprocess
import re
from datetime import datetime
import json

class VPNChecker:
    """Classe pour vérifier l'état du tunnel VPN"""
    
    def __init__(self):
        """Initialiser le vérificateur VPN"""
        self.hq_router_ip = "203.0.113.2"
        self.branch_router_ip = "203.0.113.6"
        self.tunnel_network = "10.0.0.0/30"
    
    def check_ikev2_status(self, router_ip):
        """
        Vérifier l'état IKEv2 sur un routeur
        
        Args:
            router_ip (str): Adresse IP du routeur
            
        Returns:
            dict: État IKEv2
        """
        # Simulation de la vérification IKEv2
        # En réalité, cela ferait un appel SSH vers le routeur
        return {
            'status': 'active',
            'peer_ip': self.branch_router_ip if router_ip == self.hq_router_ip else self.hq_router_ip,
            'encryption': 'AES-256',
            'integrity': 'SHA-256',
            'dh_group': 14,
            'uptime': '2 days, 14 hours',
            'last_rekey': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def check_ipsec_status(self, router_ip):
        """
        Vérifier l'état IPsec sur un routeur
        
        Args:
            router_ip (str): Adresse IP du routeur
            
        Returns:
            dict: État IPsec
        """
        # Simulation de la vérification IPsec
        return {
            'status': 'active',
            'transform_set': 'ESP-AES256-SHA256',
            'mode': 'tunnel',
            'packets_encrypted': 125000,
            'packets_decrypted': 125000,
            'bytes_encrypted': 1250000,
            'bytes_decrypted': 1250000
        }
    
    def check_tunnel_interface(self, router_ip):
        """
        Vérifier l'état de l'interface tunnel
        
        Args:
            router_ip (str): Adresse IP du routeur
            
        Returns:
            dict: État de l'interface tunnel
        """
        # Simulation de la vérification de l'interface
        tunnel_ip = "10.0.0.1" if router_ip == self.hq_router_ip else "10.0.0.2"
        
        return {
            'interface': 'Tunnel0',
            'ip_address': tunnel_ip,
            'status': 'up',
            'line_protocol': 'up',
            'mtu': 1400,
            'bandwidth': 1000000
        }
    
    def test_connectivity(self, source_ip, destination_ip):
        """
        Tester la connectivité entre deux adresses IP
        
        Args:
            source_ip (str): Adresse IP source
            destination_ip (str): Adresse IP destination
            
        Returns:
            dict: Résultat du test
        """
        # Simulation du test de ping
        # En réalité, cela ferait un ping réel
        return {
            'source': source_ip,
            'destination': destination_ip,
            'status': 'success',
            'packets_sent': 5,
            'packets_received': 5,
            'packet_loss': '0%',
            'avg_rtt': '5ms',
            'min_rtt': '4ms',
            'max_rtt': '7ms'
        }
    
    def get_vpn_summary(self):
        """
        Obtenir un résumé complet de l'état VPN
        
        Returns:
            dict: Résumé VPN complet
        """
        hq_ikev2 = self.check_ikev2_status(self.hq_router_ip)
        branch_ikev2 = self.check_ikev2_status(self.branch_router_ip)
        hq_ipsec = self.check_ipsec_status(self.hq_router_ip)
        branch_ipsec = self.check_ipsec_status(self.branch_router_ip)
        hq_tunnel = self.check_tunnel_interface(self.hq_router_ip)
        branch_tunnel = self.check_tunnel_interface(self.branch_router_ip)
        
        # Test de connectivité
        connectivity_test = self.test_connectivity("192.168.1.10", "192.168.2.10")
        
        return {
            'overall_status': 'active' if all([
                hq_ikev2['status'] == 'active',
                branch_ikev2['status'] == 'active',
                hq_ipsec['status'] == 'active',
                branch_ipsec['status'] == 'active',
                connectivity_test['status'] == 'success'
            ]) else 'inactive',
            'hq_router': {
                'ip': self.hq_router_ip,
                'ikev2': hq_ikev2,
                'ipsec': hq_ipsec,
                'tunnel': hq_tunnel
            },
            'branch_router': {
                'ip': self.branch_router_ip,
                'ikev2': branch_ikev2,
                'ipsec': branch_ipsec,
                'tunnel': branch_tunnel
            },
            'connectivity': connectivity_test,
            'last_check': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def get_vpn_status():
    """
    Fonction utilitaire pour obtenir l'état VPN
    
    Returns:
        dict: État VPN actuel
    """
    checker = VPNChecker()
    return checker.get_vpn_summary()

def simulate_vpn_commands():
    """
    Simuler les commandes Cisco pour la vérification VPN
    
    Returns:
        dict: Résultats des commandes
    """
    return {
        'show_crypto_ikev2_sa': """
IKEv2 Session Information
Session-id:1, Status:UP-IDLE, IKE count:1, CHILD count:1

Tunnel-id Local                 Remote                fvrf/ivrf            Status
1         203.0.113.2/500      203.0.113.6/500       none/none            READY
      Encr: AES-CBC, keysize: 256, PRF: SHA256, Hash: SHA256, DH Grp:14, Auth sign: PSK, Auth verify: PSK
      Life/Active Time: 86400/3600 sec
""",
        'show_crypto_ipsec_sa': """
interface: Tunnel0
    Crypto map tag: Tunnel0-head-0, local addr 203.0.113.2

   protected vrf: (none)
   local  ident (addr/mask/prot/port): (192.168.1.0/255.255.255.0/0/0)
   remote ident (addr/mask/prot/port): (192.168.2.0/255.255.255.0/0/0)
   current_peer 203.0.113.6 port 500
     PERMIT, flags={origin_is_acl,}
    #pkts encaps: 125000, #pkts encrypt: 125000, #pkts digest: 125000
    #pkts decaps: 125000, #pkts decrypt: 125000, #pkts verify: 125000
    #pkts compressed: 0, #pkts decompressed: 0
    #pkts not compressed: 0, #pkts compr. failed: 0
    #pkts not decompressed: 0, #pkts decompress failed: 0
    #send errors 0, #recv errors 0

     local crypto endpt.: 203.0.113.2, remote crypto endpt.: 203.0.113.6
     plaintext mtu 1422, path mtu 1500, ip mtu 1422, ip mtu idb Tunnel0
     current outbound spi: 0x12345678(305419896)
     PFS (Y/N): N, DH group: none

     inbound esp sas:
      spi: 0x87654321 (2271560481)
        transform: esp-256-aes esp-sha256-hmac ,
        in use settings ={Tunnel, }
        conn id: 2001, flow_id: 1, crypto map: Tunnel0-head-0
        sa timing: remaining key lifetime (k/sec): (4607999/3600)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE

     inbound ah sas:

     inbound pcp sas:

     outbound esp sas:
      spi: 0x12345678 (305419896)
        transform: esp-256-aes esp-sha256-hmac ,
        in use settings ={Tunnel, }
        conn id: 2002, flow_id: 2, crypto map: Tunnel0-head-0
        sa timing: remaining key lifetime (k/sec): (4607999/3600)
        IV size: 16 bytes
        replay detection support: Y
        Status: ACTIVE
""",
        'show_interfaces_tunnel0': """
Tunnel0 is up, line protocol is up
  Hardware is Tunnel
  Internet address is 10.0.0.1/30
  MTU 1400 bytes, BW 1000000 Kbit/sec, DLY 50000 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation TUNNEL, loopback not set
  Keepalive not set
  Tunnel source 203.0.113.2, destination 203.0.113.6
  Tunnel protocol/transport IPSEC/IP
  Tunnel TTL 255, Fast tunneling enabled
  Tunnel transport MTU 1422 bytes
  Tunnel transmit bandwidth 8000 (kbps)
  Tunnel receive bandwidth 8000 (kbps)
  Last input never, output never, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/0 (size/max)
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec
     125000 packets input, 125000000 bytes, 0 no buffer
     Received 0 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
     125000 packets output, 125000000 bytes, 0 underruns
     0 output errors, 0 collisions, 0 interface resets
     0 unknown protocol drops
     0 output buffer failures, 0 output buffers swapped out
"""
    }

