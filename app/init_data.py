"""
Script para inicializar datos básicos en la base de datos
"""
from app import db
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado

def init_basic_data():
    """Inicializa datos básicos necesarios para el funcionamiento del sistema"""
    
    # Crear tipos de usuario básicos
    user_types = [
        {'type_name': 'Admin', 'description': 'Administrador del sistema con acceso completo'},
        {'type_name': 'Supervisor', 'description': 'Supervisor con acceso a reportes y gestión limitada'},
        {'type_name': 'Empleado', 'description': 'Empleado regular con acceso básico al sistema'}
    ]
    
    for user_type_data in user_types:
        existing = UserType.query.filter_by(type_name=user_type_data['type_name']).first()
        if not existing:
            user_type = UserType(**user_type_data)
            db.session.add(user_type)
            print(f"Tipo de usuario creado: {user_type_data['type_name']}")
    
    # Crear zonas básicas
    zonas = [
        {'nombre': 'Sede Principal', 'departamento': 'Administración', 'ciudad': 'Bogotá'},
        {'nombre': 'Sucursal Norte', 'departamento': 'Ventas', 'ciudad': 'Medellín'},
        {'nombre': 'Sucursal Sur', 'departamento': 'Producción', 'ciudad': 'Cali'},
        {'nombre': 'Almacén Central', 'departamento': 'Logística', 'ciudad': 'Barranquilla'}
    ]
    
    for zona_data in zonas:
        existing = Zona.query.filter_by(nombre=zona_data['nombre']).first()
        if not existing:
            zona = Zona(**zona_data)
            db.session.add(zona)
            print(f"Zona creada: {zona_data['nombre']}")
    
    # Crear estados básicos
    estados = [
        {'nombre': 'Activo', 'description': 'Usuario activo en el sistema'},
        {'nombre': 'Inactivo', 'description': 'Usuario inactivo temporalmente'},
        {'nombre': 'Suspendido', 'description': 'Usuario suspendido por violaciones'},
        {'nombre': 'Retirado', 'description': 'Usuario retirado del sistema'}
    ]
    
    for estado_data in estados:
        existing = Estado.query.filter_by(nombre=estado_data['nombre']).first()
        if not existing:
            estado = Estado(**estado_data)
            db.session.add(estado)
            print(f"Estado creado: {estado_data['nombre']}")
    
    try:
        db.session.commit()
        print("Datos básicos inicializados correctamente")
    except Exception as e:
        db.session.rollback()
        print(f"Error al inicializar datos: {e}")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_basic_data()
