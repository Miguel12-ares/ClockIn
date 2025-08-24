from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'), nullable=False)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), nullable=False)
    fingerprint_data = db.Column(db.LargeBinary)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

<<<<<<< HEAD
    access_logs = db.relationship('AccessLog', foreign_keys='AccessLog.user_id', backref='user', lazy=True)
    access_logs_created = db.relationship('AccessLog', foreign_keys='AccessLog.created_by', backref='creator', lazy=True)
    active_sessions = db.relationship('ActiveSession', backref='user', lazy=True)
    anomalies = db.relationship('Anomaly', foreign_keys='Anomaly.user_id', backref='user', lazy=True)
    anomalies_resolved = db.relationship('Anomaly', foreign_keys='Anomaly.resolved_by', backref='resolved_by_user', lazy=True)
=======
    # Relaciones con claves foráneas específicas
    access_logs = db.relationship('AccessLog', backref='user', foreign_keys='AccessLog.user_id', lazy=True)
    access_logs_created = db.relationship('AccessLog', backref='created_by_user', foreign_keys='AccessLog.created_by', lazy=True)
    active_sessions = db.relationship('ActiveSession', backref='user', lazy=True)
    anomalies = db.relationship('Anomaly', backref='user', foreign_keys='Anomaly.user_id', lazy=True)
    anomalies_resolved = db.relationship('Anomaly', backref='resolved_by_user', foreign_keys='Anomaly.resolved_by', lazy=True)
>>>>>>> origin/CLOCK-17-Gestión-de-Usuarios-y-Roles
    system_audits = db.relationship('SystemAudit', backref='user', lazy=True)
    admin_zonas = db.relationship('AdminZona', backref='admin', lazy=True)
