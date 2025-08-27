# Documentación ClockIn

## Sistema de Control de Acceso

ClockIn es un sistema de gestión de usuarios y control de acceso para empresas, desarrollado con Flask, SQLAlchemy y MySQL.

## Estado Actual del Sistema

### ✅ Funcionalidades Operativas
- **Dashboard Administrativo**: Funciona correctamente con estadísticas
- **Gestión de Usuarios**: CRUD completo operativo
- **Base de Datos**: Conexión estable y datos inicializados
- **Frontend**: CSS y iconos corregidos
- **Docker**: Contenedores funcionando correctamente

### 🔧 Errores Corregidos Recientemente

#### 1. Error de Base de Datos
- **Problema**: Inconsistencia en nombres de columnas (`sede_nombre` vs `nombre`, `name` vs `nombre`)
- **Solución**: Corregidos los modelos `Zona` y `Estado` para usar nombres consistentes
- **Archivos afectados**: `app/models/zona.py`, `app/models/estado.py`, `app/init_data.py`

#### 2. Error de CSS y Frontend
- **Problema**: Iconos gigantes y CSS no cargando correctamente
- **Solución**: Cambio a CDN de Tailwind CSS y corrección de tamaños de iconos
- **Archivos afectados**: `app/templates/admin/base.html`

#### 3. Error de Bucles de Redirección
- **Problema**: Decorador `@admin_required` causaba bucles infinitos
- **Solución**: Corrección de redirecciones y manejo de errores
- **Archivos afectados**: `app/__init__.py`, `app/controllers/admin.py`

#### 4. Error de Dependencias
- **Problema**: Faltaba paquete `cryptography` para MySQL
- **Solución**: Agregado al `requirements.txt`

## Documentación Detallada

### [Errores y Soluciones](./errores_y_soluciones.md)
Documento completo que explica todos los errores encontrados, sus causas y las soluciones implementadas.

### [Plan de Completación](./plan_completacion_sistema.md)
Plan detallado para completar los módulos de autenticación (CLOCK-16) y mejorar la gestión de usuarios (CLOCK-17).

## Acceso al Sistema

### URLs Principales
- **Dashboard**: http://localhost:5000/admin/dashboard
- **Gestión de Usuarios**: http://localhost:5000/admin/users
- **phpMyAdmin**: http://localhost:8080

### Credenciales de Base de Datos
- **Host**: localhost:3307
- **Usuario**: root
- **Contraseña**: rootpass
- **Base de datos**: db_name

## Comandos Útiles

### Reiniciar Sistema
```bash
docker-compose -f Docker/docker-compose.yml down
docker-compose -f Docker/docker-compose.yml up --build
```

### Ver Logs
```bash
docker-compose -f Docker/docker-compose.yml logs app
```

### Acceder a Base de Datos
```bash
docker exec -it docker-db-1 mysql -u root -prootpass
```

## Próximos Pasos

1. **Implementar Autenticación** (CLOCK-16)
   - Sistema de login/logout
   - Registro de usuarios
   - Protección de rutas

2. **Mejorar Gestión de Usuarios** (CLOCK-17)
   - Filtros avanzados
   - Exportación de datos
   - Interfaz mejorada

3. **Sistema de Auditoría**
   - Dashboard de auditoría
   - Reportes y alertas
   - Logs del sistema

## Estructura del Proyecto

```
ClockIn/
├── app/
│   ├── controllers/          # Controladores de la aplicación
│   ├── models/              # Modelos de base de datos
│   ├── templates/           # Plantillas HTML
│   └── static/              # Archivos estáticos
├── Docker/                  # Configuración de Docker
├── docs/                    # Documentación
└── requirements.txt         # Dependencias de Python
```

## Tecnologías Utilizadas

- **Backend**: Flask, SQLAlchemy, MySQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Contenedores**: Docker, Docker Compose
- **Base de Datos**: MySQL 8.0
- **Herramientas**: phpMyAdmin

## Contribución

Para contribuir al proyecto:

1. Revisar la documentación de errores y soluciones
2. Seguir el plan de completación del sistema
3. Implementar funcionalidades siguiendo las mejores prácticas
4. Probar cambios antes de hacer commit

## Soporte

Para reportar errores o solicitar funcionalidades, revisar la documentación en la carpeta `docs/`.
