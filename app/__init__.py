from flask import Flask, request, redirect, url_for, flash, render_template_string, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from functools import wraps
import os

app = Flask(__name__)
app.config.from_object('app.config.Config')
db = SQLAlchemy(app)
jwt = JWTManager(app)

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
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                background: white; 
                border-radius: 15px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                padding: 40px;
                max-width: 500px;
                width: 90%;
                text-align: center;
            }
            .logo { 
                font-size: 2.5em; 
                font-weight: bold; 
                color: #333;
                margin-bottom: 10px;
            }
            .subtitle { 
                color: #666; 
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .login-form {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .form-group {
                text-align: left;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 500;
            }
            .form-group input {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .form-group input:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
            }
            .message {
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                display: none;
            }
            .message.success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .message.error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .links {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #eee;
            }
            .links a {
                color: #667eea;
                text-decoration: none;
                margin: 0 10px;
                font-weight: 500;
            }
            .links a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">ClockIn</div>
            <div class="subtitle">Sistema de Control de Acceso</div>
            
            <div id="message" class="message"></div>
            
            <form class="login-form" id="loginForm">
                <div class="form-group">
                    <label for="idDocumento">Número de Documento</label>
                    <input type="text" id="idDocumento" name="idDocumento" required 
                           placeholder="Ingrese su número de documento">
                </div>
                
                <button type="submit" class="btn" id="loginBtn">
                    Iniciar Sesión
                </button>
            </form>
            
            <div class="links">
                <a href="/admin/dashboard">Panel Administrativo</a>
                <a href="/docs">Documentación</a>
            </div>
        </div>

        <script>
            document.getElementById('loginForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const idDocumento = document.getElementById('idDocumento').value;
                const loginBtn = document.getElementById('loginBtn');
                const messageDiv = document.getElementById('message');
                
                // Deshabilitar botón y mostrar estado de carga
                loginBtn.disabled = true;
                loginBtn.textContent = 'Iniciando sesión...';
                messageDiv.style.display = 'none';
                
                try {
                    const response = await fetch('/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ idDocumento: idDocumento })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Guardar tokens
                        localStorage.setItem('access_token', data.data.access_token);
                        localStorage.setItem('refresh_token', data.data.refresh_token);
                        
                        // Mostrar mensaje de éxito
                        messageDiv.className = 'message success';
                        messageDiv.textContent = 'Inicio de sesión exitoso. Redirigiendo...';
                        messageDiv.style.display = 'block';
                        
                        // Redirigir según el rol
                        setTimeout(() => {
                            if (data.data.user.user_type === 'Admin' || data.data.user.user_type === 'SAdmin') {
                                window.location.href = '/admin/dashboard';
                            } else {
                                window.location.href = '/dashboard';
                            }
                        }, 1500);
                        
                    } else {
                        // Mostrar error
                        messageDiv.className = 'message error';
                        messageDiv.textContent = data.message || 'Error en el inicio de sesión';
                        messageDiv.style.display = 'block';
                    }
                    
                } catch (error) {
                    messageDiv.className = 'message error';
                    messageDiv.textContent = 'Error de conexión. Intente nuevamente.';
                    messageDiv.style.display = 'block';
                } finally {
                    // Restaurar botón
                    loginBtn.disabled = false;
                    loginBtn.textContent = 'Iniciar Sesión';
                }
            });
        </script>
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
