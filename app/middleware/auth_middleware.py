from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from app.models.user import User
from app.models.estado import Estado


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
                user_id = get_jwt_identity()
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
                
                # Verificar que el estado del usuario sea "Activo" en la base de datos
                user = User.query.get(user_id)
                if not user:
                    return jsonify({
                        'success': False,
                        'error': 'Usuario no encontrado',
                        'message': 'El usuario no existe'
                    }), 401
                
                estado_activo = Estado.query.filter_by(nombre='Activo').first()
                if not estado_activo or user.estado_id != estado_activo.id:
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
