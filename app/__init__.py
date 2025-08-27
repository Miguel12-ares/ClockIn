from flask import Flask, request, redirect, url_for, flash, render_template_string, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object('app.config.Config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Decorador RBAC para simular control de acceso
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # En desarrollo, asumimos acceso admin
        # En producción, aquí se verificaría la autenticación real
        admin_mode = os.getenv('ADMIN_MODE', 'true').lower() == 'true'
        if not admin_mode:
            # Evitar redirección al index; devolver 403 claro
            return Response('Acceso denegado. Se requieren permisos de administrador.', status=403)
        return f(*args, **kwargs)
    return decorated_function

# Ruta principal
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ClockIn - Sistema de Control de Acceso</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .header { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
            .links { display: flex; gap: 20px; flex-wrap: wrap; }
            .link { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            .link:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>ClockIn - Sistema de Control de Acceso</h1>
                <p>Sistema de gestión de usuarios y control de acceso para empresas</p>
            </div>
            
            <h2>Acceso Rápido</h2>
            <div class="links">
                <a href="/admin/dashboard" class="link">Dashboard Administrativo</a>
                <a href="/admin/users" class="link">Gestión de Usuarios</a>
                <a href="/user_types" class="link">Tipos de Usuario</a>
                <a href="/zonas" class="link">Gestión de Zonas</a>
                <a href="/auth/login" class="link">Acceso de Usuarios</a>
            </div>
            
            <h2>Estado del Sistema</h2>
            <p>Servidor funcionando correctamente</p>
            <p>Base de datos conectada</p>
            <p>Panel administrativo disponible</p>
        </div>
    </body>
    </html>
    ''')

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
from app.controllers.auth import bp as auth_bp
from app.controllers.admin import admin_bp

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(zona_bp, url_prefix='/zonas')
app.register_blueprint(user_type_bp, url_prefix='/user_types')
app.register_blueprint(estado_bp, url_prefix='/estados')
app.register_blueprint(admin_zona_bp, url_prefix='/admin_zona')
app.register_blueprint(access_log_bp, url_prefix='/access_logs')
app.register_blueprint(active_session_bp, url_prefix='/active_sessions')
app.register_blueprint(anomaly_bp, url_prefix='/anomalies')
app.register_blueprint(system_audit_bp, url_prefix='/system_audits')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

# -------- Inicialización de BD al arranque (para entornos con Gunicorn) --------
def _init_db_on_start():
    should_init = os.getenv('INIT_DB_ON_START', 'true').lower() == 'true'
    if not should_init:
        return
    try:
        with app.app_context():
            # Importar modelos para registrar metadatos
            from app.models import user_type, zona, estado, user, admin_zona, access_log, active_session, anomaly, system_audit  # noqa: F401
            # Crear tablas que no existan (idempotente)
            db.create_all()
            try:
                from app.init_data import init_basic_data
                init_basic_data()
            except Exception as e:
                print(f"Advertencia al inicializar datos: {e}")
            print('Created tables and initialized seed data')
    except Exception as e:
        print(f"Error en inicialización de BD al arranque: {e}")

_init_db_on_start()
