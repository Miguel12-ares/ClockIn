from flask import jsonify, request
from app.controllers.zona import zona_bp
from app.models.zona import Zona
from app.middleware.auth_middleware import admin_required
from app import db

@zona_bp.route('/', methods=['POST'])
@admin_required
def create():
    """
    Crea una nueva zona
    Requiere rol de administrador
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear la zona'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['sede_nombre', 'departamento', 'ciudad']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': 'Campo requerido faltante',
                    'message': f'El campo {field} es requerido'
                }), 400
        
        # Verificar si ya existe una zona con el mismo nombre en la misma ciudad
        existing_zona = Zona.query.filter_by(
            sede_nombre=data['sede_nombre'],
            ciudad=data['ciudad']
        ).first()
        
        if existing_zona:
            return jsonify({
                'success': False,
                'error': 'Zona duplicada',
                'message': f'Ya existe una zona con el nombre {data["sede_nombre"]} en {data["ciudad"]}'
            }), 400
        
        # Crear nueva zona
        new_zona = Zona(
            sede_nombre=data['sede_nombre'],
            departamento=data['departamento'],
            ciudad=data['ciudad']
        )
        
        db.session.add(new_zona)
        db.session.commit()
        
        # Retornar zona creada
        zona_data = {
            'id': new_zona.id,
            'sede_nombre': new_zona.sede_nombre,
            'departamento': new_zona.departamento,
            'ciudad': new_zona.ciudad,
            'users_count': 0,
            'admins_count': 0
        }
        
        return jsonify({
            'success': True,
            'message': 'Zona creada exitosamente',
            'data': zona_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
