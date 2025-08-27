import os
from dotenv import load_dotenv

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
