# Controlador de Usuarios

Este controlador maneja todas las operaciones relacionadas con los usuarios del sistema ClockIn.

## Rutas Disponibles

### GET /users
Lista todos los usuarios con información relacionada.

**Parámetros de consulta:**
- `page` (opcional): Número de página (por defecto: 1)
- `per_page` (opcional): Elementos por página (por defecto: 10)
- `user_type_id` (opcional): Filtrar por tipo de usuario
- `zona_id` (opcional): Filtrar por zona
- `estado_id` (opcional): Filtrar por estado
- `is_active` (opcional): Filtrar por estado activo (true/false)

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "idDocumento": 12345678,
      "first_name": "Juan",
      "last_name": "Pérez",
      "user_type": {
        "id": 1,
        "type_name": "Empleado"
      },
      "zona": {
        "id": 1,
        "sede_nombre": "Sede Principal",
        "departamento": "Bogotá",
        "ciudad": "Bogotá"
      },
      "estado": {
        "id": 1,
        "name": "Activo"
      },
      "is_active": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 50,
    "pages": 5,
    "has_next": true,
    "has_prev": false
  }
}
```

### GET /users/{id}
Obtiene un usuario específico por ID.

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "idDocumento": 12345678,
    "first_name": "Juan",
    "last_name": "Pérez",
    "user_type": {
      "id": 1,
      "type_name": "Empleado",
      "description": "Empleado regular"
    },
    "zona": {
      "id": 1,
      "sede_nombre": "Sede Principal",
      "departamento": "Bogotá",
      "ciudad": "Bogotá"
    },
    "estado": {
      "id": 1,
      "name": "Activo",
      "description": "Usuario activo"
    },
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "access_logs_count": 5,
    "active_sessions_count": 1,
    "anomalies_count": 0,
    "admin_zonas_count": 0
  }
}
```

### POST /users
Crea un nuevo usuario.

**Cuerpo de la petición:**
```json
{
  "idDocumento": 12345678,
  "first_name": "Juan",
  "last_name": "Pérez",
  "user_type_id": 1,
  "zona_id": 1,
  "estado_id": 1,
  "is_active": true,
  "fingerprint_data": "base64_encoded_data"
}
```

**Campos requeridos:**
- `idDocumento`: Número de documento único
- `first_name`: Nombre del usuario
- `last_name`: Apellido del usuario
- `user_type_id`: ID del tipo de usuario
- `zona_id`: ID de la zona

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "data": {
    "id": 1,
    "idDocumento": 12345678,
    "first_name": "Juan",
    "last_name": "Pérez",
    "user_type": {
      "id": 1,
      "type_name": "Empleado"
    },
    "zona": {
      "id": 1,
      "sede_nombre": "Sede Principal"
    },
    "estado": {
      "id": 1,
      "name": "Activo"
    },
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### PUT /users/{id}
Actualiza un usuario existente.

**Cuerpo de la petición:**
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Pérez García",
  "user_type_id": 2,
  "zona_id": 2,
  "estado_id": 1,
  "is_active": false
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Usuario actualizado exitosamente",
  "data": {
    "id": 1,
    "idDocumento": 12345678,
    "first_name": "Juan Carlos",
    "last_name": "Pérez García",
    "user_type": {
      "id": 2,
      "type_name": "Supervisor"
    },
    "zona": {
      "id": 2,
      "sede_nombre": "Sede Norte"
    },
    "estado": {
      "id": 1,
      "name": "Activo"
    },
    "is_active": false,
    "updated_at": "2024-01-01T12:00:00"
  }
}
```

### DELETE /users/{id}
Elimina un usuario.

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Usuario eliminado exitosamente",
  "data": {
    "id": 1,
    "idDocumento": 12345678,
    "first_name": "Juan",
    "last_name": "Pérez",
    "user_type": "Empleado",
    "zona": "Sede Principal"
  }
}
```

## Códigos de Error

- **400**: Datos inválidos o campos requeridos faltantes
- **404**: Usuario no encontrado
- **500**: Error interno del servidor

## Validaciones

- El `idDocumento` debe ser único
- Los usuarios no pueden eliminarse si tienen sesiones activas
- Los usuarios no pueden eliminarse si son administradores de zonas
- Los campos `user_type_id`, `zona_id` y `estado_id` deben referenciar registros existentes
