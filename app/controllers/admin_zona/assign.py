from flask import jsonify, request
from app.controllers.admin_zona import admin_zona_bp
from app.models.admin_zona import AdminZona
from app.models.user import User
from app.models.zona import Zona
from app import db

@admin_zona_bp.route('/', methods=['POST'])
def assign():
    """
    Asigna un administrador a una zona
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para asignar el administrador'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['admin_id', 'zona_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': 'Campo requerido faltante',
                    'message': f'El campo {field} es requerido'
                }), 400
        
        admin_id = data['admin_id']
        zona_id = data['zona_id']
        
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
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Usuario inactivo',
                'message': 'No se puede asignar un usuario inactivo como administrador'
            }), 400
        
        # Verificar si ya existe la asignación
        existing_assignment = AdminZona.query.filter_by(
            admin_id=admin_id,
            zona_id=zona_id
        ).first()
        
        if existing_assignment:
            return jsonify({
                'success': False,
                'error': 'Asignación duplicada',
                'message': f'El usuario {user.first_name} {user.last_name} ya es administrador de la zona {zona.sede_nombre}'
            }), 400
        
        # Crear nueva asignación
        new_assignment = AdminZona(
            admin_id=admin_id,
            zona_id=zona_id
        )
        
        db.session.add(new_assignment)
        db.session.commit()
        
        # Retornar información de la asignación
        assignment_data = {
            'admin_id': admin_id,
            'admin_name': f"{user.first_name} {user.last_name}",
            'admin_document': user.idDocumento,
            'zona_id': zona_id,
            'zona_name': zona.sede_nombre,
            'zona_location': f"{zona.ciudad}, {zona.departamento}"
        }
        
        return jsonify({
            'success': True,
            'message': 'Administrador asignado exitosamente',
            'data': assignment_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
