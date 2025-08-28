from flask import jsonify, request
from app.controllers.zona import zona_bp
from app.models.zona import Zona
from app.middleware.auth_middleware import admin_required
from app import db
from app.models.user import User
from app.models.admin_zona import AdminZona

@zona_bp.route('/<int:zona_id>', methods=['GET'])
@admin_required
def show(zona_id):
    """
    Obtiene una zona específica por ID con información relacionada
    Requiere rol de administrador
    """
    try:
        zona = Zona.query.options(
            db.selectinload(Zona.users).selectinload(User.user_type),
            db.selectinload(Zona.admins).selectinload(AdminZona.admin)
        ).get(zona_id)
        
        if not zona:
            return jsonify({
                'success': False,
                'error': 'Zona no encontrada',
                'message': f'No existe una zona con ID {zona_id}'
            }), 404
        
        # Obtener información relacionada
        zona_data = {
            'id': zona.id,
            'sede_nombre': zona.sede_nombre,
            'departamento': zona.departamento,
            'ciudad': zona.ciudad,
            'users': [
                {
                    'id': user.id,
                    'idDocumento': user.idDocumento,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_type': user.user_type.type_name if user.user_type else None,
                    'is_active': user.is_active
                }
                for user in zona.users
            ],
            'admins': [
                {
                    'admin_id': admin.admin_id,
                    'admin_name': f"{admin.admin.first_name} {admin.admin.last_name}" if admin.admin else None
                }
                for admin in zona.admins
            ],
            'users_count': len(zona.users),
            'admins_count': len(zona.admins)
        }
        
        return jsonify({
            'success': True,
            'data': zona_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
