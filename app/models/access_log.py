from app import db
from datetime import datetime

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    fingerprint_confidence = db.Column(db.Numeric(5, 4))
    status = db.Column(db.String(50))
    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relaciones explícitas con foreign_keys especificadas
    user = db.relationship('User', foreign_keys=[user_id], backref='action_logs')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_logs')
