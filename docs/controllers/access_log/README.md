# Controlador de Logs de Acceso

Este controlador maneja el registro y consulta de logs de acceso al sistema ClockIn.

## Rutas Disponibles

### GET /access_logs
Lista todos los logs de acceso con información relacionada.

**Parámetros de consulta:**
- `page` (opcional): Número de página (por defecto: 1)
- `per_page` (opcional): Elementos por página (por defecto: 10)
- `user_id` (opcional): Filtrar por ID del usuario
- `action_type` (opcional): Filtrar por tipo de acción
- `status` (opcional): Filtrar por estado
- `date_from` (opcional): Filtrar desde fecha (formato: YYYY-MM-DD)
- `date_to` (opcional): Filtrar hasta fecha (formato: YYYY-MM-DD)

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "idDocumento": 12345678,
        "first_name": "Juan",
        "last_name": "Pérez",
        "user_type": "Empleado",
        "zona": "Sede Principal"
      },
      "action_type": "entry",
      "timestamp": "2024-01-01T08:00:00",
      "fingerprint_confidence": 0.95,
      "status": "success",
      "notes": "Entrada normal",
      "created_by": {
        "id": 1,
        "name": "Juan Pérez"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

### GET /access_logs/{id}
Obtiene un log de acceso específico por ID.

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "user": {
      "id": 1,
      "idDocumento": 12345678,
      "first_name": "Juan",
      "last_name": "Pérez",
      "user_type": "Empleado",
      "zona": {
        "id": 1,
        "sede_nombre": "Sede Principal",
        "departamento": "Bogotá",
        "ciudad": "Bogotá"
      },
      "estado": "Activo",
      "is_active": true
    },
    "action_type": "entry",
    "timestamp": "2024-01-01T08:00:00",
    "fingerprint_confidence": 0.95,
    "status": "success",
    "notes": "Entrada normal",
    "created_by": {
      "id": 1,
      "idDocumento": 12345678,
      "first_name": "Juan",
      "last_name": "Pérez",
      "user_type": "Empleado"
    }
  }
}
```

### POST /access_logs
Crea un nuevo log de acceso (para entradas/salidas).

**Cuerpo de la petición:**
```json
{
  "user_id": 1,
  "action_type": "entry",
  "timestamp": "2024-01-01T08:00:00",
  "fingerprint_confidence": 0.95,
  "status": "success",
  "notes": "Entrada normal",
  "created_by": 1
}
```

**Campos requeridos:**
- `user_id`: ID del usuario
- `action_type`: Tipo de acción (entry, exit, etc.)

**Campos opcionales:**
- `timestamp`: Fecha y hora del acceso (por defecto: ahora)
- `fingerprint_confidence`: Confianza de la huella dactilar
- `status`: Estado del acceso (por defecto: success)
- `notes`: Notas adicionales
- `created_by`: ID del usuario que creó el log

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Log de acceso creado exitosamente",
  "data": {
    "id": 1,
    "user": {
      "id": 1,
      "idDocumento": 12345678,
      "first_name": "Juan",
      "last_name": "Pérez",
      "user_type": "Empleado",
      "zona": "Sede Principal"
    },
    "action_type": "entry",
    "timestamp": "2024-01-01T08:00:00",
    "fingerprint_confidence": 0.95,
    "status": "success",
    "notes": "Entrada normal"
  }
}
```

## Códigos de Error

- **400**: Datos inválidos, campos requeridos faltantes o usuario inactivo
- **404**: Usuario no encontrado
- **500**: Error interno del servidor

## Validaciones

- El usuario debe existir y estar activo
- Los tipos de acción comunes son: "entry", "exit", "denied", "error"
- Los estados comunes son: "success", "failed", "denied", "error"
- La confianza de huella dactilar debe estar entre 0 y 1

## Ejemplos de Uso

### Registrar una entrada
```bash
curl -X POST http://localhost:5000/access_logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "action_type": "entry",
    "fingerprint_confidence": 0.95,
    "status": "success",
    "notes": "Entrada por huella dactilar"
  }'
```

### Registrar una salida
```bash
curl -X POST http://localhost:5000/access_logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "action_type": "exit",
    "status": "success",
    "notes": "Salida normal"
  }'
```

### Consultar logs de un usuario específico
```bash
curl "http://localhost:5000/access_logs?user_id=1"
```

### Consultar logs por fecha
```bash
curl "http://localhost:5000/access_logs?date_from=2024-01-01&date_to=2024-01-31"
```

### Consultar logs por tipo de acción
```bash
curl "http://localhost:5000/access_logs?action_type=entry"
```

## Tipos de Acción Comunes

- **entry**: Entrada al sistema
- **exit**: Salida del sistema
- **denied**: Acceso denegado
- **error**: Error en el acceso
- **timeout**: Tiempo de espera agotado
- **invalid_fingerprint**: Huella dactilar inválida

## Estados Comunes

- **success**: Acceso exitoso
- **failed**: Acceso fallido
- **denied**: Acceso denegado
- **error**: Error en el sistema
- **timeout**: Tiempo de espera agotado
