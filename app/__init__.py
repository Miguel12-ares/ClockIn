from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from dotenv import load_dotenv
import threading
import time
from sqlalchemy import text

# Create unbound DB instance (bound inside create_app)
db = SQLAlchemy()
_db_lock = threading.Lock()


def create_app():
    load_dotenv()

    app = Flask(__name__)

    # Configuración basada en variables de entorno
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret')

    # Inicializar extensiones
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app)

    # Cargar modelos y crear tablas con lock (evitar DDL concurrente en multi-worker)
    with app.app_context():
        # CRÍTICO: importar todos los modelos ANTES de create_all()
        print("🔍 IMPORTANDO TODOS LOS MODELOS...")
        from app.models import user_type  # noqa: F401
        from app.models import zona       # noqa: F401
        from app.models import estado     # noqa: F401
        from app.models import user       # noqa: F401
        from app.models import admin_zona # noqa: F401
        from app.models import access_log # noqa: F401
        from app.models import active_session  # noqa: F401
        from app.models import anomaly    # noqa: F401
        from app.models import system_audit  # noqa: F401

        print(f"📋 Modelos detectados: {list(db.Model.metadata.tables.keys())}")

        with _db_lock:
            max_retries = 10
            for attempt in range(max_retries):
                try:
                    print(f"🔄 Intento {attempt + 1}/{max_retries} - probando conexión MySQL...")
                    # Verificar conexión
                    db.session.execute(text("SELECT 1"))
                    print("✅ MySQL conectado exitosamente")

                    # Crear tablas
                    print("🔄 Creando tablas...")
                    db.create_all()
                    print("✅ Tablas creadas exitosamente")

                    # Seeds seguros
                    init_default_data()
                    try:
                        from app.utils.init_data import create_initial_data
                        create_initial_data()
                        print("✅ Datos iniciales creados")
                    except Exception as se:
                        print(f"Seed data error: {se}")

                    break
                except Exception as e:
                    print(f"❌ Intento {attempt + 1} falló: {e}")
                    if attempt < max_retries - 1:
                        print("⏱️ Esperando 3s antes de reintentar...")
                        time.sleep(3)
                    else:
                        print("❌ FALLO CRÍTICO: No se pudo conectar a MySQL para crear tablas y sembrar datos")

    # Registrar blueprints
    from app.controllers.user import user_bp
    from app.controllers.zona import zona_bp
    from app.controllers.user_type import user_type_bp
    from app.controllers.estado import estado_bp
    from app.controllers.admin_zona import admin_zona_bp
    from app.controllers.access_log import access_log_bp
    from app.controllers.active_session import active_session_bp
    from app.controllers.anomaly import anomaly_bp
    from app.controllers.system_audit import system_audit_bp
    from app.controllers.auth import auth_bp
    from app.controllers.main import main_bp
    from app.controllers.admin import admin_bp
    from app.controllers.attendance import attendance_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(zona_bp, url_prefix='/zonas')
    app.register_blueprint(user_type_bp, url_prefix='/user_types')
    app.register_blueprint(estado_bp, url_prefix='/estados')
    app.register_blueprint(admin_zona_bp, url_prefix='/admin_zona')
    app.register_blueprint(access_log_bp, url_prefix='/access_logs')
    app.register_blueprint(active_session_bp, url_prefix='/active_sessions')
    app.register_blueprint(anomaly_bp, url_prefix='/anomalies')
    app.register_blueprint(system_audit_bp, url_prefix='/system_audits')
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(attendance_bp)

    return app


def init_default_data():
    from app.models.estado import Estado
    from app.models.user_type import UserType
    from app.models.zona import Zona
    
    if Estado.query.count() == 0:
        estados = [
            Estado(name='activo', description='Usuario activo'),
            Estado(name='inactivo', description='Usuario inactivo o suspendido'),
            Estado(name='pendiente', description='Estado pendiente de autorización'),
            Estado(name='eliminado', description='Usuario eliminado o inhabilitado')
        ]
        for estado in estados:
            db.session.add(estado)
        db.session.commit()
