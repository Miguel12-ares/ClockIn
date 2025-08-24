#!/usr/bin/env python3
"""
Script de prueba para el módulo de administración de ClockIn
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_admin_endpoints():
    """Prueba los endpoints principales del módulo de administración"""
    
    print("🧪 Iniciando pruebas del módulo de administración...")
    print("=" * 50)
    
    # Test 1: Dashboard
    print("\n1. Probando Dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/admin/dashboard")
        if response.status_code == 200:
            print("✅ Dashboard accesible")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al dashboard: {e}")
    
    # Test 2: Lista de usuarios
    print("\n2. Probando lista de usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/admin/users")
        if response.status_code == 200:
            print("✅ Lista de usuarios accesible")
        else:
            print(f"❌ Error en lista de usuarios: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando a lista de usuarios: {e}")
    
    # Test 3: Formulario de creación
    print("\n3. Probando formulario de creación...")
    try:
        response = requests.get(f"{BASE_URL}/admin/users/create")
        if response.status_code == 200:
            print("✅ Formulario de creación accesible")
        else:
            print(f"❌ Error en formulario de creación: {response.status_code}")
    except Exception as e:
        print(f"❌ Error conectando al formulario: {e}")
    
    # Test 4: Crear usuario de prueba
    print("\n4. Probando creación de usuario...")
    test_user_data = {
        'idDocumento': '12345678',
        'first_name': 'Usuario',
        'last_name': 'Prueba',
        'user_type_id': '1',
        'zona_id': '1',
        'estado_id': '1',
        'is_active': 'true'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/admin/users/create", data=test_user_data)
        if response.status_code in [200, 302]:  # 302 es redirect después de crear
            print("✅ Usuario de prueba creado exitosamente")
        else:
            print(f"❌ Error creando usuario: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error en creación de usuario: {e}")
    
    # Test 5: Verificar que el usuario aparece en la lista
    print("\n5. Verificando usuario en lista...")
    try:
        response = requests.get(f"{BASE_URL}/admin/users?search=12345678")
        if response.status_code == 200:
            if "12345678" in response.text:
                print("✅ Usuario encontrado en la lista")
            else:
                print("⚠️ Usuario no encontrado en la lista (puede ser normal si hay paginación)")
        else:
            print(f"❌ Error buscando usuario: {response.status_code}")
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Pruebas completadas")

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\n🔍 Probando conexión a base de datos...")
    
    try:
        from app import app, db
        from app.models.user_type import UserType
        from app.models.zona import Zona
        from app.models.estado import Estado
        
        with app.app_context():
            # Verificar que las tablas existen
            user_types = UserType.query.all()
            zonas = Zona.query.all()
            estados = Estado.query.all()
            
            print(f"✅ Conexión exitosa")
            print(f"   - Tipos de usuario: {len(user_types)}")
            print(f"   - Zonas: {len(zonas)}")
            print(f"   - Estados: {len(estados)}")
            
            # Mostrar datos básicos
            if user_types:
                print(f"   - Tipos disponibles: {[ut.type_name for ut in user_types]}")
            if zonas:
                print(f"   - Zonas disponibles: {[z.nombre for z in zonas]}")
            if estados:
                print(f"   - Estados disponibles: {[e.nombre for e in estados]}")
                
    except Exception as e:
        print(f"❌ Error en conexión a BD: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando pruebas del sistema ClockIn - Módulo de Administración")
    print("Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    print("=" * 60)
    
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando 3 segundos para que el servidor esté listo...")
    time.sleep(3)
    
    # Probar conexión a BD
    test_database_connection()
    
    # Probar endpoints
    test_admin_endpoints()
    
    print("\n" + "=" * 60)
    print("📋 Resumen de pruebas:")
    print("- Si ves ✅, la funcionalidad está operativa")
    print("- Si ves ❌, hay un problema que necesita atención")
    print("- Si ves ⚠️, es una advertencia menor")
    print("\n🎯 Para acceder al panel administrativo:")
    print("   http://localhost:5000/admin/dashboard")
    print("   http://localhost:5000/admin/users")

if __name__ == "__main__":
    main()
