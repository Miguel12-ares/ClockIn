from flask import jsonify, request
from app.controllers.access_log import access_log_bp
from app.models.access_log import AccessLog
from app import db

@access_log_bp.route('/', methods=['GET'])
def index():
    """
    Lista todos los logs de acceso con información relacionada
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        user_id = request.args.get('user_id', type=int)
        action_type = request.args.get('action_type')
        status = request.args.get('status')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Construir query base
        query = AccessLog.query
        
        # Aplicar filtros
        if user_id:
            query = query.filter(AccessLog.user_id == user_id)
        if action_type:
            query = query.filter(AccessLog.action_type == action_type)
        if status:
            query = query.filter(AccessLog.status == status)
        if date_from:
            query = query.filter(AccessLog.timestamp >= date_from)
        if date_to:
            query = query.filter(AccessLog.timestamp <= date_to)
        
        # Ordenar por timestamp descendente (más recientes primero)
        query = query.order_by(AccessLog.timestamp.desc())
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        logs = []
        for log in pagination.items:
            log_data = {
                'id': log.id,
                'user': {
                    'id': log.user.id,
                    'idDocumento': log.user.idDocumento,
                    'first_name': log.user.first_name,
                    'last_name': log.user.last_name,
                    'user_type': log.user.user_type.type_name if log.user.user_type else None,
                    'zona': log.user.zona.sede_nombre if log.user.zona else None
                },
                'action_type': log.action_type,
                'timestamp': log.timestamp.isoformat() if log.timestamp else None,
                'fingerprint_confidence': float(log.fingerprint_confidence) if log.fingerprint_confidence else None,
                'status': log.status,
                'notes': log.notes,
                'created_by': {
                    'id': log.created_by_user.id,
                    'name': f"{log.created_by_user.first_name} {log.created_by_user.last_name}"
                } if log.created_by_user else None
            }
            logs.append(log_data)
        
        return jsonify({
            'success': True,
            'data': logs,
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
