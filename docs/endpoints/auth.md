# Documentación - Endpoints de Autenticación

Esta documentación describe los endpoints del sistema de autenticación del ClockIn.

## Endpoints Disponibles

### 1. Login - Autenticación por ID

**POST** `/auth/login`

Autentica un usuario usando su número de identificación único y retorna un token JWT.

#### Request Body
```json
{
    "idDocumento": "12345678"
}
```

#### Response Exitoso (200)
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

#### Response Error (401)
```json
{
    "success": false,
    "error": "Usuario no encontrado",
    "message": "No existe un usuario registrado con ese número de identificación"
}
```

#### Response Error (400)
```json
{
    "success": false,
    "error": "ID documento requerido",
    "message": "Se requiere el número de identificación para autenticarse"
}
```

### 2. Logout - Cerrar Sesión

**POST** `/auth/logout`

Cierra la sesión activa del usuario autenticado.

#### Headers
```
Authorization: Bearer <token_jwt>
```

#### Response Exitoso (200)
```json
{
    "success": true,
    "message": "Sesión cerrada exitosamente"
}
```

#### Response Error (401)
```json
{
    "success": false,
    "error": "Token inválido",
    "message": "Token de autenticación inválido o expirado"
}
```

### 3. Verificar Token

**GET** `/auth/verify`

Verifica si un token JWT es válido y retorna información del usuario.

#### Headers
```
Authorization: Bearer <token_jwt>
```

#### Response Exitoso (200)
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

### 4. Formulario de Login

**GET** `/auth/login`

Muestra el formulario web de login.

#### Response
Retorna página HTML con formulario de autenticación.

## Sistema de Roles y Redirección

El sistema maneja los siguientes roles con sus respectivas URLs de redirección:

| Rol | URL de Redirección |
|-----|-------------------|
| SAdmin | `/admin/dashboard` |
| Admin | `/admin/dashboard` |
| Funcionario SENA | `/funcionario/dashboard` |
| Instructor | `/instructor/dashboard` |
| Aprendiz | `/aprendiz/dashboard` |
| Administrativo | `/administrativo/dashboard` |
| Ciudadano | `/ciudadano/dashboard` |

## Seguridad

### Token JWT
- **Duración**: 8 horas
- **Algoritmo**: HS256
- **Payload incluye**:
  - user_id: ID interno del usuario
  - id_documento: Número de identificación
  - user_type: Tipo/rol del usuario
  - zona_id: ID de la zona asignada
  - exp: Fecha de expiración
  - iat: Fecha de emisión

### Validaciones
- El ID documento debe existir en la base de datos
- El usuario debe estar activo (`is_active = true`)
- Se registra cada intento de login (exitoso o fallido)
- Se maneja una sesión activa por usuario
- Se cierra automáticamente la sesión anterior al crear una nueva

## Middleware de Autenticación

### @token_required
Decorador para proteger rutas que requieren autenticación.

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

## Registro de Actividad

Todas las acciones de autenticación se registran en la tabla `access_logs`:

- **LOGIN_SUCCESS**: Login exitoso
- **LOGIN_FAILED**: Login fallido (usuario no encontrado, inactivo)
- **LOGOUT**: Cierre de sesión manual

## Ejemplo de Uso

### JavaScript (Frontend)
```javascript
// Login
const response = await fetch('/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        idDocumento: '12345678'
    })
});

const data = await response.json();

if (data.success) {
    // Guardar token
    localStorage.setItem('token', data.data.token);
    // Redirigir
    window.location.href = data.data.redirect_url;
}

// Usar token en requests posteriores
const protectedResponse = await fetch('/some-protected-route', {
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
});
```

### Python (Cliente API)
```python
import requests

# Login
login_response = requests.post('http://localhost:5000/auth/login', 
    json={'idDocumento': '12345678'})

if login_response.json()['success']:
    token = login_response.json()['data']['token']
    
    # Usar token
    headers = {'Authorization': f'Bearer {token}'}
    protected_response = requests.get('http://localhost:5000/some-route', 
        headers=headers)
```
