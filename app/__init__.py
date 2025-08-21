from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import os
import time  # Para retries

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Importa controladores (rutas)
from .controllers import auth
app.register_blueprint(auth.bp)


# Función para crear tablas con retries (evita race conditions en Docker)
def init_db_with_retries(max_retries=5, delay=5):
    retries = 0
    while retries < max_retries:
        try:
            with app.app_context():
                db.create_all()
            print("Tablas creadas exitosamente.")
            return
        except Exception as e:
            print(f"Error al conectar a DB (intento {retries+1}/{max_retries}): {e}")
            retries += 1
            time.sleep(delay)
    raise Exception("No se pudo inicializar la DB después de retries.")

# Ejecuta init solo si no es producción (en Docker, usa migraciones o init manual si es necesario)
if os.getenv('FLASK_ENV') != 'production':
    init_db_with_retries()
else:
    # En producción/Docker, asume que DB ya está inicializada; agrega logging
    print("Modo producción: Saltando create_all automático.")
