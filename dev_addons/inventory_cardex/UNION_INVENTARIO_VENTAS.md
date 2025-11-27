# 🔗 Unión de Datos de Inventario y Ventas

## 📋 Resumen

Se han agregado **campos de venta** (`sale_order_line`) a la vista de **Movimientos Detallados (Cardex)** en `stock_move_line`. Ahora puedes ver tanto la información de inventario como la información de ventas en una sola vista.

## 🎯 Campos Agregados

### Campos de Venta Disponibles

| Campo Técnico | Nombre en Vista | Descripción |
|---------------|-----------------|-------------|
| `has_sale` | Tiene Venta | Indica si el movimiento está relacionado con una venta |
| `sale_order_id` | Pedido Venta | Número del pedido de venta |
| `sale_product_name` | Descripción Venta | Descripción del producto en la venta |
| `sale_product_uom_qty` | Cantidad Vendida | Cantidad en el pedido de venta |
| `sale_price_unit` | Precio Unit. Venta | Precio unitario de venta |
| `sale_price_subtotal` | Subtotal Venta | Subtotal sin impuestos |
| `sale_price_tax` | Impuestos Venta | Monto de impuestos |
| `sale_price_total` | Total Venta | Total con impuestos |
| `sale_state` | Estado Venta | Estado del pedido de venta |

### Campos de Inventario (Existentes)

| Campo Técnico | Nombre en Vista | Descripción |
|---------------|-----------------|-------------|
| `date` | Fecha | Fecha del movimiento |
| `reference` | Referencia | Referencia del movimiento |
| `location_id` | Desde | Ubicación de origen |
| `location_dest_id` | A | Ubicación de destino |
| `product_id` | Producto | Producto |
| `quantity` | Cantidad | Cantidad movida |
| `product_cost` | Costo Unitario | Costo unitario del producto |
| `line_cost` | Costo Total | Costo total del movimiento |
| `state` | Estado | Estado del movimiento |

## 🔗 Cómo Funciona la Relación

La relación entre `stock_move_line` y `sale_order_line` se establece a través de:

```
stock_move_line → move_id → sale_line_id → sale_order_line
```

### Diagrama de Relación

```
┌─────────────────┐
│ sale.order      │ (Pedido de Venta)
│ - name          │
│ - partner_id    │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────────┐
│ sale.order.line     │ (Línea de Pedido)
│ - name              │
│ - product_uom_qty   │
│ - price_unit        │
│ - price_subtotal    │
│ - price_tax         │
│ - price_total       │
└────────┬────────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│ stock.move      │ (Movimiento de Stock)
│ - sale_line_id  │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────────┐
│ stock.move.line     │ (Movimiento Detallado)
│ - move_id           │
│ - sale_line_id ⭐   │ (Campo relacionado)
│ - quantity          │
│ - product_cost      │
└─────────────────────┘
```

## 📊 Vista Combinada

### Ubicación de la Vista

**Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**

### Columnas Visibles por Defecto

#### Inventario (Siempre Visibles)
- Fecha
- Referencia
- Desde
- A
- Producto
- Cantidad
- Costo Unitario
- Costo Total
- Estado

#### Ventas (Opcionales - Ocultas por Defecto)
- Tiene Venta
- Pedido Venta
- Descripción Venta
- Cantidad Vendida
- Precio Unit. Venta
- Subtotal Venta
- Impuestos Venta
- Total Venta
- Estado Venta

### Cómo Mostrar las Columnas de Venta

1. Ve a **Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**
2. Haz clic en el icono de **columnas** (⚙️) en la esquina superior derecha
3. Marca las columnas de venta que quieras ver:
   - ☑️ Pedido Venta
   - ☑️ Precio Unit. Venta
   - ☑️ Subtotal Venta
   - ☑️ Total Venta
   - etc.

## 🔍 Casos de Uso

### Caso 1: Ver Movimientos con Información de Venta

**Objetivo**: Ver qué productos se movieron y a qué precio se vendieron.

**Pasos**:
1. Ve a **Movimientos Detallados (Cardex)**
2. Activa las columnas:
   - Pedido Venta
   - Precio Unit. Venta
   - Total Venta
3. Filtra por `Tiene Venta = Sí` (si quieres ver solo movimientos relacionados con ventas)

### Caso 2: Comparar Costo vs Precio de Venta

**Objetivo**: Analizar el margen de ganancia.

**Pasos**:
1. Ve a **Movimientos Detallados (Cardex)**
2. Activa las columnas:
   - Producto
   - Cantidad
   - Costo Unitario (inventario)
   - Precio Unit. Venta (venta)
   - Costo Total (inventario)
   - Total Venta (venta)
3. Compara los valores para calcular el margen

### Caso 3: Rastrear Pedidos de Venta

**Objetivo**: Ver qué movimientos de stock están asociados a un pedido específico.

**Pasos**:
1. Ve a **Movimientos Detallados (Cardex)**
2. Activa la columna **Pedido Venta**
3. Busca o filtra por el número de pedido

## 📝 Consulta SQL Equivalente

La vista muestra datos equivalentes a esta consulta SQL:

