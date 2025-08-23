from flask import jsonify, request
from app.controllers.estado import estado_bp
from app.models.estado import Estado
from app import db

@estado_bp.route('/<int:estado_id>', methods=['DELETE'])
def delete(estado_id):
    """
    Elimina un estado (solo si no tiene usuarios asociados)
    """
    try:
        estado = Estado.query.get(estado_id)
        
        if not estado:
            return jsonify({
                'success': False,
                'error': 'Estado no encontrado',
                'message': f'No existe un estado con ID {estado_id}'
            }), 404
        
        # Verificar si el estado tiene usuarios asociados
        if len(estado.users) > 0:
            return jsonify({
                'success': False,
                'error': 'Estado con usuarios asociados',
                'message': f'No se puede eliminar el estado porque tiene {len(estado.users)} usuarios asociados'
            }), 400
        
        # Obtener información del estado antes de eliminar
        estado_info = {
            'id': estado.id,
            'name': estado.name,
            'description': estado.description
        }
        
        # Eliminar estado
        db.session.delete(estado)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Estado eliminado exitosamente',
            'data': estado_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
