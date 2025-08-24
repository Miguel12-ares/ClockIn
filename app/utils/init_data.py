from app.models.user_type import UserType
from app.models.estado import Estado
from app.models.zona import Zona
from app import db


def init_user_types():
    """
    Inicializa los tipos de usuario básicos del sistema ClockIn
    """
    user_types = [
        {
            'type_name': 'SAdmin',
            'description': 'Super Administrador del sistema con acceso completo'
        },
        {
            'type_name': 'Admin',
            'description': 'Administrador con permisos de gestión'
        },
        {
            'type_name': 'Funcionario SENA',
            'description': 'Funcionario del SENA con acceso a funcionalidades específicas'
        },
        {
            'type_name': 'Instructor',
            'description': 'Instructor con acceso a gestión de aprendices'
        },
        {
            'type_name': 'Aprendiz',
            'description': 'Aprendiz con acceso básico al sistema'
        },
        {
            'type_name': 'Administrativo',
            'description': 'Personal administrativo'
        },
        {
            'type_name': 'Ciudadano',
            'description': 'Ciudadano con acceso limitado'
        }
    ]
    
    for user_type_data in user_types:
        existing_type = UserType.query.filter_by(type_name=user_type_data['type_name']).first()
        if not existing_type:
            new_type = UserType(
                type_name=user_type_data['type_name'],
                description=user_type_data['description']
            )
            db.session.add(new_type)
            print(f"Tipo de usuario creado: {user_type_data['type_name']}")
    
    db.session.commit()
    print("Tipos de usuario inicializados correctamente")


def init_estados():
    """
    Inicializa los estados básicos del sistema
    """
    estados = [
        {
            'name': 'Activo',
            'description': 'Usuario activo en el sistema'
        },
        {
            'name': 'Inactivo',
            'description': 'Usuario inactivo temporalmente'
        },
        {
            'name': 'Suspendido',
            'description': 'Usuario suspendido por violación de políticas'
        },
        {
            'name': 'Bloqueado',
            'description': 'Usuario bloqueado por seguridad'
        }
    ]
    
    for estado_data in estados:
        existing_estado = Estado.query.filter_by(name=estado_data['name']).first()
        if not existing_estado:
            new_estado = Estado(
                name=estado_data['name'],
                description=estado_data['description']
            )
            db.session.add(new_estado)
            print(f"Estado creado: {estado_data['name']}")
    
    db.session.commit()
    print("Estados inicializados correctamente")


def init_zonas():
    """
    Inicializa zonas básicas del sistema
    """
    zonas = [
        {
            'sede_nombre': 'Sede Principal',
            'departamento': 'Cundinamarca',
            'ciudad': 'Bogotá'
        },
        {
            'sede_nombre': 'Sede Norte',
            'departamento': 'Cundinamarca',
            'ciudad': 'Bogotá'
        },
        {
            'sede_nombre': 'Sede Industrial',
            'departamento': 'Cundinamarca',
            'ciudad': 'Bogotá'
        }
    ]
    
    for zona_data in zonas:
        existing_zona = Zona.query.filter_by(sede_nombre=zona_data['sede_nombre']).first()
        if not existing_zona:
            new_zona = Zona(
                sede_nombre=zona_data['sede_nombre'],
                departamento=zona_data['departamento'],
                ciudad=zona_data['ciudad']
            )
            db.session.add(new_zona)
            print(f"Zona creada: {zona_data['sede_nombre']}")
    
    db.session.commit()
    print("Zonas inicializadas correctamente")


def init_all_data():
    """
    Inicializa todos los datos básicos del sistema
    """
    print("Inicializando datos básicos del sistema ClockIn...")
    
    try:
        init_user_types()
        init_estados()
        init_zonas()
        
        print("Datos básicos inicializados correctamente!")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al inicializar datos: {str(e)}")
        raise e
