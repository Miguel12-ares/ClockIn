from app import db

class SystemAudit(db.Model):
    __tablename__ = 'system_audit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    table_affected = db.Column(db.String(100), nullable=True)
    action_type = db.Column(db.String(100), nullable=True)
    old_values = db.Column(db.Text, nullable=True)
    new_values = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    ip_address = db.Column(db.String(45), nullable=True)
