# Plan de Completación - Sistema ClockIn

## Objetivo
Completar los módulos de autenticación (CLOCK-16) y gestión de usuarios (CLOCK-17) para tener un sistema funcional y seguro.

## Estado Actual
- ✅ **CLOCK-17**: Gestión de Usuarios - Básico implementado
- ❌ **CLOCK-16**: Autenticación - No implementado
- ✅ **Infraestructura**: Docker, Base de datos, Frontend funcionando

## Fase 1: Implementación de Autenticación (CLOCK-16)

### 1.1 Estructura de Archivos a Crear

```
app/
├── controllers/
│   └── auth.py                    # Controlador de autenticación
├── templates/
│   └── auth/
│       ├── login.html             # Página de login
│       ├── register.html          # Página de registro
│       ├── forgot_password.html   # Recuperación de contraseña
│       └── reset_password.html    # Reset de contraseña
├── models/
│   └── session.py                 # Modelo de sesiones (opcional)
├── middleware/
│   └── auth.py                    # Middleware de autenticación
└── utils/
    └── auth_utils.py              # Utilidades de autenticación
```

### 1.2 Implementación del Controlador de Autenticación

#### `app/controllers/auth.py`
```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        id_documento = request.form.get('id_documento')
        password = request.form.get('password')
        
        user = User.query.filter_by(idDocumento=id_documento).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Tu cuenta está desactivada', 'error')
                return redirect(url_for('auth.login'))
            
            # Crear sesión
            session['user_id'] = user.id
            session['user_type'] = user.user_type.type_name
            session['user_name'] = f"{user.first_name} {user.last_name}"
            
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Credenciales inválidas', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuarios"""
    if request.method == 'POST':
        # Validar datos
        id_documento = request.form.get('id_documento')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(url_for('auth.register'))
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(idDocumento=id_documento).first()
        if existing_user:
            flash('El número de documento ya está registrado', 'error')
            return redirect(url_for('auth.register'))
        
        # Crear nuevo usuario
        new_user = User(
            idDocumento=id_documento,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            password_hash=generate_password_hash(password),
            user_type_id=3,  # Empleado por defecto
            zona_id=1,       # Zona por defecto
            estado_id=1,     # Activo por defecto
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')
```

### 1.3 Plantillas de Autenticación

