from app import app, db
from app.models.user import User
from app.models.estado import Estado

with app.app_context():
    user = User.query.filter_by(idDocumento=111).first()
    if user:
        estado = Estado.query.get(user.estado_id)
        print(f"Usuario: {user.first_name} {user.last_name}")
        print(f"Estado ID: {user.estado_id}")
        print(f"Estado Nombre: {estado.nombre if estado else 'No encontrado'}")
        print(f"Is Active: {user.is_active}")
        
        # Listar todos los estados
        estados = Estado.query.all()
        print("\nEstados disponibles:")
        for e in estados:
            print(f"  ID: {e.id}, Nombre: {e.nombre}")
    else:
        print("Usuario no encontrado")
