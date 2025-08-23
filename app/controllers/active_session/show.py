from flask import jsonify, request
from app.controllers.active_session import active_session_bp
from app.models.active_session import ActiveSession
from app import db

@active_session_bp.route('/<int:session_id>', methods=['GET'])
def show(session_id):
    """
    Obtiene una sesión activa específica por ID
    """
    try:
        session = ActiveSession.query.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sesión activa no encontrada',
                'message': f'No existe una sesión activa con ID {session_id}'
            }), 404
        
        # Obtener información relacionada
        session_data = {
            'id': session.id,
            'user': {
                'id': session.user.id,
                'idDocumento': session.user.idDocumento,
                'first_name': session.user.first_name,
                'last_name': session.user.last_name,
                'user_type': session.user.user_type.type_name if session.user.user_type else None,
                'zona': {
                    'id': session.user.zona.id,
                    'sede_nombre': session.user.zona.sede_nombre,
                    'departamento': session.user.zona.departamento,
                    'ciudad': session.user.zona.ciudad
                } if session.user.zona else None,
                'estado': session.user.estado.name if session.user.estado else None,
                'is_active': session.user.is_active
            },
            'entry_time': session.entry_time.isoformat() if session.entry_time else None,
            'status': session.status,
            'created_at': session.created_at.isoformat() if session.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': session_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
