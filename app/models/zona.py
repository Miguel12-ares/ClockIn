from app import db

class Zona(db.Model):
    __tablename__ = 'zonas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column('sede_nombre', db.String(100), nullable=False)
    departamento = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)

    users = db.relationship('User', back_populates='zona', lazy=True)
    admins = db.relationship('AdminZona', backref='zona', lazy=True)
