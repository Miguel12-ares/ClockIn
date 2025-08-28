# ClockIn - Sistema de Control de Acceso

Sistema de gestión de usuarios y control de acceso para empresas, desarrollado con Flask, SQLAlchemy y MySQL.

## Características Principales

- **Autenticación JWT**: Sistema robusto de autenticación con access y refresh tokens
- **Autorización por Roles**: Control de acceso basado en roles (RBAC)
- **Gestión de Usuarios**: CRUD completo con estados y tipos de usuario
- **Gestión de Zonas**: Administración de sedes y departamentos
- **Auditoría**: Registro completo de acciones del sistema
- **API RESTful**: Endpoints JSON para integración con frontend

## Arquitectura

### Tecnologías Utilizadas

- **Backend**: Flask 3.0.3
- **Base de Datos**: MySQL 8.0
- **ORM**: SQLAlchemy 3.1.1
- **Autenticación**: Flask-JWT-Extended 4.6.0
- **Migraciones**: Flask-Migrate 4.0.4
- **Contenedores**: Docker & Docker Compose

### Estructura del Proyecto

```
ClockIn/
├── app/
│   ├── controllers/          # Controladores de la aplicación
│   │   ├── auth.py          # Autenticación JWT
│   │   ├── admin.py         # Panel administrativo
│   │   ├── user/            # Gestión de usuarios
│   │   ├── zona/            # Gestión de zonas
│   │   └── ...
│   ├── models/              # Modelos de datos
│   ├── middleware/          # Middleware de autorización
│   ├── templates/           # Plantillas HTML
│   └── static/              # Archivos estáticos
├── db/                      # Scripts de base de datos
├── tests/                   # Pruebas de integración
├── docs/                    # Documentación técnica
└── Docker/                  # Configuración Docker
```

## Modelos de Datos

### Usuario (User)
- `idDocumento`: Identificación única del usuario
- `first_name`, `last_name`: Nombre completo
- `user_type_id`: Relación con tipo de usuario
- `zona_id`: Zona asignada
- `estado_id`: Estado del usuario (activo/inactivo)
- `is_active`: Flag de activación

### Tipo de Usuario (UserType)
- `type_name`: Nombre del rol (Admin, Supervisor, Empleado)
- `description`: Descripción del rol

### Zona
- `sede_nombre`: Nombre de la sede
- `departamento`: Departamento
- `ciudad`: Ciudad

### Estado
- `name`: Nombre del estado (activo, inactivo, pendiente, eliminado)

## Rutas y Endpoints

### Autenticación (`/auth`)

| Método | Endpoint | Descripción | Autenticación |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Iniciar sesión | No |
| POST | `/auth/refresh` | Renovar access token | Refresh token |
| POST | `/auth/logout` | Cerrar sesión | Access token |
| GET | `/auth/verify` | Verificar token | Access token |
| GET | `/auth/me` | Información del usuario actual | Access token |

### Gestión de Usuarios (`/users`)

| Método | Endpoint | Descripción | Roles Requeridos |
|--------|----------|-------------|------------------|
| GET | `/users/` | Listar usuarios | Admin, SAdmin |
| POST | `/users/` | Crear usuario | Admin, SAdmin |
| GET | `/users/<id>` | Ver usuario | Admin, SAdmin |
| PUT | `/users/<id>` | Actualizar usuario | Admin, SAdmin |
| DELETE | `/users/<id>` | Eliminar usuario | Admin, SAdmin |

### Gestión de Zonas (`/zonas`)

| Método | Endpoint | Descripción | Roles Requeridos |
|--------|----------|-------------|------------------|
| GET | `/zonas/` | Listar zonas | Admin, SAdmin |
| POST | `/zonas/` | Crear zona | Admin, SAdmin |
| GET | `/zonas/<id>` | Ver zona | Admin, SAdmin |
| PUT | `/zonas/<id>` | Actualizar zona | Admin, SAdmin |
| DELETE | `/zonas/<id>` | Eliminar zona | Admin, SAdmin |

### Panel Administrativo (`/admin`)

