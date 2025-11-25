# 🔄 Cómo Actualizar el Módulo para Ver el Campo de Costo

## ✅ El campo de costo YA está implementado

Tu módulo `inventory_cardex` ya tiene el campo de costo (`standard_price`) configurado. Solo necesitas actualizar el módulo en Odoo para que aparezca.

## 🚀 Método 1: Actualizar desde la Interfaz (Más Fácil)

### Paso 1: Activar Modo Desarrollador
1. Abre Odoo en tu navegador: http://localhost:8070
2. Ve a **Configuración** (Settings)
3. Baja hasta el final de la página
4. Haz clic en **"Activar el modo de desarrollador"** (Activate the developer mode)

### Paso 2: Actualizar el Módulo
1. Ve a **Aplicaciones** (Apps) en el menú principal
2. En el buscador, escribe: `inventory_cardex`
3. Encuentra el módulo **"Inventory Cardex"**
4. Haz clic en el botón **"Actualizar"** (Upgrade)
5. Confirma la actualización

### Paso 3: Verificar
1. Ve a: **Inventario → Operaciones → Historial de Movimientos**
   - Ruta en inglés: **Inventory → Operations → History of Movements**
2. Deberías ver la columna **"Costo Unit."** después de la columna "Producto"
3. Si no la ves, haz clic en el icono de columnas (☰) y activa "Costo Unit."

## 🔧 Método 2: Actualizar desde la Línea de Comandos

Si prefieres usar la terminal:

```bash
# Opción A: Reiniciar Odoo (más simple)
docker-compose restart

# Opción B: Actualizar específicamente el módulo (más preciso)
docker exec -it odoo-web-1 odoo -u inventory_cardex -d inventario --stop-after-init
docker-compose restart
```

## 📊 ¿Qué verás después de actualizar?

### En el Historial de Movimientos:
- **Columna "Costo Unit."**: Muestra el costo estándar del producto
- **Columna "Costo Total"**: Muestra cantidad × costo (oculta por defecto)

### Filtros disponibles:
- Costo Alto (>100)
- Costo Medio (10-100)
- Costo Bajo (<10)

## 🐛 Solución de Problemas

### El módulo no aparece en Aplicaciones
1. Ve a **Aplicaciones**
2. Haz clic en el menú (☰) → **"Actualizar lista de aplicaciones"**
3. Busca nuevamente "Inventory Cardex"

### Los costos aparecen en 0
1. Ve a **Inventario → Productos**
2. Abre un producto
3. Ve a la pestaña **"Inventario"**
4. Verifica que el campo **"Costo"** tenga un valor

### La columna no aparece
1. Limpia la caché del navegador (Ctrl+Shift+Del)
2. Recarga la página (Ctrl+F5)
3. Verifica que el módulo esté actualizado

## 📝 Archivos del Módulo

El campo de costo está implementado en:
- **Backend**: `models/stock_move.py` (campos `product_cost` y `total_cost`)
- **Frontend**: `views/stock_move_views.xml` (vistas extendidas)

## ✨ Características Implementadas

✅ Campo de costo unitario (`standard_price`)  
✅ Campo de costo total (cantidad × costo)  
✅ Visible en todas las vistas de movimientos  
✅ Filtros por rango de costo  
✅ Formato de moneda automático  

---

**Última actualización**: 2025-11-24  
**Versión del módulo**: 1.0
