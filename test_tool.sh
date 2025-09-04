#!/bin/bash
#
# Test Suite per SysAdmin Helper
# Verifica le funzionalità principali del tool
#

set -e

# Colori
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TOOL="./sysadmin_helper.py"
TESTS_PASSED=0
TESTS_FAILED=0

log_test() {
    echo -e "${BLUE}[TEST] $1${NC}"
}

log_pass() {
    echo -e "${GREEN}[PASS] $1${NC}"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL] $1${NC}"
    ((TESTS_FAILED++))
}

log_warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        SYSADMIN HELPER - TEST SUITE          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo

# Test 1: Verifica esistenza file
log_test "Verifica esistenza file principale"
if [ -f "$TOOL" ]; then
    log_pass "File sysadmin_helper.py esistente"
else
    log_fail "File sysadmin_helper.py non trovato"
fi

# Test 2: Verifica sintassi Python
log_test "Verifica sintassi Python"
if python3 -m py_compile "$TOOL" 2>/dev/null; then
    log_pass "Sintassi Python corretta"
else
    log_fail "Errori di sintassi Python"
fi

# Test 3: Test import moduli
log_test "Test import moduli Python"
if python3 -c "import sys; sys.path.insert(0, '.'); import sysadmin_helper" 2>/dev/null; then
    log_pass "Import moduli riuscito"
else
    log_fail "Errore nell'import dei moduli"
fi

# Test 4: Test argomento --version
log_test "Test argomento --version"
if python3 "$TOOL" --version 2>/dev/null | grep -q "SysAdmin Helper v1.0"; then
    log_pass "Argomento --version funzionante"
else
    log_fail "Argomento --version non funzionante"
fi

# Test 5: Test argomento --help
log_test "Test argomento --help"
if python3 "$TOOL" --help 2>/dev/null | grep -q "SysAdmin Helper"; then
    log_pass "Argomento --help funzionante"
else
    log_fail "Argomento --help non funzionante"
fi

# Test 6: Test avvio tool (timeout)
log_test "Test avvio interfaccia (3 secondi)"
if timeout 3 python3 "$TOOL" 2>/dev/null | grep -q "SYSADMIN HELPER v1.0"; then
    log_pass "Tool si avvia correttamente"
else
    log_fail "Errore nell'avvio del tool"
fi

# Test 7: Verifica dipendenze sistema
log_test "Verifica dipendenze sistema critiche"
missing_deps=0

critical_commands=("python3" "ls" "df" "free" "ps")
for cmd in "${critical_commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        log_warn "Comando critico mancante: $cmd"
        ((missing_deps++))
    fi
done

if [ $missing_deps -eq 0 ]; then
    log_pass "Tutte le dipendenze critiche sono presenti"
else
    log_warn "$missing_deps dipendenze critiche mancanti"
fi

# Test 8: Test funzioni di sistema
log_test "Test funzioni di sistema base"
if python3 -c "
import sys
sys.path.insert(0, '.')
from sysadmin_helper import SystemInfo
info = SystemInfo.get_system_overview()
print('OS:', info.get('os', 'N/A'))
print('Memory:', info.get('memory_total', 'N/A'))
" 2>/dev/null | grep -E "(OS|Memory)"; then
    log_pass "Funzioni di sistema funzionanti"
else
    log_fail "Errore nelle funzioni di sistema"
fi

# Test 9: Test permessi file
log_test "Test permessi file"
if [ -x "$TOOL" ]; then
    log_pass "File ha permessi di esecuzione"
else
    log_warn "File non ha permessi di esecuzione (chmod +x necessario)"
fi

# Test 10: Test script di installazione
log_test "Test script di installazione"
if [ -f "install.sh" ] && [ -x "install.sh" ]; then
    log_pass "Script di installazione presente e eseguibile"
else
    log_warn "Script di installazione mancante o non eseguibile"
fi

echo
echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              RISULTATI TEST                   ║${NC}"  
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo -e "${GREEN}Test Superati: $TESTS_PASSED${NC}"
echo -e "${RED}Test Falliti:  $TESTS_FAILED${NC}"

total_tests=$((TESTS_PASSED + TESTS_FAILED))
if [ $total_tests -gt 0 ]; then
    success_rate=$(( (TESTS_PASSED * 100) / total_tests ))
    echo -e "${BLUE}Tasso di successo: ${success_rate}%${NC}"
fi

echo
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 TUTTI I TEST SUPERATI! Il tool è pronto per l'uso.${NC}"
    exit 0
else
    echo -e "${RED}❌ Alcuni test sono falliti. Controlla gli errori sopra.${NC}"
    exit 1
fi