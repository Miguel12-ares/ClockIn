from app import db
from datetime import datetime

class SystemAudit(db.Model):
    __tablename__ = 'system_audit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    table_affected = db.Column(db.String(100))
    action_type = db.Column(db.String(100))
    old_values = db.Column(db.Text)
    new_values = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

    # Relación simple (solo una FK)
    user = db.relationship('User', backref='audit_logs')
