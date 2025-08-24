# Sistema de Registro de Entrada y Salida de Personal "ClockIn"

Este es un sistema web para registrar entradas y salidas de personal utilizando identificación por ID único (con futura integración de huellas digitales). Está desarrollado con Python y Flask como backend, MySQL como base de datos, Tailwind CSS para interfaces frontend, y todo dockerizado para facilitar el despliegue y la portabilidad.

La arquitectura sigue el patrón MVC (Modelo-Vista-Controlador) con principios SOLID para un código limpio y mantenible. Soporta roles de usuarios como SAdmin, admin, Funcionarios Sena, Instructores, Aprendices, Administrativo y Ciudadano.

## 🆕 Nuevas Funcionalidades - Módulo de Administración

### ✅ CLOCK-17: Gestión de Usuarios y Roles
- **CRUD completo de usuarios** con validaciones robustas
- **Control de acceso basado en roles (RBAC)** con decorador `@admin_required`
- **Dashboard administrativo** con estadísticas en tiempo real
- **Sistema de auditoría** que registra todas las operaciones CRUD
- **Interfaz moderna** con Tailwind CSS y componentes interactivos
- **Paginación y búsqueda** para manejo eficiente de grandes volúmenes de datos

### 🎯 Acceso al Panel Administrativo
```
http://localhost:5000/admin/dashboard    # Dashboard principal
http://localhost:5000/admin/users        # Gestión de usuarios
```

### 🔧 Características del Módulo Admin
- **Sin autenticación en desarrollo** (configurable via `ADMIN_MODE`)
- **Validaciones de formulario** en frontend y backend
- **Manejo de errores** con mensajes descriptivos
- **Transacciones de base de datos** con rollback automático
- **Responsive design** para dispositivos móviles y desktop

