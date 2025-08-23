from app import db

class Estado(db.Model):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    users = db.relationship('User', backref='estado', lazy=True)
