# Cómo Agregar el Campo Costo al Historial de Movimientos

## 📋 Resumen

Hemos agregado el campo **Costo** (standard_price) al historial de movimientos de inventario en Odoo.

## 🎯 ¿Qué se hizo?

### 1. **Backend (Python)** - Modelos extendidos

#### `models/stock_move.py`
- **Campo `product_cost`**: Muestra el costo unitario del producto
- **Campo `total_cost`**: Calcula el costo total (cantidad × costo unitario)
- **Campo `company_currency_id`**: Para mostrar la moneda correcta

#### `models/product_template.py`
- Métodos auxiliares para trabajar con costos
- Acceso al historial de costos
- Logging de información de costos

### 2. **Frontend (XML)** - Vistas extendidas

#### `views/stock_move_views.xml`
Extiende las siguientes vistas:
- **Vista de árbol (lista)**: Agrega columnas de Costo Unit. y Costo Total
- **Vista de formulario**: Muestra información de costo en el detalle
- **Vista de búsqueda**: Agrega filtros por rangos de costo

## 🚀 Cómo Actualizar el Módulo

### Opción 1: Desde la Interfaz de Odoo (Recomendado)

1. Ir a **Aplicaciones** (Apps)
2. Buscar "Inventory Cardex"
3. Click en **Actualizar** (Upgrade)

### Opción 2: Desde la Línea de Comandos

```bash
# Reiniciar Odoo con actualización del módulo
docker-compose restart

# O actualizar específicamente el módulo
docker exec -it odoo-web-1 odoo -u inventory_cardex -d inventario --stop-after-init
docker-compose restart
```

### Opción 3: Modo Desarrollo (Más rápido)

1. Activar **Modo Desarrollador**:
   - Ir a Configuración → Activar modo desarrollador

2. Ir a **Aplicaciones**

3. Click en el menú (☰) → **Actualizar lista de aplicaciones**

4. Buscar "Inventory Cardex" y hacer click en **Actualizar**

## 📊 Campos Agregados

| Campo | Nombre Técnico | Tipo | Descripción |
|-------|---------------|------|-------------|
| **Costo Unit.** | `product_cost` | Float/Monetary | Costo estándar del producto |
| **Costo Total** | `total_cost` | Monetary | Cantidad × Costo unitario |

## 🔍 Dónde Verás los Cambios

### Historial de Movimientos
**Ruta**: Inventario → Operaciones → Historial de Movimientos

Verás dos nuevas columnas:
- **Costo Unit.**: Visible por defecto
- **Costo Total**: Oculta por defecto (puedes activarla)

### Filtros Nuevos
- Costo Alto (>100)
- Costo Medio (10-100)
- Costo Bajo (<10)

## ⚠️ Importante: ¿Por qué NO se puede hacer solo con JavaScript?

**No es posible agregar este campo solo con JavaScript** porque:

1. **El campo `standard_price` NO existe en `stock.move`**
   - Está en el modelo `product.product`
   - Necesitas una relación entre modelos

2. **Necesitas cálculos del lado del servidor**
   - El costo total requiere multiplicar cantidad × costo
   - Estos cálculos deben ser consistentes y seguros

3. **JavaScript solo modifica la presentación**
   - No puede crear campos nuevos en la base de datos
   - No puede acceder a relaciones entre modelos

4. **Seguridad y permisos**
   - Los campos deben respetar los permisos de acceso
   - JavaScript no puede garantizar esto

## 🔧 Estructura del Módulo

```
inventory_cardex/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── product_template.py  ← NUEVO
│   ├── stock_move.py         ← NUEVO
│   └── order.py
└── views/
    ├── stock_picking_views.xml
    └── stock_move_views.xml  ← NUEVO
```

## 📝 Notas Técnicas

### ¿Dónde está `standard_price` en la base de datos?

En Odoo 17, el campo `standard_price` se almacena en:

1. **Tabla `product_product`** (variantes de producto)
   - Campo directo en versiones antiguas
   - Campo computado en versiones nuevas

2. **Tabla `stock_valuation_layer`** (capas de valoración)
   - Historial de cambios de costo
   - Usado en valoración automática

### Acceso desde SQL

```sql
-- Ver el costo de un producto
SELECT 
    pp.id,
    pt.name->>'en_US' as product_name,
    pp.default_code,
    pp.standard_price as cost
FROM product_product pp
JOIN product_template pt ON pp.product_tmpl_id = pt.id
WHERE pt.id = 1;

-- Ver movimientos con costo
SELECT 
    sm.id,
    sm.name,
    sm.product_qty,
    pp.standard_price as unit_cost,
    (sm.product_qty * pp.standard_price) as total_cost
FROM stock_move sm
JOIN product_product pp ON sm.product_id = pp.id
WHERE sm.state = 'done'
ORDER BY sm.date DESC
LIMIT 10;
```

## 🎨 Personalización Adicional

Si quieres personalizar más, puedes:

1. **Cambiar el formato de moneda**
   - Editar el widget en `stock_move_views.xml`

2. **Agregar más campos calculados**
   - Editar `models/stock_move.py`

3. **Modificar los filtros**
   - Editar la vista de búsqueda en `stock_move_views.xml`

## ✅ Verificación

Después de actualizar, verifica:

1. ✓ El módulo se actualizó sin errores
2. ✓ La columna "Costo Unit." aparece en el historial
3. ✓ Los valores de costo son correctos
4. ✓ Los filtros funcionan

## 🐛 Solución de Problemas

### Error: "Campo no encontrado"
- Asegúrate de actualizar el módulo
- Reinicia Odoo después de actualizar

### Los costos aparecen en 0
- Verifica que los productos tengan costo configurado
- Ve a Inventario → Productos → [Producto] → Pestaña "Inventario" → Campo "Costo"

### La vista no se actualiza
- Limpia la caché del navegador
- Actualiza la página con Ctrl+F5
- Desactiva y reactiva el modo desarrollador

---

**Autor**: Antigravity AI  
**Fecha**: 2025-11-24  
**Módulo**: inventory_cardex v1.0