#### `app/templates/auth/login.html`
```html
{% extends "base.html" %}

{% block content %}
<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <div>
            <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                Iniciar Sesión
            </h2>
            <p class="mt-2 text-center text-sm text-gray-600">
                Sistema de Control de Acceso ClockIn
            </p>
        </div>
        <form class="mt-8 space-y-6" method="POST">
            <div class="rounded-md shadow-sm -space-y-px">
                <div>
                    <label for="id_documento" class="sr-only">Número de Documento</label>
                    <input id="id_documento" name="id_documento" type="number" required 
                           class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
                           placeholder="Número de Documento">
                </div>
                <div>
                    <label for="password" class="sr-only">Contraseña</label>
                    <input id="password" name="password" type="password" required 
                           class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" 
                           placeholder="Contraseña">
                </div>
            </div>

            <div>
                <button type="submit" 
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Iniciar Sesión
                </button>
            </div>

            <div class="flex items-center justify-between">
                <div class="text-sm">
                    <a href="{{ url_for('auth.forgot_password') }}" class="font-medium text-blue-600 hover:text-blue-500">
                        ¿Olvidaste tu contraseña?
                    </a>
                </div>
                <div class="text-sm">
                    <a href="{{ url_for('auth.register') }}" class="font-medium text-blue-600 hover:text-blue-500">
                        Registrarse
                    </a>
                </div>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

### 1.4 Middleware de Autenticación

#### `app/middleware/auth.py`
```python
from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir permisos de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        
        if session.get('user_type') != 'Admin':
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('admin.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def supervisor_required(f):
    """Decorador para requerir permisos de supervisor"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))
        
        user_type = session.get('user_type')
        if user_type not in ['Admin', 'Supervisor']:
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('admin.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function
```

### 1.5 Actualización del Modelo User

#### Agregar campo de contraseña a `app/models/user.py`
```python
# Agregar este campo al modelo User
password_hash = db.Column(db.String(255), nullable=True)  # Para usuarios existentes
```

## Fase 2: Mejoras al Módulo de Gestión de Usuarios (CLOCK-17)

### 2.1 Funcionalidades a Agregar

#### 2.1.1 Filtros Avanzados
```python
@admin_bp.route('/users')
@admin_required
def users_index():
    """Lista de usuarios con filtros avanzados"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Filtros
    search = request.args.get('search', '')
    user_type_filter = request.args.get('user_type', '')
    zona_filter = request.args.get('zona', '')
    status_filter = request.args.get('status', '')
    
    query = User.query
    
    # Aplicar filtros
    if search:
        query = query.filter(
            db.or_(
                User.first_name.contains(search),
                User.last_name.contains(search),
                User.idDocumento.contains(search)
            )
        )
    
    if user_type_filter:
        query = query.filter(User.user_type_id == user_type_filter)
    
    if zona_filter:
        query = query.filter(User.zona_id == zona_filter)
    
    if status_filter:
        is_active = status_filter == 'active'
        query = query.filter(User.is_active == is_active)
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Obtener opciones para filtros
    user_types = UserType.query.all()
    zonas = Zona.query.all()
    
    return render_template('admin/users.html', 
                         users=users, 
                         search=search,
                         user_types=user_types,
                         zonas=zonas,
                         user_type_filter=user_type_filter,
                         zona_filter=zona_filter,
                         status_filter=status_filter)
```

#### 2.1.2 Exportación de Datos
```python
@admin_bp.route('/users/export')
@admin_required
def export_users():
    """Exportar usuarios a CSV"""
    import csv
    from io import StringIO
    
    # Obtener todos los usuarios
    users = User.query.all()
    
    # Crear CSV
    si = StringIO()
    cw = csv.writer(si)
    
    # Headers
    cw.writerow(['ID', 'Documento', 'Nombre', 'Apellido', 'Tipo', 'Zona', 'Estado', 'Activo'])
    
    # Datos
    for user in users:
        cw.writerow([
            user.id,
            user.idDocumento,
            user.first_name,
            user.last_name,
            user.user_type.type_name if user.user_type else 'N/A',
            user.zona.nombre if user.zona else 'N/A',
            user.estado.nombre if user.estado else 'N/A',
            'Sí' if user.is_active else 'No'
        ])
    
    output = si.getvalue()
    
    from flask import Response
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=usuarios.csv'}
    )
```

### 2.2 Mejoras en la Interfaz

#### 2.2.1 Filtros en la Vista de Usuarios
```html
<!-- Agregar a app/templates/admin/users.html -->
<div class="px-6 py-4 border-b border-gray-200">
    <form method="GET" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <!-- Búsqueda -->
        <div>
            <input type="text" name="search" value="{{ search }}" 
                   placeholder="Buscar usuarios..."
                   class="w-full px-3 py-2 border border-gray-300 rounded-md">
        </div>
        
        <!-- Filtro por tipo -->
        <div>
            <select name="user_type" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                <option value="">Todos los tipos</option>
                {% for user_type in user_types %}
                    <option value="{{ user_type.id }}" 
                            {% if user_type_filter|string == user_type.id|string %}selected{% endif %}>
                        {{ user_type.type_name }}
                    </option>
                {% endfor %}
            </select>
        </div>
        
        <!-- Filtro por zona -->
        <div>
            <select name="zona" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                <option value="">Todas las zonas</option>
                {% for zona in zonas %}
                    <option value="{{ zona.id }}" 
                            {% if zona_filter|string == zona.id|string %}selected{% endif %}>
                        {{ zona.nombre }}
                    </option>
                {% endfor %}
            </select>
        </div>
        
        <!-- Filtro por estado -->
        <div>
            <select name="status" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                <option value="">Todos los estados</option>
                <option value="active" {% if status_filter == 'active' %}selected{% endif %}>Activos</option>
                <option value="inactive" {% if status_filter == 'inactive' %}selected{% endif %}>Inactivos</option>
            </select>
        </div>
        
        <!-- Botones -->
        <div class="flex space-x-2">
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-md">
                Filtrar
            </button>
            <a href="{{ url_for('admin.users_index') }}" class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md">
                Limpiar
            </a>
            <a href="{{ url_for('admin.export_users') }}" class="bg-green-600 text-white px-4 py-2 rounded-md">
                Exportar
            </a>
        </div>
    </form>
