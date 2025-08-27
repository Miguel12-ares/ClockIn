#!/usr/bin/env python3
"""
Script para probar la configuración de Docker de ClockIn
"""
import os
import sys

def test_docker_config():
    """Prueba la configuración para Docker"""
    try:
        print("Probando configuracion para Docker...")
        
        # Simular entorno Docker
        os.environ['DATABASE_URL'] = 'mysql+pymysql://user:pass@db:3306/db_name'
        os.environ['FLASK_ENV'] = 'production'
        os.environ['ADMIN_MODE'] = 'true'
        
        from app.config import Config
        from app import app, db
        
        print(f"URL de base de datos: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"SECRET_KEY configurada: {app.config['SECRET_KEY'] is not None}")
        print(f"ADMIN_MODE: {app.config['ADMIN_MODE']}")
        print("Configuracion de Docker correcta")
        return True
    except Exception as e:
        print(f"Error en configuracion de Docker: {e}")
        return False

def test_models_import():
    """Prueba que todos los modelos se puedan importar"""
    try:
        print("Probando importacion de modelos...")
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
        print("Probando importacion de blueprints...")
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
    print("Probando configuracion de Docker para ClockIn")
    print("=" * 60)
    
    tests = [
        test_docker_config,
        test_models_import,
        test_blueprints_import,
        test_routes_registration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("Todas las pruebas pasaron! La aplicacion esta lista para Docker.")
        print("\nComandos para ejecutar en Docker:")
        print("1. Construir y ejecutar: docker-compose up --build")
        print("2. Solo ejecutar: docker-compose up")
        print("3. Ejecutar en segundo plano: docker-compose up -d")
        print("4. Ver logs: docker-compose logs -f")
        print("5. Detener: docker-compose down")
        print("\nURLs de acceso:")
        print("- Aplicacion principal: http://localhost:5000")
        print("- Panel administrativo: http://localhost:5000/admin/dashboard")
        print("- Gestion de usuarios: http://localhost:5000/admin/users")
        print("- Login de usuarios: http://localhost:5000/auth/login")
        return 0
    else:
        print("Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
