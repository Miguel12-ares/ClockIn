import pytest
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

def create_test_app():
    """Crear aplicación de prueba independiente"""
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    test_app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    test_app.config['WTF_CSRF_ENABLED'] = False
    
    # Inicializar extensiones
    db = SQLAlchemy(test_app)
    jwt = JWTManager(test_app)
    
    # Importar todos los modelos para que se registren
    from app.models import user, user_type, zona, estado, admin_zona, access_log, active_session, anomaly, system_audit
    
    # Registrar blueprints
    from app.controllers.auth import bp as auth_bp
    from app.controllers.user import user_bp
    from app.controllers.zona import zona_bp
    
    test_app.register_blueprint(auth_bp, url_prefix='/auth')
    test_app.register_blueprint(user_bp, url_prefix='/users')
    test_app.register_blueprint(zona_bp, url_prefix='/zonas')
    
    return test_app, db

@pytest.fixture
def app_and_db():
    """Fixture para aplicación y base de datos de prueba"""
    test_app, db = create_test_app()
    
    with test_app.app_context():
        db.create_all()
        yield test_app, db
        db.drop_all()

@pytest.fixture
def client(app_and_db):
    """Cliente de prueba"""
    test_app, db = app_and_db
    return test_app.test_client()

@pytest.fixture
def db_session(app_and_db):
    """Sesión de base de datos"""
    test_app, db = app_and_db
    return db

class TestSimpleAuth:
    """Pruebas simplificadas de autenticación"""
    
    def _create_test_data(self, db):
        """Crear datos de prueba"""
        from app.models.user import User
        from app.models.user_type import UserType
        from app.models.zona import Zona
        from app.models.estado import Estado
        
        # Crear estados
        estado_activo = Estado(nombre='activo', description='Usuario activo')
        estado_inactivo = Estado(nombre='inactivo', description='Usuario inactivo')
        db.session.add_all([estado_activo, estado_inactivo])
        
        # Crear tipos de usuario
        admin_type = UserType(type_name='Admin', description='Administrador del sistema')
        supervisor_type = UserType(type_name='Supervisor', description='Supervisor de zona')
        empleado_type = UserType(type_name='Empleado', description='Empleado regular')
        db.session.add_all([admin_type, supervisor_type, empleado_type])
        
        # Crear zonas
        zona_principal = Zona(nombre='Sede Principal', departamento='Antioquia', ciudad='Medellín')
        zona_secundaria = Zona(nombre='Sede Secundaria', departamento='Valle', ciudad='Cali')
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
        
        db.session.add_all([admin_user, supervisor_user])
        db.session.commit()
    
    def test_login_success_admin(self, client, db_session):
        """Prueba login exitoso con usuario administrador"""
        self._create_test_data(db_session)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '12345678'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']
        assert data['data']['user']['user_type'] == 'Admin'
    
    def test_login_success_supervisor(self, client, db_session):
        """Prueba login exitoso con usuario supervisor"""
        self._create_test_data(db_session)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '87654321'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['success'] is True
        assert data['data']['user']['user_type'] == 'Supervisor'
    
    def test_login_user_not_found(self, client, db_session):
        """Prueba login con usuario inexistente"""
        self._create_test_data(db_session)
        
        response = client.post('/auth/login', 
                             json={'idDocumento': '99999999'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'Usuario no encontrado' in data['message']
    
    def test_login_missing_data(self, client, db_session):
        """Prueba login sin datos requeridos"""
        self._create_test_data(db_session)
        
        response = client.post('/auth/login', 
                             json={})
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['success'] is False
        assert 'ID documento requerido' in data['message']
    
    def test_refresh_token_success(self, client, db_session):
        """Prueba renovación exitosa de token"""
        self._create_test_data(db_session)
        
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
    
    def test_verify_token_success(self, client, db_session):
        """Prueba verificación exitosa de token"""
        self._create_test_data(db_session)
        
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
