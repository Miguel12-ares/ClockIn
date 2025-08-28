from flask import jsonify, request
from app.controllers.user_type import user_type_bp
from app.models.user_type import UserType
from app.middleware.auth_middleware import admin_required
from app import db

@user_type_bp.route('/', methods=['GET'])
@admin_required
def index():
    """
    Lista todos los tipos de usuario
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construir query base
        query = UserType.query
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        user_types = []
        for user_type in pagination.items:
            user_type_data = {
                'id': user_type.id,
                'type_name': user_type.type_name,
                'description': user_type.description,
                'created_at': user_type.created_at.isoformat() if user_type.created_at else None,
                'users_count': len(user_type.users)
            }
            user_types.append(user_type_data)
        
        return jsonify({
            'success': True,
            'data': user_types,
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
