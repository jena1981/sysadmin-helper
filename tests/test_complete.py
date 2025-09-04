#!/usr/bin/env python3
"""
Test completo per verificare le funzionalità principali del SysAdmin Helper
"""

import sys
import os

# Aggiungi il path corrente
sys.path.insert(0, '.')

def test_imports():
    """Test import moduli"""
    try:
        from sysadmin_helper import (
            SystemInfo, MenuSystem, LVMManager, NetworkManager, 
            LogManager, SystemAuditManager, SystemMonitor, ServiceManager,
            SecurityManager, MaintenanceManager, ReportManager, ConfigManager
        )
        print("✅ Import moduli: OK")
        return True
    except Exception as e:
        print(f"❌ Import moduli: FAIL - {e}")
        return False

def test_system_info():
    """Test SystemInfo"""
    try:
        from sysadmin_helper import SystemInfo
        
        # Test get_system_overview
        overview = SystemInfo.get_system_overview()
        if isinstance(overview, dict) and 'os' in overview:
            print("✅ SystemInfo.get_system_overview(): OK")
        else:
            print("❌ SystemInfo.get_system_overview(): FAIL")
            return False
        
        # Test run_command
        ret, out, err = SystemInfo.run_command("echo test")
        if ret == 0 and "test" in out:
            print("✅ SystemInfo.run_command(): OK")
        else:
            print("❌ SystemInfo.run_command(): FAIL")
            return False
            
        return True
    except Exception as e:
        print(f"❌ SystemInfo: FAIL - {e}")
        return False

def test_managers():
    """Test basic manager functionality"""
    try:
        from sysadmin_helper import (
            LVMManager, NetworkManager, LogManager, 
            SystemAuditManager, SystemMonitor, ServiceManager,
            SecurityManager, MaintenanceManager, ReportManager, ConfigManager
        )
        
        managers = [
            ("LVMManager", LVMManager),
            ("NetworkManager", NetworkManager), 
            ("LogManager", LogManager),
            ("SystemAuditManager", SystemAuditManager),
            ("SystemMonitor", SystemMonitor),
            ("ServiceManager", ServiceManager),
            ("SecurityManager", SecurityManager),
            ("MaintenanceManager", MaintenanceManager),
            ("ReportManager", ReportManager),
            ("ConfigManager", ConfigManager)
        ]
        
        for name, manager_class in managers:
            # Test che la classe abbia il metodo show_*_menu
            menu_methods = [method for method in dir(manager_class) if method.startswith('show_') and method.endswith('_menu')]
            if menu_methods:
                print(f"✅ {name}: OK (metodi menu trovati)")
            else:
                print(f"❌ {name}: FAIL (nessun metodo menu)")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Managers test: FAIL - {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TEST COMPLETO SYSADMIN HELPER")
    print("=" * 50)
    
    tests = [
        ("Import moduli", test_imports),
        ("SystemInfo", test_system_info),
        ("Managers", test_managers)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        if test_func():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RISULTATI:")
    print(f"✅ Test superati: {passed}")
    print(f"❌ Test falliti: {failed}")
    
    if failed == 0:
        print("🎉 TUTTI I TEST SUPERATI!")
        return True
    else:
        print("⚠️  ALCUNI TEST FALLITI")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)