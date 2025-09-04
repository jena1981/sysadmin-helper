#!/bin/bash
#
# Script per deploy automatico su GitHub
# 
# IMPORTANTE: Prima di eseguire questo script:
# 1. Crea un nuovo repository su GitHub chiamato "sysadmin-helper"  
# 2. Sostituisci YOUR_USERNAME con il tuo username GitHub
# 3. Assicurati di aver configurato Git con le tue credenziali

set -e

# Colori per output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 DEPLOY SYSADMIN HELPER SU GITHUB${NC}"
echo "========================================"

# Controlla che siamo nella directory corretta
if [ ! -f "sysadmin_helper.py" ]; then
    echo -e "${YELLOW}❌ Errore: Esegui questo script nella directory del tool${NC}"
    exit 1
fi

echo -e "${GREEN}📋 Step 1: Configurazione Git...${NC}"

# Inizializza Git se non già fatto
if [ ! -d ".git" ]; then
    echo "Inizializzazione repository Git..."
    git init
fi

# Chiedi username GitHub se non è configurato
if ! git config user.name >/dev/null 2>&1; then
    read -p "Inserisci il tuo nome per Git: " git_name
    git config user.name "$git_name"
fi

if ! git config user.email >/dev/null 2>&1; then
    read -p "Inserisci la tua email per Git: " git_email
    git config user.email "$git_email"
fi

read -p "Inserisci il tuo username GitHub: " github_username

if [ -z "$github_username" ]; then
    echo -e "${YELLOW}❌ Username GitHub richiesto${NC}"
    exit 1
fi

echo -e "${GREEN}📦 Step 2: Pulizia e preparazione...${NC}"

# Rimuovi cache se esistente
rm -rf __pycache__

echo -e "${GREEN}📁 Step 3: Aggiunta file...${NC}"
git add .

echo -e "${GREEN}💾 Step 4: Commit iniziale...${NC}"
git commit -m "🎉 Initial release: SysAdmin Helper v1.0

Complete Linux Administration Tool with:
- ✅ LVM management with guided expansion
- ✅ Advanced network diagnostics  
- ✅ Application log discovery and search
- ✅ System audit and security logging
- ✅ Real-time system monitoring
- ✅ SystemD service management
- ✅ User and security management
- ✅ System maintenance and cleanup
- ✅ Complete dashboard and reporting
- ✅ Professional deployment ready

🚀 2500+ lines of code, 60+ functions, 10 complete modules
Ready for production deployment on Linux servers!"

echo -e "${GREEN}🔗 Step 5: Connessione al repository GitHub...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${github_username}/sysadmin-helper.git"

echo -e "${GREEN}⬆️  Step 6: Push su GitHub...${NC}"
git branch -M main
git push -u origin main

echo
echo -e "${GREEN}✅ DEPLOY COMPLETATO!${NC}"
echo "========================================"
echo -e "🌐 Repository: ${BLUE}https://github.com/${github_username}/sysadmin-helper${NC}"
echo
echo -e "${YELLOW}📋 Prossimi passi:${NC}"
echo "1. Vai su GitHub e verifica che tutti i file siano stati caricati"
echo "2. Crea una release da GitHub: Releases → Create a new release"
echo "3. Tagga come v1.0.0 e pubblica"
echo "4. Condividi il link con il tuo team!"
echo
echo -e "${GREEN}🎉 Il tuo super-tool è ora pubblico su GitHub!${NC}"