</div>
```

## Fase 3: Integración y Testing

### 3.1 Actualización de `app/__init__.py`
```python
# Agregar el blueprint de autenticación
from app.controllers.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Actualizar el decorador admin_required
from app.middleware.auth import admin_required
```

### 3.2 Script de Migración de Base de Datos
```python
# app/migrations/add_password_field.py
from app import app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

def add_password_field():
    """Agregar campo de contraseña a usuarios existentes"""
    with app.app_context():
        # Agregar columna si no existe
        try:
            db.engine.execute('ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)')
        except:
            pass  # La columna ya existe
        
        # Asignar contraseñas por defecto a usuarios existentes
        users = User.query.filter_by(password_hash=None).all()
        for user in users:
            # Contraseña por defecto: documento + "123"
            default_password = f"{user.idDocumento}123"
            user.password_hash = generate_password_hash(default_password)
        
        db.session.commit()
        print(f"Se actualizaron {len(users)} usuarios con contraseñas por defecto")
```

### 3.3 Testing del Sistema

#### 3.3.1 Script de Pruebas
```python
# test_auth.py
import requests

def test_auth_system():
    """Probar el sistema de autenticación"""
    base_url = "http://localhost:5000"
    
    # Probar login
    login_data = {
        'id_documento': '111',
        'password': '111123'
    }
    
    response = requests.post(f"{base_url}/auth/login", data=login_data)
    print(f"Login response: {response.status_code}")
    
    # Probar acceso a dashboard
    response = requests.get(f"{base_url}/admin/dashboard")
    print(f"Dashboard response: {response.status_code}")

if __name__ == "__main__":
    test_auth_system()
```

## Cronograma de Implementación

### Semana 1: Autenticación Básica
- [ ] Implementar controlador `auth.py`
- [ ] Crear plantillas de login/registro
- [ ] Implementar middleware de autenticación
- [ ] Actualizar modelo User con password_hash
- [ ] Testing básico

### Semana 2: Integración y Mejoras
- [ ] Integrar autenticación con el sistema existente
- [ ] Implementar filtros avanzados en gestión de usuarios
- [ ] Agregar exportación de datos
- [ ] Mejorar interfaz de usuario
- [ ] Testing completo

### Semana 3: Optimización y Documentación
- [ ] Optimizar consultas de base de datos
- [ ] Implementar caché
- [ ] Documentar APIs
- [ ] Crear guías de usuario
- [ ] Testing de rendimiento

## Comandos de Implementación

### 1. Crear archivos necesarios
```bash
# Crear directorios
mkdir -p app/templates/auth
mkdir -p app/middleware
mkdir -p app/utils

# Crear archivos
touch app/controllers/auth.py
touch app/middleware/auth.py
touch app/utils/auth_utils.py
touch app/templates/auth/login.html
touch app/templates/auth/register.html
```

### 2. Ejecutar migración de base de datos
```bash
# Dentro del contenedor
docker exec -it docker-app-1 python -c "
from app import app, db
from app.models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    try:
        db.engine.execute('ALTER TABLE users ADD COLUMN password_hash VARCHAR(255)')
    except:
        pass
    
    users = User.query.filter_by(password_hash=None).all()
    for user in users:
        default_password = f'{user.idDocumento}123'
        user.password_hash = generate_password_hash(default_password)
    
    db.session.commit()
    print(f'Actualizados {len(users)} usuarios')
"
```

### 3. Reiniciar sistema
```bash
docker-compose -f Docker/docker-compose.yml down
docker-compose -f Docker/docker-compose.yml up --build
```

## Resultado Esperado

Al completar estas fases, el sistema ClockIn tendrá:

1. ✅ **Sistema de autenticación completo**
   - Login/logout funcional
   - Registro de usuarios
   - Protección de rutas
   - Gestión de sesiones

2. ✅ **Gestión de usuarios avanzada**
   - Filtros múltiples
   - Exportación de datos
   - Interfaz mejorada
   - Validaciones robustas

3. ✅ **Sistema seguro y escalable**
   - Contraseñas hasheadas
   - Control de acceso granular
   - Auditoría completa
   - Performance optimizado

El sistema estará listo para uso en producción con todas las funcionalidades básicas implementadas y probadas.
