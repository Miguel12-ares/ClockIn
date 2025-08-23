from flask import jsonify, request
from app.controllers.anomaly import anomaly_bp
from app.models.anomaly import Anomaly
from app.models.user import User
from app import db
from datetime import datetime

@anomaly_bp.route('/', methods=['POST'])
def create():
    """
    Crea una nueva anomalía
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear la anomalía'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['user_id', 'anomaly_type']
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
        
        # Crear nueva anomalía
        new_anomaly = Anomaly(
            user_id=user_id,
            anomaly_type=data['anomaly_type'],
            description=data.get('description'),
            detected_at=data.get('detected_at', datetime.now()),
            resolved=data.get('resolved', False),
            resolved_at=data.get('resolved_at'),
            resolved_by=data.get('resolved_by'),
            resolution_notes=data.get('resolution_notes')
        )
        
        db.session.add(new_anomaly)
        db.session.commit()
        
        # Retornar anomalía creada
        anomaly_data = {
            'id': new_anomaly.id,
            'user': {
                'id': new_anomaly.user.id,
                'idDocumento': new_anomaly.user.idDocumento,
                'first_name': new_anomaly.user.first_name,
                'last_name': new_anomaly.user.last_name,
                'user_type': new_anomaly.user.user_type.type_name if new_anomaly.user.user_type else None,
                'zona': new_anomaly.user.zona.sede_nombre if new_anomaly.user.zona else None
            },
            'anomaly_type': new_anomaly.anomaly_type,
            'description': new_anomaly.description,
            'detected_at': new_anomaly.detected_at.isoformat() if new_anomaly.detected_at else None,
            'resolved': new_anomaly.resolved,
            'resolved_at': new_anomaly.resolved_at.isoformat() if new_anomaly.resolved_at else None,
            'resolution_notes': new_anomaly.resolution_notes
        }
        
        return jsonify({
            'success': True,
            'message': 'Anomalía creada exitosamente',
            'data': anomaly_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
