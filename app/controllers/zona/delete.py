from flask import jsonify, request
from app.controllers.zona import zona_bp
from app.models.zona import Zona
from app.middleware.auth_middleware import admin_required
from app import db

@zona_bp.route('/<int:zona_id>', methods=['DELETE'])
@admin_required
def delete(zona_id):
    """
    Elimina una zona (solo si no tiene usuarios asociados)
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
        
        # Verificar si la zona tiene usuarios asociados
        if len(zona.users) > 0:
            return jsonify({
                'success': False,
                'error': 'Zona con usuarios asociados',
                'message': f'No se puede eliminar la zona porque tiene {len(zona.users)} usuarios asociados'
            }), 400
        
        # Verificar si la zona tiene administradores asociados
        if len(zona.admins) > 0:
            return jsonify({
                'success': False,
                'error': 'Zona con administradores asociados',
                'message': f'No se puede eliminar la zona porque tiene {len(zona.admins)} administradores asociados'
            }), 400
        
        # Obtener información de la zona antes de eliminar
        zona_info = {
            'id': zona.id,
            'sede_nombre': zona.sede_nombre,
            'departamento': zona.departamento,
            'ciudad': zona.ciudad
        }
        
        # Eliminar zona
        db.session.delete(zona)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Zona eliminada exitosamente',
            'data': zona_info
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
