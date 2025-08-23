from flask import jsonify, request
from app.controllers.estado import estado_bp
from app.models.estado import Estado
from app import db

@estado_bp.route('/', methods=['GET'])
def index():
    """
    Lista todos los estados
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construir query base
        query = Estado.query
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        estados = []
        for estado in pagination.items:
            estado_data = {
                'id': estado.id,
                'name': estado.name,
                'description': estado.description,
                'users_count': len(estado.users)
            }
            estados.append(estado_data)
        
        return jsonify({
            'success': True,
            'data': estados,
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
