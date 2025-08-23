from flask import jsonify, request
from app.controllers.access_log import access_log_bp
from app.models.access_log import AccessLog
from app import db

@access_log_bp.route('/<int:log_id>', methods=['GET'])
def show(log_id):
    """
    Obtiene un log de acceso específico por ID
    """
    try:
        log = AccessLog.query.get(log_id)
        
        if not log:
            return jsonify({
                'success': False,
                'error': 'Log de acceso no encontrado',
                'message': f'No existe un log de acceso con ID {log_id}'
            }), 404
        
        # Obtener información relacionada
        log_data = {
            'id': log.id,
            'user': {
                'id': log.user.id,
                'idDocumento': log.user.idDocumento,
                'first_name': log.user.first_name,
                'last_name': log.user.last_name,
                'user_type': log.user.user_type.type_name if log.user.user_type else None,
                'zona': {
                    'id': log.user.zona.id,
                    'sede_nombre': log.user.zona.sede_nombre,
                    'departamento': log.user.zona.departamento,
                    'ciudad': log.user.zona.ciudad
                } if log.user.zona else None,
                'estado': log.user.estado.name if log.user.estado else None,
                'is_active': log.user.is_active
            },
            'action_type': log.action_type,
            'timestamp': log.timestamp.isoformat() if log.timestamp else None,
            'fingerprint_confidence': float(log.fingerprint_confidence) if log.fingerprint_confidence else None,
            'status': log.status,
            'notes': log.notes,
            'created_by': {
                'id': log.created_by_user.id,
                'idDocumento': log.created_by_user.idDocumento,
                'first_name': log.created_by_user.first_name,
                'last_name': log.created_by_user.last_name,
                'user_type': log.created_by_user.user_type.type_name if log.created_by_user.user_type else None
            } if log.created_by_user else None
        }
        
        return jsonify({
            'success': True,
            'data': log_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
