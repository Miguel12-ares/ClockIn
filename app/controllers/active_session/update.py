from flask import jsonify, request
from app.controllers.active_session import active_session_bp
from app.models.active_session import ActiveSession
from app import db
from datetime import datetime

@active_session_bp.route('/<int:session_id>', methods=['PUT'])
def update(session_id):
    """
    Actualiza una sesión activa (e.g., salida)
    """
    try:
        session = ActiveSession.query.get(session_id)
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Sesión activa no encontrada',
                'message': f'No existe una sesión activa con ID {session_id}'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para actualizar la sesión activa'
            }), 400
        
        # Validar y actualizar campos
        if 'entry_time' in data:
            session.entry_time = data['entry_time']
        
        if 'status' in data:
            session.status = data['status']
        
        db.session.commit()
        
        # Retornar sesión actualizada
        session_data = {
            'id': session.id,
            'user': {
                'id': session.user.id,
                'idDocumento': session.user.idDocumento,
                'first_name': session.user.first_name,
                'last_name': session.user.last_name,
                'user_type': session.user.user_type.type_name if session.user.user_type else None,
                'zona': session.user.zona.sede_nombre if session.user.zona else None
            },
            'entry_time': session.entry_time.isoformat() if session.entry_time else None,
            'status': session.status,
            'created_at': session.created_at.isoformat() if session.created_at else None
        }
        
        return jsonify({
            'success': True,
            'message': 'Sesión activa actualizada exitosamente',
            'data': session_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
