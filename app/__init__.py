from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

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

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(zona_bp, url_prefix='/zonas')
app.register_blueprint(user_type_bp, url_prefix='/user_types')
app.register_blueprint(estado_bp, url_prefix='/estados')
app.register_blueprint(admin_zona_bp, url_prefix='/admin_zona')
app.register_blueprint(access_log_bp, url_prefix='/access_logs')
app.register_blueprint(active_session_bp, url_prefix='/active_sessions')
app.register_blueprint(anomaly_bp, url_prefix='/anomalies')
app.register_blueprint(system_audit_bp, url_prefix='/system_audits')