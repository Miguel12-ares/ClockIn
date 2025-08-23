from flask import jsonify, request
from app.controllers.user_type import user_type_bp
from app.models.user_type import UserType
from app import db

@user_type_bp.route('/<int:user_type_id>', methods=['PUT'])
def update(user_type_id):
    """
    Actualiza un tipo de usuario existente
    """
    try:
        user_type = UserType.query.get(user_type_id)
        
        if not user_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de usuario no encontrado',
                'message': f'No existe un tipo de usuario con ID {user_type_id}'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para actualizar el tipo de usuario'
            }), 400
        
        # Validar y actualizar campos
        if 'type_name' in data:
            # Verificar que no exista otro tipo con el mismo nombre
            existing_type = UserType.query.filter(
                UserType.type_name == data['type_name'],
                UserType.id != user_type_id
            ).first()
            if existing_type:
                return jsonify({
                    'success': False,
                    'error': 'Tipo de usuario duplicado',
                    'message': f'Ya existe otro tipo de usuario con el nombre {data["type_name"]}'
                }), 400
            user_type.type_name = data['type_name']
        
        if 'description' in data:
            user_type.description = data['description']
        
        db.session.commit()
        
        # Retornar tipo de usuario actualizado
        user_type_data = {
            'id': user_type.id,
            'type_name': user_type.type_name,
            'description': user_type.description,
            'created_at': user_type.created_at.isoformat() if user_type.created_at else None,
            'users_count': len(user_type.users)
        }
        
        return jsonify({
            'success': True,
            'message': 'Tipo de usuario actualizado exitosamente',
            'data': user_type_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
