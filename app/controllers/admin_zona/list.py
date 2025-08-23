from flask import jsonify, request
from app.controllers.admin_zona import admin_zona_bp
from app.models.admin_zona import AdminZona
from app import db

@admin_zona_bp.route('/', methods=['GET'])
def list():
    """
    Lista todas las asignaciones de administradores a zonas
    """
    try:
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Filtros opcionales
        admin_id = request.args.get('admin_id', type=int)
        zona_id = request.args.get('zona_id', type=int)
        
        # Construir query base
        query = AdminZona.query
        
        # Aplicar filtros
        if admin_id:
            query = query.filter(AdminZona.admin_id == admin_id)
        if zona_id:
            query = query.filter(AdminZona.zona_id == zona_id)
        
        # Paginar resultados
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        assignments = []
        for assignment in pagination.items:
            assignment_data = {
                'admin_id': assignment.admin_id,
                'admin_name': f"{assignment.admin.first_name} {assignment.admin.last_name}" if assignment.admin else None,
                'admin_document': assignment.admin.idDocumento if assignment.admin else None,
                'admin_user_type': assignment.admin.user_type.type_name if assignment.admin and assignment.admin.user_type else None,
                'zona_id': assignment.zona_id,
                'zona_name': assignment.zona.sede_nombre if assignment.zona else None,
                'zona_location': f"{assignment.zona.ciudad}, {assignment.zona.departamento}" if assignment.zona else None
            }
            assignments.append(assignment_data)
        
        return jsonify({
            'success': True,
            'data': assignments,
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
