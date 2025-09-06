# SysAdmin Helper v1.0

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-green.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

**Super Tool per Sistemisti Linux** - Un tool completo e user-friendly per semplificare l'amministrazione dei server Linux, progettato per sistemisti di tutti i livelli di esperienza.

## 🚀 Caratteristiche Principali

### 💾 Gestione LVM e Filesystem
- **Visualizzazione completa** di Physical Volumes, Volume Groups e Logical Volumes
- **Espansione guidata** di Logical Volumes con resize automatico del filesystem
- **Verifica spazio** filesystem con alert per utilizzo critico
- **Gestione dischi** - rilevamento dischi disponibili per espansione
- **Report storage** completi con statistiche I/O

### 🌐 Gestione Interfacce di Rete
- **Diagnostica completa** della connettività di rete
- **Monitoraggio traffico** con statistiche dettagliate
- **Configurazione IP** e gestione NetworkManager
- **Gestione routing** e tabelle di routing
- **DNS e risoluzione nomi** con test automatici
- **Status firewall** (iptables, ufw, firewalld)

### 📋 Controllo Log Applicativi
- **Scoperta automatica** di tutti i log applicativi nel sistema
- **Ricerca avanzata** con supporto regex e filtri temporali
- **Visualizzazione real-time** di log multipli
- **Ricerca errori comuni** con categorizzazione automatica
- **Gestione rotazione log** con verifiche logrotate
- **Statistiche utilizzo** e analisi performance

### 🔍 Log di Sistema e Audit
- **Integrazione journalctl** completa per log systemd
- **Analisi autenticazione** con rilevamento tentativi falliti
- **Audit di sicurezza** con supporto auditd
- **Monitoraggio attività utenti** e comandi sudo
- **Log boot e kernel** con rilevamento hardware
- **Rilevamento eventi critici** automatico

### 📊 Funzionalità Aggiuntive
- **Dashboard stato sistema** in tempo reale
- **Report automatici** esportabili
- **Interfaccia colorata** e user-friendly
- **Controlli di sicurezza** integrati
- **Supporto multi-distribuzione** Linux

## 📋 Requisiti di Sistema

### Requisiti Minimi
- **Sistema Operativo**: Linux (qualsiasi distribuzione moderna)
- **Python**: 3.6 o superiore
- **RAM**: 512 MB
- **Spazio Disco**: 50 MB

### Dipendenze Consigliate
```bash
# Comandi base (solitamente preinstallati)
lsblk, df, free, ps, ss, lsof, mount, umount

# Gestione LVM
lvm2, pvdisplay, vgdisplay, lvdisplay

# Gestione rete
iproute2, net-tools, bind-utils

# Log di sistema
systemd, journalctl

# Opzionali (per funzionalità avanzate)
vnstat, iostat, auditd
```

## 🔧 Installazione

### Installazione Automatica (Consigliata)
```bash
# Clona o scarica il repository
git clone https://github.com/your-org/sysadmin-helper.git
cd sysadmin-helper

# Esegui l'installer (richiede privilegi root)
sudo ./install.sh
```

### Installazione Manuale
```bash
# Copia il file principale
sudo cp sysadmin_helper.py /usr/local/bin/sysadmin-helper
sudo chmod +x /usr/local/bin/sysadmin-helper

# Crea alias per facilità d'uso
sudo ln -s /usr/local/bin/sysadmin-helper /usr/local/bin/sah

# Crea directory di configurazione
sudo mkdir -p /etc/sysadmin-helper
```

### Verifica Installazione
```bash
# Test rapido
sysadmin-helper --version
# oppure
sah --version
```

## 🎯 Utilizzo

### Avvio Tool
```bash
# Metodi di avvio equivalenti
sysadmin-helper
sah
python3 /usr/local/bin/sysadmin-helper
```

### Esempi d'Uso

#### 1. Espansione LVM
```
Menu Principale → 1. Gestione LVM → 3. Espandi Logical Volume
```
Il wizard ti guiderà attraverso:
- Selezione del Logical Volume da espandere
- Verifica spazio disponibile nel Volume Group
- Inserimento dimensione da aggiungere (+5G, +100%FREE, etc.)
- Espansione automatica del filesystem (ext4/xfs)

#### 2. Diagnostica Rete
```
Menu Principale → 2. Gestione Rete → 2. Diagnostica connettività
```
Esegue automaticamente:
- Test ping al gateway
- Verifica risoluzione DNS
- Test connettività Internet
- Lista porte in ascolto

#### 3. Ricerca Log
```
Menu Principale → 3. Log Applicativi → 3. Ricerca nei log
```
Permette di:
- Inserire pattern di ricerca (supporta regex)
- Filtrare per periodo temporale
- Visualizzare risultati con highlighting
- Statistiche per file

#### 4. Monitoraggio Real-time
```
Menu Principale → 4. Log Sistema → 1. Log di sistema → 5. Monitoring real-time
```
Mostra log di sistema in tempo reale con `journalctl -f`

## ⚙️ Configurazione

### File di Configurazione
Il file principale di configurazione si trova in:
```
/etc/sysadmin-helper/config.conf
```

