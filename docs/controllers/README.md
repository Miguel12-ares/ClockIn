# Documentación de Controladores - ClockIn

Esta documentación describe la estructura completa de controladores del sistema ClockIn, implementada siguiendo el patrón MVC con Flask Blueprints.

## Estructura de Controladores

```
app/controllers/
├── user/                    # Gestión de usuarios
│   ├── __init__.py
│   ├── index.py            # GET /users - Lista todos
│   ├── show.py             # GET /users/{id} - Obtiene uno
│   ├── create.py           # POST /users - Crea nuevo
│   ├── update.py           # PUT /users/{id} - Actualiza
│   └── delete.py           # DELETE /users/{id} - Elimina
├── zona/                   # Gestión de zonas
│   ├── __init__.py
│   ├── index.py            # GET /zonas - Lista todas
│   ├── show.py             # GET /zonas/{id} - Obtiene una
│   ├── create.py           # POST /zonas - Crea nueva
│   ├── update.py           # PUT /zonas/{id} - Actualiza
│   └── delete.py           # DELETE /zonas/{id} - Elimina
├── user_type/              # Gestión de tipos de usuario
│   ├── __init__.py
│   ├── index.py            # GET /user_types - Lista todos
│   ├── show.py             # GET /user_types/{id} - Obtiene uno
│   ├── create.py           # POST /user_types - Crea nuevo
│   ├── update.py           # PUT /user_types/{id} - Actualiza
│   └── delete.py           # DELETE /user_types/{id} - Elimina
├── estado/                 # Gestión de estados
│   ├── __init__.py
│   ├── index.py            # GET /estados - Lista todos
│   ├── show.py             # GET /estados/{id} - Obtiene uno
│   ├── create.py           # POST /estados - Crea nuevo
│   ├── update.py           # PUT /estados/{id} - Actualiza
│   └── delete.py           # DELETE /estados/{id} - Elimina
├── admin_zona/             # Gestión de administradores por zona
│   ├── __init__.py
│   ├── assign.py           # POST /admin_zona - Asigna admin
│   ├── remove.py           # DELETE /admin_zona/{admin_id}/{zona_id} - Remueve
│   └── list.py             # GET /admin_zona - Lista asignaciones
├── access_log/             # Gestión de logs de acceso
│   ├── __init__.py
│   ├── index.py            # GET /access_logs - Lista logs
│   ├── show.py             # GET /access_logs/{id} - Obtiene log
│   └── create.py           # POST /access_logs - Registra log
├── active_session/         # Gestión de sesiones activas
│   ├── __init__.py
│   ├── index.py            # GET /active_sessions - Lista sesiones
│   ├── show.py             # GET /active_sessions/{id} - Obtiene sesión
│   ├── create.py           # POST /active_sessions - Inicia sesión
│   ├── update.py           # PUT /active_sessions/{id} - Actualiza sesión
│   └── delete.py           # DELETE /active_sessions/{id} - Cierra sesión
├── anomaly/                # Gestión de anomalías
│   ├── __init__.py
│   ├── index.py            # GET /anomalies - Lista anomalías
│   ├── show.py             # GET /anomalies/{id} - Obtiene anomalía
│   ├── create.py           # POST /anomalies - Registra anomalía
│   └── resolve.py          # PUT /anomalies/{id}/resolve - Resuelve anomalía
└── system_audit/           # Gestión de auditorías del sistema
    ├── __init__.py
    ├── index.py            # GET /system_audits - Lista auditorías
    └── show.py             # GET /system_audits/{id} - Obtiene auditoría
```

## Características Principales

### 1. Arquitectura MVC con Blueprints
- Cada entidad tiene su propio blueprint de Flask
- Separación clara de responsabilidades
- Código modular y escalable

### 2. Rutas RESTful
- **GET**: Obtener recursos (listar todos o uno específico)
- **POST**: Crear nuevos recursos
- **PUT**: Actualizar recursos existentes
- **DELETE**: Eliminar recursos

### 3. Validaciones Robustas
- Validación de campos requeridos
- Verificación de existencia de registros relacionados
- Prevención de duplicados
- Validación de integridad referencial

### 4. Manejo de Errores
- Códigos de estado HTTP apropiados
- Mensajes de error descriptivos
- Rollback automático en caso de errores
- Respuestas JSON consistentes

### 5. Paginación
- Soporte para paginación en todas las listas
- Parámetros configurables (page, per_page)
- Información de paginación en respuestas

