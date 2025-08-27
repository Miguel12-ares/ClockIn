from flask import jsonify, request
from app.controllers.zona import zona_bp
from app.models.zona import Zona
from app import db
from sqlalchemy.exc import OperationalError

@zona_bp.route('/', methods=['GET'])
def index():
    """
    Lista todas las zonas con información relacionada
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        ciudad = request.args.get('ciudad')
        departamento = request.args.get('departamento')
        
        # Construir query base
        query = Zona.query
        
        # Aplicar filtros
        if ciudad:
            query = query.filter(Zona.ciudad.ilike(f'%{ciudad}%'))
        if departamento:
            query = query.filter(Zona.departamento.ilike(f'%{departamento}%'))
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        zonas = []
        for zona in pagination.items:
            zona_data = {
                'id': zona.id,
                'nombre': zona.nombre,  # Usar el atributo mapeado
                'departamento': zona.departamento,
                'ciudad': zona.ciudad,
                'users_count': len(zona.users),
                'admins_count': len(zona.admins)
            }
            zonas.append(zona_data)
        
        return jsonify({
            'success': True,
            'data': zonas,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except OperationalError as e:
        return jsonify({
            'success': False,
            'error': 'Error de base de datos',
            'message': 'Error al acceder a la base de datos'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
