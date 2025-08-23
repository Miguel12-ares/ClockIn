from flask import jsonify, request
from app.controllers.admin_zona import admin_zona_bp
from app.models.admin_zona import AdminZona
from app.models.user import User
from app.models.zona import Zona
from app import db

@admin_zona_bp.route('/<int:admin_id>/<int:zona_id>', methods=['DELETE'])
def remove(admin_id, zona_id):
    """
    Remueve un administrador de una zona
    """
    try:
        # Verificar que el usuario existe
        user = User.query.get(admin_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {admin_id}'
            }), 404
        
        # Verificar que la zona existe
        zona = Zona.query.get(zona_id)
        if not zona:
            return jsonify({
                'success': False,
                'error': 'Zona no encontrada',
                'message': f'No existe una zona con ID {zona_id}'
            }), 404
        
        # Buscar la asignación
        assignment = AdminZona.query.filter_by(
            admin_id=admin_id,
            zona_id=zona_id
        ).first()
        
        if not assignment:
            return jsonify({
                'success': False,
                'error': 'Asignación no encontrada',
                'message': f'El usuario {user.first_name} {user.last_name} no es administrador de la zona {zona.sede_nombre}'
            }), 404
        
        # Obtener información antes de eliminar
        assignment_info = {
            'admin_id': admin_id,
            'admin_name': f"{user.first_name} {user.last_name}",
            'admin_document': user.idDocumento,
            'zona_id': zona_id,
            'zona_name': zona.sede_nombre,
            'zona_location': f"{zona.ciudad}, {zona.departamento}"
        }
        
        # Eliminar asignación
        db.session.delete(assignment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Administrador removido exitosamente',
            'data': assignment_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
