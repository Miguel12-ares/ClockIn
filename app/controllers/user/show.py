from flask import jsonify, request
from app.controllers.user import user_bp
from app.models.user import User
from app import db

@user_bp.route('/<int:user_id>', methods=['GET'])
def show(user_id):
    """
    Obtiene un usuario específico por ID con información relacionada
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {user_id}'
            }), 404
        
        # Obtener información relacionada
        user_data = {
            'id': user.id,
            'idDocumento': user.idDocumento,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': {
                'id': user.user_type.id,
                'type_name': user.user_type.type_name,
                'description': user.user_type.description
            },
            'zona': {
                'id': user.zona.id,
                'sede_nombre': user.zona.sede_nombre,
                'departamento': user.zona.departamento,
                'ciudad': user.zona.ciudad
            },
            'estado': {
                'id': user.estado.id,
                'name': user.estado.name,
                'description': user.estado.description
            },
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            # Información adicional
            'access_logs_count': len(user.access_logs),
            'active_sessions_count': len(user.active_sessions),
            'anomalies_count': len(user.anomalies),
            'admin_zonas_count': len(user.admin_zonas)
        }
        
        return jsonify({
            'success': True,
            'data': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
