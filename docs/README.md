# Documentación ClockIn

Documentación completa del sistema de registro de entrada y salida de personal ClockIn.

## 📚 Estructura de Documentación

### 🚀 [Setup y Configuración](setup/README.md)
Guía completa de instalación, configuración e inicialización del sistema.

### 🎛️ [Controladores](controllers/README.md)
Documentación de todos los controladores del sistema MVC.

#### Controladores Específicos:
- **[Auth](controllers/auth/README.md)** - Sistema de autenticación JWT
- **[User](controllers/user/README.md)** - Gestión de usuarios
- **[Zona](controllers/zona/README.md)** - Gestión de zonas
- **[Admin Zona](controllers/admin_zona/README.md)** - Administradores por zona
- **[Access Log](controllers/access_log/README.md)** - Logs de acceso

### 🌐 [Endpoints de API](endpoints/)
Documentación detallada de todos los endpoints REST.

- **[Authentication API](endpoints/auth.md)** - Endpoints de autenticación

### 🔧 [Implementación](implementation/)
Documentación técnica de implementaciones específicas.

- **[Sistema de Autenticación](implementation/authentication_implementation.md)** - Implementación completa del sistema JWT

## 🏗️ Arquitectura del Sistema

```
ClockIn/
├── app/                    # Aplicación principal
│   ├── controllers/        # Controladores MVC
│   ├── models/            # Modelos de base de datos
│   ├── templates/         # Templates HTML
│   ├── middleware/        # Middleware de seguridad
│   └── utils/            # Utilidades y helpers
├── docs/                  # Documentación
├── Docker/               # Configuración Docker
└── requirements.txt      # Dependencias Python
```

## 🚀 Inicio Rápido

### 1. Instalación
```bash
pip install -r requirements.txt
python init_db.py
python run.py
```

### 2. Acceso
- **Web**: `http://localhost:5000/auth/login`
- **API**: `http://localhost:5000/auth/login` (POST)

### 3. Usuario de Prueba
- **ID**: `12345678`
- **Tipo**: Instructor

## 🔑 Funcionalidades Principales

### ✅ Sistema de Autenticación
- Autenticación por ID único
- Tokens JWT con 8 horas de duración
- Manejo seguro de sesiones
- Sistema de roles completo

### ✅ Gestión de Usuarios
- CRUD completo de usuarios
- 7 tipos de usuario predefinidos
- Estados y zonas configurables
- Relaciones completas en BD

### ✅ API REST Completa
- Endpoints documentados
- Validaciones robustas
- Responses consistentes
- Manejo de errores

### ✅ Seguridad
- Middleware de autenticación
- Protección por roles
- Registro de actividad
- Validaciones de entrada

## 📊 Base de Datos

### Tablas Principales
- **users** - Información de usuarios
- **user_types** - Tipos/roles de usuario
- **zonas** - Zonas de acceso
- **estados** - Estados de usuario
- **active_sessions** - Sesiones activas
- **access_logs** - Logs de acceso

### Datos Iniciales
- **7 tipos de usuario** creados automáticamente
- **4 estados** básicos configurados
- **3 zonas** de ejemplo inicializadas

## 🛠️ Desarrollo

### Stack Tecnológico
- **Backend**: Python + Flask
- **Base de Datos**: SQLite (desarrollo) / MySQL (producción)
- **Frontend**: HTML + JavaScript (sin frameworks)
- **Autenticación**: JWT
- **Estilo**: Sin framework CSS (funcional)

### Patrones Implementados
- **MVC** - Separación clara de responsabilidades
- **Blueprint** - Modularización de rutas
- **Repository** - Acceso a datos
- **Middleware** - Funcionalidades transversales

## 📖 Guías Específicas

### Para Desarrolladores
1. **[Setup](setup/README.md)** - Configuración de entorno
2. **[Controladores](controllers/README.md)** - Desarrollo de nuevos controladores
3. **[API](endpoints/auth.md)** - Uso de endpoints existentes

### Para Administradores
1. **[Instalación](setup/README.md)** - Despliegue en producción
2. **[Configuración](setup/README.md)** - Variables de entorno
3. **[Mantenimiento](implementation/authentication_implementation.md)** - Gestión del sistema

### Para Usuarios Finales
1. **Acceso**: Ir a `/auth/login`
2. **Login**: Ingresar ID de documento
3. **Navegación**: Usar dashboard según rol

## 🔍 Referencias Rápidas

### URLs Principales
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Redirige a login |
| `/auth/login` | GET/POST | Autenticación |
| `/auth/logout` | POST | Cerrar sesión |
| `/users/` | GET/POST | Gestión usuarios |

### Códigos de Estado
- **200** - Éxito
- **201** - Creado
- **400** - Error de validación
- **401** - No autorizado
- **403** - Prohibido
- **404** - No encontrado
- **500** - Error interno

### Tipos de Usuario
1. **SAdmin** - Super Administrador
2. **Admin** - Administrador
3. **Funcionario SENA** - Funcionario
4. **Instructor** - Instructor
5. **Aprendiz** - Aprendiz
6. **Administrativo** - Administrativo
7. **Ciudadano** - Ciudadano

## 📞 Soporte

### Documentación Técnica
- **Implementación**: `docs/implementation/`
- **API**: `docs/endpoints/`
- **Controladores**: `docs/controllers/`

### Configuración
- **Setup**: `docs/setup/README.md`
- **Archivos**: `app/config.py`
- **Variables**: `.env` (crear si es necesario)

---

**Sistema ClockIn** - Registro de entrada y salida de personal con autenticación por ID único.
