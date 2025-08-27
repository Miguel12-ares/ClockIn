#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación ClockIn se inicie correctamente
"""
import sys
import os

def test_app_import():
    """Prueba que la aplicación se pueda importar sin errores"""
    try:
        print("Probando importación de la aplicación...")
        from app import app, db
        print("Aplicación importada correctamente")
        return True
    except Exception as e:
        print(f"Error al importar la aplicación: {e}")
        return False

def test_models_import():
    """Prueba que todos los modelos se puedan importar"""
    try:
        print("Probando importación de modelos...")
        from app.models.user import User
        from app.models.user_type import UserType
        from app.models.zona import Zona
        from app.models.estado import Estado
        from app.models.access_log import AccessLog
        from app.models.active_session import ActiveSession
        from app.models.anomaly import Anomaly
        from app.models.system_audit import SystemAudit
        from app.models.admin_zona import AdminZona
        print("Todos los modelos importados correctamente")
        return True
    except Exception as e:
        print(f"Error al importar modelos: {e}")
        return False

def test_blueprints_import():
    """Prueba que todos los blueprints se puedan importar"""
    try:
        print("Probando importación de blueprints...")
        from app.controllers.user import user_bp
        from app.controllers.zona import zona_bp
        from app.controllers.user_type import user_type_bp
        from app.controllers.estado import estado_bp
        from app.controllers.admin_zona import admin_zona_bp
        from app.controllers.access_log import access_log_bp
        from app.controllers.active_session import active_session_bp
        from app.controllers.anomaly import anomaly_bp
        from app.controllers.system_audit import system_audit_bp
        from app.controllers.auth import bp as auth_bp
        from app.controllers.admin import admin_bp
        print("Todos los blueprints importados correctamente")
        return True
    except Exception as e:
        print(f"Error al importar blueprints: {e}")
        return False

def test_app_config():
    """Prueba la configuración de la aplicación"""
    try:
        print("Probando configuración de la aplicación...")
        from app import app
        from app.config import Config
        
        # Verificar configuración básica
        assert app.config['SECRET_KEY'] is not None, "SECRET_KEY no configurada"
        assert app.config['SQLALCHEMY_DATABASE_URI'] is not None, "DATABASE_URL no configurada"
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False, "SQLALCHEMY_TRACK_MODIFICATIONS debe ser False"
        
        print("Configuración de la aplicación correcta")
        return True
    except Exception as e:
        print(f"Error en la configuración: {e}")
        return False

def test_routes_registration():
    """Prueba que las rutas estén registradas correctamente"""
    try:
        print("Probando registro de rutas...")
        from app import app
        
        # Verificar que no hay endpoints duplicados
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.endpoint)
        
        # Verificar duplicados
        duplicates = [route for route in set(routes) if routes.count(route) > 1]
        if duplicates:
            print(f"Endpoints duplicados encontrados: {duplicates}")
            return False
        
        print(f"{len(routes)} rutas registradas correctamente")
        return True
    except Exception as e:
        print(f"Error al verificar rutas: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de la aplicación ClockIn")
    print("=" * 50)
    
    tests = [
        test_app_import,
        test_models_import,
        test_blueprints_import,
        test_app_config,
        test_routes_registration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("Todas las pruebas pasaron. La aplicación está lista para ejecutarse.")
        print("Ejecuta: python run.py")
        return 0
    else:
        print("Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
