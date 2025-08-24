from flask import Flask, request, redirect, url_for, flash, render_template_string
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
            flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
            # Redirigir a una página simple en lugar de otra ruta admin
            return redirect('/')
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
                <h1>🚀 ClockIn - Sistema de Control de Acceso</h1>
                <p>Sistema de gestión de usuarios y control de acceso para empresas</p>
            </div>
            
            <h2>Acceso Rápido</h2>
            <div class="links">
                <a href="/admin/dashboard" class="link">📊 Dashboard Administrativo</a>
                <a href="/admin/users" class="link">👥 Gestión de Usuarios</a>
                <a href="/user_types" class="link">🏷️ Tipos de Usuario</a>
                <a href="/zonas" class="link">📍 Gestión de Zonas</a>
            </div>
            
            <h2>Estado del Sistema</h2>
            <p>✅ Servidor funcionando correctamente</p>
            <p>✅ Base de datos conectada</p>
            <p>✅ Panel administrativo disponible</p>
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
<<<<<<< HEAD
from app.controllers.auth import bp as auth_bp
=======
from app.controllers.admin import admin_bp
>>>>>>> origin/CLOCK-17-Gestión-de-Usuarios-y-Roles

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(zona_bp, url_prefix='/zonas')
app.register_blueprint(user_type_bp, url_prefix='/user_types')
app.register_blueprint(estado_bp, url_prefix='/estados')
app.register_blueprint(admin_zona_bp, url_prefix='/admin_zona')
app.register_blueprint(access_log_bp, url_prefix='/access_logs')
app.register_blueprint(active_session_bp, url_prefix='/active_sessions')
app.register_blueprint(anomaly_bp, url_prefix='/anomalies')
app.register_blueprint(system_audit_bp, url_prefix='/system_audits')
<<<<<<< HEAD
app.register_blueprint(auth_bp, url_prefix='/auth')

# Registrar ruta principal
@app.route('/')
def index():
    from flask import redirect, url_for
    return redirect(url_for('auth.login_form'))
=======
app.register_blueprint(admin_bp, url_prefix='/admin')
>>>>>>> origin/CLOCK-17-Gestión-de-Usuarios-y-Roles
