from flask import jsonify, request
from app.controllers.active_session import active_session_bp
from app.models.active_session import ActiveSession
from app.models.user import User
from app import db
from datetime import datetime

@active_session_bp.route('/', methods=['POST'])
def create():
    """
    Crea una nueva sesión activa (inicia sesión)
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para crear la sesión activa'
            }), 400
        
        # Validar campos requeridos
        if 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo requerido faltante',
                'message': 'El campo user_id es requerido'
            }), 400
        
        user_id = data['user_id']
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': f'No existe un usuario con ID {user_id}'
            }), 404
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Usuario inactivo',
                'message': 'No se puede crear una sesión para un usuario inactivo'
            }), 400
        
        # Verificar si el usuario ya tiene una sesión activa
        existing_session = ActiveSession.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if existing_session:
            return jsonify({
                'success': False,
                'error': 'Sesión activa existente',
                'message': f'El usuario {user.first_name} {user.last_name} ya tiene una sesión activa'
            }), 400
        
        # Crear nueva sesión activa
        new_session = ActiveSession(
            user_id=user_id,
            entry_time=data.get('entry_time', datetime.now()),
            status=data.get('status', 'active')
        )
        
        db.session.add(new_session)
        db.session.commit()
        
        # Retornar sesión creada
        session_data = {
            'id': new_session.id,
            'user': {
                'id': new_session.user.id,
                'idDocumento': new_session.user.idDocumento,
                'first_name': new_session.user.first_name,
                'last_name': new_session.user.last_name,
                'user_type': new_session.user.user_type.type_name if new_session.user.user_type else None,
                'zona': new_session.user.zona.sede_nombre if new_session.user.zona else None
            },
            'entry_time': new_session.entry_time.isoformat() if new_session.entry_time else None,
            'status': new_session.status,
            'created_at': new_session.created_at.isoformat() if new_session.created_at else None
        }
        
        return jsonify({
            'success': True,
            'message': 'Sesión activa creada exitosamente',
            'data': session_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': str(e)
        }), 500
