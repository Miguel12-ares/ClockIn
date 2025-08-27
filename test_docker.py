#!/usr/bin/env python3
"""
Script para probar la aplicación ClockIn en Docker
"""
import os
import sys

def test_docker_config():
    """Prueba la configuración para Docker"""
    try:
        print("🔍 Probando configuración para Docker...")
        
        # Simular entorno Docker
        os.environ['DATABASE_URL'] = 'mysql+pymysql://user:pass@db:3306/db_name'
        os.environ['FLASK_ENV'] = 'production'
        
        from app.config import Config
        from app import app, db
        
        print(f"✅ URL de base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("✅ Configuración de Docker correcta")
        return True
    except Exception as e:
        print(f"❌ Error en configuración de Docker: {e}")
        return False

def test_local_config():
    """Prueba la configuración para desarrollo local"""
    try:
        print("🔍 Probando configuración para desarrollo local...")
        
        # Limpiar variables de entorno
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        
        from app.config import Config
        from app import app, db
        
        print(f"✅ URL de base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("✅ Configuración local correcta")
        return True
    except Exception as e:
        print(f"❌ Error en configuración local: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Probando configuraciones de ClockIn")
    print("=" * 50)
    
    tests = [
        test_local_config,
        test_docker_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las configuraciones funcionan correctamente!")
        return 0
    else:
        print("❌ Algunas configuraciones fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
