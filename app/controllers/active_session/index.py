from flask import jsonify, request
from app.controllers.active_session import active_session_bp
from app.models.active_session import ActiveSession
from app import db

@active_session_bp.route('/', methods=['GET'])
def index():
    """
    Lista todas las sesiones activas
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        user_id = request.args.get('user_id', type=int)
        status = request.args.get('status')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Construir query base
        query = ActiveSession.query
        
        # Aplicar filtros
        if user_id:
            query = query.filter(ActiveSession.user_id == user_id)
        if status:
            query = query.filter(ActiveSession.status == status)
        if date_from:
            query = query.filter(ActiveSession.entry_time >= date_from)
        if date_to:
            query = query.filter(ActiveSession.entry_time <= date_to)
        
        # Ordenar por entry_time descendente (más recientes primero)
        query = query.order_by(ActiveSession.entry_time.desc())
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        sessions = []
        for session in pagination.items:
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
            sessions.append(session_data)
        
        return jsonify({
            'success': True,
            'data': sessions,
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
