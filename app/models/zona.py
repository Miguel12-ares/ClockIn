from app import db

class Zona(db.Model):
    __tablename__ = 'zonas'
    id = db.Column(db.Integer, primary_key=True)
    sede_nombre = db.Column(db.String(100), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)

    users = db.relationship('User', backref='zona', lazy=True)
    admins = db.relationship('AdminZona', backref='zona', lazy=True)
