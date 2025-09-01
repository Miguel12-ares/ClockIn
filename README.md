# ClockIn - Sistema de Control de Asistencia

![ClockIn Logo](https://img.shields.io/badge/ClockIn-Sistema%20de%20Asistencia-blue?style=for-the-badge)

Un sistema completo de control de asistencia diseñado para gestionar el registro de entrada y salida de empleados, administración de usuarios y auditoría de actividades en tiempo real.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Prerrequisitos](#-prerrequisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [API Endpoints](#-api-endpoints)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

### 🔐 Sistema de Autenticación
- Login seguro con validación de credenciales
- Gestión de sesiones
- Roles diferenciados (Administrador/Empleado)

### 👥 Gestión de Usuarios
- **CRUD completo** de usuarios
- Asignación y modificación de roles
- Validación de permisos por rol
- Búsqueda y paginación de usuarios
- Estados de usuario (Activo/Inactivo/Suspendido)

### ⏰ Control de Asistencia
- Registro de entrada y salida por ID de documento
- Auto-detección de tipo de evento (entrada vs salida)
- Captura automática de timestamp
- Validación de usuario existente y activo
- Control de sesiones activas

### 📊 Panel Administrativo
- Dashboard con métricas en tiempo real
- Vista de sesiones activas (usuarios sin salida registrada)
- Historial completo de asistencia con filtros
- Registro manual de entrada/salida por administradores
- Auditoría completa del sistema

### 🔍 Sistema de Auditoría
- Logging automático de todos los cambios
- Trazabilidad completa de acciones administrativas
- Registro de IP y timestamps
- Historial de modificaciones de usuarios

## 🚀 Tecnologías

**Backend:**
- ![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
- ![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask)
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?logo=sqlalchemy)
- ![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)

**Frontend:**
- ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1-purple?logo=bootstrap)
- ![Jinja2](https://img.shields.io/badge/Jinja2-Templates-orange)
- ![FontAwesome](https://img.shields.io/badge/FontAwesome-Icons-blue?logo=fontawesome)

**Infraestructura:**
- ![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)
- ![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-green)
- ![phpMyAdmin](https://img.shields.io/badge/phpMyAdmin-DB%20Admin-orange)

## 📋 Prerrequisitos

- **Docker** y **Docker Compose** instalados
- **Git** para clonar el repositorio
- **Navegador web** moderno (Chrome, Firefox, Safari, Edge)

## 🛠 Instalación

### 1. Clonar el Repositorio

```  
git clone https://github.com/Miguel12-ares/ClockIn.git
cd ClockIn
git checkout test2 
 ```

### 2. Navegar al Directorio Docker
``` 
cd Docker
 ```

### 3. Construir y Ejecutar con Docker Compose
Limpiar contenedores existentes (opcional)
```
docker-compose down -v
```
 Construir y levantar servicios

```
docker-compose up --build
```

### 4. Verificar Instalación
Verificar que las tablas se crearon correctamente
```
docker-compose exec app python debug_db.py
```

## ⚙️ Configuración

### URLs del Sistema
- **Aplicación Principal:** http://localhost:5000
- **phpMyAdmin:** http://localhost:8080
- **Base de Datos:** localhost:3307

### Credenciales por Defecto
**Usuario Admin:**

ID Documento: 12345678

Contraseña: admin123

**Base de Datos (phpMyAdmin):**

Usuario: root

Contraseña: rootpass

### Variables de Entorno
Las principales configuraciones están en `docker-compose.yml`:
```
MYSQL_DATABASE: db_name
MYSQL_USER: user
MYSQL_PASSWORD: user_password
FLASK_DEBUG: 1
```

## 📱 Uso del Sistema

### Para Administradores

#### 1. Acceso al Sistema
1. Ir a http://localhost:5000
2. Iniciar sesión con las credenciales de admin
3. Acceder al dashboard administrativo

#### 2. Gestión de Usuarios
- **Crear usuarios:** `/admin/usuarios/nuevo`
- **Editar usuarios:** Botón "Editar" en la lista de usuarios
- **Eliminar usuarios:** Botón "Eliminar" (con confirmación)
- **Buscar usuarios:** Usar el filtro de búsqueda

#### 3. Control de Asistencia
- **Ver sesiones activas:** `/admin/sesiones-activas`
- **Historial completo:** `/admin/historial-asistencia`
- **Registro manual:** Botones en el dashboard

#### 4. Auditoría
- **Ver logs:** `/admin/auditoria`
- Filtrar por fechas, usuarios y tipos de acción

### Para Desarrolladores

#### API Endpoints para Registro de Asistencia

**Registrar Entrada:**
---
curl -X POST http://localhost:5000/attendance/checkin
-H "Content-Type: application/json"
-d '{"idDocumento": "12345678"}'
---

**Registrar Salida:**
---
curl -X POST http://localhost:5000/attendance/checkout
-H "Content-Type: application/json"
-d '{"idDocumento": "12345678"}'
---

## 🔌 API Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/logout` | Cerrar sesión |

### Administración de Usuarios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/usuarios` | Listar usuarios |
| GET | `/admin/usuarios/nuevo` | Formulario nuevo usuario |
| POST | `/admin/usuarios/nuevo` | Crear usuario |
| GET | `/admin/usuarios/<id>/editar` | Formulario editar |
| POST | `/admin/usuarios/<id>/editar` | Actualizar usuario |
| POST | `/admin/usuarios/<id>/eliminar` | Eliminar usuario |

### Control de Asistencia
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/attendance/checkin` | Registrar entrada |
| POST | `/attendance/checkout` | Registrar salida |
| GET | `/admin/sesiones-activas` | Ver sesiones activas |
| GET | `/admin/historial-asistencia` | Historial completo |

### Auditoría
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/admin/auditoria` | Ver logs de auditoría |

## 📁 Estructura del Proyecto
ClockIn/
├── app/
│ ├── controllers/ # Controladores Flask
│ │ ├── admin.py # Gestión administrativa
│ │ ├── attendance.py # Control de asistencia
│ │ ├── auth.py # Autenticación
│ │ └── main.py # Rutas principales
│ ├── models/ # Modelos de base de datos
│ │ ├── access_log.py # Logs de acceso
│ │ ├── active_session.py # Sesiones activas
│ │ ├── admin_zona.py # Administradores por zona
│ │ ├── anomaly.py # Detección de anomalías
│ │ ├── estado.py # Estados de usuario
│ │ ├── system_audit.py # Auditoría del sistema
│ │ ├── user.py # Usuarios
│ │ ├── user_type.py # Tipos de usuario
│ │ └── zona.py # Zonas/Sedes
│ ├── templates/ # Plantillas HTML
│ │ ├── admin/ # Vistas administrativas
│ │ └── auth/ # Vistas de autenticación
│ ├── utils/ # Utilidades
│ │ ├── decorators.py # Decoradores personalizados
│ │ └── init_data.py # Datos iniciales
│ └── init.py # Inicialización de la app
├── Docker/
│ └── docker-compose.yml # Configuración Docker
├── dockerfile # Imagen de la aplicación
├── requirements.txt # Dependencias Python
├── run.py # Punto de entrada
└── debug_db.py # Utilidad de debugging


## 📸 Capturas de Pantalla

### Dashboard Administrativo
El dashboard principal muestra:
- Panel de gestión de usuarios
- Control de sesiones activas
- Acceso a auditoría del sistema
- Botones para registro manual

### Gestión de Usuarios
- Lista paginada de usuarios
- Filtros de búsqueda
- Formularios de creación/edición
- Asignación de roles y estados

### Control de Asistencia
- Vista en tiempo real de sesiones activas
- Historial completo con filtros por fecha y usuario
- Indicadores de tiempo transcurrido

## 🐛 Solución de Problemas

### Problemas Comunes

**1. Las tablas no se crean:**
```
docker-compose down -v
docker-compose up --build
```

**2. Error de conexión a MySQL:**
Verificar que MySQL esté ejecutándose
```
docker-compose logs db
```

**3. Verificar estado de la base de datos:**
```
docker-compose exec app python debug_db.py
```

### Logs de Debugging
Ver logs de la aplicación
```
docker-compose logs app
```
Ver logs de MySQL
```
docker-compose logs db
```

Ver logs en tiempo real
```
docker-compose logs -f
```

## 🤝 Contribución

1. **Fork** el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un **Pull Request**

### Guías de Contribución
- Seguir las convenciones de código existentes
- Agregar tests para nuevas funcionalidades
- Actualizar documentación si es necesario
- Usar mensajes de commit descriptivos

## 📝 Notas de Desarrollo

### Comandos Útiles
Reiniciar solo la aplicación
```
docker-compose restart app
```

Ejecutar comandos dentro del contenedor
```
docker-compose exec app python debug_db.py
```

Ver estructura de tablas
```
docker-compose exec app python -c "from app import create_app, db; app = create_app(); app.app_context().push(); print(list(db.Model.metadata.tables.keys()))"
```

### Próximas Funcionalidades
- [ ] dashboard de usuarios
- [ ] Mejoras de frontend
- [ ] Integración con lectores biométricos


## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Miguel Arévalo**
- GitHub: [@Miguel12-ares](https://github.com/Miguel12-ares)
- Proyecto: [ClockIn](https://github.com/Miguel12-ares/ClockIn)

---

## 🙏 Agradecimientos

- Tecnología SENA por el marco de desarrollo
- Comunidad Flask por la excelente documentación
- Bootstrap por los componentes UI
- Docker por facilitar el deployment

---

**¿Encontraste útil este proyecto? ¡Dale una ⭐ en GitHub!**
