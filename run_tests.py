#!/usr/bin/env python3
"""
Script para ejecutar pruebas de integración del sistema ClockIn
"""

import subprocess
import sys
import os

def run_tests():
    """Ejecuta las pruebas de integración"""
    print("🧪 Ejecutando pruebas de integración para ClockIn...")
    print("=" * 60)
    
    # Verificar que pytest esté instalado
    try:
        import pytest
    except ImportError:
        print("❌ Error: pytest no está instalado")
        print("Instala pytest con: pip install pytest")
        return False
    
    # Ejecutar pruebas
    test_files = [
        "tests/test_auth_integration.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Ejecutando pruebas en: {test_file}")
            print("-" * 40)
            
            result = subprocess.run([
                sys.executable, "-m", "pytest", 
                test_file, "-v", "--tb=short"
            ], capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print("Errores:")
                print(result.stderr)
            
            if result.returncode != 0:
                print(f"❌ Las pruebas en {test_file} fallaron")
                return False
        else:
            print(f"⚠️  Archivo de prueba no encontrado: {test_file}")
    
    print("\n✅ Todas las pruebas completadas")
    return True

def main():
    """Función principal"""
    print("ClockIn - Sistema de Pruebas de Integración")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("\n💥 Algunas pruebas fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()
