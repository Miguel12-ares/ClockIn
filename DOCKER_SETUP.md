## Inicialización de MySQL

Para garantizar que el usuario `user` tenga acceso desde cualquier host (`%`), se usa un script en `Docker/mysql-init/01-create-user.sql` que se ejecuta automáticamente al crear el contenedor por primera vez.

Si cambias las credenciales, recrea los volúmenes: `docker-compose down -v` y luego `docker-compose up --build`.

# ClockIn - Configuracion para Docker

## Estado del Proyecto

El proyecto ClockIn ha sido **completamente corregido** y esta listo para ejecutarse en Docker. Se han resuelto todos los problemas de endpoints duplicados y configuraciones.

## Problemas Resueltos

1. **AssertionError de endpoints duplicados** - Eliminada funcion `index()` duplicada en `app/__init__.py`
2. **Inconsistencias en modelos** - Corregidos campos `sede_nombre` y `name` en modelos Zona y Estado
3. **Relaciones de base de datos** - Corregidas relaciones con claves foraneas multiples
4. **Configuracion de Docker** - Optimizada para MySQL en Docker
5. **Dependencias** - Instaladas y verificadas todas las dependencias

## Comandos para Ejecutar en Docker

### Opción 1: Script de PowerShell (Recomendado)
```powershell
# Mostrar ayuda
.\docker_commands.ps1

# Construir y ejecutar
.\docker_commands.ps1 build

# Solo ejecutar (si ya está construido)
.\docker_commands.ps1 start

# Ver logs
.\docker_commands.ps1 logs

# Detener
.\docker_commands.ps1 stop
```

### Opción 2: Comandos Docker Directos
```bash
# Construir y ejecutar
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## URLs de Acceso

Una vez que la aplicacion este ejecutandose:

- **Aplicacion Principal**: http://localhost:5000
- **Panel Administrativo**: http://localhost:5000/admin/dashboard
- **Gestion de Usuarios**: http://localhost:5000/admin/users
- **Login de Usuarios**: http://localhost:5000/auth/login
- **API de Usuarios**: http://localhost:5000/users
- **API de Zonas**: http://localhost:5000/zonas

## Pruebas de Configuracion

Antes de ejecutar Docker, puedes verificar que todo este correcto:

```powershell
# Ejecutar pruebas de configuración
python test_docker_setup.py

# O usar el script
.\docker_commands.ps1 test
```

## Funcionalidades Disponibles

### Autenticacion
- Login por numero de documento
- Tokens JWT para sesiones
- Logout automatico
- Registro de accesos

### Gestion de Usuarios
- CRUD completo de usuarios
- Asignacion de tipos de usuario
- Gestion de zonas y estados
- Activacion/desactivacion

### Gestion de Zonas
- Crear, editar, eliminar zonas
- Asignar administradores por zona
- Filtros por ciudad/departamento

### Auditoria
- Registro de todas las acciones
- Logs de acceso
- Auditoria del sistema
- Deteccion de anomalias

## Configuracion Tecnica

### Base de Datos
- **MySQL 8.0** en contenedor Docker
- **Host**: `db` (interno del Docker network)
- **Puerto**: `3306`
- **Base de datos**: `db_name`
- **Usuario**: `user`
- **Contraseña**: `pass`

### Aplicación
- **Flask 3.0.3** con Gunicorn
- **Puerto**: `5000`
- **Workers**: `2`
- **Timeout**: `120s`

## Solucion de Problemas

### Si la aplicacion no inicia:
1. Verificar que Docker este ejecutandose
2. Ejecutar `.\docker_commands.ps1 clean` para limpiar
3. Reconstruir con `.\docker_commands.ps1 build`

### Si hay problemas de base de datos:
1. Verificar que el puerto 3306 este libre
2. Revisar logs con `.\docker_commands.ps1 logs`
3. Reiniciar con `.\docker_commands.ps1 restart`

### Si hay problemas de red:
1. Verificar que el puerto 5000 este libre
2. Cambiar puerto en `Docker/docker-compose.yml` si es necesario

## Notas Importantes

- **ADMIN_MODE**: Habilitado por defecto para desarrollo
- **Datos de prueba**: Se crean automaticamente al iniciar
- **Persistencia**: Los datos se mantienen en volumen Docker
- **Logs**: Disponibles en tiempo real con `docker-compose logs -f`

## Proximos Pasos

1. Ejecutar `.\docker_commands.ps1 build`
2. Acceder a http://localhost:5000
3. Probar la gestion de usuarios
4. Verificar la auditoria del sistema

La aplicacion esta lista para usar!
