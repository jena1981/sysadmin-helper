#!/usr/bin/env python3
"""
SysAdmin Helper - Super Tool per Sistemisti Linux
Un tool completo per semplificare le operazioni di amministrazione sistema
"""

import os
import sys
import subprocess
import json
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import argparse

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class SystemInfo:
    """Classe per raccogliere informazioni di sistema"""
    
    @staticmethod
    def run_command(cmd: str, capture_output: bool = True) -> Tuple[int, str, str]:
        """Esegue un comando e restituisce il risultato"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=capture_output,
                text=True,
                timeout=30
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    @staticmethod
    def check_root():
        """Verifica se il tool è eseguito come root"""
        return os.geteuid() == 0
    
    @staticmethod
    def get_system_overview():
        """Restituisce una panoramica del sistema"""
        overview = {}
        
        # Sistema operativo
        ret, out, _ = SystemInfo.run_command("cat /etc/os-release")
        if ret == 0:
            for line in out.split('\n'):
                if line.startswith('PRETTY_NAME='):
                    overview['os'] = line.split('=')[1].strip('"')
                    break
        
        # Uptime
        ret, out, _ = SystemInfo.run_command("uptime -p")
        if ret == 0:
            overview['uptime'] = out.strip()
        
        # Memoria
        ret, out, _ = SystemInfo.run_command("free -h")
        if ret == 0:
            lines = out.split('\n')[1].split()
            overview['memory_total'] = lines[1]
            overview['memory_used'] = lines[2]
            overview['memory_available'] = lines[6]
        
        # Spazio disco
        ret, out, _ = SystemInfo.run_command("df -h / | tail -1")
        if ret == 0:
            parts = out.split()
            overview['disk_total'] = parts[1]
            overview['disk_used'] = parts[2]
            overview['disk_available'] = parts[3]
            overview['disk_usage'] = parts[4]
        
        # Load average
        ret, out, _ = SystemInfo.run_command("cat /proc/loadavg")
        if ret == 0:
            overview['load_avg'] = out.split()[0:3]
        
        return overview

class MenuSystem:
    """Sistema di menu interattivo"""
    
    def __init__(self):
        self.current_menu = "main"
        self.menu_history = []
    
    def clear_screen(self):
        """Pulisce lo schermo"""
        os.system('clear')
    
    def print_header(self):
        """Stampa l'header del tool"""
        self.clear_screen()
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    SYSADMIN HELPER v1.0                     ║")
        print("║              Super Tool per Sistemisti Linux                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        
        if not SystemInfo.check_root():
            print(f"{Colors.YELLOW}⚠️  ATTENZIONE: Non sei root. Alcune funzionalità potrebbero non essere disponibili.{Colors.RESET}")
        
        # Mostra informazioni di sistema
        overview = SystemInfo.get_system_overview()
        print(f"\n{Colors.BLUE}📊 Sistema: {overview.get('os', 'N/A')}")
        print(f"⏰ Uptime: {overview.get('uptime', 'N/A')}")
        print(f"💾 Memoria: {overview.get('memory_used', 'N/A')}/{overview.get('memory_total', 'N/A')} (Libera: {overview.get('memory_available', 'N/A')})")
        print(f"💽 Disco /: {overview.get('disk_used', 'N/A')}/{overview.get('disk_total', 'N/A')} ({overview.get('disk_usage', 'N/A')})")
        if overview.get('load_avg'):
            print(f"📈 Load Avg: {' '.join(overview['load_avg'])}")
        print(f"{Colors.RESET}")
    
    def show_main_menu(self):
        """Mostra il menu principale"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}🏠 MENU PRINCIPALE{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1.  💾 Gestione LVM e Filesystem")
        print(f"2.  🌐 Gestione Interfacce di Rete")
        print(f"3.  📋 Controllo Log Applicativi")
        print(f"4.  🔍 Log di Sistema e Audit")
        print(f"5.  📊 Monitoring Sistema")
        print(f"6.  ⚙️  Gestione Servizi")
        print(f"7.  🔒 Sicurezza e Utenti")
        print(f"8.  🧹 Manutenzione Sistema")
        print(f"9.  📈 Report e Dashboard")
        print(f"10. ⚙️  Configurazioni Tool")
        print(f"0.  ❌ Esci")
        print(f"{Colors.RESET}")
    
    def get_user_input(self, prompt: str = "Seleziona opzione: ") -> str:
        """Ottiene input dall'utente"""
        try:
            return input(f"{Colors.CYAN}{prompt}{Colors.RESET}").strip()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operazione annullata dall'utente.{Colors.RESET}")
            return "0"
    
    def pause(self, message: str = "Premi INVIO per continuare..."):
        """Mette in pausa per permettere all'utente di leggere"""
        input(f"\n{Colors.YELLOW}{message}{Colors.RESET}")

class LVMManager:
    """Gestore per operazioni LVM"""
    
    @staticmethod
    def show_lvm_menu():
        """Mostra il menu LVM"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}💾 GESTIONE LVM E FILESYSTEM{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 📊 Visualizza informazioni LVM")
        print(f"2. 💽 Lista dischi disponibili")
        print(f"3. 📈 Espandi Logical Volume")
        print(f"4. 🔍 Verifica spazio filesystem")
        print(f"5. 📋 Report completo storage")
        print(f"6. 🆕 Crea nuovo Physical Volume")
        print(f"7. 🔗 Estendi Volume Group")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def show_lvm_info():
        """Mostra informazioni LVM complete"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 INFORMAZIONI LVM{Colors.RESET}")
        print("=" * 60)
        
        # Physical Volumes
        print(f"\n{Colors.CYAN}🔷 Physical Volumes:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("pvdisplay")
        if ret == 0 and out.strip():
            print(out)
        else:
            print("Nessun Physical Volume trovato o LVM non configurato")
        
        # Volume Groups
        print(f"\n{Colors.CYAN}🔶 Volume Groups:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("vgdisplay")
        if ret == 0 and out.strip():
            print(out)
        else:
            print("Nessun Volume Group trovato")
        
        # Logical Volumes
        print(f"\n{Colors.CYAN}🔸 Logical Volumes:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("lvdisplay")
        if ret == 0 and out.strip():
            print(out)
        else:
            print("Nessun Logical Volume trovato")
    
    @staticmethod
    def show_available_disks():
        """Mostra dischi disponibili per espansione"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}💽 DISCHI DISPONIBILI{Colors.RESET}")
        print("=" * 60)
        
        # Lista tutti i dischi
        ret, out, err = SystemInfo.run_command("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE")
        if ret == 0:
            print(f"{Colors.WHITE}📋 Tutti i dischi:{Colors.RESET}")
            print(out)
        
        # Dischi non partizionati
        print(f"\n{Colors.GREEN}🆓 Dischi/partizioni libere (utilizzabili per LVM):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command(
            "lsblk -rno NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE | grep 'disk\\|part' | grep -v -E '(boot|swap|/)' | awk '$4==\"\" && $5==\"\"'"
        )
        if ret == 0 and out.strip():
            print("DEVICE    SIZE    TYPE")
            for line in out.split('\n'):
                if line.strip():
                    print(f"/dev/{line}")
        else:
            print("Nessun disco/partizione libera trovata")
        
        # Spazio libero nei VG esistenti
        print(f"\n{Colors.YELLOW}📊 Spazio libero nei Volume Groups:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("vgdisplay | grep -E '(VG Name|Free)'")
        if ret == 0 and out.strip():
            print(out)
    
    @staticmethod
    def get_logical_volumes():
        """Restituisce lista dei Logical Volumes"""
        ret, out, err = SystemInfo.run_command("lvs --noheadings -o lv_name,vg_name,lv_size")
        volumes = []
        if ret == 0:
            for line in out.split('\n'):
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        volumes.append({
                            'name': parts[0],
                            'vg': parts[1],
                            'size': parts[2],
                            'path': f"/dev/{parts[1]}/{parts[0]}"
                        })
        return volumes
    
    @staticmethod
    def get_volume_groups():
        """Restituisce lista dei Volume Groups con spazio libero"""
        ret, out, err = SystemInfo.run_command("vgs --noheadings -o vg_name,vg_size,vg_free")
        groups = []
        if ret == 0:
            for line in out.split('\n'):
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        groups.append({
                            'name': parts[0],
                            'size': parts[1],
                            'free': parts[2]
                        })
        return groups
    
    @staticmethod
    def expand_logical_volume():
        """Wizard per espandere un Logical Volume"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📈 ESPANSIONE LOGICAL VOLUME{Colors.RESET}")
        print("=" * 60)
        
        if not SystemInfo.check_root():
            print(f"{Colors.RED}❌ Questa operazione richiede privilegi di root{Colors.RESET}")
            return
        
        # Mostra LV disponibili
        volumes = LVMManager.get_logical_volumes()
        if not volumes:
            print(f"{Colors.YELLOW}⚠️  Nessun Logical Volume trovato{Colors.RESET}")
            return
        
        print(f"\n{Colors.WHITE}📋 Logical Volumes disponibili:{Colors.RESET}")
        for i, vol in enumerate(volumes, 1):
            print(f"{i}. {vol['path']} ({vol['size']})")
        
        # Selezione LV
        try:
            choice = int(input(f"\n{Colors.CYAN}Seleziona LV da espandere (1-{len(volumes)}): {Colors.RESET}"))
            if choice < 1 or choice > len(volumes):
                raise ValueError()
            selected_lv = volumes[choice - 1]
        except (ValueError, IndexError):
            print(f"{Colors.RED}❌ Selezione non valida{Colors.RESET}")
            return
        
        # Verifica spazio libero nel VG
        groups = LVMManager.get_volume_groups()
        vg_info = next((g for g in groups if g['name'] == selected_lv['vg']), None)
        
        if not vg_info:
            print(f"{Colors.RED}❌ Impossibile trovare informazioni del Volume Group{Colors.RESET}")
            return
        
        print(f"\n{Colors.WHITE}📊 Volume Group '{selected_lv['vg']}':{Colors.RESET}")
        print(f"   Dimensione totale: {vg_info['size']}")
        print(f"   Spazio libero: {vg_info['free']}")
        
        # Controllo filesystem
        ret, out, err = SystemInfo.run_command(f"df -h {selected_lv['path']}")
        if ret == 0:
            print(f"\n{Colors.WHITE}💽 Filesystem corrente:{Colors.RESET}")
            print(out)
        
        # Input della dimensione da aggiungere
        print(f"\n{Colors.YELLOW}💡 Formati supportati: +5G, +100%FREE, +50%VG{Colors.RESET}")
        size_input = input(f"{Colors.CYAN}Inserisci la dimensione da aggiungere: {Colors.RESET}")
        
        if not size_input:
            print(f"{Colors.RED}❌ Dimensione non specificata{Colors.RESET}")
            return
        
        # Conferma operazione
        print(f"\n{Colors.YELLOW}⚠️  ATTENZIONE: Stai per espandere:{Colors.RESET}")
        print(f"   Logical Volume: {selected_lv['path']}")
        print(f"   Dimensione da aggiungere: {size_input}")
        
        confirm = input(f"\n{Colors.RED}Confermi l'operazione? (scrivi 'CONFERMA'): {Colors.RESET}")
        if confirm != "CONFERMA":
            print(f"{Colors.YELLOW}Operazione annullata{Colors.RESET}")
            return
        
        # Esecuzione espansione
        print(f"\n{Colors.BLUE}🔄 Espansione del Logical Volume...{Colors.RESET}")
        ret, out, err = SystemInfo.run_command(f"lvextend -L {size_input} {selected_lv['path']}")
        
        if ret != 0:
            print(f"{Colors.RED}❌ Errore nell'espansione del LV: {err}{Colors.RESET}")
            return
        
        print(f"{Colors.GREEN}✅ Logical Volume espanso con successo{Colors.RESET}")
        
        # Resize del filesystem
        print(f"\n{Colors.BLUE}🔄 Espansione del filesystem...{Colors.RESET}")
        
        # Rileva tipo di filesystem
        ret, out, err = SystemInfo.run_command(f"blkid -o value -s TYPE {selected_lv['path']}")
        fs_type = out.strip() if ret == 0 else ""
        
        if fs_type == "ext4" or fs_type == "ext3":
            ret, out, err = SystemInfo.run_command(f"resize2fs {selected_lv['path']}")
        elif fs_type == "xfs":
            # Per XFS serve il punto di mount
            ret2, mount_out, _ = SystemInfo.run_command(f"findmnt -n -o TARGET {selected_lv['path']}")
            if ret2 == 0:
                mount_point = mount_out.strip()
                ret, out, err = SystemInfo.run_command(f"xfs_growfs {mount_point}")
            else:
                print(f"{Colors.YELLOW}⚠️  Impossibile trovare il punto di mount per XFS{Colors.RESET}")
                ret = 1
        else:
            print(f"{Colors.YELLOW}⚠️  Filesystem {fs_type} non supportato per l'auto-resize{Colors.RESET}")
            ret = 1
        
        if ret == 0:
            print(f"{Colors.GREEN}✅ Filesystem espanso con successo{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}⚠️  Espandere manualmente il filesystem con resize2fs o xfs_growfs{Colors.RESET}")
        
        # Verifica finale
        print(f"\n{Colors.BLUE}📊 Verifica finale:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command(f"df -h {selected_lv['path']}")
        if ret == 0:
            print(out)
    
    @staticmethod
    def check_filesystem_space():
        """Verifica spazio filesystem"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 VERIFICA SPAZIO FILESYSTEM{Colors.RESET}")
        print("=" * 60)
        
        # Uso disco generale
        print(f"\n{Colors.WHITE}💽 Utilizzo disco generale:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("df -h")
        if ret == 0:
            print(out)
        
        # Filesystem con utilizzo alto
        print(f"\n{Colors.YELLOW}⚠️  Filesystem con utilizzo > 80%:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("df -h | awk 'NR>1 && $5+0 > 80 {print $0}'")
        if ret == 0 and out.strip():
            print(out)
        else:
            print("Nessun filesystem con utilizzo critico")
        
        # Inodes
        print(f"\n{Colors.WHITE}📊 Utilizzo inodes:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("df -i")
        if ret == 0:
            lines = out.split('\n')[1:]  # Skip header
            critical_inodes = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5 and '%' in parts[4]:
                        usage = int(parts[4].replace('%', ''))
                        if usage > 80:
                            critical_inodes.append(line)
            
            if critical_inodes:
                print(f"{Colors.YELLOW}⚠️  Utilizzo inodes critico:{Colors.RESET}")
                for line in critical_inodes:
                    print(line)
            else:
                print(f"{Colors.GREEN}✅ Utilizzo inodes normale{Colors.RESET}")
    
    @staticmethod
    def storage_report():
        """Report completo dello storage"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📋 REPORT COMPLETO STORAGE{Colors.RESET}")
        print("=" * 60)
        
        # Informazioni generali
        print(f"\n{Colors.CYAN}📊 PANORAMICA GENERALE{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,UUID")
        if ret == 0:
            print(out)
        
        # Statistiche LVM se disponibile
        ret, out, err = SystemInfo.run_command("pvs --noheadings")
        if ret == 0 and out.strip():
            print(f"\n{Colors.CYAN}🔷 STATISTICHE LVM{Colors.RESET}")
            print("Physical Volumes:")
            SystemInfo.run_command("pvs")
            print("\nVolume Groups:")
            SystemInfo.run_command("vgs") 
            print("\nLogical Volumes:")
            SystemInfo.run_command("lvs")
        
        # I/O Statistics
        print(f"\n{Colors.CYAN}📈 STATISTICHE I/O{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("iostat -x 1 1 2>/dev/null || echo 'iostat non disponibile'")
        if ret == 0:
            print(out)
        
        # Mount options
        print(f"\n{Colors.CYAN}🔧 OPZIONI MOUNT{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("mount | grep -v tmpfs | grep -v devpts | grep -v sysfs | grep -v proc")
        if ret == 0:
            print(out)

class NetworkManager:
    """Gestore per operazioni di rete"""
    
    @staticmethod
    def show_network_menu():
        """Mostra il menu gestione rete"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}🌐 GESTIONE INTERFACCE DI RETE{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 📊 Stato interfacce di rete")
        print(f"2. 🔍 Diagnostica connettività")
        print(f"3. 📈 Statistiche traffico")
        print(f"4. ⚙️  Configurazione IP")
        print(f"5. 🔧 Gestione routing")
        print(f"6. 🌍 DNS e risoluzione nomi")
        print(f"7. 🔒 Firewall status")
        print(f"8. 📋 Report completo rete")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def show_network_interfaces():
        """Mostra stato interfacce di rete"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 STATO INTERFACCE DI RETE{Colors.RESET}")
        print("=" * 60)
        
        # Interfacce con ip
        print(f"\n{Colors.CYAN}🔌 Interfacce configurate:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip addr show")
        if ret == 0:
            print(out)
        
        # Link status
        print(f"\n{Colors.CYAN}🔗 Stato dei link:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip link show")
        if ret == 0:
            # Estrai solo le info essenziali
            lines = out.split('\n')
            for line in lines:
                if ':' in line and 'state' in line.lower():
                    print(line.strip())
        
        # Routing table
        print(f"\n{Colors.CYAN}🛤️  Tabella di routing:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip route show")
        if ret == 0:
            print(out)
    
    @staticmethod
    def network_diagnostics():
        """Diagnostica connettività di rete"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 DIAGNOSTICA CONNETTIVITÀ{Colors.RESET}")
        print("=" * 60)
        
        # Gateway predefinito
        print(f"\n{Colors.WHITE}🚪 Gateway predefinito:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip route | grep default")
        if ret == 0:
            print(out)
            
            # Estrai IP del gateway per il ping
            gateway_ip = None
            for line in out.split('\n'):
                if 'default' in line:
                    parts = line.split()
                    if len(parts) > 2:
                        gateway_ip = parts[2]
                        break
            
            if gateway_ip:
                print(f"\n{Colors.WHITE}🏓 Test ping gateway ({gateway_ip}):{Colors.RESET}")
                ret, out, err = SystemInfo.run_command(f"ping -c 3 {gateway_ip}")
                if ret == 0:
                    print(f"{Colors.GREEN}✅ Gateway raggiungibile{Colors.RESET}")
                    # Mostra solo il summary
                    lines = out.split('\n')
                    for line in lines:
                        if 'packet loss' in line or 'min/avg/max' in line:
                            print(line)
                else:
                    print(f"{Colors.RED}❌ Gateway non raggiungibile{Colors.RESET}")
        
        # Test DNS
        print(f"\n{Colors.WHITE}🌐 Test risoluzione DNS:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("nslookup google.com 2>/dev/null | grep -E '(Server|Address)'")
        if ret == 0:
            print(out)
            print(f"{Colors.GREEN}✅ DNS funzionante{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Problemi con DNS{Colors.RESET}")
        
        # Test connettività Internet
        print(f"\n{Colors.WHITE}🌍 Test connettività Internet:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ping -c 2 8.8.8.8 2>/dev/null")
        if ret == 0:
            print(f"{Colors.GREEN}✅ Connettività Internet OK{Colors.RESET}")
        else:
            print(f"{Colors.RED}❌ Nessuna connettività Internet{Colors.RESET}")
        
        # Porte in ascolto
        print(f"\n{Colors.WHITE}👂 Porte in ascolto:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ss -tuln | head -20")
        if ret == 0:
            print(out)
    
    @staticmethod
    def traffic_statistics():
        """Statistiche traffico di rete"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📈 STATISTICHE TRAFFICO{Colors.RESET}")
        print("=" * 60)
        
        # Statistiche interfacce
        print(f"\n{Colors.CYAN}📊 Statistiche per interfaccia:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("cat /proc/net/dev")
        if ret == 0:
            lines = out.split('\n')
            print(f"{'Interface':<10} {'RX Bytes':<12} {'RX Packets':<12} {'TX Bytes':<12} {'TX Packets':<12}")
            print("-" * 70)
            for line in lines[2:]:  # Skip header lines
                if ':' in line:
                    parts = line.split()
                    if len(parts) >= 10:
                        iface = parts[0].rstrip(':')
                        rx_bytes = int(parts[1])
                        rx_packets = int(parts[2])
                        tx_bytes = int(parts[9])
                        tx_packets = int(parts[10])
                        
                        # Format bytes in human readable
                        rx_mb = rx_bytes / (1024*1024)
                        tx_mb = tx_bytes / (1024*1024)
                        
                        print(f"{iface:<10} {rx_mb:<12.1f} {rx_packets:<12} {tx_mb:<12.1f} {tx_packets:<12}")
        
        # Connessioni attive
        print(f"\n{Colors.CYAN}🔗 Connessioni attive (top 10):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ss -tuln | grep LISTEN | head -10")
        if ret == 0:
            print(out)
        
        # Bandwidth monitoring se disponibile
        print(f"\n{Colors.CYAN}📶 Utilizzo banda (iftop/vnstat se disponibili):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("which vnstat")
        if ret == 0:
            ret, out, err = SystemInfo.run_command("vnstat -i $(ip route | awk '/default/ {print $5}' | head -1) --json 2>/dev/null")
            if ret == 0 and out.strip():
                print("Statistiche vnstat disponibili (formato JSON)")
            else:
                ret, out, err = SystemInfo.run_command("vnstat -s")
                if ret == 0:
                    print(out)
        else:
            print("vnstat non installato - statistiche limitate")
    
    @staticmethod
    def ip_configuration():
        """Configurazione IP"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}⚙️  CONFIGURAZIONE IP{Colors.RESET}")
        print("=" * 60)
        
        if not SystemInfo.check_root():
            print(f"{Colors.YELLOW}⚠️  Molte operazioni richiedono privilegi di root{Colors.RESET}")
        
        # Mostra configurazione attuale
        print(f"\n{Colors.WHITE}📋 Configurazione attuale:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip addr show | grep -E '(^[0-9]+:|inet )'")
        if ret == 0:
            print(out)
        
        # DHCP clients attivi
        print(f"\n{Colors.WHITE}🔄 Client DHCP attivi:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ps aux | grep dhcp | grep -v grep")
        if ret == 0 and out.strip():
            print(out)
        else:
            print("Nessun client DHCP attivo")
        
        # NetworkManager status se presente
        ret, out, err = SystemInfo.run_command("which nmcli")
        if ret == 0:
            print(f"\n{Colors.WHITE}🔧 NetworkManager:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("nmcli general status")
            if ret == 0:
                print(out)
            
            print(f"\n{Colors.WHITE}📡 Connessioni NetworkManager:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("nmcli connection show")
            if ret == 0:
                print(out)
    
    @staticmethod
    def routing_management():
        """Gestione routing"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔧 GESTIONE ROUTING{Colors.RESET}")
        print("=" * 60)
        
        # Tabella di routing principale
        print(f"\n{Colors.WHITE}🛤️  Tabella routing principale:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip route show table main")
        if ret == 0:
            print(out)
        
        # Altre tabelle di routing
        print(f"\n{Colors.WHITE}📋 Tabelle routing disponibili:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip rule show")
        if ret == 0:
            print(out)
        
        # Forwarding IP
        print(f"\n{Colors.WHITE}↔️  IP Forwarding:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("cat /proc/sys/net/ipv4/ip_forward")
        if ret == 0:
            forwarding = out.strip()
            if forwarding == "1":
                print(f"{Colors.GREEN}✅ IP Forwarding abilitato{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠️  IP Forwarding disabilitato{Colors.RESET}")
        
        # ARP table
        print(f"\n{Colors.WHITE}🔍 Tabella ARP:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip neigh show")
        if ret == 0:
            print(out)
    
    @staticmethod
    def dns_management():
        """Gestione DNS"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🌍 DNS E RISOLUZIONE NOMI{Colors.RESET}")
        print("=" * 60)
        
        # File resolv.conf
        print(f"\n{Colors.WHITE}📄 Configurazione DNS (/etc/resolv.conf):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("cat /etc/resolv.conf")
        if ret == 0:
            print(out)
        
        # File hosts
        print(f"\n{Colors.WHITE}🏠 File hosts (/etc/hosts):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("cat /etc/hosts")
        if ret == 0:
            print(out)
        
        # systemd-resolved se presente
        ret, out, err = SystemInfo.run_command("systemctl is-active systemd-resolved 2>/dev/null")
        if ret == 0:
            print(f"\n{Colors.WHITE}🔧 systemd-resolved status:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("systemd-resolve --status 2>/dev/null || resolvectl status 2>/dev/null")
            if ret == 0:
                print(out)
        
        # Test risoluzione
        print(f"\n{Colors.WHITE}🧪 Test risoluzione DNS:{Colors.RESET}")
        test_domains = ["google.com", "github.com", "localhost"]
        for domain in test_domains:
            ret, out, err = SystemInfo.run_command(f"nslookup {domain} 2>/dev/null | grep -E '(Address:|Name:)'")
            if ret == 0:
                print(f"{Colors.GREEN}✅ {domain}: {Colors.RESET}")
                print(f"   {out.strip()}")
            else:
                print(f"{Colors.RED}❌ {domain}: risoluzione fallita{Colors.RESET}")
    
    @staticmethod
    def firewall_status():
        """Stato firewall"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔒 FIREWALL STATUS{Colors.RESET}")
        print("=" * 60)
        
        # iptables
        print(f"\n{Colors.WHITE}🛡️  Regole iptables:{Colors.RESET}")
        if SystemInfo.check_root():
            ret, out, err = SystemInfo.run_command("iptables -L -n")
            if ret == 0:
                print(out)
        else:
            print(f"{Colors.YELLOW}⚠️  Privilegi di root richiesti per visualizzare iptables{Colors.RESET}")
        
        # ufw se presente
        ret, out, err = SystemInfo.run_command("which ufw")
        if ret == 0:
            print(f"\n{Colors.WHITE}🔥 UFW Status:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("ufw status verbose")
            if ret == 0:
                print(out)
        
        # firewalld se presente
        ret, out, err = SystemInfo.run_command("which firewall-cmd")
        if ret == 0:
            print(f"\n{Colors.WHITE}🔥 Firewalld Status:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("firewall-cmd --state 2>/dev/null")
            if ret == 0:
                print("Firewalld attivo")
                ret, out, err = SystemInfo.run_command("firewall-cmd --list-all 2>/dev/null")
                if ret == 0:
                    print(out)
            else:
                print("Firewalld non attivo")
        
        # Connessioni stabilite
        print(f"\n{Colors.WHITE}🔗 Connessioni stabilite:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ss -tuln | grep ESTAB | wc -l")
        if ret == 0:
            count = out.strip()
            print(f"Connessioni attive: {count}")
    
    @staticmethod
    def network_report():
        """Report completo rete"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📋 REPORT COMPLETO RETE{Colors.RESET}")
        print("=" * 60)
        
        # Hostname e dominio
        print(f"\n{Colors.CYAN}🏷️  Identificazione sistema:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("hostname -f")
        if ret == 0:
            print(f"FQDN: {out.strip()}")
        
        ret, out, err = SystemInfo.run_command("hostname -d")
        if ret == 0 and out.strip():
            print(f"Dominio: {out.strip()}")
        
        # Interfacce summary
        print(f"\n{Colors.CYAN}📊 Summary interfacce:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ip -o addr show | awk '{print $2, $4}'")
        if ret == 0:
            print(out)
        
        # Servizi di rete attivi
        print(f"\n{Colors.CYAN}⚡ Servizi rete attivi:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ss -tuln | awk 'NR>1 {print $1, $5}' | sort -u")
        if ret == 0:
            print(out)
        
        # Configurazioni importanti
        print(f"\n{Colors.CYAN}⚙️  File configurazione principali:{Colors.RESET}")
        config_files = [
            "/etc/network/interfaces",
            "/etc/netplan/*.yaml",
            "/etc/NetworkManager/NetworkManager.conf"
        ]
        
        for config in config_files:
            if "*" in config:
                ret, out, err = SystemInfo.run_command(f"ls {config} 2>/dev/null")
                if ret == 0 and out.strip():
                    print(f"✅ {config} (esistente)")
            else:
                ret, out, err = SystemInfo.run_command(f"test -f {config}")
                if ret == 0:
                    print(f"✅ {config}")

class LogManager:
    """Gestore per controllo log applicativi"""
    
    # Directory comuni dove cercare log
    LOG_DIRECTORIES = [
        "/var/log",
        "/var/log/apache2",
        "/var/log/nginx",
        "/var/log/mysql",
        "/var/log/postgresql", 
        "/var/log/mail",
        "/var/log/samba",
        "/home/*/logs",
        "/opt/*/logs",
        "/usr/local/*/logs"
    ]
    
    @staticmethod
    def show_log_menu():
        """Mostra il menu gestione log"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}📋 CONTROLLO LOG APPLICATIVI{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 🔍 Scopri log applicativi")
        print(f"2. 📖 Visualizza log file")
        print(f"3. 🔎 Ricerca nei log")
        print(f"4. 📊 Analisi log real-time")
        print(f"5. 📈 Statistiche log")
        print(f"6. ⚠️  Ricerca errori comuni")
        print(f"7. 🗂️  Gestione rotazione log")
        print(f"8. 📋 Report log completo")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def discover_logs():
        """Scopre i log applicativi nel sistema"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔍 SCOPERTA LOG APPLICATIVI{Colors.RESET}")
        print("=" * 60)
        
        discovered_logs = {}
        
        # Cerca in directory standard
        print(f"{Colors.CYAN}📁 Ricerca in directory standard...{Colors.RESET}")
        for log_dir in LogManager.LOG_DIRECTORIES:
            if "*" in log_dir:
                ret, out, err = SystemInfo.run_command(f"find {log_dir.replace('*', '')} -name '*.log' -type f 2>/dev/null | head -20")
            else:
                ret, out, err = SystemInfo.run_command(f"find {log_dir} -name '*.log' -type f 2>/dev/null | head -20")
            
            if ret == 0 and out.strip():
                log_files = out.strip().split('\n')
                if log_files:
                    discovered_logs[log_dir] = log_files
        
        # Cerca processi con log attivi
        print(f"\n{Colors.CYAN}🔍 Ricerca processi con log attivi...{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("lsof 2>/dev/null | grep '\\.log' | awk '{print $2, $9}' | sort -u")
        active_logs = []
        if ret == 0 and out.strip():
            active_logs = out.strip().split('\n')
        
        # Mostra risultati
        print(f"\n{Colors.WHITE}📊 LOG SCOPERTI:{Colors.RESET}")
        total_logs = 0
        
        for directory, logs in discovered_logs.items():
            if logs:
                print(f"\n{Colors.GREEN}📁 {directory}:{Colors.RESET}")
                for log in logs[:10]:  # Limita a 10 per directory
                    # Mostra info sul file
                    ret, out, err = SystemInfo.run_command(f"ls -lh '{log}' 2>/dev/null")
                    if ret == 0:
                        parts = out.split()
                        if len(parts) >= 5:
                            size = parts[4]
                            print(f"   📄 {log} ({size})")
                            total_logs += 1
                
                if len(logs) > 10:
                    print(f"   ... e altri {len(logs) - 10} file")
        
        if active_logs:
            print(f"\n{Colors.YELLOW}🔥 LOG CON PROCESSI ATTIVI:{Colors.RESET}")
            for log_info in active_logs[:15]:
                print(f"   {log_info}")
        
        # Servizi systemd con log
        print(f"\n{Colors.CYAN}⚙️  SERVIZI SYSTEMD CON LOG:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("systemctl list-units --type=service --state=active | grep -E '(apache|nginx|mysql|postgres|ssh|mail)' | awk '{print $1}'")
        if ret == 0 and out.strip():
            services = out.strip().split('\n')
            for service in services[:10]:
                print(f"   🔧 {service} (journalctl -u {service})")
        
        print(f"\n{Colors.GREEN}✅ Totale log scoperti: {total_logs}{Colors.RESET}")
        
        return discovered_logs
    
    @staticmethod
    def view_log_file():
        """Visualizza contenuto di un log file"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📖 VISUALIZZA LOG FILE{Colors.RESET}")
        print("=" * 60)
        
        # Scopri log prima
        discovered_logs = LogManager.discover_logs()
        
        # Lista file per selezione
        all_logs = []
        for directory, logs in discovered_logs.items():
            all_logs.extend(logs)
        
        if not all_logs:
            print(f"{Colors.YELLOW}⚠️  Nessun log file trovato{Colors.RESET}")
            return
        
        print(f"\n{Colors.WHITE}📋 Seleziona log file da visualizzare:{Colors.RESET}")
        for i, log in enumerate(all_logs[:20], 1):
            print(f"{i:2}. {log}")
        
        if len(all_logs) > 20:
            print(f"    ... e altri {len(all_logs) - 20} file")
        
        print(f"{Colors.WHITE}21. 📝 Inserisci percorso manuale{Colors.RESET}")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Seleziona opzione (1-21): {Colors.RESET}"))
            
            if choice == 21:
                log_path = input(f"{Colors.CYAN}Inserisci percorso completo: {Colors.RESET}")
            elif 1 <= choice <= min(20, len(all_logs)):
                log_path = all_logs[choice - 1]
            else:
                print(f"{Colors.RED}❌ Selezione non valida{Colors.RESET}")
                return
                
        except ValueError:
            print(f"{Colors.RED}❌ Input non valido{Colors.RESET}")
            return
        
        # Visualizza il log
        print(f"\n{Colors.WHITE}📄 Visualizzazione: {log_path}{Colors.RESET}")
        
        # Opzioni visualizzazione
        print(f"\n{Colors.CYAN}Modalità visualizzazione:{Colors.RESET}")
        print("1. Ultime 50 righe (tail -50)")
        print("2. Prime 50 righe (head -50)")
        print("3. Real-time (tail -f)")
        print("4. File completo (less)")
        
        view_mode = input(f"{Colors.CYAN}Modalità (1-4): {Colors.RESET}")
        
        if view_mode == "1":
            ret, out, err = SystemInfo.run_command(f"tail -50 '{log_path}'")
            if ret == 0:
                print(out)
            else:
                print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
        
        elif view_mode == "2":
            ret, out, err = SystemInfo.run_command(f"head -50 '{log_path}'")
            if ret == 0:
                print(out)
            else:
                print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
                
        elif view_mode == "3":
            print(f"{Colors.YELLOW}📡 Modalità real-time (Ctrl+C per uscire):{Colors.RESET}")
            try:
                SystemInfo.run_command(f"tail -f '{log_path}'", capture_output=False)
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}✅ Uscita da modalità real-time{Colors.RESET}")
        
        elif view_mode == "4":
            SystemInfo.run_command(f"less '{log_path}'", capture_output=False)
    
    @staticmethod
    def search_in_logs():
        """Ricerca nei log con pattern"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔎 RICERCA NEI LOG{Colors.RESET}")
        print("=" * 60)
        
        # Pattern di ricerca
        search_pattern = input(f"{Colors.CYAN}Inserisci pattern di ricerca (regex supportata): {Colors.RESET}")
        if not search_pattern:
            print(f"{Colors.RED}❌ Pattern non specificato{Colors.RESET}")
            return
        
        # Opzioni ricerca
        print(f"\n{Colors.WHITE}🔍 Opzioni ricerca:{Colors.RESET}")
        case_sensitive = input(f"Case sensitive? (y/N): ").lower() == 'y'
        
        # Periodo temporale
        print(f"\n{Colors.WHITE}📅 Filtro temporale:{Colors.RESET}")
        print("1. Ultima ora")
        print("2. Ultime 24 ore") 
        print("3. Ultima settimana")
        print("4. Nessun filtro")
        
        time_filter = input(f"{Colors.CYAN}Selezione (1-4): {Colors.RESET}")
        
        # Costruisci comando grep
        grep_cmd = "grep"
        if not case_sensitive:
            grep_cmd += " -i"
        
        grep_cmd += f" -r '{search_pattern}'"
        
        # Applica filtro temporale se necessario
        if time_filter in ["1", "2", "3"]:
            if time_filter == "1":
                find_time = "-mmin -60"
            elif time_filter == "2":
                find_time = "-mtime 0"
            else:  # time_filter == "3"
                find_time = "-mtime -7"
            
            search_cmd = f"find /var/log -type f {find_time} -exec {grep_cmd} {{}} +"
        else:
            search_cmd = f"{grep_cmd} /var/log/* 2>/dev/null"
        
        print(f"\n{Colors.BLUE}🔄 Ricerca in corso...{Colors.RESET}")
        ret, out, err = SystemInfo.run_command(search_cmd)
        
        if ret == 0 and out.strip():
            results = out.strip().split('\n')
            print(f"\n{Colors.GREEN}✅ Trovate {len(results)} occorrenze:{Colors.RESET}")
            
            # Mostra prime 50 risultati
            for i, result in enumerate(results[:50], 1):
                if ':' in result:
                    parts = result.split(':', 2)
                    if len(parts) >= 3:
                        file_path = parts[0]
                        line_num = parts[1] if parts[1].isdigit() else ""
                        content = parts[2] if len(parts) > 2 else parts[1]
                        
                        # Evidenzia il pattern trovato
                        highlighted = content.replace(search_pattern, f"{Colors.YELLOW}{Colors.BOLD}{search_pattern}{Colors.RESET}")
                        print(f"{i:3}. {Colors.CYAN}{file_path}{Colors.RESET}:{line_num} - {highlighted}")
                else:
                    print(f"{i:3}. {result}")
            
            if len(results) > 50:
                print(f"\n{Colors.YELLOW}... e altri {len(results) - 50} risultati{Colors.RESET}")
            
            # Statistiche per file
            file_counts = {}
            for result in results:
                if ':' in result:
                    file_path = result.split(':', 1)[0]
                    file_counts[file_path] = file_counts.get(file_path, 0) + 1
            
            if file_counts:
                print(f"\n{Colors.WHITE}📊 Occorrenze per file:{Colors.RESET}")
                sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)
                for file_path, count in sorted_files[:10]:
                    print(f"   {count:3} - {file_path}")
        else:
            print(f"{Colors.YELLOW}⚠️  Nessun risultato trovato per '{search_pattern}'{Colors.RESET}")
    
    @staticmethod
    def realtime_analysis():
        """Analisi log in tempo reale"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 ANALISI LOG REAL-TIME{Colors.RESET}")
        print("=" * 60)
        
        print(f"{Colors.WHITE}Seleziona modalità:{Colors.RESET}")
        print("1. 📡 Monitor log di sistema (journalctl -f)")
        print("2. 🌐 Monitor log web server")
        print("3. 🔒 Monitor log sicurezza")
        print("4. 📧 Monitor log mail")
        print("5. 🗃️  Monitor log personalizzato")
        
        mode = input(f"{Colors.CYAN}Modalità (1-5): {Colors.RESET}")
        
        try:
            if mode == "1":
                print(f"{Colors.GREEN}📡 Monitoring system logs (Ctrl+C per uscire)...{Colors.RESET}")
                SystemInfo.run_command("journalctl -f", capture_output=False)
            
            elif mode == "2":
                # Trova log web server
                web_logs = []
                for log_path in ["/var/log/apache2/access.log", "/var/log/nginx/access.log", "/var/log/httpd/access_log"]:
                    ret, out, err = SystemInfo.run_command(f"test -f '{log_path}'")
                    if ret == 0:
                        web_logs.append(log_path)
                
                if web_logs:
                    print(f"{Colors.GREEN}🌐 Monitoring web server logs (Ctrl+C per uscire)...{Colors.RESET}")
                    SystemInfo.run_command(f"tail -f {' '.join(web_logs)}", capture_output=False)
                else:
                    print(f"{Colors.YELLOW}⚠️  Nessun log web server trovato{Colors.RESET}")
            
            elif mode == "3":
                print(f"{Colors.GREEN}🔒 Monitoring security logs (Ctrl+C per uscire)...{Colors.RESET}")
                SystemInfo.run_command("tail -f /var/log/auth.log /var/log/secure 2>/dev/null", capture_output=False)
            
            elif mode == "4":
                print(f"{Colors.GREEN}📧 Monitoring mail logs (Ctrl+C per uscire)...{Colors.RESET}")
                SystemInfo.run_command("tail -f /var/log/mail.log /var/log/maillog 2>/dev/null", capture_output=False)
            
            elif mode == "5":
                log_path = input(f"{Colors.CYAN}Inserisci percorso log: {Colors.RESET}")
                if log_path:
                    print(f"{Colors.GREEN}📄 Monitoring {log_path} (Ctrl+C per uscire)...{Colors.RESET}")
                    SystemInfo.run_command(f"tail -f '{log_path}'", capture_output=False)
                    
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}✅ Monitoring terminato{Colors.RESET}")
    
    @staticmethod
    def log_statistics():
        """Statistiche sui log"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📈 STATISTICHE LOG{Colors.RESET}")
        print("=" * 60)
        
        # Statistiche generali
        print(f"\n{Colors.CYAN}📊 STATISTICHE GENERALI{Colors.RESET}")
        
        # Conteggio file log
        ret, out, err = SystemInfo.run_command("find /var/log -name '*.log' -type f | wc -l")
        if ret == 0:
            log_count = out.strip()
            print(f"File .log totali: {log_count}")
        
        # Spazio occupato
        ret, out, err = SystemInfo.run_command("du -sh /var/log")
        if ret == 0:
            log_size = out.split()[0]
            print(f"Spazio occupato da /var/log: {log_size}")
        
        # Log più grandi
        print(f"\n{Colors.CYAN}📊 LOG PIÙ GRANDI (top 10):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("find /var/log -type f -exec du -h {} + 2>/dev/null | sort -rh | head -10")
        if ret == 0:
            print(out)
        
        # Attività recente
        print(f"\n{Colors.CYAN}🕐 ATTIVITÀ RECENTE (file modificati nelle ultime 24h):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("find /var/log -type f -mtime 0 -exec ls -lth {} + 2>/dev/null | head -15")
        if ret == 0:
            print(out)
        
        # Errori comuni nelle ultime 24h
        print(f"\n{Colors.CYAN}⚠️  ERRORI COMUNI (ultime 24h):{Colors.RESET}")
        error_patterns = ["error", "Error", "ERROR", "fail", "FAIL", "exception", "Exception"]
        
        for pattern in error_patterns[:3]:  # Limita per performance
            ret, out, err = SystemInfo.run_command(f"find /var/log -type f -mtime 0 -exec grep -l '{pattern}' {{}} + 2>/dev/null | wc -l")
            if ret == 0:
                count = out.strip()
                if int(count) > 0:
                    print(f"File con '{pattern}': {count}")
    
    @staticmethod
    def search_common_errors():
        """Ricerca errori comuni"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}⚠️  RICERCA ERRORI COMUNI{Colors.RESET}")
        print("=" * 60)
        
        # Pattern di errori comuni
        error_patterns = {
            "Errori Autenticazione": ["authentication failed", "login failed", "invalid password", "access denied"],
            "Errori Connessione": ["connection refused", "connection timeout", "network unreachable", "host unreachable"],
            "Errori Filesystem": ["no space left", "permission denied", "file not found", "disk full"],
            "Errori Applicazione": ["segmentation fault", "core dumped", "fatal error", "critical error"],
            "Errori Sistema": ["kernel panic", "out of memory", "cpu lockup", "hardware error"]
        }
        
        print(f"{Colors.WHITE}Categorie disponibili:{Colors.RESET}")
        categories = list(error_patterns.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. Tutti gli errori")
        
        try:
            choice = int(input(f"\n{Colors.CYAN}Seleziona categoria (1-{len(categories) + 1}): {Colors.RESET}"))
            
            if choice == len(categories) + 1:
                # Cerca tutti gli errori
                search_patterns = []
                for patterns in error_patterns.values():
                    search_patterns.extend(patterns)
            elif 1 <= choice <= len(categories):
                selected_category = categories[choice - 1]
                search_patterns = error_patterns[selected_category]
                print(f"\n{Colors.GREEN}🔍 Ricerca: {selected_category}{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Selezione non valida{Colors.RESET}")
                return
                
        except ValueError:
            print(f"{Colors.RED}❌ Input non valido{Colors.RESET}")
            return
        
        # Esegui ricerca per ogni pattern
        all_results = {}
        for pattern in search_patterns:
            print(f"\n{Colors.BLUE}🔍 Ricerca '{pattern}'...{Colors.RESET}")
            ret, out, err = SystemInfo.run_command(f"grep -ri '{pattern}' /var/log/*.log 2>/dev/null | head -20")
            
            if ret == 0 and out.strip():
                results = out.strip().split('\n')
                all_results[pattern] = results
                
                print(f"{Colors.GREEN}✅ Trovate {len(results)} occorrenze per '{pattern}'{Colors.RESET}")
                
                # Mostra prime 5 per questo pattern
                for i, result in enumerate(results[:5], 1):
                    if ':' in result:
                        parts = result.split(':', 2)
                        if len(parts) >= 2:
                            file_path = parts[0]
                            content = parts[-1].strip()
                            print(f"  {i}. {Colors.CYAN}{file_path}{Colors.RESET}: {content}")
                
                if len(results) > 5:
                    print(f"    ... e altri {len(results) - 5} risultati")
        
        # Riepilogo
        if all_results:
            print(f"\n{Colors.WHITE}📊 RIEPILOGO ERRORI TROVATI:{Colors.RESET}")
            total_errors = sum(len(results) for results in all_results.values())
            print(f"Totale errori: {total_errors}")
            
            for pattern, results in all_results.items():
                if results:
                    print(f"  • {pattern}: {len(results)} occorrenze")
        else:
            print(f"\n{Colors.GREEN}✅ Nessun errore trovato per i pattern specificati{Colors.RESET}")
    
    @staticmethod
    def log_rotation_management():
        """Gestione rotazione log"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🗂️  GESTIONE ROTAZIONE LOG{Colors.RESET}")
        print("=" * 60)
        
        # Verifica logrotate
        print(f"\n{Colors.CYAN}⚙️  CONFIGURAZIONE LOGROTATE{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("which logrotate")
        if ret == 0:
            print(f"{Colors.GREEN}✅ logrotate installato{Colors.RESET}")
            
            # Mostra configurazione principale
            ret, out, err = SystemInfo.run_command("cat /etc/logrotate.conf")
            if ret == 0:
                print(f"\n{Colors.WHITE}📄 Configurazione principale (/etc/logrotate.conf):{Colors.RESET}")
                print(out)
            
            # Configurazioni aggiuntive
            print(f"\n{Colors.WHITE}📁 Configurazioni in /etc/logrotate.d/:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("ls -la /etc/logrotate.d/")
            if ret == 0:
                print(out)
        else:
            print(f"{Colors.YELLOW}⚠️  logrotate non installato{Colors.RESET}")
        
        # Status ultima rotazione
        print(f"\n{Colors.CYAN}📅 ULTIMA ROTAZIONE{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("cat /var/lib/logrotate/status 2>/dev/null || cat /var/lib/logrotate.status 2>/dev/null")
        if ret == 0:
            lines = out.split('\n')[:20]  # Prime 20 righe
            for line in lines:
                if line.strip():
                    print(line)
        else:
            print("Informazioni rotazione non disponibili")
        
        # Analisi log grandi che potrebbero necessitare rotazione
        print(f"\n{Colors.CYAN}🔍 LOG GRANDI (>100MB):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("find /var/log -type f -size +100M -exec ls -lh {} + 2>/dev/null")
        if ret == 0 and out.strip():
            print(out)
        else:
            print(f"{Colors.GREEN}✅ Nessun log file superiore a 100MB{Colors.RESET}")
        
        # Test configurazione logrotate
        if SystemInfo.check_root():
            print(f"\n{Colors.CYAN}🧪 TEST CONFIGURAZIONE{Colors.RESET}")
            print("1. Test configurazione logrotate")
            print("2. Rotazione forzata (dry-run)")
            print("3. Visualizza prossime rotazioni")
            
            test_choice = input(f"\n{Colors.CYAN}Opzione (1-3, INVIO per saltare): {Colors.RESET}")
            
            if test_choice == "1":
                ret, out, err = SystemInfo.run_command("logrotate -d /etc/logrotate.conf")
                if ret == 0:
                    print(f"{Colors.GREEN}✅ Configurazione valida{Colors.RESET}")
                else:
                    print(f"{Colors.RED}❌ Errori nella configurazione: {err}{Colors.RESET}")
            
            elif test_choice == "2":
                ret, out, err = SystemInfo.run_command("logrotate -d -f /etc/logrotate.conf | head -50")
                if ret == 0:
                    print(f"{Colors.WHITE}Simulazione rotazione forzata:{Colors.RESET}")
                    print(out)
        else:
            print(f"\n{Colors.YELLOW}⚠️  Privilegi di root richiesti per test configurazione{Colors.RESET}")

class SystemAuditManager:
    """Gestore per log di sistema e audit"""
    
    @staticmethod
    def show_audit_menu():
        """Mostra il menu log di sistema e audit"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}🔍 LOG DI SISTEMA E AUDIT{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 🖥️  Log di sistema (journalctl)")
        print(f"2. 🔐 Log di autenticazione")
        print(f"3. 🛡️  Log di sicurezza e audit")
        print(f"4. 👥 Attività utenti")
        print(f"5. 🔄 Log di boot e kernel")
        print(f"6. ⚠️  Analisi eventi critici")
        print(f"7. 📊 Statistiche sistema")
        print(f"8. 📋 Report audit completo")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def system_logs():
        """Visualizza e analizza log di sistema"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🖥️  LOG DI SISTEMA{Colors.RESET}")
        print("=" * 60)
        
        print(f"{Colors.WHITE}Opzioni disponibili:{Colors.RESET}")
        print("1. Ultime 50 entry del sistema")
        print("2. Log di oggi")
        print("3. Errori di sistema")
        print("4. Log per servizio specifico")
        print("5. Monitoring real-time")
        
        choice = input(f"{Colors.CYAN}Selezione (1-5): {Colors.RESET}")
        
        if choice == "1":
            print(f"\n{Colors.WHITE}📄 Ultime 50 entry del sistema:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("journalctl -n 50 --no-pager")
            if ret == 0:
                print(out)
            else:
                print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
        
        elif choice == "2":
            print(f"\n{Colors.WHITE}📅 Log di oggi:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("journalctl --since today --no-pager")
            if ret == 0:
                lines = out.split('\n')
                if len(lines) > 100:
                    print('\n'.join(lines[:50]))
                    print(f"\n{Colors.YELLOW}... [mostrate prime 50 righe di {len(lines)}]{Colors.RESET}")
                else:
                    print(out)
            else:
                print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
        
        elif choice == "3":
            print(f"\n{Colors.WHITE}⚠️  Errori di sistema:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("journalctl -p err --no-pager -n 100")
            if ret == 0:
                if out.strip():
                    print(out)
                else:
                    print(f"{Colors.GREEN}✅ Nessun errore recente trovato{Colors.RESET}")
            else:
                print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
        
        elif choice == "4":
            service_name = input(f"{Colors.CYAN}Nome del servizio: {Colors.RESET}")
            if service_name:
                print(f"\n{Colors.WHITE}📋 Log per servizio '{service_name}':{Colors.RESET}")
                ret, out, err = SystemInfo.run_command(f"journalctl -u {service_name} --no-pager -n 50")
                if ret == 0:
                    print(out)
                else:
                    print(f"{Colors.RED}❌ Errore: {err}{Colors.RESET}")
        
        elif choice == "5":
            print(f"{Colors.GREEN}📡 Monitoring real-time (Ctrl+C per uscire)...{Colors.RESET}")
            try:
                SystemInfo.run_command("journalctl -f", capture_output=False)
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}✅ Monitoring terminato{Colors.RESET}")
    
    @staticmethod
    def auth_logs():
        """Analizza log di autenticazione"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔐 LOG DI AUTENTICAZIONE{Colors.RESET}")
        print("=" * 60)
        
        # Login riusciti
        print(f"\n{Colors.CYAN}✅ LOGIN RIUSCITI (ultime 24h):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl --since '24 hours ago' | grep -i 'session opened' | tail -20")
        if ret == 0 and out.strip():
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {line}")
        else:
            print("Nessun login recente trovato")
        
        # Tentativi di login falliti
        print(f"\n{Colors.YELLOW}❌ TENTATIVI FALLITI:{Colors.RESET}")
        failed_patterns = ["authentication failure", "failed login", "invalid user", "failed password"]
        
        for pattern in failed_patterns:
            ret, out, err = SystemInfo.run_command(f"journalctl --since '24 hours ago' | grep -i '{pattern}' | wc -l")
            if ret == 0 and out.strip():
                count = int(out.strip())
                if count > 0:
                    print(f"  {pattern}: {count} tentativi")
                    
                    # Mostra alcuni esempi
                    ret2, out2, err2 = SystemInfo.run_command(f"journalctl --since '24 hours ago' | grep -i '{pattern}' | head -3")
                    if ret2 == 0 and out2.strip():
                        for line in out2.split('\n')[:3]:
                            if line.strip():
                                print(f"    → {line}")
        
        # Utenti più attivi
        print(f"\n{Colors.CYAN}👥 UTENTI PIÙ ATTIVI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl --since '24 hours ago' | grep 'session opened' | awk '{print $6}' | sort | uniq -c | sort -rn | head -10")
        if ret == 0 and out.strip():
            print("Count  User")
            print("=" * 15)
            print(out)
        
        # Connessioni SSH
        print(f"\n{Colors.CYAN}🔗 CONNESSIONI SSH:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl -u ssh --since '24 hours ago' | grep -E '(Accepted|Failed)' | tail -15")
        if ret == 0 and out.strip():
            for line in out.split('\n'):
                if 'Accepted' in line:
                    print(f"{Colors.GREEN}  ✅ {line}{Colors.RESET}")
                elif 'Failed' in line:
                    print(f"{Colors.RED}  ❌ {line}{Colors.RESET}")
        else:
            print("Nessuna attività SSH recente")
    
    @staticmethod
    def security_audit_logs():
        """Log di sicurezza e audit"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🛡️  LOG DI SICUREZZA E AUDIT{Colors.RESET}")
        print("=" * 60)
        
        # Verifica auditd
        ret, out, err = SystemInfo.run_command("systemctl is-active auditd 2>/dev/null")
        if ret == 0:
            print(f"{Colors.GREEN}✅ auditd attivo{Colors.RESET}")
            
            # Log audit recenti
            print(f"\n{Colors.CYAN}📋 LOG AUDIT RECENTI:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("ausearch -ts today 2>/dev/null | head -20")
            if ret == 0 and out.strip():
                print(out)
            else:
                print("Nessun evento audit recente")
            
            # Eventi di sicurezza
            print(f"\n{Colors.CYAN}🔍 EVENTI DI SICUREZZA:{Colors.RESET}")
            security_events = ["SYSCALL", "USER_LOGIN", "USER_AUTH", "CRED_ACQ", "USER_START"]
            
            for event in security_events:
                ret, out, err = SystemInfo.run_command(f"ausearch -m {event} -ts today 2>/dev/null | grep 'type=' | wc -l")
                if ret == 0 and out.strip():
                    count = int(out.strip())
                    if count > 0:
                        print(f"  {event}: {count} eventi")
        else:
            print(f"{Colors.YELLOW}⚠️  auditd non attivo{Colors.RESET}")
        
        # File di log di sicurezza alternativi
        print(f"\n{Colors.CYAN}📄 LOG DI SICUREZZA ALTERNATIVI:{Colors.RESET}")
        security_logs = ["/var/log/auth.log", "/var/log/secure", "/var/log/messages"]
        
        for log_file in security_logs:
            ret, out, err = SystemInfo.run_command(f"test -f {log_file}")
            if ret == 0:
                print(f"✅ {log_file}")
                
                # Analizza contenuto per eventi di sicurezza
                ret2, out2, err2 = SystemInfo.run_command(f"grep -i 'failed\\|error\\|denied' {log_file} | tail -5")
                if ret2 == 0 and out2.strip():
                    print(f"  Ultimi eventi di sicurezza:")
                    for line in out2.split('\n')[:3]:
                        if line.strip():
                            print(f"    {line}")
            else:
                print(f"❌ {log_file} non trovato")
        
        # Processi con privilegi elevati
        print(f"\n{Colors.CYAN}👑 PROCESSI CON PRIVILEGI ELEVATI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ps aux | awk '$1 == \"root\" {print $1, $2, $11}' | head -15")
        if ret == 0:
            print("USER  PID   COMMAND")
            print("=" * 30)
            print(out)
    
    @staticmethod
    def user_activity():
        """Analizza attività utenti"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}👥 ATTIVITÀ UTENTI{Colors.RESET}")
        print("=" * 60)
        
        # Utenti attualmente loggati
        print(f"\n{Colors.CYAN}👤 UTENTI CORRENTEMENTE LOGGATI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("w")
        if ret == 0:
            print(out)
        
        # Storico login
        print(f"\n{Colors.CYAN}📅 STORICO LOGIN (last 20):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("last -20")
        if ret == 0:
            print(out)
        
        # Utenti con accesso sudo
        print(f"\n{Colors.CYAN}🔐 UTENTI CON ACCESSO SUDO:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("getent group sudo | cut -d: -f4")
        if ret == 0 and out.strip():
            sudo_users = out.strip().split(',')
            for user in sudo_users:
                if user.strip():
                    print(f"  • {user.strip()}")
        
        ret, out, err = SystemInfo.run_command("getent group wheel | cut -d: -f4")
        if ret == 0 and out.strip():
            wheel_users = out.strip().split(',')
            print(f"\n{Colors.CYAN}⚙️  UTENTI NEL GRUPPO WHEEL:{Colors.RESET}")
            for user in wheel_users:
                if user.strip():
                    print(f"  • {user.strip()}")
        
        # Comandi sudo recenti
        print(f"\n{Colors.CYAN}⚡ COMANDI SUDO RECENTI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl | grep sudo | tail -10")
        if ret == 0 and out.strip():
            for line in out.split('\n'):
                if 'sudo' in line.lower():
                    print(f"  {line}")
        else:
            print("Nessun comando sudo recente trovato")
        
        # File di configurazione utenti modificati di recente
        print(f"\n{Colors.CYAN}📝 FILE UTENTI MODIFICATI (ultime 24h):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("find /home -name '.*' -mtime 0 -type f 2>/dev/null | head -10")
        if ret == 0 and out.strip():
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {line}")
        else:
            print("Nessun file utente modificato recentemente")
    
    @staticmethod
    def boot_kernel_logs():
        """Analizza log di boot e kernel"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🔄 LOG DI BOOT E KERNEL{Colors.RESET}")
        print("=" * 60)
        
        # Informazioni ultimo boot
        print(f"\n{Colors.CYAN}🚀 INFORMAZIONI ULTIMO BOOT:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl -b 0 | head -20")
        if ret == 0:
            print(out)
        
        # Messaggi kernel
        print(f"\n{Colors.CYAN}🐧 MESSAGGI KERNEL RECENTI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("dmesg | tail -15")
        if ret == 0:
            print(out)
        
        # Errori di boot
        print(f"\n{Colors.CYAN}❌ ERRORI DI BOOT:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl -b 0 -p err --no-pager")
        if ret == 0 and out.strip():
            lines = out.split('\n')
            if len(lines) > 20:
                print('\n'.join(lines[:20]))
                print(f"\n{Colors.YELLOW}... [mostrate prime 20 righe di {len(lines)}]{Colors.RESET}")
            else:
                print(out)
        else:
            print(f"{Colors.GREEN}✅ Nessun errore di boot trovato{Colors.RESET}")
        
        # Servizi falliti
        print(f"\n{Colors.CYAN}💥 SERVIZI FALLITI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("systemctl --failed --no-pager")
        if ret == 0:
            if "0 loaded units" in out:
                print(f"{Colors.GREEN}✅ Nessun servizio fallito{Colors.RESET}")
            else:
                print(out)
        
        # Hardware detection
        print(f"\n{Colors.CYAN}🔌 RILEVAMENTO HARDWARE:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("dmesg | grep -E '(USB|PCI|SATA|eth|wlan)' | tail -10")
        if ret == 0 and out.strip():
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {line}")
    
    @staticmethod
    def critical_events():
        """Analizza eventi critici"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}⚠️  ANALISI EVENTI CRITICI{Colors.RESET}")
        print("=" * 60)
        
        # Eventi critici nelle ultime 24h
        critical_patterns = [
            ("Kernel Panic", "kernel panic"),
            ("Out of Memory", "out of memory"),
            ("Disk Full", "no space left"),
            ("Hardware Error", "hardware error"),
            ("System Crash", "segmentation fault"),
            ("Network Error", "network unreachable"),
            ("Authentication Failure", "authentication failure")
        ]
        
        print(f"{Colors.WHITE}🔍 Ricerca eventi critici (ultime 24h):{Colors.RESET}")
        
        found_critical = False
        for event_name, pattern in critical_patterns:
            ret, out, err = SystemInfo.run_command(f"journalctl --since '24 hours ago' | grep -i '{pattern}' | wc -l")
            if ret == 0:
                count = int(out.strip())
                if count > 0:
                    found_critical = True
                    print(f"\n{Colors.RED}🚨 {event_name}: {count} occorrenze{Colors.RESET}")
                    
                    # Mostra esempi
                    ret2, out2, err2 = SystemInfo.run_command(f"journalctl --since '24 hours ago' | grep -i '{pattern}' | head -3")
                    if ret2 == 0 and out2.strip():
                        for line in out2.split('\n')[:3]:
                            if line.strip():
                                print(f"  → {line}")
        
        if not found_critical:
            print(f"{Colors.GREEN}✅ Nessun evento critico rilevato nelle ultime 24h{Colors.RESET}")
        
        # Controlli aggiuntivi
        print(f"\n{Colors.CYAN}🔍 CONTROLLI AGGIUNTIVI:{Colors.RESET}")
        
        # Load average alto
        ret, out, err = SystemInfo.run_command("uptime")
        if ret == 0:
            load_avg = out.split("load average:")[-1].strip().split(",")[0]
            try:
                load_val = float(load_avg)
                if load_val > 5:
                    print(f"{Colors.YELLOW}⚠️  Load average alto: {load_avg}{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}✅ Load average normale: {load_avg}{Colors.RESET}")
            except:
                print(f"Load average: {load_avg}")
        
        # Memoria bassa
        ret, out, err = SystemInfo.run_command("free | awk 'NR==2{printf \"%.2f%%\\n\", $3*100/$2}'")
        if ret == 0:
            mem_usage = float(out.strip().replace('%', ''))
            if mem_usage > 90:
                print(f"{Colors.RED}🚨 Utilizzo memoria critico: {mem_usage:.1f}%{Colors.RESET}")
            elif mem_usage > 80:
                print(f"{Colors.YELLOW}⚠️  Utilizzo memoria alto: {mem_usage:.1f}%{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}✅ Utilizzo memoria normale: {mem_usage:.1f}%{Colors.RESET}")
        
        # Spazio disco basso
        ret, out, err = SystemInfo.run_command("df / | awk 'NR==2{print $5}' | sed 's/%//'")
        if ret == 0:
            disk_usage = int(out.strip())
            if disk_usage > 95:
                print(f"{Colors.RED}🚨 Spazio disco critico: {disk_usage}%{Colors.RESET}")
            elif disk_usage > 85:
                print(f"{Colors.YELLOW}⚠️  Spazio disco alto: {disk_usage}%{Colors.RESET}")
            else:
                print(f"{Colors.GREEN}✅ Spazio disco normale: {disk_usage}%{Colors.RESET}")
    
    @staticmethod
    def system_statistics():
        """Statistiche del sistema"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 STATISTICHE SISTEMA{Colors.RESET}")
        print("=" * 60)
        
        # Statistiche generali log
        print(f"\n{Colors.CYAN}📈 STATISTICHE LOG:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl --disk-usage")
        if ret == 0:
            print(f"Utilizzo disco journal: {out.strip()}")
        
        # Conteggio messaggi per priorità
        priorities = {
            "emerg": "Emergenza",
            "alert": "Allarme", 
            "crit": "Critico",
            "err": "Errore",
            "warning": "Warning",
            "notice": "Notice",
            "info": "Info",
            "debug": "Debug"
        }
        
        print(f"\n{Colors.WHITE}📊 MESSAGGI PER PRIORITÀ (ultime 24h):{Colors.RESET}")
        for level, description in priorities.items():
            ret, out, err = SystemInfo.run_command(f"journalctl --since '24 hours ago' -p {level} | wc -l")
            if ret == 0:
                count = int(out.strip())
                if count > 0:
                    if level in ["emerg", "alert", "crit"]:
                        color = Colors.RED
                    elif level in ["err", "warning"]:
                        color = Colors.YELLOW
                    else:
                        color = Colors.GREEN
                    print(f"  {color}{description:10}: {count:6}{Colors.RESET}")
        
        # Top servizi per numero di log
        print(f"\n{Colors.CYAN}🔝 SERVIZI PIÙ VERBOSI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("journalctl --since '24 hours ago' -o json | jq -r '._SYSTEMD_UNIT' 2>/dev/null | grep -v null | sort | uniq -c | sort -rn | head -10")
        if ret != 0:  # Fallback se jq non è disponibile
            ret, out, err = SystemInfo.run_command("journalctl --since '24 hours ago' | awk '{print $5}' | sort | uniq -c | sort -rn | head -10")
        
        if ret == 0 and out.strip():
            print("Count   Service")
            print("=" * 25)
            print(out)
        
        # Uptime e boot history
        print(f"\n{Colors.CYAN}🕐 INFORMAZIONI TEMPORALI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("uptime -p")
        if ret == 0:
            print(f"Uptime: {out.strip()}")
        
        ret, out, err = SystemInfo.run_command("journalctl --list-boots | wc -l")
        if ret == 0:
            boot_count = out.strip()
            print(f"Numero di boot registrati: {boot_count}")
    
    @staticmethod
    def full_audit_report():
        """Report audit completo"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📋 REPORT AUDIT COMPLETO{Colors.RESET}")
        print("=" * 60)
        
        # Timestamp del report
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕐 Report generato: {current_time}")
        
        # Sommario sistema
        print(f"\n{Colors.CYAN}💻 SOMMARIO SISTEMA:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("uname -a")
        if ret == 0:
            print(f"Sistema: {out.strip()}")
        
        ret, out, err = SystemInfo.run_command("uptime")
        if ret == 0:
            print(f"Uptime: {out.strip()}")
        
        # Conteggio eventi per categoria
        print(f"\n{Colors.CYAN}📊 EVENTI SISTEMA (24h):{Colors.RESET}")
        
        event_categories = [
            ("Login riusciti", "journalctl --since '24 hours ago' | grep -i 'session opened' | wc -l"),
            ("Tentativi login falliti", "journalctl --since '24 hours ago' | grep -i 'authentication failure' | wc -l"),
            ("Comandi sudo", "journalctl --since '24 hours ago' | grep -i sudo | wc -l"),
            ("Errori sistema", "journalctl --since '24 hours ago' -p err | wc -l"),
            ("Warning", "journalctl --since '24 hours ago' -p warning | wc -l"),
        ]
        
        for category, command in event_categories:
            ret, out, err = SystemInfo.run_command(command)
            if ret == 0:
                count = out.strip()
                print(f"  {category:20}: {count}")
        
        # Riepilogo sicurezza
        print(f"\n{Colors.CYAN}🔒 RIEPILOGO SICUREZZA:{Colors.RESET}")
        
        # Utenti con privilegi
        ret, out, err = SystemInfo.run_command("getent group sudo | cut -d: -f4 | tr ',' '\n' | wc -l")
        if ret == 0:
            sudo_count = out.strip()
            print(f"  Utenti con sudo: {sudo_count}")
        
        # Servizi attivi
        ret, out, err = SystemInfo.run_command("systemctl list-units --type=service --state=active | wc -l")
        if ret == 0:
            active_services = int(out.strip()) - 1  # Rimuovi header
            print(f"  Servizi attivi: {active_services}")
        
        # Porte aperte
        ret, out, err = SystemInfo.run_command("ss -tuln | grep LISTEN | wc -l")
        if ret == 0:
            open_ports = out.strip()
            print(f"  Porte in ascolto: {open_ports}")
        
        # Raccomandazioni
        print(f"\n{Colors.CYAN}💡 RACCOMANDAZIONI:{Colors.RESET}")
        recommendations = []
        
        # Controlla log grandi
        ret, out, err = SystemInfo.run_command("find /var/log -name '*.log' -size +100M | wc -l")
        if ret == 0 and int(out.strip()) > 0:
            recommendations.append("Considera la rotazione dei log grandi (>100MB)")
        
        # Controlla servizi falliti
        ret, out, err = SystemInfo.run_command("systemctl --failed --quiet")
        if ret != 0:  # Ha servizi falliti
            recommendations.append("Verifica e ripara servizi falliti")
        
        # Controlla errori recenti
        ret, out, err = SystemInfo.run_command("journalctl --since '24 hours ago' -p err | wc -l")
        if ret == 0 and int(out.strip()) > 10:
            recommendations.append("Investiga errori di sistema frequenti")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        else:
            print(f"  {Colors.GREEN}✅ Sistema in buone condizioni{Colors.RESET}")

class SystemMonitor:
    """Gestore per monitoring sistema"""
    
    @staticmethod
    def show_monitoring_menu():
        """Mostra il menu monitoring sistema"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}📊 MONITORING SISTEMA{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 💻 Overview sistema tempo reale")
        print(f"2. 🧠 Monitoraggio CPU e processi")
        print(f"3. 💾 Monitoraggio memoria")
        print(f"4. 💽 Monitoraggio I/O disco")
        print(f"5. 🌡️  Temperature e sensori")
        print(f"6. ⚡ Processi e utilizzo risorse")
        print(f"7. 📈 Grafici performance")
        print(f"8. 🔔 Alert e soglie")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def system_overview():
        """Overview sistema in tempo reale"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}💻 OVERVIEW SISTEMA TEMPO REALE{Colors.RESET}")
        print("=" * 60)
        
        for i in range(10):  # 10 refresh invece di infinito
            # Clear screen per refresh
            os.system('clear')
            print(f"\n{Colors.BLUE}{Colors.BOLD}💻 OVERVIEW SISTEMA TEMPO REALE{Colors.RESET}")
            print("=" * 60)
            print(f"{Colors.YELLOW}⚠️  Refresh automatico ({10-i} rimanenti) - Ctrl+C per uscire{Colors.RESET}")
            print()
            
            # Timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🕐 Aggiornamento: {current_time}")
            print()
            
            # CPU
            ret, out, err = SystemInfo.run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | sed 's/%us,//'")
            if ret == 0:
                cpu_usage = out.strip()
                print(f"🧠 CPU: {cpu_usage}%")
            
            # Load Average
            ret, out, err = SystemInfo.run_command("uptime | awk -F'load average:' '{ print $2 }'")
            if ret == 0:
                load_avg = out.strip()
                print(f"📊 Load Average:{load_avg}")
            
            # Memoria
            ret, out, err = SystemInfo.run_command("free -m | awk 'NR==2{printf \"%.1f%% (%s/%s MB)\", $3*100/$2, $3, $2}'")
            if ret == 0:
                mem_info = out.strip()
                print(f"💾 Memoria: {mem_info}")
            
            # Disco
            ret, out, err = SystemInfo.run_command("df -h / | awk 'NR==2{printf \"%s/%s (%s)\", $3, $2, $5}'")
            if ret == 0:
                disk_info = out.strip()
                print(f"💽 Disco /: {disk_info}")
            
            # Processi top CPU
            print(f"\n{Colors.CYAN}🔥 TOP 5 PROCESSI CPU:{Colors.RESET}")
            ret, out, err = SystemInfo.run_command("ps aux --sort=-%cpu | head -6")
            if ret == 0:
                lines = out.split('\n')[1:6]  # Skip header
                for line in lines:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 11:
                            user = parts[0]
                            cpu = parts[2]
                            mem = parts[3]
                            command = ' '.join(parts[10:])[:40]
                            print(f"  {user:8} {cpu:5}% {mem:5}% {command}")
            
            try:
                time.sleep(3)
            except KeyboardInterrupt:
                print(f"\n{Colors.GREEN}✅ Monitoring terminato{Colors.RESET}")
                return
        
        print(f"\n{Colors.GREEN}✅ Monitoring completato{Colors.RESET}")
    
    @staticmethod
    def cpu_monitoring():
        """Monitoraggio CPU dettagliato"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🧠 MONITORAGGIO CPU E PROCESSI{Colors.RESET}")
        print("=" * 60)
        
        # Info CPU
        print(f"\n{Colors.CYAN}ℹ️  INFORMAZIONI CPU:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("lscpu | grep -E '(Model name|CPU\\(s\\)|Thread|Core|Socket)'")
        if ret == 0:
            print(out)
        
        # Top processi CPU
        print(f"\n{Colors.CYAN}🔥 TOP 15 PROCESSI CPU:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ps aux --sort=-%cpu | head -16")
        if ret == 0:
            print(out)
    
    @staticmethod
    def memory_monitoring():
        """Monitoraggio memoria"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}💾 MONITORAGGIO MEMORIA{Colors.RESET}")
        print("=" * 60)
        
        # Overview memoria
        print(f"\n{Colors.CYAN}📊 OVERVIEW MEMORIA:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("free -h")
        if ret == 0:
            print(out)
        
        # Top processi memoria
        print(f"\n{Colors.CYAN}🧠 TOP 15 PROCESSI MEMORIA:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("ps aux --sort=-%mem | head -16")
        if ret == 0:
            print(out)

class ServiceManager:
    """Gestore per servizi di sistema"""
    
    @staticmethod
    def show_service_menu():
        """Mostra il menu gestione servizi"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}⚙️  GESTIONE SERVIZI{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 📋 Lista tutti i servizi")
        print(f"2. ✅ Servizi attivi")
        print(f"3. ❌ Servizi falliti")
        print(f"4. 🔄 Start/Stop/Restart servizio")
        print(f"5. 🔧 Abilitazione servizio")
        print(f"6. 📊 Status dettagliato servizio")
        print(f"7. 📄 Log servizio")
        print(f"8. 🕐 Servizi con timer")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def list_all_services():
        """Lista tutti i servizi"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📋 LISTA TUTTI I SERVIZI{Colors.RESET}")
        print("=" * 60)
        
        ret, out, err = SystemInfo.run_command("systemctl list-units --type=service --all --no-pager")
        if ret == 0:
            lines = out.split('\n')
            if len(lines) > 50:
                print('\n'.join(lines[:50]))
                print(f"\n{Colors.YELLOW}... [mostrati primi 50 di {len(lines)} servizi]{Colors.RESET}")
            else:
                print(out)
        else:
            print(f"{Colors.RED}❌ Errore nel recuperare lista servizi{Colors.RESET}")
    
    @staticmethod
    def active_services():
        """Mostra servizi attivi"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}✅ SERVIZI ATTIVI{Colors.RESET}")
        print("=" * 60)
        
        ret, out, err = SystemInfo.run_command("systemctl list-units --type=service --state=active --no-pager")
        if ret == 0:
            print(out)
        else:
            print(f"{Colors.RED}❌ Errore nel recuperare servizi attivi{Colors.RESET}")
    
    @staticmethod
    def failed_services():
        """Mostra servizi falliti"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}❌ SERVIZI FALLITI{Colors.RESET}")
        print("=" * 60)
        
        ret, out, err = SystemInfo.run_command("systemctl list-units --type=service --state=failed --no-pager")
        if ret == 0:
            if "0 loaded units" in out:
                print(f"{Colors.GREEN}✅ Nessun servizio fallito{Colors.RESET}")
            else:
                print(out)
        else:
            print(f"{Colors.RED}❌ Errore nel recuperare servizi falliti{Colors.RESET}")

class SecurityManager:
    """Gestore per sicurezza e utenti"""
    
    @staticmethod
    def show_security_menu():
        """Mostra il menu sicurezza"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}🔒 SICUREZZA E UTENTI{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 👥 Gestione utenti")
        print(f"2. 🔑 Password e autenticazione")
        print(f"3. 🛡️  Permessi e sudo")
        print(f"4. 🔐 Chiavi SSH")
        print(f"5. 🔥 Firewall e iptables")
        print(f"6. 🚨 Eventi sicurezza")
        print(f"7. 📋 Audit sicurezza")
        print(f"8. 🔒 Hardening sistema")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def user_management():
        """Gestione utenti"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}👥 GESTIONE UTENTI{Colors.RESET}")
        print("=" * 60)
        
        # Lista utenti
        print(f"\n{Colors.CYAN}👤 UTENTI SISTEMA:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("awk -F: '$3>=1000 {print $1,$3,$5,$6}' /etc/passwd")
        if ret == 0:
            print("USER     UID   DESCRIPTION                    HOME")
            print("=" * 60)
            for line in out.split('\n'):
                if line.strip():
                    print(f"  {line}")
        
        # Utenti loggati
        print(f"\n{Colors.CYAN}🟢 UTENTI ATTUALMENTE LOGGATI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("who")
        if ret == 0:
            print(out)
        
        # Ultimo accesso
        print(f"\n{Colors.CYAN}📅 ULTIMI ACCESSI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("last -10")
        if ret == 0:
            print(out)

class MaintenanceManager:
    """Gestore per manutenzione sistema"""
    
    @staticmethod
    def show_maintenance_menu():
        """Mostra il menu manutenzione"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}🧹 MANUTENZIONE SISTEMA{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 🗑️  Pulizia sistema")
        print(f"2. 📦 Gestione pacchetti")
        print(f"3. 🔄 Aggiornamenti sistema")
        print(f"4. 📊 Controllo integrità")
        print(f"5. 💾 Backup configurazioni")
        print(f"6. 🔧 Ottimizzazioni")
        print(f"7. 📋 Report manutenzione")
        print(f"8. ⏰ Manutenzione programmata")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def system_cleanup():
        """Pulizia sistema"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}🗑️  PULIZIA SISTEMA{Colors.RESET}")
        print("=" * 60)
        
        # Spazio disco
        print(f"\n{Colors.CYAN}💽 UTILIZZO SPAZIO DISCO:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("df -h")
        if ret == 0:
            print(out)
        
        # File temporanei
        print(f"\n{Colors.CYAN}🗂️  FILE TEMPORANEI:{Colors.RESET}")
        temp_dirs = ["/tmp", "/var/tmp", "/var/cache"]
        for temp_dir in temp_dirs:
            ret, out, err = SystemInfo.run_command(f"du -sh {temp_dir} 2>/dev/null")
            if ret == 0:
                print(f"  {out.strip()}")
        
        # Log grandi
        print(f"\n{Colors.CYAN}📋 LOG FILES GRANDI (>10MB):{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("find /var/log -name '*.log' -size +10M -exec du -h {} \\; 2>/dev/null")
        if ret == 0 and out.strip():
            print(out)
        else:
            print(f"{Colors.GREEN}✅ Nessun log file grande trovato{Colors.RESET}")

class ReportManager:
    """Gestore per report e dashboard"""
    
    @staticmethod
    def show_report_menu():
        """Mostra il menu report"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}📈 REPORT E DASHBOARD{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 📊 Dashboard completo")
        print(f"2. 📋 Report giornaliero")
        print(f"3. 📈 Report settimanale")
        print(f"4. 💾 Export report")
        print(f"5. 📊 Statistiche utilizzo")
        print(f"6. 🔍 Report personalizzato")
        print(f"7. 📧 Configurazione email")
        print(f"8. 📅 Report programmati")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def complete_dashboard():
        """Dashboard completo sistema"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}📊 DASHBOARD COMPLETO{Colors.RESET}")
        print("=" * 60)
        
        # Header con timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🕐 Report generato: {current_time}")
        print()
        
        # Sistema base
        overview = SystemInfo.get_system_overview()
        print(f"{Colors.CYAN}💻 SISTEMA:{Colors.RESET}")
        for key, value in overview.items():
            print(f"  {key}: {value}")
        print()
        
        # Status servizi
        print(f"{Colors.CYAN}⚙️  SERVIZI:{Colors.RESET}")
        ret, out, err = SystemInfo.run_command("systemctl list-units --failed --no-pager | wc -l")
        if ret == 0:
            failed_count = int(out.strip()) - 1  # Remove header
            if failed_count > 0:
                print(f"  ❌ Servizi falliti: {failed_count}")
            else:
                print(f"  ✅ Tutti i servizi OK")
        
        # Rete
        ret, out, err = SystemInfo.run_command("ip route | grep default")
        if ret == 0:
            print(f"  🌐 Gateway: {out.split()[2] if len(out.split()) > 2 else 'N/A'}")
        
        # Alert
        print(f"\n{Colors.YELLOW}🚨 ALERT:{Colors.RESET}")
        alerts = []
        
        # Check memoria
        ret, out, err = SystemInfo.run_command("free | awk 'NR==2{print ($3/$2)*100}'")
        if ret == 0:
            mem_usage = float(out.strip())
            if mem_usage > 90:
                alerts.append(f"Memoria alta: {mem_usage:.1f}%")
        
        # Check disco
        ret, out, err = SystemInfo.run_command("df / | awk 'NR==2{print ($3/$2)*100}'")
        if ret == 0:
            disk_usage = float(out.strip())
            if disk_usage > 90:
                alerts.append(f"Disco pieno: {disk_usage:.1f}%")
        
        if alerts:
            for alert in alerts:
                print(f"  ⚠️  {alert}")
        else:
            print(f"  ✅ Nessun alert")

class ConfigManager:
    """Gestore per configurazioni tool"""
    
    @staticmethod
    def show_config_menu():
        """Mostra il menu configurazioni"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}⚙️  CONFIGURAZIONI TOOL{Colors.RESET}")
        print("=" * 50)
        print(f"{Colors.WHITE}1. 🎨 Impostazioni display")
        print(f"2. ⏰ Timeout e limiti")
        print(f"3. 📁 Percorsi personalizzati")
        print(f"4. 🔔 Soglie alert")
        print(f"5. 📧 Notifiche")
        print(f"6. 💾 Salva configurazione")
        print(f"7. 🔄 Ripristina default")
        print(f"8. ℹ️  Info versione")
        print(f"0. ↩️  Torna al menu principale")
        print(f"{Colors.RESET}")
    
    @staticmethod
    def version_info():
        """Informazioni versione"""
        print(f"\n{Colors.BLUE}{Colors.BOLD}ℹ️  INFORMAZIONI VERSIONE{Colors.RESET}")
        print("=" * 60)
        print(f"🚀 SysAdmin Helper v1.0")
        print(f"📅 Rilasciato: 2024")
        print(f"👨‍💻 Sviluppato per sistemisti Linux")
        print(f"🐍 Python: {sys.version}")
        print(f"💻 Piattaforma: {os.uname().system} {os.uname().release}")
        print(f"📁 Directory: {os.getcwd()}")

def main():
    """Funzione principale"""
    # Gestisci argomenti command line
    parser = argparse.ArgumentParser(description='SysAdmin Helper - Super Tool per Sistemisti Linux')
    parser.add_argument('--version', action='version', version='SysAdmin Helper v1.0')
    parser.add_argument('--monitor-daemon', action='store_true', help='Avvia in modalità daemon per monitoring continuo')
    args = parser.parse_args()
    
    if args.monitor_daemon:
        print("Modalità daemon non ancora implementata")
        sys.exit(1)
    
    menu = MenuSystem()
    lvm = LVMManager()
    net = NetworkManager()
    log = LogManager()
    audit = SystemAuditManager()
    monitor = SystemMonitor()
    service = ServiceManager()
    security = SecurityManager()
    maintenance = MaintenanceManager()
    report = ReportManager()
    config = ConfigManager()
    
    while True:
        try:
            menu.print_header()
            menu.show_main_menu()
            
            choice = menu.get_user_input()
            
            if choice == "0":
                print(f"{Colors.GREEN}👋 Grazie per aver usato SysAdmin Helper!{Colors.RESET}")
                sys.exit(0)
            
            elif choice == "1":
                while True:
                    menu.print_header()
                    lvm.show_lvm_menu()
                    lvm_choice = menu.get_user_input()
                    
                    if lvm_choice == "0":
                        break
                    elif lvm_choice == "1":
                        menu.clear_screen()
                        lvm.show_lvm_info()
                        menu.pause()
                    elif lvm_choice == "2":
                        menu.clear_screen()
                        lvm.show_available_disks()
                        menu.pause()
                    elif lvm_choice == "3":
                        menu.clear_screen()
                        lvm.expand_logical_volume()
                        menu.pause()
                    elif lvm_choice == "4":
                        menu.clear_screen()
                        lvm.check_filesystem_space()
                        menu.pause()
                    elif lvm_choice == "5":
                        menu.clear_screen()
                        lvm.storage_report()
                        menu.pause()
                    elif lvm_choice == "6":
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    elif lvm_choice == "7":
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "2":
                while True:
                    menu.print_header()
                    net.show_network_menu()
                    net_choice = menu.get_user_input()
                    
                    if net_choice == "0":
                        break
                    elif net_choice == "1":
                        menu.clear_screen()
                        net.show_network_interfaces()
                        menu.pause()
                    elif net_choice == "2":
                        menu.clear_screen()
                        net.network_diagnostics()
                        menu.pause()
                    elif net_choice == "3":
                        menu.clear_screen()
                        net.traffic_statistics()
                        menu.pause()
                    elif net_choice == "4":
                        menu.clear_screen()
                        net.ip_configuration()
                        menu.pause()
                    elif net_choice == "5":
                        menu.clear_screen()
                        net.routing_management()
                        menu.pause()
                    elif net_choice == "6":
                        menu.clear_screen()
                        net.dns_management()
                        menu.pause()
                    elif net_choice == "7":
                        menu.clear_screen()
                        net.firewall_status()
                        menu.pause()
                    elif net_choice == "8":
                        menu.clear_screen()
                        net.network_report()
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "3":
                while True:
                    menu.print_header()
                    log.show_log_menu()
                    log_choice = menu.get_user_input()
                    
                    if log_choice == "0":
                        break
                    elif log_choice == "1":
                        menu.clear_screen()
                        log.discover_logs()
                        menu.pause()
                    elif log_choice == "2":
                        menu.clear_screen()
                        log.view_log_file()
                        menu.pause()
                    elif log_choice == "3":
                        menu.clear_screen()
                        log.search_in_logs()
                        menu.pause()
                    elif log_choice == "4":
                        menu.clear_screen()
                        log.realtime_analysis()
                        menu.pause()
                    elif log_choice == "5":
                        menu.clear_screen()
                        log.log_statistics()
                        menu.pause()
                    elif log_choice == "6":
                        menu.clear_screen()
                        log.search_common_errors()
                        menu.pause()
                    elif log_choice == "7":
                        menu.clear_screen()
                        log.log_rotation_management()
                        menu.pause()
                    elif log_choice == "8":
                        print(f"{Colors.YELLOW}🚧 Report completo log in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "4":
                while True:
                    menu.print_header()
                    audit.show_audit_menu()
                    audit_choice = menu.get_user_input()
                    
                    if audit_choice == "0":
                        break
                    elif audit_choice == "1":
                        menu.clear_screen()
                        audit.system_logs()
                        menu.pause()
                    elif audit_choice == "2":
                        menu.clear_screen()
                        audit.auth_logs()
                        menu.pause()
                    elif audit_choice == "3":
                        menu.clear_screen()
                        audit.security_audit_logs()
                        menu.pause()
                    elif audit_choice == "4":
                        menu.clear_screen()
                        audit.user_activity()
                        menu.pause()
                    elif audit_choice == "5":
                        menu.clear_screen()
                        audit.boot_kernel_logs()
                        menu.pause()
                    elif audit_choice == "6":
                        menu.clear_screen()
                        audit.critical_events()
                        menu.pause()
                    elif audit_choice == "7":
                        menu.clear_screen()
                        audit.system_statistics()
                        menu.pause()
                    elif audit_choice == "8":
                        menu.clear_screen()
                        audit.full_audit_report()
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "5":
                while True:
                    menu.print_header()
                    monitor.show_monitoring_menu()
                    mon_choice = menu.get_user_input()
                    
                    if mon_choice == "0":
                        break
                    elif mon_choice == "1":
                        menu.clear_screen()
                        monitor.system_overview()
                        menu.pause()
                    elif mon_choice == "2":
                        menu.clear_screen()
                        monitor.cpu_monitoring()
                        menu.pause()
                    elif mon_choice == "3":
                        menu.clear_screen()
                        monitor.memory_monitoring()
                        menu.pause()
                    elif mon_choice in ["4", "5", "6", "7", "8"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "6":
                while True:
                    menu.print_header()
                    service.show_service_menu()
                    srv_choice = menu.get_user_input()
                    
                    if srv_choice == "0":
                        break
                    elif srv_choice == "1":
                        menu.clear_screen()
                        service.list_all_services()
                        menu.pause()
                    elif srv_choice == "2":
                        menu.clear_screen()
                        service.active_services()
                        menu.pause()
                    elif srv_choice == "3":
                        menu.clear_screen()
                        service.failed_services()
                        menu.pause()
                    elif srv_choice in ["4", "5", "6", "7", "8"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "7":
                while True:
                    menu.print_header()
                    security.show_security_menu()
                    sec_choice = menu.get_user_input()
                    
                    if sec_choice == "0":
                        break
                    elif sec_choice == "1":
                        menu.clear_screen()
                        security.user_management()
                        menu.pause()
                    elif sec_choice in ["2", "3", "4", "5", "6", "7", "8"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "8":
                while True:
                    menu.print_header()
                    maintenance.show_maintenance_menu()
                    mnt_choice = menu.get_user_input()
                    
                    if mnt_choice == "0":
                        break
                    elif mnt_choice == "1":
                        menu.clear_screen()
                        maintenance.system_cleanup()
                        menu.pause()
                    elif mnt_choice in ["2", "3", "4", "5", "6", "7", "8"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "9":
                while True:
                    menu.print_header()
                    report.show_report_menu()
                    rep_choice = menu.get_user_input()
                    
                    if rep_choice == "0":
                        break
                    elif rep_choice == "1":
                        menu.clear_screen()
                        report.complete_dashboard()
                        menu.pause()
                    elif rep_choice in ["2", "3", "4", "5", "6", "7", "8"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            elif choice == "10":
                while True:
                    menu.print_header()
                    config.show_config_menu()
                    cfg_choice = menu.get_user_input()
                    
                    if cfg_choice == "0":
                        break
                    elif cfg_choice == "8":
                        menu.clear_screen()
                        config.version_info()
                        menu.pause()
                    elif cfg_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                        print(f"{Colors.YELLOW}🚧 Funzionalità in sviluppo...{Colors.RESET}")
                        menu.pause()
                    else:
                        print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                        menu.pause()
            
            else:
                print(f"{Colors.RED}❌ Opzione non valida{Colors.RESET}")
                menu.pause()
                
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}👋 Uscita dal programma.{Colors.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{Colors.RED}❌ Errore: {e}{Colors.RESET}")
            menu.pause()

if __name__ == "__main__":
    main()