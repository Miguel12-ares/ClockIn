import pytest
import os
from app import app, db

@pytest.fixture(scope='session')
def test_app():
    """Configurar aplicación para pruebas"""
    # Configurar variables de entorno para pruebas
    os.environ['TESTING'] = 'true'
    os.environ['INIT_DB_ON_START'] = 'false'
    
    # Configurar aplicación para pruebas
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['ADMIN_MODE'] = 'false'
    
    return app

@pytest.fixture(scope='function')
def client(test_app):
    """Cliente de prueba"""
    with test_app.app_context():
        db.create_all()
        yield test_app.test_client()
        db.drop_all()

@pytest.fixture(scope='function')
def db_session(test_app):
    """Sesión de base de datos para pruebas"""
    with test_app.app_context():
        db.create_all()
        yield db
        db.drop_all()
