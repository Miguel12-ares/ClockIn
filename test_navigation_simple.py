#!/usr/bin/env python3
"""
Script simple para probar la navegación del dashboard y gestión de usuarios
Usa el test client de Flask (no requiere requests)
"""

from app import app

def test_admin_routes():
    """Prueba las rutas administrativas"""
    print("Probando rutas administrativas...")
    print("=" * 50)
    
    with app.test_client() as client:
        # Test 1: Dashboard
        print("\n1. Probando Dashboard...")
        response = client.get('/admin/dashboard', follow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Dashboard accesible correctamente")
        else:
            print(f"   Error: {response.status_code}")
            if response.status_code == 302:
                print(f"   Redirigido a: {response.location}")
        
        # Test 2: Lista de usuarios
        print("\n2. Probando lista de usuarios...")
        response = client.get('/admin/users', follow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Lista de usuarios accesible correctamente")
        else:
            print(f"   Error: {response.status_code}")
            if response.status_code == 302:
                print(f"   Redirigido a: {response.location}")
        
        # Test 3: Formulario de creación
        print("\n3. Probando formulario de creación...")
        response = client.get('/admin/users/create', follow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   Formulario de creación accesible correctamente")
        else:
            print(f"   Error: {response.status_code}")
            if response.status_code == 302:
                print(f"   Redirigido a: {response.location}")
        
        # Test 4: API user_types
        print("\n4. Probando API user_types...")
        response = client.get('/user_types/', follow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   API user_types accesible correctamente")
        else:
            print(f"   Error: {response.status_code}")
        
        # Test 5: API zonas
        print("\n5. Probando API zonas...")
        response = client.get('/zonas/', follow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   API zonas accesible correctamente")
        else:
            print(f"   Error: {response.status_code}")

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("\nProbando conexión a base de datos...")
    print("=" * 50)
    
    try:
        from app import app, db
        from app.models.user_type import UserType
        from app.models.zona import Zona
        from app.models.estado import Estado
        from app.models.user import User
        
        with app.app_context():
            # Verificar que las tablas existen y tienen datos
            user_types = UserType.query.all()
            zonas = Zona.query.all()
            estados = Estado.query.all()
            users = User.query.all()
            
            print(f"Conexión exitosa")
            print(f"   - Tipos de usuario: {len(user_types)}")
            print(f"   - Zonas: {len(zonas)}")
            print(f"   - Estados: {len(estados)}")
            print(f"   - Usuarios: {len(users)}")
            
            # Mostrar datos básicos
            if user_types:
                print(f"   - Tipos disponibles: {[ut.type_name for ut in user_types]}")
            if zonas:
                print(f"   - Zonas disponibles: {[z.nombre for z in zonas]}")
            if estados:
                print(f"   - Estados disponibles: {[e.nombre for e in estados]}")
            if users:
                print(f"   - Usuarios: {[f'{u.first_name} {u.last_name}' for u in users[:3]]}")
                
    except Exception as e:
        print(f"Error en conexión a BD: {e}")

if __name__ == "__main__":
    print("Iniciando pruebas de navegación simple")
    print("=" * 60)
    
    # Probar conexión a BD
    test_database_connection()
    
    # Probar rutas
    test_admin_routes()
    
    print("\n" + "=" * 60)
    print("Resumen de pruebas:")
    print("- Status 200: La ruta funciona correctamente")
    print("- Status 302: La ruta redirige (posible problema)")
    print("- Status 403: Acceso denegado")
    print("- Status 500: Error interno del servidor")
    print("\nPara acceder al panel administrativo:")
    print("   http://localhost:5000/admin/dashboard")
    print("   http://localhost:5000/admin/users")
