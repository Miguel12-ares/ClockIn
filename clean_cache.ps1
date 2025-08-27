# Script para limpiar archivos de caché de Python
Write-Host "Limpiando archivos de cache de Python..." -ForegroundColor Yellow

# Buscar y eliminar directorios __pycache__
$pycacheDirs = Get-ChildItem -Path . -Name "__pycache__" -Recurse -Directory
if ($pycacheDirs) {
    foreach ($dir in $pycacheDirs) {
        $fullPath = Join-Path (Get-Location) $dir
        Write-Host "Eliminando: $fullPath" -ForegroundColor Red
        Remove-Item -Path $fullPath -Recurse -Force
    }
    Write-Host "Directorios __pycache__ eliminados" -ForegroundColor Green
} else {
    Write-Host "No se encontraron directorios __pycache__" -ForegroundColor Blue
}

# Buscar y eliminar archivos .pyc
$pycFiles = Get-ChildItem -Path . -Name "*.pyc" -Recurse
if ($pycFiles) {
    foreach ($file in $pycFiles) {
        $fullPath = Join-Path (Get-Location) $file
        Write-Host "Eliminando: $fullPath" -ForegroundColor Red
        Remove-Item -Path $fullPath -Force
    }
    Write-Host "Archivos .pyc eliminados" -ForegroundColor Green
} else {
    Write-Host "No se encontraron archivos .pyc" -ForegroundColor Blue
}

# Buscar y eliminar archivos .pyo
$pyoFiles = Get-ChildItem -Path . -Name "*.pyo" -Recurse
if ($pyoFiles) {
    foreach ($file in $pyoFiles) {
        $fullPath = Join-Path (Get-Location) $file
        Write-Host "Eliminando: $fullPath" -ForegroundColor Red
        Remove-Item -Path $fullPath -Force
    }
    Write-Host "Archivos .pyo eliminados" -ForegroundColor Green
} else {
    Write-Host "No se encontraron archivos .pyo" -ForegroundColor Blue
}

Write-Host "Limpieza completada!" -ForegroundColor Green
Write-Host "Ahora puedes ejecutar: docker-compose up --build" -ForegroundColor Cyan
