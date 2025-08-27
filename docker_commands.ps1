# Script de comandos útiles para Docker - ClockIn
param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "ClockIn - Comandos de Docker" -ForegroundColor Cyan
    Write-Host "=" * 50
    Write-Host ""
    Write-Host "Comandos disponibles:" -ForegroundColor Yellow
    Write-Host "  build     - Construir y ejecutar la aplicacion"
    Write-Host "  start     - Iniciar la aplicacion"
    Write-Host "  stop      - Detener la aplicacion"
    Write-Host "  restart   - Reiniciar la aplicacion"
    Write-Host "  logs      - Ver logs en tiempo real"
    Write-Host "  status    - Ver estado de los contenedores"
    Write-Host "  clean     - Limpiar contenedores e imagenes"
    Write-Host "  test      - Ejecutar pruebas de configuracion"
    Write-Host "  help      - Mostrar esta ayuda"
    Write-Host ""
    Write-Host "Ejemplo: .\docker_commands.ps1 build" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs de acceso:" -ForegroundColor Cyan
    Write-Host "  - Aplicacion: http://localhost:5000" -ForegroundColor White
    Write-Host "  - Admin: http://localhost:5000/admin/dashboard" -ForegroundColor White
    Write-Host "  - Usuarios: http://localhost:5000/admin/users" -ForegroundColor White
    Write-Host "  - Login: http://localhost:5000/auth/login" -ForegroundColor White
}

function Start-DockerBuild {
    Write-Host "Construyendo y ejecutando ClockIn..." -ForegroundColor Yellow
    docker-compose up --build
}

function Start-DockerApp {
    Write-Host "Iniciando ClockIn..." -ForegroundColor Yellow
    docker-compose up -d
}

function Stop-DockerApp {
    Write-Host "Deteniendo ClockIn..." -ForegroundColor Yellow
    docker-compose down
}

function Restart-DockerApp {
    Write-Host "Reiniciando ClockIn..." -ForegroundColor Yellow
    docker-compose down
    docker-compose up -d
}

function Show-DockerLogs {
    Write-Host "Mostrando logs de ClockIn..." -ForegroundColor Yellow
    docker-compose logs -f
}

function Show-DockerStatus {
    Write-Host "Estado de los contenedores:" -ForegroundColor Yellow
    docker-compose ps
}

function Clear-DockerData {
    Write-Host "Limpiando contenedores e imagenes..." -ForegroundColor Yellow
    docker-compose down --volumes --remove-orphans
    docker system prune -f
    Write-Host "Limpieza completada" -ForegroundColor Green
}

function Test-DockerConfig {
    Write-Host "Ejecutando pruebas de configuracion..." -ForegroundColor Yellow
    python test_docker_setup.py
}

# Ejecutar comando según parámetro
switch ($Command.ToLower()) {
    "build" { Start-DockerBuild }
    "start" { Start-DockerApp }
    "stop" { Stop-DockerApp }
    "restart" { Restart-DockerApp }
    "logs" { Show-DockerLogs }
    "status" { Show-DockerStatus }
    "clean" { Clear-DockerData }
    "test" { Test-DockerConfig }
    default { Show-Help }
}
