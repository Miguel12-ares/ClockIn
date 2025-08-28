from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt,
    verify_jwt_in_request,
    set_access_cookies, set_refresh_cookies
)
from app.models.user import User
from app.models.user_type import UserType
from app.models.estado import Estado
from app.models.active_session import ActiveSession
from app.models.access_log import AccessLog
from app import db
import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de autenticación por ID de documento y contraseña

    Body esperado:
    {
        "idDocumento": "12345678",
        "password": "contraseña123"
    }

    Respuesta exitosa (tokens en cookies, no en JSON):
    {
        "success": true,
        "message": "Autenticación exitosa",
        "data": {
            "user": {
                "id": 1,
                "idDocumento": "12345678",
                "full_name": "Juan Pérez",
                "user_type": "Admin",
                "zona_id": 1
            },
            "session_id": 123
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Datos requeridos',
                'message': 'Se requieren datos JSON para autenticación'
            }), 400
        
        # Validar que el ID documento esté presente
        if 'idDocumento' not in data or not data['idDocumento']:
            return jsonify({
                'success': False,
                'error': 'ID documento requerido',
                'message': 'Se requiere el número de identificación para autenticarse'
            }), 400
        
        # Validar que la contraseña esté presente
        if 'password' not in data or not data['password']:
            return jsonify({
                'success': False,
                'error': 'Contraseña requerida',
                'message': 'Se requiere la contraseña para autenticarse'
            }), 400
        
        # Buscar usuario por ID documento
        id_documento = str(data['idDocumento']).strip()
        user = User.query.filter_by(idDocumento=id_documento).first()
        
        if not user:
            # Registrar intento de acceso fallido
            access_log = AccessLog(
                user_id=None,
                action_type='LOGIN_FAILED',
                status='USUARIO_NO_ENCONTRADO',
                notes=f'Intento de login con ID: {id_documento}'
            )
            db.session.add(access_log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': 'No existe un usuario registrado con ese número de identificación'
            }), 401
        
        # Verificar contraseña
        if not user.check_password(data['password']):
            # Registrar intento de acceso con contraseña incorrecta
            access_log = AccessLog(
                user_id=user.id,
                action_type='LOGIN_FAILED',
                status='CONTRASEÑA_INCORRECTA',
                notes=f'Intento de login con contraseña incorrecta: {id_documento}'
            )
            db.session.add(access_log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Credenciales incorrectas',
                'message': 'El número de identificación o la contraseña son incorrectos'
            }), 401
        
        # Verificar si el usuario está activo
        if not user.is_active:
            # Registrar intento de acceso con usuario inactivo
            access_log = AccessLog(
                user_id=user.id,
                action_type='LOGIN_FAILED',
                status='USUARIO_INACTIVO',
                notes=f'Intento de login con usuario inactivo: {id_documento}'
            )
            db.session.add(access_log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Usuario inactivo',
                'message': 'Su cuenta se encuentra desactivada. Contacte al administrador.'
            }), 401
        
        # Verificar que el estado del usuario sea "Activo"
        estado_activo = Estado.query.filter_by(nombre='Activo').first()
        if not estado_activo or user.estado_id != estado_activo.id:
            # Registrar intento de acceso con estado incorrecto
            access_log = AccessLog(
                user_id=user.id,
                action_type='LOGIN_FAILED',
                status='ESTADO_INCORRECTO',
                notes=f'Intento de login con estado incorrecto: {id_documento}'
            )
            db.session.add(access_log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Estado de usuario incorrecto',
                'message': 'Su cuenta no está en estado activo. Contacte al administrador.'
            }), 401
        
        # Crear tokens JWT (identity como string para 'sub')
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'id_documento': user.idDocumento,
                'user_type': user.user_type.type_name,
                'zona_id': user.zona_id,
                'is_active': user.is_active
            }
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={
                'id_documento': user.idDocumento,
                'user_type': user.user_type.type_name,
                'zona_id': user.zona_id,
                'is_active': user.is_active
            }
        )
        
        # Verificar si ya tiene una sesión activa
        existing_session = ActiveSession.query.filter_by(
            user_id=user.id,
            status='ACTIVE'
        ).first()
        
        if existing_session:
            # Cerrar sesión anterior
            existing_session.status = 'CLOSED_BY_NEW_LOGIN'
            
        # Crear nueva sesión activa
        new_session = ActiveSession(
            user_id=user.id,
            entry_time=datetime.datetime.utcnow(),
            status='ACTIVE'
        )
        db.session.add(new_session)
        
        # Registrar acceso exitoso
        access_log = AccessLog(
            user_id=user.id,
            action_type='LOGIN_SUCCESS',
            status='EXITOSO',
            notes=f'Login exitoso para usuario: {user.first_name} {user.last_name}'
        )
        db.session.add(access_log)
        
        db.session.commit()
        
        response = jsonify({
            'success': True,
            'message': 'Autenticación exitosa',
            'data': {
                'user': {
                    'id': user.id,
                    'idDocumento': user.idDocumento,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'user_type': user.user_type.type_name,
                    'zona_id': user.zona_id
                },
                'session_id': new_session.id
            }
        })
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error en login: {str(e)}")  # Para debugging
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante el proceso de autenticación'
        }), 500

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Endpoint para renovar access token usando refresh token
    
    Headers requeridos:
    Authorization: Bearer <refresh_token>
    
    Respuesta exitosa:
    {
        "success": true,
        "message": "Token renovado exitosamente",
        "data": {
            "access_token": "..."
        }
    }
    """
    try:
        # Obtener identidad del refresh token
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Verificar que el usuario aún existe y está activo
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Usuario inválido',
                'message': 'Usuario no encontrado o inactivo'
            }), 401
        
        # Verificar que el estado del usuario sea "Activo"
        estado_activo = Estado.query.filter_by(nombre='Activo').first()
        if not estado_activo or user.estado_id != estado_activo.id:
            return jsonify({
                'success': False,
                'error': 'Estado de usuario incorrecto',
                'message': 'Su cuenta no está en estado activo'
            }), 401
        
        # Crear nuevo access token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'id_documento': user.idDocumento,
                'user_type': user.user_type.type_name,
                'zona_id': user.zona_id,
                'is_active': user.is_active
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Token renovado exitosamente',
            'data': {
                'access_token': access_token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante la renovación del token'
        }), 500

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Endpoint para cerrar sesión
    Requiere access token en el header Authorization: Bearer <token>
    """
    try:
        user_id = get_jwt_identity()
        
        # Cerrar sesión activa
        active_session = ActiveSession.query.filter_by(
            user_id=user_id,
            status='ACTIVE'
        ).first()
        
        if active_session:
            active_session.status = 'CLOSED_BY_USER'
            
        # Registrar logout
        access_log = AccessLog(
            user_id=user_id,
            action_type='LOGOUT',
            status='EXITOSO',
            notes='Logout exitoso'
        )
        db.session.add(access_log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Sesión cerrada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante el proceso de logout'
        }), 500

@bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """
    Endpoint para verificar si un access token es válido
    """
    try:
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        # Verificar que el usuario aún existe y está activo
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'error': 'Usuario inválido',
                'message': 'Usuario no encontrado o inactivo'
            }), 401
        
        return jsonify({
            'success': True,
            'message': 'Token válido',
            'data': {
                'user_id': user_id,
                'id_documento': claims.get('id_documento'),
                'user_type': claims.get('user_type'),
                'zona_id': claims.get('zona_id')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante la verificación del token'
        }), 500

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Endpoint para obtener información del usuario actual
    """
    try:
        user_id = get_jwt_identity()
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado',
                'message': 'El usuario no existe'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': user.id,
                'idDocumento': user.idDocumento,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'full_name': f"{user.first_name} {user.last_name}",
                'user_type': user.user_type.type_name,
                'zona_id': user.zona_id,
                'is_active': user.is_active,
                'estado_id': user.estado_id
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error al obtener la información del usuario'
        }), 500


