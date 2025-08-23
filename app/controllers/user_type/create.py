from flask import jsonify, request
from app.controllers.user_type import user_type_bp
from app.models.user_type import UserType
from app import db

@user_type_bp.route('/', methods=['POST'])
def create():
    """
    Crea un nuevo tipo de usuario
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear el tipo de usuario'
            }), 400
        
        # Validar campos requeridos
        if 'type_name' not in data or not data['type_name']:
            return jsonify({
                'success': False,
                'error': 'Campo requerido faltante',
                'message': 'El campo type_name es requerido'
            }), 400
        
        # Verificar si ya existe un tipo con el mismo nombre
        existing_type = UserType.query.filter_by(type_name=data['type_name']).first()
        if existing_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de usuario duplicado',
                'message': f'Ya existe un tipo de usuario con el nombre {data["type_name"]}'
            }), 400
        
        # Crear nuevo tipo de usuario
        new_user_type = UserType(
            type_name=data['type_name'],
            description=data.get('description', '')
        )
        
        db.session.add(new_user_type)
        db.session.commit()
        
        # Retornar tipo de usuario creado
        user_type_data = {
            'id': new_user_type.id,
            'type_name': new_user_type.type_name,
            'description': new_user_type.description,
            'created_at': new_user_type.created_at.isoformat() if new_user_type.created_at else None,
            'users_count': 0
        }
        
        return jsonify({
            'success': True,
            'message': 'Tipo de usuario creado exitosamente',
            'data': user_type_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
