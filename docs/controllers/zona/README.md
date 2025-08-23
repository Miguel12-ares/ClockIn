# Controlador de Zonas

Este controlador maneja todas las operaciones relacionadas con las zonas del sistema ClockIn.

## Rutas Disponibles

### GET /zonas
Lista todas las zonas con información relacionada.

**Parámetros de consulta:**
- `page` (opcional): Número de página (por defecto: 1)
- `per_page` (opcional): Elementos por página (por defecto: 10)
- `ciudad` (opcional): Filtrar por ciudad
- `departamento` (opcional): Filtrar por departamento

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "sede_nombre": "Sede Principal",
      "departamento": "Bogotá",
      "ciudad": "Bogotá",
      "users_count": 25,
      "admins_count": 3
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

### GET /zonas/{id}
Obtiene una zona específica por ID con información detallada.

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "sede_nombre": "Sede Principal",
    "departamento": "Bogotá",
    "ciudad": "Bogotá",
    "users": [
      {
        "id": 1,
        "idDocumento": 12345678,
        "first_name": "Juan",
        "last_name": "Pérez",
        "user_type": "Empleado",
        "is_active": true
      }
    ],
    "admins": [
      {
        "admin_id": 2,
        "admin_name": "María García"
      }
    ],
    "users_count": 25,
    "admins_count": 3
  }
}
```

### POST /zonas
Crea una nueva zona.

**Cuerpo de la petición:**
```json
{
  "sede_nombre": "Sede Norte",
  "departamento": "Antioquia",
  "ciudad": "Medellín"
}
```

**Campos requeridos:**
- `sede_nombre`: Nombre de la sede
- `departamento`: Departamento donde se ubica
- `ciudad`: Ciudad donde se ubica

**Respuesta exitosa (201):**
```json
{
  "success": true,
  "message": "Zona creada exitosamente",
  "data": {
    "id": 2,
    "sede_nombre": "Sede Norte",
    "departamento": "Antioquia",
    "ciudad": "Medellín",
    "users_count": 0,
    "admins_count": 0
  }
}
```

### PUT /zonas/{id}
Actualiza una zona existente.

**Cuerpo de la petición:**
```json
{
  "sede_nombre": "Sede Norte Actualizada",
  "departamento": "Antioquia",
  "ciudad": "Medellín"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Zona actualizada exitosamente",
  "data": {
    "id": 2,
    "sede_nombre": "Sede Norte Actualizada",
    "departamento": "Antioquia",
    "ciudad": "Medellín",
    "users_count": 15,
    "admins_count": 2
  }
}
```

### DELETE /zonas/{id}
Elimina una zona (solo si no tiene usuarios o administradores asociados).

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Zona eliminada exitosamente",
  "data": {
    "id": 2,
    "sede_nombre": "Sede Norte",
    "departamento": "Antioquia",
    "ciudad": "Medellín"
  }
}
```

## Códigos de Error

- **400**: Datos inválidos, campos requeridos faltantes, zona duplicada o zona con usuarios/administradores asociados
- **404**: Zona no encontrada
- **500**: Error interno del servidor

## Validaciones

- El nombre de la sede debe ser único por ciudad
- Las zonas no pueden eliminarse si tienen usuarios asociados
- Las zonas no pueden eliminarse si tienen administradores asociados
- Todos los campos son obligatorios al crear una zona

## Ejemplos de Uso

### Crear una nueva zona
```bash
curl -X POST http://localhost:5000/zonas \
  -H "Content-Type: application/json" \
  -d '{
    "sede_nombre": "Sede Sur",
    "departamento": "Valle del Cauca",
    "ciudad": "Cali"
  }'
```

### Obtener todas las zonas de una ciudad
```bash
curl "http://localhost:5000/zonas?ciudad=Bogotá"
```

### Actualizar una zona
```bash
curl -X PUT http://localhost:5000/zonas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "sede_nombre": "Sede Principal Renovada"
  }'
```
