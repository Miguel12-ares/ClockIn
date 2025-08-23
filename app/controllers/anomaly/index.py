from flask import jsonify, request
from app.controllers.anomaly import anomaly_bp
from app.models.anomaly import Anomaly
from app import db

@anomaly_bp.route('/', methods=['GET'])
def index():
    """
    Lista todas las anomalías
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        user_id = request.args.get('user_id', type=int)
        anomaly_type = request.args.get('anomaly_type')
        resolved = request.args.get('resolved', type=lambda v: v.lower() == 'true')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Construir query base
        query = Anomaly.query
        
        # Aplicar filtros
        if user_id:
            query = query.filter(Anomaly.user_id == user_id)
        if anomaly_type:
            query = query.filter(Anomaly.anomaly_type == anomaly_type)
        if resolved is not None:
            query = query.filter(Anomaly.resolved == resolved)
        if date_from:
            query = query.filter(Anomaly.detected_at >= date_from)
        if date_to:
            query = query.filter(Anomaly.detected_at <= date_to)
        
        # Ordenar por detected_at descendente (más recientes primero)
        query = query.order_by(Anomaly.detected_at.desc())
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        anomalies = []
        for anomaly in pagination.items:
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
            anomalies.append(anomaly_data)
        
        return jsonify({
            'success': True,
            'data': anomalies,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
