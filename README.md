# Sistema de Registro de Entrada y Salida de Personal "ClockIn"

Este es un sistema web para registrar entradas y salidas de personal utilizando identificación por ID único (con futura integración de huellas digitales). Está desarrollado con Python y Flask como backend, MySQL como base de datos, Tailwind CSS para interfaces frontend, y todo dockerizado para facilitar el despliegue y la portabilidad.

La arquitectura sigue el patrón MVC (Modelo-Vista-Controlador) con principios SOLID para un código limpio y mantenible. Soporta roles de usuarios como SAdmin, admin, Funcionarios Sena, Instructores, Aprendices, Administrativo y Ciudadano.

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
``` git clone https://github.com/Miguel12-ares/ClockIn ```


2. **Configura Variables de Entorno** (opcional, pero recomendado para personalización):
- Crea un archivo `.env` en la raíz del proyecto con:
  ```
  SECRET_KEY=tu_secreto_aqui  # Clave secreta para Flask
  DATABASE_URL=mysql+pymysql://user:pass@db:3306/db_name  # Credenciales de DB (ajusta si es necesario)
  FLASK_ENV=development  # O 'production' para modo prod
  ```
- Nota: En Docker, estas se sobreescriben por las definidas en `docker-compose.yml`.

3. **Instala Dependencias de Frontend (si modificas Tailwind localmente)**:
``` npm install ```
``` npm run build-css ```


## Cómo Correr el Proyecto con Docker
El proyecto está completamente dockerizado para un setup fácil y consistente. No necesitas instalar Python o MySQL localmente.

1. **Construye y Ejecuta los Contenedores** (desde la raíz del proyecto):
``` docker-compose -f Docker/docker-compose.yml up --build ```

- Esto inicia dos contenedores: `app` (Flask) y `db` (MySQL).
- La primera vez puede tardar (descarga imágenes y configura DB).
- Accede a la app en http://localhost:5000.

2. **Detener los Contenedores**:
```  docker-compose -f Docker/docker-compose.yml down ```

- Agrega `-v` para borrar volúmenes y resetear la DB: `docker-compose -f Docker/docker-compose.yml down -v`.

3. **Modo Desarrollo**:
- Para hot-reload (cambios automáticos), agrega volúmenes en `docker-compose.yml` bajo `app`:
  ```
  volumes:
    - .:/app
  ```
- Reconstruye con `--build` después de cambios en código.

## Estructura de Carpetas
- **app/**: Núcleo MVC (modelos, controladores, templates, static).
- **Docker/**: Archivos para dockerización (Dockerfile, docker-compose.yml).
- **static/**: CSS/JS compilados (Tailwind).
- **templates/**: Vistas HTML con Jinja2.
- **requirements.txt**: Dependencias Python.
- **package.json**: Dependencias npm (Tailwind).

## Uso
- **Registro por ID**: Accede a /login e ingresa un ID único.
- **Dashboards**: Dependiendo del rol, verás historiales y reportes.
- **Expansión**: Futura integración de huellas con pyfingerprint (o alternativas como pyzk).

Para más detalles, consulta el plan de desarrollo en el repositorio.

## Contribuyendo
1. Forkea el repositorio.
2. Crea una branch: `git checkout -b feature/nueva-funcionalidad`.
3. Commit tus cambios: `git commit -m 'Agrega nueva funcionalidad'`.
4. Push: `git push origin feature/nueva-funcionalidad`.
5. Abre un Pull Request.

Sigue los principios SOLID y tests con pytest.

## Licencia
Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para detalles.

Si encuentras problemas, abre un issue o contacta al maintainer.
