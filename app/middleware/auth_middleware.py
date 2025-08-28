from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models.user import User
from app.models.estado import Estado


def token_required(f):
    """
    Decorador para proteger rutas que requieren autenticación JWT
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Token requerido',
                'message': 'Se requiere token de autenticación'
            }), 401
        
        try:
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
            
            # Agregar datos del usuario al contexto de la request
            request.current_user = user
            request.current_user_payload = payload
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Error de autenticación',
                'message': 'Error al validar el token'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(*allowed_roles):
    """
    Decorador para proteger rutas según roles específicos
    Debe usarse junto con @token_required
    
    Ejemplo de uso:
    @token_required
    @role_required('SAdmin', 'Admin')
    def admin_only_endpoint():
        pass
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not hasattr(request, 'current_user'):
                return jsonify({
                    'success': False,
                    'error': 'Autenticación requerida',
                    'message': 'Debe estar autenticado para acceder a este recurso'
                }), 401
            
            user_role = request.current_user.user_type.type_name
            
            if user_role not in allowed_roles:
                return jsonify({
                    'success': False,
                    'error': 'Acceso denegado',
                    'message': f'No tiene permisos para acceder a este recurso. Rol requerido: {", ".join(allowed_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator


def admin_required(f):
    """
    Decorador conveniente para rutas que solo pueden acceder administradores
    """
    return role_required('SAdmin', 'Admin')(f)


def get_current_user():
    """
    Función helper para obtener el usuario actual en las rutas protegidas
    """
    if hasattr(request, 'current_user'):
        return request.current_user
    return None


def get_current_user_payload():
    """
    Función helper para obtener el payload JWT del usuario actual
    """
    if hasattr(request, 'current_user_payload'):
        return request.current_user_payload
    return None


def roles_required(*roles):
    """
    Decorador para verificar roles de usuario
    
    Args:
        *roles: Lista de roles permitidos (nombres de user_type)
    
    Ejemplo:
        @roles_required('Admin', 'SAdmin')
        def admin_only():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Verificar que el JWT sea válido
                verify_jwt_in_request()
                claims = get_jwt()
                
                # Obtener información del usuario desde el token
                user_id = claims.get('sub')  # sub es la identidad del token
                user_type = claims.get('user_type')
                is_active = claims.get('is_active')
                
                # Verificar que el usuario esté activo
                if not is_active:
                    return jsonify({
                        'success': False,
                        'error': 'Usuario inactivo',
                        'message': 'Su cuenta se encuentra desactivada'
                    }), 403
                
                # Verificar que el rol del usuario esté en la lista de roles permitidos
                if user_type not in roles:
                    return jsonify({
                        'success': False,
                        'error': 'Acceso denegado',
                        'message': 'No tiene permisos para acceder a este recurso'
                    }), 403
                
                # Verificar que el estado del usuario sea "activo" en la base de datos
                user = User.query.get(user_id)
                if not user:
                    return jsonify({
                        'success': False,
                        'error': 'Usuario no encontrado',
                        'message': 'El usuario no existe'
                    }), 401
                
                estado_activo = Estado.query.filter_by(name='activo').first()
                if user.estado_id != estado_activo.id:
                    return jsonify({
                        'success': False,
                        'error': 'Estado de usuario incorrecto',
                        'message': 'Su cuenta no está en estado activo'
                    }), 403
                
                return f(*args, **kwargs)
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Error de autenticación',
                    'message': 'Token inválido o expirado'
                }), 401
        
        return decorated_function
    return decorator

def admin_required(f):
    """
    Decorador específico para requerir rol de administrador
    """
    return roles_required('Admin', 'SAdmin')(f)

def fresh_token_required(f):
    """
    Decorador para requerir un token "fresco" (recién emitido)
    Útil para acciones sensibles como cambios de rol
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            
            # Verificar que el token sea "fresco" (no renovado)
            if not claims.get('fresh', False):
                return jsonify({
                    'success': False,
                    'error': 'Token no fresco',
                    'message': 'Se requiere un token recién emitido para esta acción'
                }), 401
            
            return f(*args, **kwargs)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Error de autenticación',
                'message': 'Token inválido o expirado'
            }), 401
    
    return decorated_function
