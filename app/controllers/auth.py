from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from app.models.user import User
from app.models.user_type import UserType
from app.models.active_session import ActiveSession
from app.models.access_log import AccessLog
from app import db
import jwt
import datetime
import os

bp = Blueprint('auth', __name__)

def generate_jwt_token(user):
    """Genera un token JWT para el usuario"""
    payload = {
        'user_id': user.id,
        'id_documento': user.idDocumento,
        'user_type': user.user_type.type_name,
        'zona_id': user.zona_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),  # Token válido por 8 horas
        'iat': datetime.datetime.utcnow()
    }
    secret_key = os.getenv('SECRET_KEY', 'default_secret')
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_jwt_token(token):
    """Verifica y decodifica un token JWT"""
    try:
        secret_key = os.getenv('SECRET_KEY', 'default_secret')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint de autenticación por ID de documento
    
    Body esperado:
    {
        "idDocumento": "12345678"
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
        
        # Generar token JWT
        token = generate_jwt_token(user)
        
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
        
        # Determinar redirección según rol
        redirect_url = get_redirect_url_by_role(user.user_type.type_name)
        
        return jsonify({
            'success': True,
            'message': 'Autenticación exitosa',
            'data': {
                'token': token,
                'user': {
                    'id': user.id,
                    'idDocumento': user.idDocumento,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'user_type': user.user_type.type_name,
                    'zona_id': user.zona_id
                },
                'session_id': new_session.id,
                'redirect_url': redirect_url
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante el proceso de autenticación'
        }), 500

@bp.route('/logout', methods=['POST'])
def logout():
    """
    Endpoint para cerrar sesión
    Requiere token JWT en el header Authorization: Bearer <token>
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Token requerido',
                'message': 'Se requiere token de autenticación'
            }), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Token inválido',
                'message': 'Token de autenticación inválido o expirado'
            }), 401
        
        user_id = payload['user_id']
        
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
def verify_token():
    """
    Endpoint para verificar si un token JWT es válido
    """
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Token requerido',
                'message': 'Se requiere token de autenticación'
            }), 401
        
        token = auth_header.split(' ')[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Token inválido',
                'message': 'Token de autenticación inválido o expirado'
            }), 401
        
        # Verificar que el usuario aún existe y está activo
        user = User.query.get(payload['user_id'])
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
                'user_id': payload['user_id'],
                'id_documento': payload['id_documento'],
                'user_type': payload['user_type'],
                'zona_id': payload['zona_id']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'message': 'Ocurrió un error durante la verificación del token'
        }), 500

def get_redirect_url_by_role(user_type):
    """
    Determina la URL de redirección según el tipo de usuario
    """
    role_redirects = {
        'SAdmin': '/admin/dashboard',
        'Admin': '/admin/dashboard',
        'Funcionario SENA': '/funcionario/dashboard',
        'Instructor': '/instructor/dashboard',
        'Aprendiz': '/aprendiz/dashboard',
        'Administrativo': '/administrativo/dashboard',
        'Ciudadano': '/ciudadano/dashboard'
    }
    
    return role_redirects.get(user_type, '/dashboard')

@bp.route('/login', methods=['GET'])
def login_form():
    """
    Muestra el formulario de login
    """
    return render_template('login.html')