```sql
SELECT 
    -- Campos de inventario
    sml.date,
    sml.reference,
    loc_from.complete_name AS location_id,
    loc_to.complete_name AS location_dest_id,
    pp.name_template AS product_id,
    sml.quantity,
    sm.product_cost,
    (sml.quantity * sm.product_cost) AS line_cost,
    sml.state,
    
    -- Campos de venta
    so.name AS sale_order_id,
    sol.name AS sale_product_name,
    sol.product_uom_qty AS sale_product_uom_qty,
    sol.price_unit AS sale_price_unit,
    sol.price_subtotal AS sale_price_subtotal,
    sol.price_tax AS sale_price_tax,
    sol.price_total AS sale_price_total,
    sol.state AS sale_state,
    
    -- Indicador
    CASE WHEN sol.id IS NOT NULL THEN TRUE ELSE FALSE END AS has_sale

FROM stock_move_line sml
LEFT JOIN stock_move sm ON sml.move_id = sm.id
LEFT JOIN sale_order_line sol ON sm.sale_line_id = sol.id
LEFT JOIN sale_order so ON sol.order_id = so.id
LEFT JOIN product_product pp ON sml.product_id = pp.id
LEFT JOIN stock_location loc_from ON sml.location_id = loc_from.id
LEFT JOIN stock_location loc_to ON sml.location_dest_id = loc_to.id

ORDER BY sml.date DESC;
```

## ⚠️ Notas Importantes

### 1. No Todos los Movimientos Tienen Venta

- Los movimientos de inventario pueden ser por **transferencias internas**, **ajustes**, **recepciones de compra**, etc.
- Solo los movimientos relacionados con **entregas de pedidos de venta** tendrán datos en los campos de venta
- Usa el campo **Tiene Venta** para filtrar solo movimientos con venta

### 2. Campos Relacionados

- Los campos de venta son **campos relacionados** (`related` fields)
- Se calculan automáticamente basándose en la relación con `sale_order_line`
- Son de **solo lectura**

### 3. Rendimiento

- Los campos están marcados con `store=True` para mejorar el rendimiento
- Los datos se almacenan en la base de datos
- Se actualizan automáticamente cuando cambia la venta relacionada

## 🚀 Actualización del Módulo

Para aplicar estos cambios:

### Opción 1: Desde la Interfaz Web (Recomendado)

```powershell
# 1. Reiniciar el contenedor
docker restart odoo-web-1

# 2. Esperar 15 segundos
Start-Sleep -Seconds 15
```

Luego:
1. Accede a Odoo: http://localhost:8070
2. Activa el modo desarrollador
3. Ve a **Aplicaciones**
4. Busca `inventory_cardex`
5. Haz clic en **Actualizar**

### Opción 2: Script Rápido

```powershell
cd c:\Mis-Documentos\Appex\odoo\dev_addons\inventory_cardex
.\reiniciar_odoo.ps1
```

## 📊 Ejemplo de Datos

### Movimiento CON Venta

| Fecha | Producto | Cantidad | Costo Unit. | Total Costo | Pedido Venta | Precio Unit. Venta | Total Venta |
|-------|----------|----------|-------------|-------------|--------------|-------------------|-------------|
| 2025-11-27 | Laptop Dell | 5 | $800 | $4,000 | SO001 | $1,200 | $6,000 |

**Margen**: $6,000 - $4,000 = **$2,000** (33% de ganancia)

### Movimiento SIN Venta

| Fecha | Producto | Cantidad | Costo Unit. | Total Costo | Pedido Venta | Precio Unit. Venta | Total Venta |
|-------|----------|----------|-------------|-------------|--------------|-------------------|-------------|
| 2025-11-27 | Mouse USB | 10 | $5 | $50 | - | - | - |

Este es un movimiento interno (transferencia entre almacenes), no tiene venta asociada.

## 🔧 Personalización Futura

Si necesitas agregar más campos:

1. **Edita**: `models/stock_move_line.py`
2. **Agrega campos relacionados** usando `related='sale_line_id.campo'`
3. **Actualiza la vista**: `views/stock_move_views.xml`
4. **Actualiza el reporte**: `models/stock_move_line_report.py`

### Ejemplo: Agregar Cliente

```python
# En stock_move_line.py
sale_partner_id = fields.Many2one(
    'res.partner',
    string='Cliente',
    related='sale_order_id.partner_id',
    readonly=True,
    store=True
)
```

```xml
<!-- En stock_move_views.xml -->
<field name="sale_partner_id" string="Cliente" optional="hide"/>
```

## 📞 Información de Conexión

- **URL Odoo**: http://localhost:8070
- **Base de Datos**: inventario
- **Usuario Maestro**: 123456

## ✅ Checklist de Verificación

- [ ] Módulo actualizado
- [ ] Vista muestra campos de inventario
- [ ] Columnas de venta disponibles (ocultas por defecto)
- [ ] Campos de venta se pueden activar desde el menú de columnas
- [ ] Datos de venta aparecen solo en movimientos relacionados con ventas
- [ ] Campo "Tiene Venta" funciona correctamente

---

**Fecha de creación**: 2025-11-27
**Versión**: 1.1
**Autor**: Inventory Cardex Module
