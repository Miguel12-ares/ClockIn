# Configuración e Instalación - ClockIn

Esta guía describe el proceso completo de configuración e instalación del sistema ClockIn.

## 📋 Requisitos Previos

### Desarrollo Local
- **Python 3.10+**
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para clonar repositorio)

### Producción (Opcional)
- **Docker** y **Docker Compose**
- **MySQL** (si no se usa SQLite)
- **Servidor web** (Nginx, Apache)

## 🚀 Instalación Rápida

### 1. Clonar Repositorio
```bash
git clone https://github.com/Miguel12-ares/ClockIn
cd ClockIn
```

### 2. Crear Entorno Virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno (Opcional)
Crear archivo `.env` en la raíz:
```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
DATABASE_URL=sqlite:///clockin.db
FLASK_ENV=development
```

### 5. Inicializar Base de Datos
```bash
python init_db.py
```

### 6. Iniciar Servidor
```bash
python run.py
```

**Sistema disponible en**: `http://localhost:5000`

## 🔧 Configuración Detallada

### Base de Datos

#### SQLite (Por Defecto - Desarrollo)
```python
# app/config.py
SQLALCHEMY_DATABASE_URI = 'sqlite:///clockin.db'
```

#### MySQL (Producción)
```python
# app/config.py
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/clockin_db'
```

#### Variables de Entorno
```env
DATABASE_URL=mysql+pymysql://user:password@localhost/clockin_db
SECRET_KEY=clave_secreta_production
FLASK_ENV=production
```

### Configuración de Seguridad

#### Clave Secreta
```env
# .env
SECRET_KEY=clave_muy_segura_para_jwt_tokens
```

#### JWT Configuración
- **Duración**: 8 horas por defecto
- **Algoritmo**: HS256
- **Modificar en**: `app/controllers/auth.py`

### Estructura de Archivos de Configuración

```
ClockIn/
├── .env                    # Variables de entorno (crear)
├── app/config.py          # Configuración principal
├── init_db.py            # Script de inicialización
├── requirements.txt      # Dependencias Python
└── run.py               # Punto de entrada
```

## 📊 Inicialización de Datos

### Datos Básicos Creados Automáticamente

#### Tipos de Usuario
1. **SAdmin** - Super Administrador
2. **Admin** - Administrador
3. **Funcionario SENA** - Funcionario SENA
4. **Instructor** - Instructor
5. **Aprendiz** - Aprendiz
6. **Administrativo** - Administrativo
7. **Ciudadano** - Ciudadano

#### Estados
1. **Activo** - Usuario activo
2. **Inactivo** - Usuario inactivo temporalmente
3. **Suspendido** - Usuario suspendido
4. **Bloqueado** - Usuario bloqueado

#### Zonas
1. **Sede Principal** - Bogotá, Cundinamarca
2. **Sede Norte** - Bogotá, Cundinamarca
3. **Sede Industrial** - Bogotá, Cundinamarca

### Crear Usuario de Prueba

```bash
# PowerShell
$body = @{
    idDocumento="12345678"
    first_name="Juan"
    last_name="Pérez"
    user_type_id=4  # Instructor
    zona_id=1       # Sede Principal
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/users/ -Method POST -Body $body -ContentType "application/json"
```

## 🐳 Instalación con Docker

### 1. Construir Imagen
```bash
docker build -t clockin .
```

### 2. Ejecutar con Docker Compose
```bash
docker-compose -f Docker/docker-compose.yml up --build
```

### 3. Acceder
- **Aplicación**: `http://localhost:5000`
- **Base de datos**: MySQL en puerto 3306

## 🔍 Verificación de Instalación

### 1. Verificar Servidor
```bash
curl http://localhost:5000/auth/login
# Debe retornar HTML del formulario de login
```

### 2. Probar API
```bash
# Crear usuario
curl -X POST http://localhost:5000/users/ \
  -H "Content-Type: application/json" \
  -d '{"idDocumento":"12345678","first_name":"Test","last_name":"User","user_type_id":4,"zona_id":1}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"idDocumento":"12345678"}'
```

### 3. Verificar Base de Datos
```bash
# SQLite
sqlite3 clockin.db ".tables"
# Debe mostrar: users, user_types, zonas, estados, access_logs, etc.
```

## 🚨 Solución de Problemas

### Error: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Error: "Access denied for user"
- Verificar credenciales de MySQL en `app/config.py`
- Usar SQLite para desarrollo: `DATABASE_URL=sqlite:///clockin.db`

### Error: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:5000 | xargs kill -9
```

### Error: "Template not found"
- Verificar que existe `app/templates/login.html`
- Verificar estructura de carpetas

## 🔧 Configuración de Producción

### 1. Variables de Entorno
```env
SECRET_KEY=clave_production_muy_segura
DATABASE_URL=mysql+pymysql://user:pass@prod-server/clockin_db
FLASK_ENV=production
```

### 2. Servidor WSGI
```bash
# Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# uWSGI
pip install uwsgi
uwsgi --http-socket 0.0.0.0:5000 --module run:app
```

### 3. Proxy Reverso (Nginx)
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📚 Recursos Adicionales

### Documentación
- **API**: `docs/endpoints/auth.md`
- **Controladores**: `docs/controllers/`
- **Implementación**: `docs/implementation/`

### Archivos de Configuración
- **Principal**: `app/config.py`
- **Inicialización**: `app/utils/init_data.py`
- **Dependencias**: `requirements.txt`

### Logs
- **Aplicación**: Consola del servidor
- **Accesos**: Tabla `access_logs` en BD
- **Errores**: Logs de Flask/Python

## ✅ Checklist de Instalación

- [ ] Python 3.10+ instalado
- [ ] Repositorio clonado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Variables de entorno configuradas (opcional)
- [ ] Base de datos inicializada (`python init_db.py`)
- [ ] Servidor iniciado (`python run.py`)
- [ ] Usuario de prueba creado
- [ ] Login funcionando
- [ ] API endpoints respondiendo

**¡Sistema ClockIn listo para usar!** 🎉