### 6. Filtros y Búsquedas
- Filtros por campos específicos
- Búsquedas por fecha
- Filtros por estado y tipo

## Registro de Blueprints

Todos los blueprints se registran automáticamente en `app/__init__.py`:

```python
# Registrar blueprints
from app.controllers.user import user_bp
from app.controllers.zona import zona_bp
from app.controllers.user_type import user_type_bp
from app.controllers.estado import estado_bp
from app.controllers.admin_zona import admin_zona_bp
from app.controllers.access_log import access_log_bp
from app.controllers.active_session import active_session_bp
from app.controllers.anomaly import anomaly_bp
from app.controllers.system_audit import system_audit_bp

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(zona_bp, url_prefix='/zonas')
app.register_blueprint(user_type_bp, url_prefix='/user_types')
app.register_blueprint(estado_bp, url_prefix='/estados')
app.register_blueprint(admin_zona_bp, url_prefix='/admin_zona')
app.register_blueprint(access_log_bp, url_prefix='/access_logs')
app.register_blueprint(active_session_bp, url_prefix='/active_sessions')
app.register_blueprint(anomaly_bp, url_prefix='/anomalies')
app.register_blueprint(system_audit_bp, url_prefix='/system_audits')
```

## Estructura de Respuestas

Todas las respuestas siguen un formato consistente:

### Respuesta Exitosa
```json
{
  "success": true,
  "message": "Operación realizada exitosamente",
  "data": { ... }
}
```

### Respuesta con Paginación
```json
{
  "success": true,
  "data": [ ... ],
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

### Respuesta de Error
```json
{
  "success": false,
  "error": "Tipo de error",
  "message": "Descripción detallada del error"
}
```

## Códigos de Estado HTTP

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **400**: Datos inválidos o campos requeridos faltantes
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

## Validaciones de Negocio

### Usuarios
- Documento único
- No eliminar si tiene sesiones activas
- No eliminar si es administrador de zonas

### Zonas
- Nombre único por ciudad
- No eliminar si tiene usuarios asociados
- No eliminar si tiene administradores asociados

### Tipos de Usuario
- Nombre único
- No eliminar si tiene usuarios asociados

### Estados
- Nombre único
- No eliminar si tiene usuarios asociados

### Administradores de Zona
- No asignaciones duplicadas
- Usuario debe estar activo

### Logs de Acceso
- Usuario debe estar activo
- Validación de confianza de huella dactilar

### Sesiones Activas
- Un usuario no puede tener múltiples sesiones activas
- Usuario debe estar activo

### Anomalías
- Solo se pueden resolver anomalías no resueltas
- Usuario que resuelve debe existir

## Documentación Detallada

Cada controlador tiene su propia documentación en la carpeta `docs/controllers/`:

- [Documentación de Usuarios](user/README.md)
- [Documentación de Zonas](zona/README.md)
- [Documentación de Tipos de Usuario](user_type/README.md)
- [Documentación de Estados](estado/README.md)
- [Documentación de Administradores de Zona](admin_zona/README.md)
- [Documentación de Logs de Acceso](access_log/README.md)
- [Documentación de Sesiones Activas](active_session/README.md)
- [Documentación de Anomalías](anomaly/README.md)
- [Documentación de Auditorías del Sistema](system_audit/README.md)

## Ejemplos de Uso

### Crear un nuevo usuario
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "idDocumento": 12345678,
    "first_name": "Juan",
    "last_name": "Pérez",
    "user_type_id": 1,
    "zona_id": 1
  }'
```

### Listar usuarios con filtros
```bash
curl "http://localhost:5000/users?user_type_id=1&is_active=true&page=1&per_page=20"
```

### Asignar administrador a zona
```bash
curl -X POST http://localhost:5000/admin_zona \
  -H "Content-Type: application/json" \
  -d '{
    "admin_id": 2,
    "zona_id": 1
  }'
```

### Registrar entrada de usuario
```bash
curl -X POST http://localhost:5000/access_logs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "action_type": "entry",
    "fingerprint_confidence": 0.95
  }'
```

## Consideraciones de Seguridad

- Validación de entrada en todos los endpoints
- Sanitización de datos
- Verificación de permisos (pendiente de implementar)
- Logging de auditoría para operaciones críticas
- Manejo seguro de transacciones de base de datos

## Próximos Pasos

1. Implementar autenticación y autorización
2. Agregar validación de permisos por rol
3. Implementar rate limiting
4. Agregar logging detallado
5. Implementar cache para consultas frecuentes
6. Agregar tests unitarios y de integración
