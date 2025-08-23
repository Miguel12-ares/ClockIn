from flask import jsonify, request
from app.controllers.anomaly import anomaly_bp
from app.models.anomaly import Anomaly
from app.models.user import User
from app import db
from datetime import datetime

@anomaly_bp.route('/<int:anomaly_id>/resolve', methods=['PUT'])
def resolve(anomaly_id):
    """
    Resuelve una anomalía
    """
    try:
        anomaly = Anomaly.query.get(anomaly_id)
        
        if not anomaly:
            return jsonify({
                'success': False,
                'error': 'Anomalía no encontrada',
                'message': f'No existe una anomalía con ID {anomaly_id}'
            }), 404
        
        # Verificar si ya está resuelta
        if anomaly.resolved:
            return jsonify({
                'success': False,
                'error': 'Anomalía ya resuelta',
                'message': 'Esta anomalía ya ha sido resuelta'
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para resolver la anomalía'
            }), 400
        
        # Validar campos requeridos
        if 'resolved_by' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo requerido faltante',
                'message': 'El campo resolved_by es requerido'
            }), 400
        
        resolved_by = data['resolved_by']
        
        # Verificar que el usuario que resuelve existe
        resolver_user = User.query.get(resolved_by)
        if not resolver_user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {resolved_by}'
            }), 404
        
        # Actualizar anomalía como resuelta
        anomaly.resolved = True
        anomaly.resolved_at = data.get('resolved_at', datetime.now())
        anomaly.resolved_by = resolved_by
        anomaly.resolution_notes = data.get('resolution_notes', '')
        
        db.session.commit()
        
        # Retornar anomalía resuelta
        anomaly_data = {
            'id': anomaly.id,
            'user': {
                'id': anomaly.user.id,
                'idDocumento': anomaly.user.idDocumento,
                'first_name': anomaly.user.first_name,
                'last_name': anomaly.user.last_name,
                'user_type': anomaly.user.user_type.type_name if anomaly.user.user_type else None,
                'zona': anomaly.user.zona.sede_nombre if anomaly.user.zona else None
            },
            'anomaly_type': anomaly.anomaly_type,
            'description': anomaly.description,
            'detected_at': anomaly.detected_at.isoformat() if anomaly.detected_at else None,
            'resolved': anomaly.resolved,
            'resolved_at': anomaly.resolved_at.isoformat() if anomaly.resolved_at else None,
            'resolved_by': {
                'id': anomaly.resolved_by_user.id,
                'name': f"{anomaly.resolved_by_user.first_name} {anomaly.resolved_by_user.last_name}"
            } if anomaly.resolved_by_user else None,
            'resolution_notes': anomaly.resolution_notes
        }
        
        return jsonify({
            'success': True,
            'message': 'Anomalía resuelta exitosamente',
            'data': anomaly_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
