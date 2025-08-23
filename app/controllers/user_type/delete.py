from flask import jsonify, request
from app.controllers.user_type import user_type_bp
from app.models.user_type import UserType
from app import db

@user_type_bp.route('/<int:user_type_id>', methods=['DELETE'])
def delete(user_type_id):
    """
    Elimina un tipo de usuario (solo si no tiene usuarios asociados)
    """
    try:
        user_type = UserType.query.get(user_type_id)
        
        if not user_type:
            return jsonify({
                'success': False,
                'error': 'Tipo de usuario no encontrado',
                'message': f'No existe un tipo de usuario con ID {user_type_id}'
            }), 404
        
        # Verificar si el tipo tiene usuarios asociados
        if len(user_type.users) > 0:
            return jsonify({
                'success': False,
                'error': 'Tipo con usuarios asociados',
                'message': f'No se puede eliminar el tipo porque tiene {len(user_type.users)} usuarios asociados'
            }), 400
        
        # Obtener información del tipo antes de eliminar
        user_type_info = {
            'id': user_type.id,
            'type_name': user_type.type_name,
            'description': user_type.description
        }
        
        # Eliminar tipo de usuario
        db.session.delete(user_type)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tipo de usuario eliminado exitosamente',
            'data': user_type_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
