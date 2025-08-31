from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.user import User
from app import db


def create_initial_data():
    """Crear datos iniciales para pruebas (idDocumento=12345678 / password=admin123)."""

    # Crear tipos de usuario
    if UserType.query.count() == 0:
        admin_type = UserType(type_name='admin', description='Administrador del sistema')
        empleado_type = UserType(type_name='empleado', description='Usuario empleado')
        db.session.add(admin_type)
        db.session.add(empleado_type)
        db.session.commit()

    # Crear zona de prueba
    if Zona.query.count() == 0:
        zona = Zona(sede_nombre='Sede Principal', departamento='Cundinamarca', ciudad='Bogotá')
        db.session.add(zona)
        db.session.commit()

    # Crear usuario administrador de prueba
    if User.query.filter_by(idDocumento=12345678).first() is None:
        # Asumimos ids 1 para tipos y zona recién creados
        admin_user = User(
            idDocumento=12345678,
            first_name='Admin',
            last_name='Sistema',
            user_type_id=1,
            zona_id=1,
            estado_id=1,
            is_active=True,
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
