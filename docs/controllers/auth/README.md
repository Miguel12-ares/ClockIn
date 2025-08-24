# Controlador de Autenticación

Este controlador maneja todas las operaciones relacionadas con la autenticación y manejo de sesiones del sistema ClockIn.

## Rutas Disponibles

### GET /auth/login
Muestra el formulario de login web.

**Respuesta exitosa (200):**
- Retorna página HTML con formulario de autenticación
- Interfaz simple sin diseño para ingreso de ID de documento

### POST /auth/login
Autentica un usuario usando su número de identificación único.

**Parámetros del cuerpo (JSON):**
```json
{
    "idDocumento": "12345678"
}
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Autenticación exitosa",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "idDocumento": "12345678",
            "full_name": "Juan Pérez",
            "user_type": "Instructor",
            "zona_id": 1
        },
        "session_id": 123,
        "redirect_url": "/instructor/dashboard"
    }
}
```

**Respuesta de error (401):**
```json
{
    "success": false,
    "error": "Usuario no encontrado",
    "message": "No existe un usuario registrado con ese número de identificación"
}
```

**Respuesta de error (400):**
```json
{
    "success": false,
    "error": "ID documento requerido",
    "message": "Se requiere el número de identificación para autenticarse"
}
```

### POST /auth/logout
Cierra la sesión activa del usuario autenticado.

**Headers requeridos:**
```
Authorization: Bearer <token_jwt>
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Sesión cerrada exitosamente"
}
```

**Respuesta de error (401):**
```json
{
    "success": false,
    "error": "Token inválido",
    "message": "Token de autenticación inválido o expirado"
}
```

### GET /auth/verify
Verifica si un token JWT es válido y retorna información del usuario.

**Headers requeridos:**
```
Authorization: Bearer <token_jwt>
```

**Respuesta exitosa (200):**
```json
{
    "success": true,
    "message": "Token válido",
    "data": {
        "user_id": 1,
        "id_documento": "12345678",
        "user_type": "Instructor",
        "zona_id": 1
    }
}
```

## Funcionalidades Implementadas

### Sistema JWT
- **Duración**: 8 horas por token
- **Algoritmo**: HS256
- **Payload**: user_id, id_documento, user_type, zona_id, exp, iat

### Validaciones de Seguridad
- ✅ Verificación de existencia del usuario
- ✅ Validación de estado activo
- ✅ Manejo de sesiones únicas
- ✅ Expiración automática de tokens
- ✅ Registro de intentos fallidos
- ✅ Protección contra tokens inválidos

### Sistema de Roles
Maneja 7 tipos de usuario con redirección automática:
- **SAdmin**: `/admin/dashboard`
- **Admin**: `/admin/dashboard`
- **Funcionario SENA**: `/funcionario/dashboard`
- **Instructor**: `/instructor/dashboard`
- **Aprendiz**: `/aprendiz/dashboard`
- **Administrativo**: `/administrativo/dashboard`
- **Ciudadano**: `/ciudadano/dashboard`

### Registro de Actividad
Todas las acciones se registran en `access_logs`:
- **LOGIN_SUCCESS**: Login exitoso
- **LOGIN_FAILED**: Login fallido (usuario no encontrado, inactivo)
- **LOGOUT**: Cierre de sesión manual

### Gestión de Sesiones
- Una sesión activa por usuario
- Cierre automático de sesión anterior al crear nueva
- Estado de sesiones: ACTIVE, CLOSED_BY_NEW_LOGIN, CLOSED_BY_USER

## Middleware de Seguridad

### @token_required
Decorador para proteger rutas que requieren autenticación JWT.

```python
from app.middleware.auth_middleware import token_required

@bp.route('/protected')
@token_required
def protected_route():
    # request.current_user contiene el usuario autenticado
    return jsonify({'user': request.current_user.first_name})
```

### @role_required
Decorador para proteger rutas según roles específicos.

```python
from app.middleware.auth_middleware import token_required, role_required

@bp.route('/admin-only')
@token_required
@role_required('SAdmin', 'Admin')
def admin_only():
    return jsonify({'message': 'Solo admins pueden acceder'})
```

### @admin_required
Decorador conveniente para rutas de administradores.

```python
from app.middleware.auth_middleware import token_required, admin_required

@bp.route('/admin-panel')
@token_required
@admin_required
def admin_panel():
    return jsonify({'message': 'Panel de administración'})
```

## Archivos Relacionados

- **Controlador**: `app/controllers/auth.py`
- **Middleware**: `app/middleware/auth_middleware.py`
- **Template**: `app/templates/login.html`
- **Modelos**: `app/models/user.py`, `app/models/active_session.py`, `app/models/access_log.py`

## Casos de Uso

### Flujo de Autenticación Completo
1. Usuario accede a `/auth/login`
2. Ingresa ID de documento en formulario
3. Sistema valida usuario y estado
4. Genera token JWT y sesión activa
5. Registra acceso en logs
6. Retorna token y URL de redirección
7. Cliente usa token para requests protegidos

### Ejemplo de Uso con JavaScript
```javascript
// Login
const response = await fetch('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idDocumento: '12345678' })
});

const data = await response.json();
if (data.success) {
    localStorage.setItem('token', data.data.token);
    window.location.href = data.data.redirect_url;
}

// Usar token en requests
const protectedResponse = await fetch('/some-protected-route', {
    headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
});
```

## Testing

### Crear Usuario de Prueba
```bash
# PowerShell
$body = @{idDocumento="12345678"; first_name="Juan"; last_name="Perez"; user_type_id=4; zona_id=1} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:5000/users/ -Method POST -Body $body -ContentType "application/json"
```

### Probar Login
```bash
# PowerShell
$body = @{idDocumento="12345678"} | ConvertTo-Json
Invoke-WebRequest -Uri http://localhost:5000/auth/login -Method POST -Body $body -ContentType "application/json"
```

### Verificar Token
```bash
# PowerShell
$headers = @{Authorization="Bearer TOKEN_AQUI"}
Invoke-WebRequest -Uri http://localhost:5000/auth/verify -Headers $headers
```
