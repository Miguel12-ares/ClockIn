from flask import jsonify, request
from app.controllers.anomaly import anomaly_bp
from app.models.anomaly import Anomaly
from app import db

@anomaly_bp.route('/<int:anomaly_id>', methods=['GET'])
def show(anomaly_id):
    """
    Obtiene una anomalía específica por ID
    """
    try:
        anomaly = Anomaly.query.get(anomaly_id)
        
        if not anomaly:
            return jsonify({
                'success': False,
                'error': 'Anomalía no encontrada',
                'message': f'No existe una anomalía con ID {anomaly_id}'
            }), 404
        
        # Obtener información relacionada
        anomaly_data = {
            'id': anomaly.id,
            'user': {
                'id': anomaly.user.id,
                'idDocumento': anomaly.user.idDocumento,
                'first_name': anomaly.user.first_name,
                'last_name': anomaly.user.last_name,
                'user_type': anomaly.user.user_type.type_name if anomaly.user.user_type else None,
                'zona': {
                    'id': anomaly.user.zona.id,
                    'sede_nombre': anomaly.user.zona.sede_nombre,
                    'departamento': anomaly.user.zona.departamento,
                    'ciudad': anomaly.user.zona.ciudad
                } if anomaly.user.zona else None,
                'estado': anomaly.user.estado.name if anomaly.user.estado else None,
                'is_active': anomaly.user.is_active
            },
            'anomaly_type': anomaly.anomaly_type,
            'description': anomaly.description,
            'detected_at': anomaly.detected_at.isoformat() if anomaly.detected_at else None,
            'resolved': anomaly.resolved,
            'resolved_at': anomaly.resolved_at.isoformat() if anomaly.resolved_at else None,
            'resolved_by': {
                'id': anomaly.resolved_by_user.id,
                'idDocumento': anomaly.resolved_by_user.idDocumento,
                'first_name': anomaly.resolved_by_user.first_name,
                'last_name': anomaly.resolved_by_user.last_name,
                'user_type': anomaly.resolved_by_user.user_type.type_name if anomaly.resolved_by_user.user_type else None
            } if anomaly.resolved_by_user else None,
            'resolution_notes': anomaly.resolution_notes
        }
        
        return jsonify({
            'success': True,
            'data': anomaly_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
