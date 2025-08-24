# Módulo de Administración - ClockIn

## Descripción
Este módulo proporciona funcionalidades completas de gestión de usuarios y roles para el sistema ClockIn, incluyendo CRUD de usuarios, control de acceso basado en roles (RBAC) y auditoría de cambios.

## Características Principales

### 🔐 Control de Acceso (RBAC)
- **Decorador `@admin_required`**: Simula control de acceso administrativo
- **Modo de desarrollo**: Acceso directo sin autenticación (configurable via `ADMIN_MODE`)
- **Preparado para producción**: Fácil integración con sistema de autenticación real

### 👥 Gestión de Usuarios
- **CRUD completo**: Crear, leer, actualizar, eliminar usuarios
- **Validaciones robustas**: Documento único, campos requeridos, tipos válidos
- **Estados de usuario**: Activar/desactivar usuarios
- **Búsqueda y filtros**: Búsqueda por nombre, apellido o documento
- **Paginación**: Manejo eficiente de grandes volúmenes de datos

### 📊 Dashboard Administrativo
- **Estadísticas en tiempo real**: Total de usuarios, activos, inactivos
- **Gráficos de distribución**: Usuarios por tipo y zona
- **Acciones rápidas**: Enlaces directos a funciones principales

### 🔍 Auditoría del Sistema
- **Registro automático**: Todas las operaciones CRUD se registran
- **Información detallada**: Valores anteriores y nuevos, IP, timestamp
- **Tabla `system_audit`**: Almacenamiento estructurado de auditoría

## Estructura de Archivos

```
app/controllers/admin.py          # Controlador principal
app/templates/admin/
├── base.html                     # Plantilla base administrativa
├── dashboard.html                # Dashboard principal
├── users.html                    # Lista de usuarios
└── user_form.html               # Formulario CRUD de usuarios
app/init_data.py                  # Inicialización de datos básicos
```

## Rutas Disponibles

### Dashboard
- `GET /admin/dashboard` - Dashboard administrativo con estadísticas

### Gestión de Usuarios
- `GET /admin/users` - Lista de usuarios con paginación y búsqueda
- `GET /admin/users/create` - Formulario para crear usuario
- `POST /admin/users/create` - Crear nuevo usuario
- `GET /admin/users/<id>/edit` - Formulario para editar usuario
- `POST /admin/users/<id>/edit` - Actualizar usuario
- `POST /admin/users/<id>/delete` - Eliminar usuario
- `POST /admin/users/<id>/toggle-status` - Activar/desactivar usuario

## Modelos Utilizados

### User
```python
- id: Integer (PK)
- idDocumento: Integer (unique)
- first_name: String(50)
- last_name: String(50)
- user_type_id: Integer (FK)
- zona_id: Integer (FK)
- estado_id: Integer (FK)
- is_active: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### UserType
```python
- id: Integer (PK)
- type_name: String(50) (unique)
- description: Text
```

### Zona
```python
- id: Integer (PK)
- nombre: String(100)
- departamento: String(50)
- ciudad: String(50)
```

### Estado
```python
- id: Integer (PK)
- nombre: String(50) (unique)
- description: Text
```

### SystemAudit
```python
- id: Integer (PK)
- user_id: Integer (FK, nullable)
- table_affected: String(100)
- action_type: String(100)
- old_values: Text (JSON)
- new_values: Text (JSON)
- timestamp: DateTime
- ip_address: String(45)
```

## Configuración

### Variables de Entorno
```bash
ADMIN_MODE=true  # Habilita acceso administrativo sin autenticación
```

### Base de Datos
El sistema requiere las siguientes tablas:
- `users`
- `user_types`
- `zonas`
- `estados`
- `system_audit`

## Uso

### 1. Inicialización
```bash
# Ejecutar el script de inicialización
python app/init_data.py
```

### 2. Acceso al Panel
```
http://localhost:5000/admin/dashboard
http://localhost:5000/admin/users
```

### 3. Crear Usuario
1. Navegar a `/admin/users`
2. Hacer clic en "Nuevo Usuario"
3. Completar formulario con datos requeridos
4. Guardar usuario

### 4. Gestionar Usuarios
- **Editar**: Hacer clic en icono de edición
- **Activar/Desactivar**: Hacer clic en icono de estado
- **Eliminar**: Hacer clic en icono de eliminación

## Validaciones

### Campos Requeridos
- Número de documento (único)
- Nombre
- Apellido
- Tipo de usuario
- Zona

### Validaciones Específicas
- `idDocumento`: Debe ser número entero positivo y único
- `user_type_id`: Debe existir en tabla `user_types`
- `zona_id`: Debe existir en tabla `zonas`
- `estado_id`: Debe existir en tabla `estados`

## Auditoría

### Operaciones Registradas
- **CREATE**: Creación de usuarios
- **UPDATE**: Modificación de usuarios
- **DELETE**: Eliminación de usuarios
- **TOGGLE_STATUS**: Cambio de estado activo/inactivo

### Información Capturada
- Usuario que realiza la acción (en desarrollo: null)
- Tabla afectada
- Tipo de acción
- Valores anteriores (JSON)
- Valores nuevos (JSON)
- Timestamp
- Dirección IP

## Seguridad

### En Desarrollo
- Acceso directo sin autenticación
- Modo administrador habilitado por defecto
- Validaciones de formulario en frontend y backend

### En Producción
- Integrar con sistema de autenticación real
- Implementar sesiones seguras
- Configurar `ADMIN_MODE=false`
- Validar permisos de usuario autenticado

## Errores y Manejo de Excepciones

### Errores Comunes
- **IntegrityError**: Documento duplicado, referencias inválidas
- **ValidationError**: Campos requeridos faltantes
- **DatabaseError**: Problemas de conexión a BD

### Manejo de Errores
- Rollback automático en transacciones
- Mensajes de error descriptivos
- Logging de errores para debugging
- Redirecciones apropiadas

## Próximas Mejoras

### Funcionalidades Planificadas
- [ ] Filtros avanzados por tipo de usuario y zona
- [ ] Exportación de datos a CSV/Excel
- [ ] Importación masiva de usuarios
- [ ] Historial de cambios detallado
- [ ] Notificaciones por email
- [ ] Backup automático de datos

### Mejoras de Seguridad
- [ ] Autenticación real con JWT
- [ ] Encriptación de datos sensibles
- [ ] Rate limiting en endpoints
- [ ] Logs de seguridad
- [ ] Auditoría de accesos

## Contribución

Para contribuir al módulo de administración:

1. Seguir las convenciones de código existentes
2. Agregar tests para nuevas funcionalidades
3. Actualizar documentación
4. Validar compatibilidad con Docker
5. Probar en entorno de desarrollo

## Soporte

Para reportar problemas o solicitar funcionalidades:
- Crear issue en el repositorio
- Incluir logs de error
- Describir pasos para reproducir
- Especificar versión del sistema
