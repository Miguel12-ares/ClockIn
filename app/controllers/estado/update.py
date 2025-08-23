from flask import jsonify, request
from app.controllers.estado import estado_bp
from app.models.estado import Estado
from app import db

@estado_bp.route('/<int:estado_id>', methods=['PUT'])
def update(estado_id):
    """
    Actualiza un estado existente
    """
    try:
        estado = Estado.query.get(estado_id)
        
        if not estado:
            return jsonify({
                'success': False,
                'error': 'Estado no encontrado',
                'message': f'No existe un estado con ID {estado_id}'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para actualizar el estado'
            }), 400
        
        # Validar y actualizar campos
        if 'name' in data:
            # Verificar que no exista otro estado con el mismo nombre
            existing_estado = Estado.query.filter(
                Estado.name == data['name'],
                Estado.id != estado_id
            ).first()
            if existing_estado:
                return jsonify({
                    'success': False,
                    'error': 'Estado duplicado',
                    'message': f'Ya existe otro estado con el nombre {data["name"]}'
                }), 400
            estado.name = data['name']
        
        if 'description' in data:
            estado.description = data['description']
        
        db.session.commit()
        
        # Retornar estado actualizado
        estado_data = {
            'id': estado.id,
            'name': estado.name,
            'description': estado.description,
            'users_count': len(estado.users)
        }
        
        return jsonify({
            'success': True,
            'message': 'Estado actualizado exitosamente',
            'data': estado_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