## Requisitos Previos
Para instalar y correr el proyecto, necesitas:
- **Docker**: Instala Docker Desktop desde [docker.com](https://www.docker.com/products/docker-desktop) (incluye Docker Compose).
- **Git**: Para clonar el repositorio (descarga desde [git-scm.com](https://git-scm.com/)).
- **Node.js y npm** (opcional, solo si modificas frontend localmente): Descarga desde [nodejs.org](https://nodejs.org/) para compilar Tailwind CSS.
- **Python 3.10+** (opcional, para desarrollo local sin Docker): Pero se recomienda usar Docker para evitar configuraciones locales.

No se requiere un servidor MySQL local, ya que Docker lo maneja todo.

## Instalación
Sigue estos pasos para configurar el entorno rápidamente:

1. **Clona el Repositorio**:
```bash
git clone https://github.com/Miguel12-ares/ClockIn
cd ClockIn
```

2. **Configura Variables de Entorno** (opcional, pero recomendado para personalización):
- Crea un archivo `.env` en la raíz del proyecto con:
  ```
  SECRET_KEY=tu_secreto_aqui  # Clave secreta para Flask
  DATABASE_URL=mysql+pymysql://user:pass@db:3306/db_name  # Credenciales de DB
  FLASK_ENV=development  # O 'production' para modo prod
  ADMIN_MODE=true  # Habilita acceso administrativo sin autenticación
  ```
- Nota: En Docker, estas se sobreescriben por las definidas en `docker-compose.yml`.

3. **Instala Dependencias de Frontend** (si modificas Tailwind localmente):
```bash
npm install
npm run build-css
```

## Cómo Correr el Proyecto con Docker
El proyecto está completamente dockerizado para un setup fácil y consistente. No necesitas instalar Python o MySQL localmente.

1. **Construye y Ejecuta los Contenedores** (desde la raíz del proyecto):
```bash
docker-compose -f Docker/docker-compose.yml up --build
```

- Esto inicia dos contenedores: `app` (Flask) y `db` (MySQL).
- La primera vez puede tardar (descarga imágenes y configura DB).
- Accede a la app en http://localhost:5000.
- **Panel administrativo**: http://localhost:5000/admin/dashboard

2. **Detener los Contenedores**:
```bash
docker-compose -f Docker/docker-compose.yml down
```

- Agrega `-v` para borrar volúmenes y resetear la DB: `docker-compose -f Docker/docker-compose.yml down -v`.

3. **Modo Desarrollo**:
- Para hot-reload (cambios automáticos), agrega volúmenes en `docker-compose.yml` bajo `app`:
  ```yaml
  volumes:
    - .:/app
  ```
- Reconstruye con `--build` después de cambios en código.

## 🧪 Pruebas del Sistema

### Ejecutar Pruebas Automáticas
```bash
python test_admin.py
```

Este script verifica:
- ✅ Conexión a la base de datos
- ✅ Acceso al dashboard administrativo
- ✅ Funcionalidad CRUD de usuarios
- ✅ Formularios y validaciones
- ✅ Sistema de auditoría

### Pruebas Manuales
1. **Acceder al dashboard**: http://localhost:5000/admin/dashboard
2. **Crear un usuario**: Navegar a "Nuevo Usuario" y completar formulario
3. **Editar usuario**: Hacer clic en icono de edición en la lista
4. **Activar/desactivar**: Usar botón de toggle de estado
5. **Eliminar usuario**: Usar botón de eliminación (con confirmación)

## Estructura de Carpetas
```
ClockIn/
├── app/
│   ├── controllers/
│   │   └── admin.py              # 🆕 Controlador de administración
│   ├── models/                   # Modelos de base de datos
│   ├── templates/
│   │   └── admin/               # 🆕 Plantillas del panel admin
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── users.html
│   │       └── user_form.html
│   ├── __init__.py              # Configuración Flask + RBAC
│   └── init_data.py             # 🆕 Inicialización de datos
├── Docker/                      # Configuración Docker
├── docs/                        # Documentación
├── static/                      # CSS/JS compilados
├── test_admin.py               # 🆕 Script de pruebas
└── run.py                      # Punto de entrada
```

## 📚 Documentación

### Módulo de Administración
- [Documentación completa del módulo admin](docs/controllers/admin/README.md)
- [Guía de uso y configuración](docs/controllers/admin/README.md#uso)
- [API y endpoints disponibles](docs/controllers/admin/README.md#rutas-disponibles)

### Otros Módulos
- [Gestión de usuarios](docs/controllers/user/README.md)
- [Gestión de zonas](docs/controllers/zona/README.md)
- [Tipos de usuario](docs/controllers/user_type/README.md)

## Uso

### Panel Administrativo
- **Dashboard**: Estadísticas generales del sistema
- **Gestión de Usuarios**: CRUD completo con búsqueda y filtros
- **Asignación de Roles**: Configurar tipos de usuario y permisos
- **Auditoría**: Ver historial de cambios en el sistema

### Funcionalidades Principales
- **Registro por ID**: Accede a /login e ingresa un ID único
- **Dashboards**: Dependiendo del rol, verás historiales y reportes
- **Gestión de Personal**: Panel administrativo completo
- **Expansión**: Futura integración de huellas con pyfingerprint

## 🔒 Seguridad

### En Desarrollo
- Acceso directo al panel administrativo
- Modo administrador habilitado por defecto
- Validaciones de formulario en frontend y backend

### En Producción
- Integrar con sistema de autenticación real
- Configurar `ADMIN_MODE=false`
- Implementar sesiones seguras
- Validar permisos de usuario autenticado

## Contribuyendo
1. Forkea el repositorio
2. Crea una branch: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

### Guías de Contribución
- Sigue los principios SOLID
- Escribe tests con pytest
- Actualiza documentación
- Valida compatibilidad con Docker
- Prueba en entorno de desarrollo

## 🐛 Reportar Problemas

Para reportar bugs o solicitar funcionalidades:
- Crear issue en el repositorio
- Incluir logs de error
- Describir pasos para reproducir
- Especificar versión del sistema
- Adjuntar capturas de pantalla si es relevante

## Licencia
Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para detalles.

Si encuentras problemas, abre un issue o contacta al maintainer.
