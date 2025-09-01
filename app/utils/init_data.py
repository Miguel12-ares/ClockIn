from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app.models.user import User
from app import db
from sqlalchemy import text


def create_initial_data():
    """Crear datos iniciales con verificaciones robustas."""

    try:
        print("🔄 Verificando datos iniciales...")

        # Verificar existencia de tabla principal 'users'
        result = db.session.execute(text("SHOW TABLES LIKE 'users'"))
        if not result.fetchone():
            print("❌ ERROR: Tabla 'users' no existe; omitiendo seed")
            return False

        # Estados base (solo si no existen)
        if Estado.query.count() == 0:
            print("📝 Creando estados base...")
            estados = [
                Estado(name='activo', description='Usuario activo'),
                Estado(name='inactivo', description='Usuario inactivo'),
                Estado(name='pendiente', description='Usuario pendiente de autorización'),
                Estado(name='eliminado', description='Usuario eliminado o inhabilitado'),
            ]
            db.session.add_all(estados)
            db.session.commit()
            print("✅ Estados creados")

        # Tipos de usuario
        if UserType.query.count() == 0:
            print("📝 Creando tipos de usuario...")
            admin_type = UserType(type_name='admin', description='Administrador del sistema')
            empleado_type = UserType(type_name='empleado', description='Usuario empleado')
            db.session.add_all([admin_type, empleado_type])
            db.session.commit()
            print("✅ Tipos de usuario creados")

        # Zona base
        if Zona.query.count() == 0:
            print("📝 Creando zona base...")
            zona = Zona(sede_nombre='Sede Principal', departamento='Cundinamarca', ciudad='Bogotá')
            db.session.add(zona)
            db.session.commit()
            print("✅ Zona creada")

        # Usuario administrador de prueba
        if User.query.filter_by(idDocumento=12345678).first() is None:
            print("📝 Creando usuario administrador de prueba...")
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
            print("✅ Usuario admin creado: 12345678 / admin123")
        else:
            print("ℹ️ Usuario admin ya existe, omitiendo creación")

        total_users = User.query.count()
        print(f"📊 Total usuarios en DB: {total_users}")
        return True

    except Exception as e:
        print(f"❌ ERROR en create_initial_data: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return False
