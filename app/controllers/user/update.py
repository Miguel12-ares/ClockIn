from flask import jsonify, request
from app.controllers.user import user_bp
from app.models.user import User
from app.models.user_type import UserType
from app.models.zona import Zona
from app.models.estado import Estado
from app import db

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update(user_id):
    """
    Actualiza un usuario existente
    """
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {user_id}'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para actualizar el usuario'
            }), 400
        
        # Validar y actualizar campos
        if 'idDocumento' in data:
            # Verificar que el documento no esté duplicado (excluyendo el usuario actual)
            existing_user = User.query.filter(
                User.idDocumento == data['idDocumento'],
                User.id != user_id
            ).first()
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'Documento duplicado',
                    'message': f'Ya existe otro usuario con el documento {data["idDocumento"]}'
                }), 400
            user.idDocumento = data['idDocumento']
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        if 'user_type_id' in data:
            user_type = UserType.query.get(data['user_type_id'])
            if not user_type:
                return jsonify({
                    'success': False,
                    'error': 'Tipo de usuario inválido',
                    'message': f'No existe un tipo de usuario con ID {data["user_type_id"]}'
                }), 400
            user.user_type_id = data['user_type_id']
        
        if 'zona_id' in data:
            zona = Zona.query.get(data['zona_id'])
            if not zona:
                return jsonify({
                    'success': False,
                    'error': 'Zona inválida',
                    'message': f'No existe una zona con ID {data["zona_id"]}'
                }), 400
            user.zona_id = data['zona_id']
        
        if 'estado_id' in data:
            estado = Estado.query.get(data['estado_id'])
            if not estado:
                return jsonify({
                    'success': False,
                    'error': 'Estado inválido',
                    'message': f'No existe un estado con ID {data["estado_id"]}'
                }), 400
            user.estado_id = data['estado_id']
        
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        
        if 'fingerprint_data' in data:
            user.fingerprint_data = data['fingerprint_data']
        
        db.session.commit()
        
        # Retornar usuario actualizado
        user_data = {
            'id': user.id,
            'idDocumento': user.idDocumento,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_type': {
                'id': user.user_type.id,
                'type_name': user.user_type.type_name
            },
            'zona': {
                'id': user.zona.id,
                'sede_nombre': user.zona.sede_nombre
            },
            'estado': {
                'id': user.estado.id,
                'name': user.estado.name
            },
            'is_active': user.is_active,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': user_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
