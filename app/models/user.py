from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'), nullable=False)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=False)
    fingerprint_data = db.Column(db.LargeBinary)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    active_sessions = db.relationship('ActiveSession', backref='user', lazy=True)
    admin_zonas = db.relationship('AdminZona', backref='admin', lazy=True)

    def set_password(self, password: str) -> None:
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.passwordHash, password)

    # Nota:
    # - AccessLog define backrefs: action_logs (como actor) y created_logs (como creador)
    # - Anomaly define backrefs: user_anomalies (como usuario) y resolved_anomalies (como resolvedor)
    # - SystemAudit define backref: audit_logs
