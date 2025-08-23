from app import db

class AdminZona(db.Model):
    __tablename__ = 'admin_zona'
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    zona_id = db.Column(db.Integer, db.ForeignKey('zonas.id'), primary_key=True)
