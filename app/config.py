import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

def get_database_url():
    """Determina la URL de la base de datos para Docker"""
    # Si se especifica DATABASE_URL en variables de entorno, usarla
    if os.getenv('DATABASE_URL'):
        return os.getenv('DATABASE_URL')
    
    # Configuración por defecto para Docker
    # Valor por defecto alineado con docker-compose
    return 'mysql+pymysql://user:user_password@db:3306/db_name'

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_DATABASE_URI = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_MODE = os.getenv('ADMIN_MODE', 'true').lower() == 'true'
    
    # Configuración JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_change_in_production')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_DECODE_LEEWAY = 5
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SECURE = True  # Cambia a False solo en desarrollo local
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = True
    JWT_CSRF_HEADER_NAME = 'X-CSRF-TOKEN'
    JWT_ERROR_MESSAGE_KEY = 'message'
