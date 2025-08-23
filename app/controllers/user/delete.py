from flask import jsonify, request
from app.controllers.user import user_bp
from app.models.user import User
from app.models.active_session import ActiveSession
from app.models.admin_zona import AdminZona
from app import db

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete(user_id):
    """
    Elimina un usuario (soft delete o hard delete según configuración)
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {user_id}'
            }), 404
        
        # Verificar si el usuario tiene sesiones activas
        active_sessions = ActiveSession.query.filter_by(user_id=user_id, status='active').first()
        if active_sessions:
            return jsonify({
                'success': False,
                'error': 'Usuario con sesión activa',
                'message': 'No se puede eliminar un usuario que tiene una sesión activa'
            }), 400
        
        # Verificar si el usuario es admin de alguna zona
        admin_zonas = AdminZona.query.filter_by(admin_id=user_id).first()
        if admin_zonas:
            return jsonify({
                'success': False,
                'error': 'Usuario es administrador',
                'message': 'No se puede eliminar un usuario que es administrador de una zona'
            }), 400
        
        # Obtener información del usuario antes de eliminar
        user_info = {
            'id': user.id,
            'idDocumento': user.idDocumento,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': user.user_type.type_name if user.user_type else None,
            'zona': user.zona.sede_nombre if user.zona else None
        }
        
        # Eliminar usuario (hard delete)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuario eliminado exitosamente',
            'data': user_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
