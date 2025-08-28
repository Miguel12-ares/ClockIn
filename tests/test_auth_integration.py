import pytest
import json
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado

class TestAuthIntegration:
    """Pruebas de integración para el sistema de autenticación JWT"""
    
    def _create_test_data(self, db):
        """Crear datos de prueba"""
        # Crear estados
        estado_activo = Estado(name='activo', description='Usuario activo')
        estado_inactivo = Estado(name='inactivo', description='Usuario inactivo')
        db.session.add_all([estado_activo, estado_inactivo])
        
        # Crear tipos de usuario
        admin_type = UserType(type_name='Admin', description='Administrador del sistema')
        supervisor_type = UserType(type_name='Supervisor', description='Supervisor de zona')
        empleado_type = UserType(type_name='Empleado', description='Empleado regular')
        db.session.add_all([admin_type, supervisor_type, empleado_type])
        
        # Crear zonas
        zona_principal = Zona(sede_nombre='Sede Principal', departamento='Antioquia', ciudad='Medellín')
        zona_secundaria = Zona(sede_nombre='Sede Secundaria', departamento='Valle', ciudad='Cali')
        db.session.add_all([zona_principal, zona_secundaria])
        
        db.session.commit()
        
        # Crear usuarios de prueba
        admin_user = User(
            idDocumento='12345678',
            first_name='Admin',
            last_name='Test',
            user_type_id=admin_type.id,
            zona_id=zona_principal.id,
            estado_id=estado_activo.id,
            is_active=True
        )
        
        supervisor_user = User(
            idDocumento='87654321',
            first_name='Supervisor',
            last_name='Test',
            user_type_id=supervisor_type.id,
            zona_id=zona_secundaria.id,
            estado_id=estado_activo.id,
            is_active=True
        )
        
        empleado_user = User(
            idDocumento='11111111',
            first_name='Empleado',
            last_name='Test',
            user_type_id=empleado_type.id,
            zona_id=zona_principal.id,
            estado_id=estado_activo.id,
            is_active=True
        )
        
        user_inactivo = User(
            idDocumento='22222222',
            first_name='Usuario',
            last_name='Inactivo',
            user_type_id=empleado_type.id,
            zona_id=zona_principal.id,
            estado_id=estado_inactivo.id,
            is_active=False
        )
        
        db.session.add_all([admin_user, supervisor_user, empleado_user, user_inactivo])
        db.session.commit()
    
    def test_login_success_admin(self, client, db):
        """Prueba login exitoso con usuario administrador"""
        self._create_test_data(db)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '12345678'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['user_type'] == 'Admin'
    
    def test_login_success_supervisor(self, client, db):
        """Prueba login exitoso con usuario supervisor"""
        self._create_test_data(db)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '87654321'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert data['data']['user']['user_type'] == 'Supervisor'
    
    def test_login_user_not_found(self, client, db):
        """Prueba login con usuario inexistente"""
        self._create_test_data(db)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '99999999'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'Usuario no encontrado' in data['message']
    
    def test_login_user_inactive(self, client, db):
        """Prueba login con usuario inactivo"""
        self._create_test_data(db)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '22222222'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'Estado de usuario incorrecto' in data['message']
    
    def test_login_missing_data(self, client, db):
        """Prueba login sin datos requeridos"""
        self._create_test_data(db)
        
        response = client.post('/auth/login', 
                             json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'ID documento requerido' in data['message']
    
    def test_refresh_token_success(self, client, db):
        """Prueba renovación exitosa de token"""
        self._create_test_data(db)
        
        # Primero hacer login
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '12345678'})
        login_data = json.loads(login_response.data)
        refresh_token = login_data['data']['refresh_token']
        
        # Renovar token
        response = client.post('/auth/refresh',
                             headers={'Authorization': f'Bearer {refresh_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'access_token' in data['data']
    
    def test_refresh_token_invalid(self, client, db):
        """Prueba renovación con token inválido"""
        self._create_test_data(db)
        
        response = client.post('/auth/refresh',
                             headers={'Authorization': 'Bearer invalid_token'})
        
        assert response.status_code == 401
    
    def test_access_protected_route_admin(self, client, db):
        """Prueba acceso a ruta protegida con usuario admin"""
        self._create_test_data(db)
        
        # Login
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '12345678'})
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Acceder a ruta protegida
        response = client.get('/users/',
                            headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
    
    def test_access_protected_route_supervisor_denied(self, client, db):
        """Prueba acceso denegado a ruta admin con usuario supervisor"""
        self._create_test_data(db)
        
        # Login con supervisor
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '87654321'})
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Intentar acceder a ruta protegida
        response = client.get('/users/',
                            headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'Acceso denegado' in data['error']
    
    def test_access_protected_route_no_token(self, client, db):
        """Prueba acceso a ruta protegida sin token"""
        self._create_test_data(db)
        
        response = client.get('/users/')
        
        assert response.status_code == 401
    
    def test_verify_token_success(self, client, db):
        """Prueba verificación exitosa de token"""
        self._create_test_data(db)
        
        # Login
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '12345678'})
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Verificar token
        response = client.get('/auth/verify',
                            headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_logout_success(self, client, db):
        """Prueba logout exitoso"""
        self._create_test_data(db)
        
        # Login
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '12345678'})
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Logout
        response = client.post('/auth/logout',
                             headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
    
    def test_get_current_user(self, client, db):
        """Prueba obtención de información del usuario actual"""
        self._create_test_data(db)
        
        # Login
        login_response = client.post('/auth/login', 
                                   json={'idDocumento': '12345678'})
        login_data = json.loads(login_response.data)
        access_token = login_data['data']['access_token']
        
        # Obtener información del usuario
        response = client.get('/auth/me',
                            headers={'Authorization': f'Bearer {access_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['idDocumento'] == '12345678'
        assert data['data']['user_type'] == 'Admin'
