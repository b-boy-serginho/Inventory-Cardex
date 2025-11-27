# 🚀 CAMBIOS REALIZADOS - Unión Inventario + Ventas

## ✅ Archivos Modificados

### 1. `models/stock_move_line.py`
**Cambios**: Agregados 11 campos relacionados con `sale_order_line`

**Campos agregados**:
- `sale_line_id` - Relación con la línea de venta
- `sale_order_id` - Pedido de venta
- `sale_product_name` - Descripción del producto en la venta
- `sale_product_uom_qty` - Cantidad vendida
- `sale_price_unit` - Precio unitario de venta
- `sale_price_subtotal` - Subtotal sin impuestos
- `sale_price_tax` - Impuestos
- `sale_price_total` - Total con impuestos
- `sale_currency_id` - Moneda de la venta
- `sale_state` - Estado de la venta
- `has_sale` - Indicador booleano (tiene venta o no)

### 2. `views/stock_move_views.xml`
**Cambios**: Agregadas columnas de venta a la vista de árbol

**Columnas agregadas** (todas opcionales, ocultas por defecto):
- Tiene Venta
- Pedido Venta
- Descripción Venta
- Cantidad Vendida
- Precio Unit. Venta
- Subtotal Venta
- Impuestos Venta
- Total Venta
- Estado Venta

### 3. `models/stock_move_line_report.py`
**Cambios**: Agregados campos de venta al mapeo de `field_labels`

Esto permite que los campos de venta aparezcan en los reportes PDF dinámicos.

## 📁 Archivos Creados

### `UNION_INVENTARIO_VENTAS.md`
Documentación completa con:
- Explicación de la relación entre modelos
- Diagrama de relaciones
- Casos de uso
- Consulta SQL equivalente
- Ejemplos prácticos

## 🎯 Resultado Final

### Vista: Inventario → Reportes → Movimientos Detallados (Cardex)

**Columnas Visibles por Defecto** (Inventario):
```
┌──────────┬────────────┬────────┬─────┬──────────┬──────────┬──────────────┬─────────────┬────────┐
│  Fecha   │ Referencia │ Desde  │  A  │ Producto │ Cantidad │ Costo Unit.  │ Costo Total │ Estado │
├──────────┼────────────┼────────┼─────┼──────────┼──────────┼──────────────┼─────────────┼────────┤
│ 27/11/25 │ WH/OUT/001 │ Stock  │ Cli │ Laptop   │    5     │    $800      │   $4,000    │ Hecho  │
└──────────┴────────────┴────────┴─────┴──────────┴──────────┴──────────────┴─────────────┴────────┘
```

**Columnas Opcionales** (Ventas - Activar manualmente):
```
┌──────────────┬────────────────────┬──────────────────┬─────────────┬──────────────┬─────────────┐
│ Pedido Venta │ Descripción Venta  │ Cantidad Vendida │ Precio Unit │ Subtotal     │ Total Venta │
├──────────────┼────────────────────┼──────────────────┼─────────────┼──────────────┼─────────────┤
│   SO001      │ Dell Laptop XPS 15 │        5         │   $1,200    │   $6,000     │   $6,000    │
└──────────────┴────────────────────┴──────────────────┴─────────────┴──────────────┴─────────────┘
```

## 🔗 Relación de Datos

```
stock_move_line.move_id → stock_move.sale_line_id → sale_order_line
```

**Ejemplo**:
- Un cliente hace un pedido de venta (SO001) por 5 laptops a $1,200 c/u
- Odoo crea automáticamente un movimiento de stock para entregar las laptops
- El movimiento de stock tiene:
  - **Costo**: $800 x 5 = $4,000 (datos de inventario)
  - **Venta**: $1,200 x 5 = $6,000 (datos de venta)
  - **Margen**: $2,000 (33% de ganancia)

## 📊 Comparación: Antes vs Después

### ANTES
Solo podías ver datos de inventario:
- ✅ Fecha, Producto, Cantidad
- ✅ Costo Unitario, Costo Total
- ❌ NO podías ver precio de venta
- ❌ NO podías ver pedido relacionado
- ❌ NO podías calcular margen fácilmente

### DESPUÉS
Ahora puedes ver TODO en una sola vista:
- ✅ Fecha, Producto, Cantidad
- ✅ Costo Unitario, Costo Total
- ✅ Precio de Venta, Subtotal, Impuestos, Total
- ✅ Pedido de venta relacionado
- ✅ Puedes calcular margen fácilmente
- ✅ Puedes comparar costo vs precio

## 🚀 Próximos Pasos

### 1. Reiniciar Odoo
```powershell
docker restart odoo-web-1
Start-Sleep -Seconds 15
```

### 2. Actualizar el Módulo
1. Accede a http://localhost:8070
2. Usuario: `123456`, Base de datos: `inventario`
3. Activa modo desarrollador
4. Ve a **Aplicaciones**
5. Busca `inventory_cardex`
6. Haz clic en **Actualizar**

### 3. Verificar los Cambios
1. Ve a **Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**
2. Haz clic en el icono de columnas (⚙️)
3. Activa las columnas de venta:
   - ☑️ Pedido Venta
   - ☑️ Precio Unit. Venta
   - ☑️ Total Venta

### 4. Crear Datos de Prueba (si no tienes)
Si no ves datos en las columnas de venta:

1. **Crear un pedido de venta**:
   - Ve a **Ventas** → **Pedidos** → **Crear**
   - Agrega un cliente
   - Agrega productos
   - Confirma el pedido

2. **Validar la entrega**:
   - Ve a **Inventario** → **Operaciones** → **Entregas**
   - Busca la entrega del pedido
   - Haz clic en **Validar**

3. **Ver el resultado**:
   - Ve a **Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**
   - Activa las columnas de venta
   - Deberías ver los datos de venta en el movimiento

## 🎨 Ejemplo Visual

### Movimiento CON Venta Asociada
```
Fecha: 27/11/2025
Producto: Laptop Dell XPS 15
Cantidad: 5

INVENTARIO:
  Costo Unitario: $800
  Costo Total: $4,000

VENTA:
  Pedido: SO001
  Precio Unit. Venta: $1,200
  Total Venta: $6,000

MARGEN: $2,000 (33%)
```

### Movimiento SIN Venta Asociada
```
Fecha: 27/11/2025
Producto: Mouse USB
Cantidad: 10

INVENTARIO:
  Costo Unitario: $5
  Costo Total: $50

VENTA:
  (Sin datos - es una transferencia interna)
```

## 📝 Notas Importantes

1. **No todos los movimientos tienen venta**
   - Solo las entregas de pedidos de venta tendrán datos
   - Transferencias internas, ajustes, recepciones NO tienen venta

2. **Campos opcionales**
   - Los campos de venta están ocultos por defecto
   - Actívalos según necesites desde el menú de columnas

3. **Rendimiento**
   - Los campos están almacenados (`store=True`)
   - No afecta el rendimiento de la vista

4. **Solo lectura**
   - Los campos de venta son de solo lectura
   - Se actualizan automáticamente desde el pedido de venta

## 📚 Documentación

Lee `UNION_INVENTARIO_VENTAS.md` para:
- Explicación detallada de la relación
- Diagramas de base de datos
- Casos de uso completos
- Consultas SQL equivalentes
- Guía de personalización

---

**Fecha**: 2025-11-27
**Versión**: 1.1
**Estado**: ✅ Código listo, ⏳ Pendiente actualización en Odoo
