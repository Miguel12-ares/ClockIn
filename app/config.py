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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Access token expira en 1 hora
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expira en 30 días
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ERROR_MESSAGE_KEY = 'message'
