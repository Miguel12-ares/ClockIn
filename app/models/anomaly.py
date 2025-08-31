from app import db
from datetime import datetime

class Anomaly(db.Model):
    __tablename__ = 'anomalies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    anomaly_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolution_notes = db.Column(db.Text)

    # Relaciones explícitas
    user = db.relationship('User', foreign_keys=[user_id], backref='user_anomalies')
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref='resolved_anomalies')
