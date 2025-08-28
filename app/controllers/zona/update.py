from flask import jsonify, request
from app.controllers.zona import zona_bp
from app.models.zona import Zona
from app.middleware.auth_middleware import admin_required
from app import db

@zona_bp.route('/<int:zona_id>', methods=['PUT'])
@admin_required
def update(zona_id):
    """
    Actualiza una zona existente
    Requiere rol de administrador
    """
    try:
        zona = Zona.query.get(zona_id)
        
        if not zona:
            return jsonify({
                'success': False,
                'error': 'Zona no encontrada',
                'message': f'No existe una zona con ID {zona_id}'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para actualizar la zona'
            }), 400
        
        # Validar y actualizar campos
        if 'sede_nombre' in data:
            # Verificar que no exista otra zona con el mismo nombre en la misma ciudad
            existing_zona = Zona.query.filter(
                Zona.sede_nombre == data['sede_nombre'],
                Zona.ciudad == (data.get('ciudad', zona.ciudad)),
                Zona.id != zona_id
            ).first()
            if existing_zona:
                return jsonify({
                    'success': False,
                    'error': 'Zona duplicada',
                    'message': f'Ya existe otra zona con el nombre {data["sede_nombre"]} en {data.get("ciudad", zona.ciudad)}'
                }), 400
            zona.sede_nombre = data['sede_nombre']
        
        if 'departamento' in data:
            zona.departamento = data['departamento']
        
        if 'ciudad' in data:
            # Verificar que no exista otra zona con el mismo nombre en la nueva ciudad
            if 'sede_nombre' not in data:  # Si no se está cambiando el nombre
                existing_zona = Zona.query.filter(
                    Zona.sede_nombre == zona.sede_nombre,
                    Zona.ciudad == data['ciudad'],
                    Zona.id != zona_id
                ).first()
                if existing_zona:
                    return jsonify({
                        'success': False,
                        'error': 'Zona duplicada',
                        'message': f'Ya existe otra zona con el nombre {zona.sede_nombre} en {data["ciudad"]}'
                    }), 400
            zona.ciudad = data['ciudad']
        
        db.session.commit()
        
        # Retornar zona actualizada
        zona_data = {
            'id': zona.id,
            'sede_nombre': zona.sede_nombre,
            'departamento': zona.departamento,
            'ciudad': zona.ciudad,
            'users_count': len(zona.users),
            'admins_count': len(zona.admins)
        }
        
        return jsonify({
            'success': True,
            'message': 'Zona actualizada exitosamente',
            'data': zona_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
