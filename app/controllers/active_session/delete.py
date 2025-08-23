from flask import jsonify, request
from app.controllers.active_session import active_session_bp
from app.models.active_session import ActiveSession
from app import db

@active_session_bp.route('/<int:session_id>', methods=['DELETE'])
def delete(session_id):
    """
    Elimina una sesión activa (cierra sesión)
    """
    try:
        session = ActiveSession.query.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sesión activa no encontrada',
                'message': f'No existe una sesión activa con ID {session_id}'
            }), 404
        
        # Obtener información de la sesión antes de eliminar
        session_info = {
            'id': session.id,
            'user': {
                'id': session.user.id,
                'idDocumento': session.user.idDocumento,
                'first_name': session.user.first_name,
                'last_name': session.user.last_name
            },
            'entry_time': session.entry_time.isoformat() if session.entry_time else None,
            'status': session.status,
            'created_at': session.created_at.isoformat() if session.created_at else None
        }
        
        # Eliminar sesión activa
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sesión activa eliminada exitosamente',
            'data': session_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
