# Esempi di Utilizzo - SysAdmin Helper

## 🚀 Esempi Pratici d'Uso

### 1. 💾 Espansione Logical Volume

**Scenario**: Il filesystem `/home` è pieno al 95% e deve essere espanso.

```bash
# Avvia il tool
sysadmin-helper

# Naviga nel menu
Menu Principale → 1. Gestione LVM → 3. Espandi Logical Volume

# Il wizard ti guiderà attraverso:
# 1. Selezione del LV da espandere (es. /dev/vg0/home)
# 2. Verifica spazio disponibile nel Volume Group
# 3. Inserimento dimensione da aggiungere (es. +10G)
# 4. Conferma operazione (scrivi "CONFERMA")
# 5. Espansione automatica LV e filesystem
```

**Risultato**: Il filesystem `/home` viene espanso automaticamente senza downtime.

### 2. 🌐 Diagnostica Problemi di Rete

**Scenario**: Il server ha problemi di connettività e devi identificare la causa.

```bash
sysadmin-helper

Menu Principale → 2. Gestione Rete → 2. Diagnostica connettività

# Test automatici eseguiti:
# ✅ Test ping gateway
# ✅ Verifica risoluzione DNS  
# ✅ Test connettività Internet
# ✅ Porte in ascolto
# ❌ Possibili problemi identificati
```

**Risultato**: Identifichi immediatamente se il problema è gateway, DNS o connettività.

### 3. 📋 Ricerca Errori nei Log

**Scenario**: L'applicazione ha problemi e devi trovare errori nei log.

```bash
sysadmin-helper

Menu Principale → 3. Log Applicativi → 6. Ricerca errori comuni

# Selezione categoria:
# 1. Errori Autenticazione
# 2. Errori Connessione  
# 3. Errori Filesystem
# 4. Errori Applicazione ← Seleziona questa
# 5. Errori Sistema

# Output automatico:
# ✅ Trovate 15 occorrenze per 'fatal error'
# ✅ Trovate 8 occorrenze per 'segmentation fault'
# 📊 File con più errori: /var/log/app.log (12 errori)
```

**Risultato**: Identifichi rapidamente i log problematici e la tipologia di errori.

### 4. 🔍 Monitoraggio Sistema Real-time

**Scenario**: Vuoi monitorare le performance del server in tempo reale.

```bash
sysadmin-helper

Menu Principale → 5. Monitoring Sistema → 1. Overview tempo reale

# Dashboard aggiornato ogni 3 secondi:
# 🧠 CPU: 45.2%
# 📊 Load Average: 2.1, 1.8, 1.5  
# 💾 Memoria: 78.5% (6.2G/8G)
# 💽 Disco: 12G/50G (24%)
# 
# 🔥 TOP 5 PROCESSI CPU:
# apache2  15.2%  2.1%  /usr/sbin/apache2
# mysql    12.8%  8.4%  /usr/sbin/mysqld
# ...
```

**Risultato**: Hai una vista real-time delle performance con processi più impattanti.

### 5. ⚙️ Gestione Servizi Falliti

**Scenario**: Dopo un riavvio, alcuni servizi non si sono avviati correttamente.

```bash
sysadmin-helper

Menu Principale → 6. Gestione Servizi → 3. Servizi falliti

# Output:
# ❌ SERVIZI FALLITI:
# ● nginx.service - loaded failed failed
# ● mysql.service - loaded failed failed
# 
# 📋 Dettagli servizi falliti:
# nginx.service: Main process exited, code=exited, status=1
# mysql.service: Unit not found
```

**Risultato**: Identifichi immediatamente quali servizi hanno problemi e perché.

### 6. 👥 Controllo Attività Utenti

**Scenario**: Vuoi verificare chi ha accesso al server e le ultime attività.

```bash
sysadmin-helper

Menu Principale → 7. Sicurezza e Utenti → 1. Gestione utenti

# Output:
# 👤 UTENTI SISTEMA:
# user1    1001  Developer Account      /home/user1
# user2    1002  Admin Account          /home/user2
# 
# 🟢 UTENTI ATTUALMENTE LOGGATI:
# user1    pts/0   10.0.0.50   14:30
# 
# 📅 ULTIMI ACCESSI:
# user1    pts/0   10.0.0.50   Wed Sep  4 14:30
# user2    ssh     10.0.0.100  Wed Sep  4 09:15
```

**Risultato**: Hai visibilità completa su utenti e accessi al sistema.

### 7. 🧹 Pulizia Sistema

**Scenario**: Il server sta esaurendo lo spazio disco e serve una pulizia.

```bash
sysadmin-helper

Menu Principale → 8. Manutenzione Sistema → 1. Pulizia sistema

# Analisi automatica:
# 💽 UTILIZZO SPAZIO DISCO:
# Filesystem      Size  Used Avail Use%
# /dev/sda1       50G   45G   3.8G  92%  ← Critico!
# 
# 🗂️ FILE TEMPORANEI:
# /tmp           245M
# /var/tmp       1.2G
# /var/cache     890M
# 
# 📋 LOG FILES GRANDI (>10MB):
# 125M  /var/log/syslog
# 89M   /var/log/apache2/access.log
# 234M  /var/log/mysql/mysql.log
```

**Risultato**: Identifichi rapidamente cosa sta occupando spazio e dove intervenire.

### 8. 📊 Dashboard Completo

**Scenario**: Vuoi un report completo dello stato del server.

```bash
sysadmin-helper

Menu Principale → 9. Report e Dashboard → 1. Dashboard completo

# 🕐 Report generato: 2024-09-04 15:30:45
# 
# 💻 SISTEMA:
# os: Ubuntu 20.04.3 LTS
# uptime: up 2 days, 14 hours, 23 minutes  
# memory_total: 8.0G
# disk_usage: 34%
# 
# ⚙️ SERVIZI:
# ✅ Tutti i servizi OK
# 
# 🌐 Gateway: 192.168.1.1
# 
# 🚨 ALERT:
# ✅ Nessun alert
```

**Risultato**: Hai un report completo dello stato del server con eventuali alert.

## 💡 **Tips per l'Uso Ottimale**

### **Per Sistemisti Junior:**
- Inizia sempre dal Dashboard (opzione 9.1) per avere una panoramica
- Usa le funzioni di diagnostica automatica per identificare problemi
- I wizard guidati ti accompagnano passo-passo nelle operazioni critiche

### **Per Sistemisti Senior:**
- Usa le funzioni di ricerca avanzata nei log (opzione 3.3)
- Combina monitoring real-time con analisi dei servizi
- Sfrutta i report per documentare lo stato dei server

### **Per Troubleshooting:**
1. **Dashboard completo** (9.1) - Panoramica generale
2. **Diagnostica rete** (2.2) - Se problemi di connettività  
3. **Servizi falliti** (6.3) - Se servizi non funzionanti
4. **Ricerca errori** (3.6) - Per problemi applicativi
5. **Eventi critici** (4.6) - Per problemi di sistema

### **Per Manutenzione Preventiva:**
1. **Pulizia sistema** (8.1) - Libera spazio disco
2. **Controllo LVM** (1.4) - Verifica spazio filesystem
3. **Log grandi** (3.5) - Controlla crescita log
4. **Monitoring** (5.1) - Performance generale