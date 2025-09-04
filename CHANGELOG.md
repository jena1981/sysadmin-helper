# Changelog

Tutti i cambiamenti notevoli di questo progetto saranno documentati in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-09-04

### Added
- **Modulo LVM e Filesystem**
  - Visualizzazione completa Physical Volumes, Volume Groups, Logical Volumes
  - Wizard guidato per espansione Logical Volumes
  - Resize automatico filesystem (ext4/xfs)
  - Verifica dischi disponibili per espansione
  - Controllo spazio filesystem con alert
  - Report storage completi con statistiche I/O

- **Modulo Gestione Rete**
  - Diagnostica completa connettività di rete
  - Test automatici (gateway, DNS, connettività Internet)
  - Statistiche traffico in tempo reale
  - Gestione routing e tabelle di routing
  - Configurazione IP e NetworkManager
  - Status firewall (iptables, ufw, firewalld)
  - Report completo rete

- **Modulo Log Applicativi**
  - Scoperta automatica log in tutto il sistema
  - Ricerca avanzata con supporto regex e filtri temporali
  - Visualizzazione real-time di log multipli
  - Ricerca errori comuni con categorizzazione
  - Gestione rotazione log con verifiche logrotate
  - Statistiche utilizzo e analisi performance

- **Modulo Log Sistema e Audit**
  - Integrazione completa journalctl per log systemd
  - Analisi autenticazione con rilevamento tentativi falliti
  - Audit di sicurezza con supporto auditd
  - Monitoraggio attività utenti e comandi sudo
  - Log boot, kernel e rilevamento hardware
  - Rilevamento automatico eventi critici
  - Report audit completi

- **Modulo Monitoring Sistema**
  - Overview sistema in tempo reale
  - Monitoraggio CPU dettagliato con info processi
  - Monitoraggio memoria con analisi utilizzo
  - Dashboard interattivo con refresh automatico

- **Modulo Gestione Servizi**
  - Lista completa servizi systemd
  - Visualizzazione servizi attivi e falliti
  - Status dettagliato servizi
  - Interfaccia per start/stop/restart servizi

- **Modulo Sicurezza e Utenti**
  - Gestione completa utenti sistema
  - Lista utenti con UID e descrizioni
  - Utenti attualmente loggati
  - Storico accessi (last)

- **Modulo Manutenzione Sistema**
  - Analisi completa utilizzo spazio disco
  - Identificazione file temporanei e log grandi
  - Pulizia sistema guidata
  - Report manutenzione

- **Modulo Report e Dashboard**
  - Dashboard completo sistema con timestamp
  - Report con informazioni sistema integrate
  - Alert automatici per soglie critiche
  - Statistiche utilizzo sistema

- **Modulo Configurazioni Tool**
  - Informazioni complete versione e sistema
  - Info Python e piattaforma
  - Interfaccia per configurazioni future

- **Sistema Core**
  - Interfaccia a menu colorata e intuitiva
  - Sistema di navigazione gerarchico
  - Gestione errori user-friendly
  - Supporto Ctrl+C per uscita sicura
  - Controllo privilegi automatico
  - Header dinamico con info sistema
  - Supporto argomenti command line (--version, --help)

- **Documentazione e Deploy**
  - README completo con esempi
  - Script di installazione automatico
  - Suite di test completa
  - Documentazione funzionalità
  - Sistema di deployment

### Technical Details
- **Linguaggio**: Python 3.6+
- **Architettura**: Modulare con classi manager separate
- **Righe di codice**: 2500+
- **Funzioni implementate**: 60+
- **Compatibilità**: Tutte le distribuzioni Linux moderne
- **Dipendenze**: Solo librerie standard Python + comandi sistema

### Installation
```bash
chmod +x install.sh
sudo ./install.sh
```

### Usage
```bash
sysadmin-helper
# o
sah
```