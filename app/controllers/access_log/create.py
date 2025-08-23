from flask import jsonify, request
from app.controllers.access_log import access_log_bp
from app.models.access_log import AccessLog
from app.models.user import User
from app import db
from datetime import datetime

@access_log_bp.route('/', methods=['POST'])
def create():
    """
    Crea un nuevo log de acceso (para entradas/salidas)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear el log de acceso'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['user_id', 'action_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': 'Campo requerido faltante',
                    'message': f'El campo {field} es requerido'
                }), 400
        
        user_id = data['user_id']
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {user_id}'
            }), 404
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Usuario inactivo',
                'message': 'No se puede registrar acceso para un usuario inactivo'
            }), 400
        
        # Crear nuevo log de acceso
        new_log = AccessLog(
            user_id=user_id,
            action_type=data['action_type'],
            timestamp=data.get('timestamp', datetime.now()),
            fingerprint_confidence=data.get('fingerprint_confidence'),
            status=data.get('status', 'success'),
            notes=data.get('notes'),
            created_by=data.get('created_by')
        )
        
        db.session.add(new_log)
        db.session.commit()
        
        # Retornar log creado
        log_data = {
            'id': new_log.id,
            'user': {
                'id': new_log.user.id,
                'idDocumento': new_log.user.idDocumento,
                'first_name': new_log.user.first_name,
                'last_name': new_log.user.last_name,
                'user_type': new_log.user.user_type.type_name if new_log.user.user_type else None,
                'zona': new_log.user.zona.sede_nombre if new_log.user.zona else None
            },
            'action_type': new_log.action_type,
            'timestamp': new_log.timestamp.isoformat() if new_log.timestamp else None,
            'fingerprint_confidence': float(new_log.fingerprint_confidence) if new_log.fingerprint_confidence else None,
            'status': new_log.status,
            'notes': new_log.notes
        }
        
        return jsonify({
            'success': True,
            'message': 'Log de acceso creado exitosamente',
            'data': log_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
