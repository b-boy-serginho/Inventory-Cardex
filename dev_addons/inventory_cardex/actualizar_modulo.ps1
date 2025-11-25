# Script para actualizar el módulo inventory_cardex en Odoo
# Ejecutar desde: c:\Mis-Documentos\Appex\odoo

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Actualizando módulo inventory_cardex" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Opción 1: Actualizar el módulo sin detener Odoo
Write-Host "[1/3] Actualizando módulo..." -ForegroundColor Yellow
docker exec -it odoo-web-1 odoo -u inventory_cardex -d inventario --stop-after-init

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Módulo actualizado correctamente" -ForegroundColor Green
} else {
    Write-Host "✗ Error al actualizar el módulo" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/3] Reiniciando contenedor de Odoo..." -ForegroundColor Yellow
docker restart odoo-web-1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Contenedor reiniciado" -ForegroundColor Green
} else {
    Write-Host "✗ Error al reiniciar el contenedor" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[3/3] Esperando que Odoo esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "✓ Actualización completada" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Accede a Odoo en: http://localhost:8069" -ForegroundColor Cyan
Write-Host "Ve a: Inventario → Operaciones → Historial de Movimientos" -ForegroundColor Cyan
Write-Host "Deberías ver la nueva columna 'Costo Unit.'" -ForegroundColor Cyan
Write-Host ""
