from flask import jsonify, request
from app.controllers.system_audit import system_audit_bp
from app.models.system_audit import SystemAudit
from app import db

@system_audit_bp.route('/', methods=['GET'])
def index():
    """
    Lista todas las auditorías del sistema (solo para administradores)
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        user_id = request.args.get('user_id', type=int)
        table_affected = request.args.get('table_affected')
        action_type = request.args.get('action_type')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Construir query base
        query = SystemAudit.query
        
        # Aplicar filtros
        if user_id:
            query = query.filter(SystemAudit.user_id == user_id)
        if table_affected:
            query = query.filter(SystemAudit.table_affected == table_affected)
        if action_type:
            query = query.filter(SystemAudit.action_type == action_type)
        if date_from:
            query = query.filter(SystemAudit.timestamp >= date_from)
        if date_to:
            query = query.filter(SystemAudit.timestamp <= date_to)
        
        # Ordenar por timestamp descendente (más recientes primero)
        query = query.order_by(SystemAudit.timestamp.desc())
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        audits = []
        for audit in pagination.items:
            audit_data = {
                'id': audit.id,
                'user': {
                    'id': audit.user.id,
                    'idDocumento': audit.user.idDocumento,
                    'first_name': audit.user.first_name,
                    'last_name': audit.user.last_name,
                    'user_type': audit.user.user_type.type_name if audit.user.user_type else None,
                    'zona': audit.user.zona.sede_nombre if audit.user.zona else None
                } if audit.user else None,
                'table_affected': audit.table_affected,
                'action_type': audit.action_type,
                'old_values': audit.old_values,
                'new_values': audit.new_values,
                'timestamp': audit.timestamp.isoformat() if audit.timestamp else None,
                'ip_address': audit.ip_address
            }
            audits.append(audit_data)
        
        return jsonify({
            'success': True,
            'data': audits,
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
