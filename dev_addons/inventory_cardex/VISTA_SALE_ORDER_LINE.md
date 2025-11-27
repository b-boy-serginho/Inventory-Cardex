# Vista Personalizada de Líneas de Pedido de Venta

## 📋 Resumen

He creado una vista personalizada para mostrar las líneas de pedidos de venta (`sale.order.line`) con los siguientes campos:

- **name**: Descripción del producto
- **product_uom_qty**: Cantidad
- **price_unit**: Precio Unitario
- **price_subtotal**: Subtotal (sin impuestos)
- **price_tax**: Impuestos
- **price_total**: Total (con impuestos)

## 📁 Archivos Creados/Modificados

### Archivos Nuevos:
1. **`models/sale_order_line.py`**: Modelo Python que extiende `sale.order.line`
2. **`views/sale_order_line_views.xml`**: Vista personalizada con árbol, búsqueda y menú

### Archivos Modificados:
1. **`__manifest__.py`**: 
   - Agregada dependencia `'sale'`
   - Agregado archivo de vista `'views/sale_order_line_views.xml'`
2. **`models/__init__.py`**: Agregado import del nuevo modelo

## 🚀 Pasos para Actualizar el Módulo

### Opción 1: Usando el script PowerShell (Recomendado)

```powershell
cd c:\Mis-Documentos\Appex\odoo\dev_addons\inventory_cardex
.\actualizar_modulo.ps1
```

### Opción 2: Manualmente con Docker

```powershell
# 1. Actualizar el módulo
docker exec -it odoo-web-1 odoo -u inventory_cardex -d inventario --stop-after-init

# 2. Reiniciar el contenedor
docker restart odoo-web-1

# 3. Esperar 10 segundos
Start-Sleep -Seconds 10
```

## 🔍 Cómo Acceder a la Vista

Después de actualizar el módulo:

1. **Accede a Odoo**: http://localhost:8070
2. **Credenciales**:
   - Usuario: `123456` (usuario maestro)
   - Base de datos: `inventario`
3. **Navega al menú**: 
   - **Ventas** → **Pedidos** → **Líneas de Pedido (Cardex)**

## 🎨 Características de la Vista

### Vista de Árbol
- Muestra todos los campos solicitados con formato monetario
- Campos adicionales opcionales (Pedido, Producto, Estado, Vendedor, UdM)
- No permite crear ni editar directamente (solo lectura)

### Vista de Búsqueda
- **Búsqueda por**: Descripción, Producto, Pedido, Vendedor
- **Filtros por Estado**: Borrador, Pedido de Venta, Hecho, Cancelado
- **Filtros por Precio**: Alto (>100), Medio (10-100), Bajo (<10)
- **Agrupación**: Por Pedido, Producto, Vendedor, Estado

## 📊 Consulta SQL Equivalente

La vista muestra los mismos datos que obtendrías con esta consulta SQL:

```sql
SELECT 
    name,
    product_uom_qty,
    price_unit,
    price_subtotal,
    price_tax,
    price_total
FROM sale_order_line;
```

## 🔧 Personalización Futura

Si necesitas agregar campos personalizados o cálculos adicionales:

1. **Edita**: `models/sale_order_line.py`
2. **Agrega campos computados** usando el decorador `@api.depends()`
3. **Actualiza la vista** en `views/sale_order_line_views.xml`

## ⚠️ Notas Importantes

- El módulo `sale` debe estar instalado en tu instancia de Odoo
- Los campos mostrados son estándar de Odoo 17
- La vista es de solo lectura para evitar modificaciones accidentales
- Todos los precios se muestran con formato monetario

## 🐛 Solución de Problemas

### Si el menú no aparece:
1. Verifica que el módulo `sale` esté instalado
2. Actualiza el módulo con `-u inventory_cardex`
3. Limpia la caché del navegador (Ctrl + Shift + R)

### Si hay errores de permisos:
- Los permisos de `sale.order.line` son heredados del módulo `sale`
- No necesitas agregar reglas de acceso adicionales

### Si los datos no aparecen:
- Asegúrate de tener pedidos de venta creados en Odoo
- Verifica que los pedidos tengan líneas de productos

## 📞 Información de Conexión

- **Puerto Odoo**: 8070
- **Base de Datos**: inventario
- **Usuario DB**: 123
- **Contraseña DB**: 123
- **Usuario Maestro**: 123456
