# Script alternativo para actualizar el módulo inventory_cardex
# Este script reinicia el contenedor para que Odoo detecte los cambios

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Actualizando módulo inventory_cardex" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Reiniciando contenedor de Odoo..." -ForegroundColor Yellow
docker restart odoo-web-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Contenedor reiniciado" -ForegroundColor Green
} else {
    Write-Host "✗ Error al reiniciar el contenedor" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/2] Esperando que Odoo esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "✓ Contenedor reiniciado" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANTE: Ahora debes actualizar el módulo desde la interfaz web:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Accede a Odoo en: http://localhost:8070" -ForegroundColor Cyan
Write-Host "2. Ve a: Aplicaciones" -ForegroundColor Cyan
Write-Host "3. Busca: inventory_cardex" -ForegroundColor Cyan
Write-Host "4. Haz clic en: Actualizar" -ForegroundColor Cyan
Write-Host ""
Write-Host "O usa el modo desarrollador:" -ForegroundColor Yellow
Write-Host "1. Activa el modo desarrollador: Configuración → Activar modo desarrollador" -ForegroundColor Cyan
Write-Host "2. Ve a: Aplicaciones → Actualizar lista de aplicaciones" -ForegroundColor Cyan
Write-Host "3. Busca 'inventory_cardex' y haz clic en Actualizar" -ForegroundColor Cyan
Write-Host ""