### Configurazioni Principali
```ini
[general]
# Abilita/disabilita colori
colors_enabled = true

# Timeout comandi (secondi)  
command_timeout = 30

[paths]
# Directory aggiuntive per ricerca log
additional_log_paths = /opt/app/logs,/home/app/logs

[monitoring]
# Soglie per alert
memory_threshold = 80
disk_threshold = 85
load_threshold = 5.0
```

## 🔒 Sicurezza

### Privilegi
- **Funzionamento base**: Può essere eseguito da utente normale
- **Funzionalità complete**: Richiede privilegi root per:
  - Espansione LVM
  - Visualizzazione completa log di sicurezza
  - Modifiche configurazione rete
  - Access completo ai log di audit

### Best Practices
- Esegui sempre come root sui server di produzione
- Monitora l'accesso al tool tramite sudo logging
- Revoca l'accesso quando non più necessario
- Usa il tool in combinazione con altri strumenti di monitoring

## 📊 Esempi Screenshot

### Menu Principale
```
╔══════════════════════════════════════════════════════════════╗
║                    SYSADMIN HELPER v1.0                     ║
║              Super Tool per Sistemisti Linux                ║
╚══════════════════════════════════════════════════════════════╝

📊 Sistema: Ubuntu 20.04.3 LTS
⏰ Uptime: up 2 days, 14 hours, 23 minutes
💾 Memoria: 2.1G/8.0G (Libera: 5.2G)  
💽 Disco /: 45G/100G (45%)
📈 Load Avg: 0.15 0.18 0.22

🏠 MENU PRINCIPALE
==================================================
1.  💾 Gestione LVM e Filesystem
2.  🌐 Gestione Interfacce di Rete
3.  📋 Controllo Log Applicativi
4.  🔍 Log di Sistema e Audit
5.  📊 Monitoring Sistema
6.  ⚙️  Gestione Servizi
7.  🔒 Sicurezza e Utenti
8.  🧹 Manutenzione Sistema
9.  📈 Report e Dashboard
10. ⚙️  Configurazioni Tool
0.  ❌ Esci
```

## 🔧 Sviluppo e Contributi

### Struttura Codice
```
sysadmin-helper/
├── sysadmin_helper.py      # Tool principale
├── install.sh              # Script di installazione
├── README.md               # Documentazione
├── examples/               # Esempi di configurazione
└── docs/                  # Documentazione estesa
```

### Aggiungere Nuove Funzionalità
1. Crea una nuova classe Manager (es. `ServiceManager`)
2. Implementa i metodi statici per le funzionalità
3. Aggiungi il menu nella classe `MenuSystem`
4. Integra nel `main()` loop

### Esempio Nuovo Modulo
```python
class ServiceManager:
    @staticmethod
    def show_service_menu():
        print("Menu servizi...")
    
    @staticmethod 
    def list_services():
        # Implementa funzionalità
        pass
```

## 🐛 Troubleshooting

### Problemi Comuni

#### "Permission denied" su operazioni LVM
**Soluzione**: Esegui il tool come root
```bash
sudo sah
```

#### Log non trovati
**Soluzione**: Verifica i percorsi nei log e aggiungi directory personalizzate in `/etc/sysadmin-helper/config.conf`

#### Comandi non trovati
**Soluzione**: Installa i pacchetti necessari:
```bash
# Ubuntu/Debian
sudo apt-get install lvm2 net-tools bind-utils

# RHEL/CentOS
sudo yum install lvm2 net-tools bind-utils
```

### Log di Debug
Per debug avanzato, modifica il livello di log in `config.conf`:
```ini
[general]
log_level = debug
```

## 📈 Roadmap

### Versione 1.1 (Planned)
- [ ] Modulo completo gestione servizi systemd
- [ ] Backup automatico configurazioni
- [ ] Integrazione monitoring (Nagios/Zabbix)
- [ ] Export report in PDF/HTML

### Versione 1.2 (Future)
- [ ] Interfaccia web opzionale  
- [ ] API REST per automazione
- [ ] Plugin system
- [ ] Multi-server management

## 📝 Changelog

### v1.0.0 (Current)
- ✅ Gestione completa LVM con espansione guidata
- ✅ Diagnostica rete avanzata
- ✅ Controllo log applicativi con ricerca
- ✅ Audit log di sistema completo
- ✅ Interfaccia colorata e user-friendly
- ✅ Sistema di installazione automatico

## 🤝 Supporto

### Problemi e Bug
Segnala problemi tramite:
- **Issue Tracker**: [GitHub Issues](https://github.com/your-org/sysadmin-helper/issues)
- **Email**: valerio.franconi0@gmail.com

### Richieste Funzionalità
Le richieste di nuove funzionalità sono benvenute! Usa il template nel repository.

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per dettagli.

---

## 🙏 Riconoscimenti

Grazie a tutti i sistemisti che hanno contribuito con feedback e suggerimenti per rendere questo tool più completo e user-friendly.

**Sviluppato con ❤️ per la community dei sistemisti Linux**
