# ⚡ INSTRUCCIONES RÁPIDAS - Unión Inventario + Ventas

## 🎯 ¿Qué se hizo?

Se agregaron **campos de venta** a la vista de **Movimientos Detallados (Cardex)**.

Ahora puedes ver en UNA SOLA VISTA:
- ✅ Datos de inventario (costo, cantidad, ubicaciones)
- ✅ Datos de venta (precio, pedido, total, impuestos)

## 🚀 Pasos para Actualizar

### 1️⃣ Acceder a Odoo
```
URL: http://localhost:8070
Usuario: 123456
Base de datos: inventario
```

### 2️⃣ Activar Modo Desarrollador
1. Ve a **Configuración** (Settings)
2. Busca "Activar modo desarrollador"
3. Haz clic en **Activar**

### 3️⃣ Actualizar el Módulo
1. Ve a **Aplicaciones** (Apps)
2. Quita el filtro "Aplicaciones" (debe decir "Todos")
3. Busca: `inventory_cardex`
4. Haz clic en **Actualizar** (Upgrade)
5. Espera a que termine (puede tardar 10-30 segundos)

### 4️⃣ Ver la Vista Actualizada
1. Ve a **Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**
2. Haz clic en el icono de **columnas** (⚙️) en la esquina superior derecha
3. Activa las columnas de venta que quieras ver:
   - ☑️ Pedido Venta
   - ☑️ Descripción Venta
   - ☑️ Cantidad Vendida
   - ☑️ Precio Unit. Venta
   - ☑️ Subtotal Venta
   - ☑️ Total Venta

## 📊 ¿Qué Verás?

### Columnas de Inventario (Siempre Visibles)
- Fecha
- Referencia
- Desde (ubicación origen)
- A (ubicación destino)
- Producto
- Cantidad
- Costo Unitario
- Costo Total
- Estado

### Columnas de Venta (Opcionales - Actívalas Tú)
- Pedido Venta (ej: SO001)
- Descripción Venta
- Cantidad Vendida
- Precio Unit. Venta
- Subtotal Venta
- Impuestos Venta
- Total Venta
- Estado Venta

## 💡 Ejemplo Práctico

Imagina que vendes 5 laptops:

**Vista Combinada**:
```
Producto: Laptop Dell XPS 15
Cantidad: 5

INVENTARIO:
  Costo Unitario: $800
  Costo Total: $4,000

VENTA:
  Pedido: SO001
  Precio Unit.: $1,200
  Total Venta: $6,000

MARGEN: $2,000 (33% de ganancia)
```

## ⚠️ Importante

### No todos los movimientos tienen venta
- Solo las **entregas de pedidos de venta** tienen datos de venta
- Las **transferencias internas** NO tienen venta
- Los **ajustes de inventario** NO tienen venta
- Las **recepciones de compra** NO tienen venta

### Cómo saber si un movimiento tiene venta
Activa la columna **"Tiene Venta"**:
- ✅ = Tiene venta asociada
- ❌ = No tiene venta (es otro tipo de movimiento)

## 🧪 Crear Datos de Prueba

Si no ves datos en las columnas de venta, crea un pedido:

### Paso 1: Crear Pedido de Venta
1. Ve a **Ventas** → **Pedidos** → **Crear**
2. Selecciona un cliente
3. Agrega productos (ej: 5 laptops)
4. Haz clic en **Confirmar**

### Paso 2: Validar la Entrega
1. Ve a **Inventario** → **Operaciones** → **Entregas**
2. Busca la entrega del pedido que creaste
3. Haz clic en **Validar**

### Paso 3: Ver el Resultado
1. Ve a **Inventario** → **Reportes** → **Movimientos Detallados (Cardex)**
2. Activa las columnas de venta
3. Deberías ver los datos de venta en el movimiento

## 🔍 Filtrar Solo Movimientos con Venta

Si quieres ver SOLO los movimientos que tienen venta:

1. Haz clic en **Filtros**
2. Agrega un filtro personalizado:
   - Campo: `Tiene Venta`
   - Operador: `es verdadero`
3. Aplica el filtro

## 📚 Más Información

- **Documentación completa**: Lee `UNION_INVENTARIO_VENTAS.md`
- **Resumen de cambios**: Lee `RESUMEN_UNION_INVENTARIO_VENTAS.md`

## ❓ Problemas Comunes

### No veo las columnas de venta
**Solución**: Haz clic en el icono de columnas (⚙️) y actívalas manualmente.

### Las columnas de venta están vacías
**Solución**: Ese movimiento no está relacionado con una venta. Verifica la columna "Tiene Venta".

### El módulo no se actualiza
**Solución**: 
1. Verifica que estés en modo desarrollador
2. Refresca la página (Ctrl + Shift + R)
3. Reinicia el contenedor: `docker restart odoo-web-1`

---

**¡Listo!** Ahora tienes una vista unificada de inventario y ventas. 🎉
