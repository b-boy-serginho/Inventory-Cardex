# 🚀 PASOS PARA VER EL CAMPO COSTO

## ✅ Lo que hemos hecho:

1. ✅ Creado el modelo extendido `stock_move.py` con los campos:
   - `product_cost` (Costo unitario)
   - `total_cost` (Costo total)
   - `company_currency_id` (Moneda)

2. ✅ Creado las vistas XML en `stock_move_views.xml`

3. ✅ Agregado JavaScript de debug para verificar si los campos existen

4. ✅ Corregido errores de sintaxis XML (escapado de `<` y `>`)

## 🎯 LO QUE DEBES HACER AHORA:

### Paso 1: Reiniciar Odoo (ya hecho)
```bash
docker-compose restart web
```

### Paso 2: ACTUALIZAR EL MÓDULO desde la interfaz de Odoo

**IMPORTANTE**: Solo reiniciar NO es suficiente. Debes actualizar el módulo.

#### Opción A: Actualizar desde la Interfaz (RECOMENDADO)

1. Abre Odoo en tu navegador: `http://localhost:8069` o `http://localhost:8070`

2. **Activa el Modo Desarrollador**:
   - Ve a Configuración (Settings)
   - Scroll hasta abajo
   - Click en "Activar el modo de desarrollador"
   - O usa: `http://localhost:8069/web?debug=1`

3. **Actualiza la Lista de Aplicaciones**:
   - Ve al menú Apps (Aplicaciones)
   - Click en el menú ⋮ (tres puntos verticales)
   - Selecciona "Update Apps List" (Actualizar lista de aplicaciones)
   - Click "Update" en el diálogo

4. **Actualiza el Módulo**:
   - Busca "Inventory Cardex" en Apps
   - Click en "Upgrade" (Actualizar)
   - Espera a que termine

5. **Verifica**:
   - Ve a Inventario → Operaciones → Historial de Movimientos
   - Deberías ver la columna "Costo Unit."

#### Opción B: Actualizar desde Docker (Alternativa)

```bash
# Detener Odoo
docker-compose stop web

# Actualizar el módulo
docker-compose run --rm web odoo -u inventory_cardex -d inventario --stop-after-init

# Iniciar Odoo
docker-compose start web
```

### Paso 3: Verificar con JavaScript Debug

1. Abre la consola del navegador (F12)
2. Ve a la pestaña "Console"
3. Navega a: Inventario → Operaciones → Historial de Movimientos
4. En la consola verás un mensaje como:

```
================================================================================
🔍 DEBUG: Stock Move List View
================================================================================
📋 Modelo: stock.move

🔎 Verificando campos disponibles en stock.move...

🎯 Verificando campos personalizados:
  ✅ product_cost: EXISTE
     Tipo: float
     String: Costo Unit.
  ✅ total_cost: EXISTE
     Tipo: monetary
     String: Costo Total
  ✅ company_currency_id: EXISTE
     Tipo: many2one
     String: Moneda de la Compañía
```

### Paso 4: Interpretar los Resultados

**Si ves "❌ product_cost: NO EXISTE"**:
- El módulo NO se actualizó correctamente
- Vuelve al Paso 2 y actualiza el módulo
- Verifica que no haya errores en los logs

**Si ves "✅ product_cost: EXISTE" pero no ves la columna**:
- El campo existe pero la vista no se actualizó
- Limpia la caché del navegador (Ctrl + Shift + Delete)
- Recarga la página con Ctrl + F5
- Verifica las columnas opcionales (icono ⋮ en la lista)

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
# Verifica que los archivos estén en el lugar correcto
docker exec odoo-web-1 ls -la /mnt/extra-addons/inventory_cardex/models/
docker exec odoo-web-1 ls -la /mnt/extra-addons/inventory_cardex/views/
```

### Error: "Field does not exist"
```bash
# Ver logs de Odoo
docker logs odoo-web-1 --tail 100

# Buscar errores específicos
docker logs odoo-web-1 2>&1 | grep -i error
```

### El campo aparece pero sin valores
- Verifica que los productos tengan costo configurado
- Ve a Inventario → Productos → [Producto] → Pestaña "Inventario" → Campo "Costo"

## 📋 Checklist Final

- [ ] Modo desarrollador activado
- [ ] Lista de aplicaciones actualizada
- [ ] Módulo "Inventory Cardex" actualizado (no solo reiniciado)
- [ ] Consola del navegador abierta (F12)
- [ ] Navegado a "Historial de Movimientos"
- [ ] Mensaje de debug visible en la consola
- [ ] Campo `product_cost` existe según el debug
- [ ] Columna "Costo Unit." visible en la lista

## 🎬 Siguiente Paso

**Actualiza el módulo desde la interfaz de Odoo** (Paso 2, Opción A) y luego revisa la consola del navegador para ver el debug.

¡Comparte el resultado del debug en la consola!
