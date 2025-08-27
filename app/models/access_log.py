from app import db

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    fingerprint_confidence = db.Column(db.Numeric(5,4), nullable=True)
    status = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Relación con el usuario que creó el log
    created_by_user = db.relationship('User', foreign_keys=[created_by], backref='created_logs', lazy=True)