| Método | Endpoint | Descripción | Roles Requeridos |
|--------|----------|-------------|------------------|
| GET | `/admin/dashboard` | Dashboard principal | Admin, SAdmin |
| GET | `/admin/users` | Gestión de usuarios | Admin, SAdmin |

## Autenticación y Autorización

### Sistema JWT

El sistema utiliza Flask-JWT-Extended para manejar la autenticación:

- **Access Token**: Válido por 1 hora, usado para acceder a recursos
- **Refresh Token**: Válido por 30 días, usado para renovar access tokens
- **Fresh Token**: Token recién emitido, requerido para acciones sensibles

### Decoradores de Autorización

```python
from app.middleware.auth_middleware import roles_required, admin_required

@roles_required('Admin', 'SAdmin')
def admin_only_function():
    pass

@admin_required
def admin_function():
    pass
```

### Verificaciones de Seguridad

1. **Usuario Activo**: Verifica `is_active = True`
2. **Estado Correcto**: Verifica `estado.name = 'activo'`
3. **Rol Autorizado**: Verifica `user_type.type_name` en lista de roles permitidos
4. **Token Válido**: Verifica firma y expiración del JWT

## Configuración

### Variables de Entorno

```bash
# Base de datos
DATABASE_URL=mysql+pymysql://user:password@host:port/database

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
SECRET_KEY=your_flask_secret_key_here

# Aplicación
ADMIN_MODE=true
INIT_DB_ON_START=true
```

### Configuración JWT

```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
JWT_TOKEN_LOCATION = ['headers']
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
```

## Despliegue Local

### Prerrequisitos

- Python 3.8+
- MySQL 8.0+
- Docker (opcional)

### Instalación con Docker

1. **Clonar repositorio**
   ```bash
   git clone <repository-url>
   cd ClockIn
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Ejecutar con Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Inicializar base de datos**
   ```bash
   docker-compose exec app python init_db.py
   ```

### Instalación Manual

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**
   ```bash
   # Crear base de datos MySQL
   mysql -u root -p
   CREATE DATABASE clockin;
   CREATE USER 'clockin_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON clockin.* TO 'clockin_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Ejecutar migraciones**
   ```bash
   flask db upgrade
   python init_db.py
   ```

5. **Ejecutar aplicación**
   ```bash
   python run.py
   ```

## Pruebas

### Ejecutar Pruebas de Integración

```bash
# Instalar pytest
pip install pytest

# Ejecutar pruebas
pytest tests/test_auth_integration.py -v
```

### Casos de Prueba Cubiertos

- ✅ Login exitoso con diferentes roles
- ✅ Login con usuario inexistente
- ✅ Login con usuario inactivo
- ✅ Renovación de tokens
- ✅ Acceso a rutas protegidas
- ✅ Denegación de acceso por rol
- ✅ Verificación de tokens
- ✅ Logout exitoso

## Checklist de QA

### Funcionalidad de Autenticación
- [ ] Login exitoso con ID de documento
- [ ] Validación de usuario activo
- [ ] Validación de estado correcto
- [ ] Emisión de access y refresh tokens
- [ ] Renovación de tokens
- [ ] Logout y limpieza de sesiones

### Autorización y Seguridad
- [ ] Protección de rutas administrativas
- [ ] Verificación de roles por endpoint
- [ ] Denegación de acceso para roles no autorizados
- [ ] Validación de tokens en cada request
- [ ] Manejo de tokens expirados

### Gestión de Datos
- [ ] CRUD completo de usuarios
- [ ] CRUD completo de zonas
- [ ] Paginación en listados
- [ ] Filtros y búsqueda
- [ ] Optimización de consultas (evitar N+1)

### API y Respuestas
- [ ] Respuestas JSON consistentes
- [ ] Códigos de estado HTTP apropiados
- [ ] Manejo de errores estructurado
- [ ] Documentación de endpoints

### Rendimiento
- [ ] Consultas optimizadas con joinedload/selectinload
- [ ] Paginación implementada
- [ ] Índices de base de datos apropiados
- [ ] Tiempo de respuesta aceptable

## Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o preguntas sobre el proyecto, contactar al equipo de desarrollo.
