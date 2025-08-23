from flask import jsonify, request
from app.controllers.estado import estado_bp
from app.models.estado import Estado
from app import db

@estado_bp.route('/<int:estado_id>', methods=['GET'])
def show(estado_id):
    """
    Obtiene un estado específico por ID
    """
    try:
        estado = Estado.query.get(estado_id)
        
        if not estado:
            return jsonify({
                'success': False,
                'error': 'Estado no encontrado',
                'message': f'No existe un estado con ID {estado_id}'
            }), 404
        
        # Obtener información relacionada
        estado_data = {
            'id': estado.id,
            'name': estado.name,
            'description': estado.description,
            'users': [
                {
                    'id': user.id,
                    'idDocumento': user.idDocumento,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type.type_name if user.user_type else None,
                    'zona': user.zona.sede_nombre if user.zona else None,
                    'is_active': user.is_active
                }
                for user in estado.users
            ],
            'users_count': len(estado.users)
        }
        
        return jsonify({
            'success': True,
            'data': estado_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
