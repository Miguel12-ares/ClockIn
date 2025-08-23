# Controlador de Administradores de Zona

Este controlador maneja las asignaciones de administradores a zonas en el sistema ClockIn.

## Rutas Disponibles

### GET /admin_zona
Lista todas las asignaciones de administradores a zonas.

**Parámetros de consulta:**
- `page` (opcional): Número de página (por defecto: 1)
- `per_page` (opcional): Elementos por página (por defecto: 10)
- `admin_id` (opcional): Filtrar por ID del administrador
- `zona_id` (opcional): Filtrar por ID de la zona

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": [
    {
      "admin_id": 2,
      "admin_name": "María García",
      "admin_document": 87654321,
      "admin_user_type": "Supervisor",
      "zona_id": 1,
      "zona_name": "Sede Principal",
      "zona_location": "Bogotá, Bogotá"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 5,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

### POST /admin_zona
Asigna un administrador a una zona.

**Cuerpo de la petición:**
```json
{
  "admin_id": 2,
  "zona_id": 1
}
```

**Campos requeridos:**
- `admin_id`: ID del usuario que será administrador
- `zona_id`: ID de la zona a administrar

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Administrador asignado exitosamente",
  "data": {
    "admin_id": 2,
    "admin_name": "María García",
    "admin_document": 87654321,
    "zona_id": 1,
    "zona_name": "Sede Principal",
    "zona_location": "Bogotá, Bogotá"
  }
}
```

### DELETE /admin_zona/{admin_id}/{zona_id}
Remueve un administrador de una zona.

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Administrador removido exitosamente",
  "data": {
    "admin_id": 2,
    "admin_name": "María García",
    "admin_document": 87654321,
    "zona_id": 1,
    "zona_name": "Sede Principal",
    "zona_location": "Bogotá, Bogotá"
  }
}
```

## Códigos de Error

- **400**: Datos inválidos, campos requeridos faltantes, asignación duplicada o usuario inactivo
- **404**: Usuario, zona o asignación no encontrada
- **500**: Error interno del servidor

## Validaciones

- El usuario debe existir y estar activo
- La zona debe existir
- No puede haber asignaciones duplicadas (mismo admin en la misma zona)
- Solo se pueden remover asignaciones existentes

## Ejemplos de Uso

### Asignar un administrador a una zona
```bash
curl -X POST http://localhost:5000/admin_zona \
  -H "Content-Type: application/json" \
  -d '{
    "admin_id": 2,
    "zona_id": 1
  }'
```

### Listar todas las asignaciones de un administrador
```bash
curl "http://localhost:5000/admin_zona?admin_id=2"
```

### Remover un administrador de una zona
```bash
curl -X DELETE http://localhost:5000/admin_zona/2/1
```

### Listar todas las asignaciones de una zona
```bash
curl "http://localhost:5000/admin_zona?zona_id=1"
```

## Notas Importantes

- Un usuario puede ser administrador de múltiples zonas
- Una zona puede tener múltiples administradores
- Al eliminar un usuario, se eliminan automáticamente todas sus asignaciones como administrador
- Al eliminar una zona, se eliminan automáticamente todas las asignaciones de administradores a esa zona
