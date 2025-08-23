from flask import jsonify, request
from app.controllers.user_type import user_type_bp
from app.models.user_type import UserType
from app import db

@user_type_bp.route('/<int:user_type_id>', methods=['GET'])
def show(user_type_id):
    """
    Obtiene un tipo de usuario específico por ID
    """
    try:
        user_type = UserType.query.get(user_type_id)
        
        if not user_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de usuario no encontrado',
                'message': f'No existe un tipo de usuario con ID {user_type_id}'
            }), 404
        
        # Obtener información relacionada
        user_type_data = {
            'id': user_type.id,
            'type_name': user_type.type_name,
            'description': user_type.description,
            'created_at': user_type.created_at.isoformat() if user_type.created_at else None,
            'users': [
                {
                    'id': user.id,
                    'idDocumento': user.idDocumento,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'zona': user.zona.sede_nombre if user.zona else None,
                    'is_active': user.is_active
                }
                for user in user_type.users
            ],
            'users_count': len(user_type.users)
        }
        
        return jsonify({
            'success': True,
            'data': user_type_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
