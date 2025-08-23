from flask import jsonify, request
from app.controllers.user import user_bp
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app import db

@user_bp.route('/', methods=['POST'])
def create():
    """
    Crea un nuevo usuario
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear el usuario'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['idDocumento', 'first_name', 'last_name', 'user_type_id', 'zona_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': 'Campo requerido faltante',
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Verificar si el documento ya existe
        existing_user = User.query.filter_by(idDocumento=data['idDocumento']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Documento duplicado',
                'message': f'Ya existe un usuario con el documento {data["idDocumento"]}'
            }), 400
        
        # Verificar que el user_type existe
        user_type = UserType.query.get(data['user_type_id'])
        if not user_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de usuario inválido',
                'message': f'No existe un tipo de usuario con ID {data["user_type_id"]}'
            }), 400
        
        # Verificar que la zona existe
        zona = Zona.query.get(data['zona_id'])
        if not zona:
            return jsonify({
                'success': False,
                'error': 'Zona inválida',
                'message': f'No existe una zona con ID {data["zona_id"]}'
            }), 400
        
        # Verificar estado (opcional, por defecto 1)
        estado_id = data.get('estado_id', 1)
        estado = Estado.query.get(estado_id)
        if not estado:
            return jsonify({
                'success': False,
                'error': 'Estado inválido',
                'message': f'No existe un estado con ID {estado_id}'
            }), 400
        
        # Crear nuevo usuario
        new_user = User(
            idDocumento=data['idDocumento'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            user_type_id=data['user_type_id'],
            zona_id=data['zona_id'],
            estado_id=estado_id,
            is_active=data.get('is_active', True),
            fingerprint_data=data.get('fingerprint_data')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Retornar usuario creado
        user_data = {
            'id': new_user.id,
            'idDocumento': new_user.idDocumento,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'user_type': {
                'id': new_user.user_type.id,
                'type_name': new_user.user_type.type_name
            },
            'zona': {
                'id': new_user.zona.id,
                'sede_nombre': new_user.zona.sede_nombre
            },
            'estado': {
                'id': new_user.estado.id,
                'name': new_user.estado.name
            },
            'is_active': new_user.is_active,
            'created_at': new_user.created_at.isoformat() if new_user.created_at else None
        }
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': user_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
