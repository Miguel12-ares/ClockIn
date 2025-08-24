# Implementación del Sistema de Autenticación ClockIn

Este documento describe la implementación completa del sistema de autenticación basado en ID único para el proyecto ClockIn.

## ✅ Funcionalidades Implementadas

### 1. Endpoint de Autenticación
- **POST /auth/login**: Autenticación por número de identificación
- **POST /auth/logout**: Cierre de sesión
- **GET /auth/verify**: Verificación de token JWT
- **GET /auth/login**: Formulario web de login

### 2. Sistema JWT
- Tokens con duración de 8 horas
- Payload completo con información del usuario
- Validación automática de expiración
- Manejo seguro de sesiones

### 3. Sistema de Roles
- 7 tipos de usuario predefinidos:
  - SAdmin (Super Administrador)
  - Admin (Administrador)
  - Funcionario SENA
  - Instructor
  - Aprendiz
  - Administrativo
  - Ciudadano

### 4. Middleware de Seguridad
- `@token_required`: Protege rutas con autenticación
- `@role_required`: Protege rutas por roles específicos
- `@admin_required`: Acceso solo para administradores

### 5. Redirección por Rol
- Cada tipo de usuario es redirigido a su dashboard específico
- URLs configurables por rol

### 6. Registro de Actividad
- Todos los intentos de login se registran en `access_logs`
- Seguimiento de sesiones activas
- Auditoría completa de accesos

## 📁 Archivos Creados/Modificados

### Nuevos Archivos
```
app/middleware/auth_middleware.py     # Middleware de autenticación
app/utils/init_data.py               # Inicialización de datos básicos
app/templates/login.html             # Interfaz web de login
docs/endpoints/auth.md               # Documentación de endpoints
docs/authentication_implementation.md # Este documento
init_db.py                          # Script de inicialización
```

### Archivos Modificados
```
requirements.txt                     # + PyJWT, flask-cors
app/__init__.py                     # + registro del blueprint auth
app/controllers/auth.py             # Implementación completa
```

## 🚀 Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Inicializar Base de Datos
```bash
python init_db.py
```

### 3. Variables de Entorno
Crear archivo `.env`:
```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
DATABASE_URL=mysql+pymysql://user:pass@localhost/ClinkInDB
FLASK_ENV=development
```

### 4. Crear Usuarios de Prueba
Usar el endpoint `POST /users` para crear usuarios:
```json
{
    "idDocumento": "12345678",
    "first_name": "Juan",
    "last_name": "Pérez",
    "user_type_id": 4,  // ID del tipo "Instructor"
    "zona_id": 1
}
```

## 🔧 Uso del Sistema

### Autenticación por API
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"idDocumento": "12345678"}'
```

### Uso del Token
```bash
curl -X GET http://localhost:5000/auth/verify \
  -H "Authorization: Bearer <token_recibido>"
```

### Interfaz Web
Visitar: `http://localhost:5000/auth/login`

## 🛡️ Características de Seguridad

### Validaciones Implementadas
- ✅ Verificación de existencia del usuario
- ✅ Validación de estado activo
- ✅ Manejo de sesiones únicas
- ✅ Expiración automática de tokens
- ✅ Registro de intentos fallidos
- ✅ Protección contra tokens inválidos

### Buenas Prácticas
- ✅ Separación de concerns con middleware
- ✅ Manejo de errores consistente
- ✅ Logs de auditoría completos
- ✅ Validación de roles granular
- ✅ Estructura modular y escalable

## 🔄 Flujo de Autenticación

1. **Usuario envía ID documento** → `POST /auth/login`
2. **Sistema valida usuario** → Busca en BD, verifica estado
3. **Genera token JWT** → 8 horas de validez
4. **Crea sesión activa** → Registra en `active_sessions`
5. **Registra en logs** → Auditoría en `access_logs`
6. **Retorna datos** → Token + info usuario + URL redirección
7. **Cliente usa token** → Headers `Authorization: Bearer <token>`

## 📊 Estructura de Base de Datos

### Tablas Utilizadas
- `users`: Información de usuarios
- `user_types`: Tipos/roles de usuario  
- `active_sessions`: Sesiones activas
- `access_logs`: Registro de accesos
- `zonas`: Zonas de acceso
- `estados`: Estados de usuario

### Relaciones Clave
- User → UserType (muchos a uno)
- User → Zona (muchos a uno)
- User → ActiveSession (uno a muchos)
- User → AccessLog (uno a muchos)

## 🧪 Testing

### Probar Endpoints
```bash
# 1. Login exitoso
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"idDocumento": "12345678"}'

# 2. Login fallido
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"idDocumento": "99999999"}'

# 3. Verificar token
curl -X GET http://localhost:5000/auth/verify \
  -H "Authorization: Bearer TOKEN_AQUI"

# 4. Logout
curl -X POST http://localhost:5000/auth/logout \
  -H "Authorization: Bearer TOKEN_AQUI"
```

## 🔮 Próximos Pasos

### Integraciones Futuras
- [ ] Integración con huellas digitales
- [ ] Autenticación de dos factores (2FA)
- [ ] SSO (Single Sign-On)
- [ ] Refresh tokens

### Mejoras de Seguridad
- [ ] Rate limiting para login
- [ ] Bloqueo temporal por intentos fallidos
- [ ] Notificaciones de acceso sospechoso
- [ ] Rotación automática de tokens

### Funcionalidades Adicionales
- [ ] Recuperación de acceso
- [ ] Gestión de sesiones múltiples
- [ ] API para cambio de rol temporal
- [ ] Dashboard de actividad de usuario

## 📞 Soporte

Para dudas sobre la implementación:
1. Revisar la documentación en `docs/endpoints/auth.md`
2. Verificar logs en `access_logs` para debugging
3. Usar el script `init_db.py` para reset completo
4. Consultar middleware en `app/middleware/auth_middleware.py`
