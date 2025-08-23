from flask import jsonify, request
from app.controllers.user import user_bp
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app import db

@user_bp.route('/', methods=['GET'])
def index():
    """
    Lista todos los usuarios con información relacionada
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        user_type_id = request.args.get('user_type_id', type=int)
        zona_id = request.args.get('zona_id', type=int)
        estado_id = request.args.get('estado_id', type=int)
        is_active = request.args.get('is_active', type=lambda v: v.lower() == 'true')
        
        # Construir query base
        query = User.query
        
        # Aplicar filtros
        if user_type_id:
            query = query.filter(User.user_type_id == user_type_id)
        if zona_id:
            query = query.filter(User.zona_id == zona_id)
        if estado_id:
            query = query.filter(User.estado_id == estado_id)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        users = []
        for user in pagination.items:
            user_data = {
                'id': user.id,
                'idDocumento': user.idDocumento,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_type': {
                    'id': user.user_type.id,
                    'type_name': user.user_type.type_name
                },
                'zona': {
                    'id': user.zona.id,
                    'sede_nombre': user.zona.sede_nombre,
                    'departamento': user.zona.departamento,
                    'ciudad': user.zona.ciudad
                },
                'estado': {
                    'id': user.estado.id,
                    'name': user.estado.name
                },
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None
            }
            users.append(user_data)
        
        return jsonify({
            'success': True,
            'data': users,
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
