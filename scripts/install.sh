#!/bin/bash
#
# SysAdmin Helper - Script di Installazione
# Installa il super-tool su tutti i server Linux dell'azienda
#

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzioni
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              SYSADMIN HELPER - INSTALLAZIONE                 ║"
    echo "║                  Super Tool Installer                       ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        warn "Script non eseguito come root. Alcune funzionalità potrebbero non funzionare."
        read -p "Continuare comunque? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

check_dependencies() {
    log "Verifica dipendenze..."
    
    # Python 3 richiesto
    if ! command -v python3 &> /dev/null; then
        error "Python 3 non trovato. Installare Python 3 prima di procedere."
    fi
    
    # Comandi opzionali ma raccomandati
    OPTIONAL_DEPS=("lsof" "ss" "journalctl" "systemctl" "lvm" "pvdisplay" "vgdisplay" "lvdisplay")
    MISSING_DEPS=()
    
    for dep in "${OPTIONAL_DEPS[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            MISSING_DEPS+=("$dep")
        fi
    done
    
    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        warn "Dipendenze opzionali mancanti (alcune funzionalità potrebbero essere limitate):"
        printf '%s\n' "${MISSING_DEPS[@]}"
        echo
    fi
    
    log "✅ Verifica dipendenze completata"
}

install_tool() {
    log "Installazione SysAdmin Helper..."
    
    # Directory di installazione
    INSTALL_DIR="/usr/local/bin"
    INSTALL_PATH="$INSTALL_DIR/sysadmin-helper"
    
    # Copia il file principale
    if [ -f "sysadmin_helper.py" ]; then
        cp sysadmin_helper.py "$INSTALL_PATH"
        chmod +x "$INSTALL_PATH"
        log "✅ Tool installato in $INSTALL_PATH"
    else
        error "File sysadmin_helper.py non trovato nella directory corrente"
    fi
    
    # Crea link simbolico per facilità d'uso
    if [ ! -L "/usr/local/bin/sah" ]; then
        ln -s "$INSTALL_PATH" "/usr/local/bin/sah"
        log "✅ Alias 'sah' creato"
    fi
    
    # Verifica installazione
    if "$INSTALL_PATH" --version &> /dev/null; then
        log "✅ Installazione verificata"
    else
        warn "Installazione completata ma test di verifica fallito"
    fi
}

create_config() {
    log "Creazione configurazione predefinita..."
    
    CONFIG_DIR="/etc/sysadmin-helper"
    CONFIG_FILE="$CONFIG_DIR/config.conf"
    
    # Crea directory di configurazione
    mkdir -p "$CONFIG_DIR"
    
    # File di configurazione base
    cat > "$CONFIG_FILE" << 'EOF'
# SysAdmin Helper Configuration
# Configurazione per il super-tool

[general]
# Colori abilitati (true/false)
colors_enabled = true

# Timeout per i comandi (secondi)
command_timeout = 30

# Log level (debug, info, warning, error)
log_level = info

[paths]
# Directory aggiuntive per la ricerca log
additional_log_paths = /opt/app/logs,/home/app/logs

# Directory temporanea
temp_dir = /tmp/sysadmin-helper

[monitoring]
# Soglie per alert automatici
memory_threshold = 80
disk_threshold = 85
load_threshold = 5.0

[security]
# Abilita controlli di sicurezza aggiuntivi
enhanced_security = true

# File da monitorare per modifiche
watch_files = /etc/passwd,/etc/shadow,/etc/sudoers
EOF

    chmod 644 "$CONFIG_FILE"
    log "✅ Configurazione creata in $CONFIG_FILE"
}

setup_systemd_service() {
    log "Configurazione servizio systemd (opzionale)..."
    
    read -p "Vuoi installare un servizio systemd per monitoring continuo? (y/N) " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SERVICE_FILE="/etc/systemd/system/sysadmin-helper-monitor.service"
        
        cat > "$SERVICE_FILE" << EOF
[Unit]
Description=SysAdmin Helper Monitoring Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/local/bin/sysadmin-helper --monitor-daemon
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF
        
        systemctl daemon-reload
        log "✅ Servizio systemd configurato (usa 'systemctl enable sysadmin-helper-monitor' per abilitarlo)"
    fi
}

print_post_install() {
    echo
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                 INSTALLAZIONE COMPLETATA!                   ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
    echo "🚀 Per avviare il tool utilizza uno di questi comandi:"
    echo "   • sysadmin-helper"
    echo "   • sah                (alias breve)"
    echo "   • python3 /usr/local/bin/sysadmin-helper"
    echo
    echo "📁 File di configurazione:"
    echo "   • /etc/sysadmin-helper/config.conf"
    echo
    echo "📖 Funzionalità principali disponibili:"
    echo "   • 💾 Gestione LVM e Filesystem"
    echo "   • 🌐 Gestione Interfacce di Rete"
    echo "   • 📋 Controllo Log Applicativi"
    echo "   • 🔍 Log di Sistema e Audit"
    echo "   • 📊 Monitoring Sistema"
    echo "   • ⚙️  Gestione Servizi"
    echo "   • 🔒 Sicurezza e Utenti"
    echo "   • 🧹 Manutenzione Sistema"
    echo
    echo "💡 Suggerimenti:"
    echo "   • Esegui come root per funzionalità complete"
    echo "   • Usa Ctrl+C per uscire da qualsiasi operazione"
    echo "   • I log sono accessibili in tempo reale"
    echo
}

# Main
main() {
    print_header
    
    log "Avvio installazione SysAdmin Helper..."
    
    check_root
    check_dependencies
    install_tool
    create_config
    setup_systemd_service
    
    print_post_install
    
    log "🎉 Installazione completata con successo!"
}

# Verifica se script è eseguito direttamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi