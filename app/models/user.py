from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # e.g., 'SAdmin', 'Aprendices'
    # Agrega campos para ID único y huella (encriptada)
