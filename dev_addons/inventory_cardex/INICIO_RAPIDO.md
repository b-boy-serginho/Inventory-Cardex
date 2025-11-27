# 🚀 INSTRUCCIONES RÁPIDAS

## ⚡ Pasos para Ver la Nueva Vista

### Paso 1: Abrir Odoo
1. Abre tu navegador
2. Ve a: **http://localhost:8070**
3. Selecciona la base de datos: **inventario**
4. Inicia sesión con el usuario: **123456**

### Paso 2: Activar Modo Desarrollador
1. Haz clic en **Configuración** (Settings) en el menú superior
2. Busca "Activar modo desarrollador" (Developer Mode)
3. Haz clic en **Activar**

### Paso 3: Actualizar el Módulo
1. Haz clic en **Aplicaciones** (Apps) en el menú superior
2. Haz clic en el filtro "Aplicaciones" para quitarlo (debe mostrar "Todos")
3. En el buscador, escribe: **inventory_cardex**
4. Haz clic en el botón **Actualizar** (Upgrade) del módulo

### Paso 4: Ver la Nueva Vista
1. Ve al menú **Ventas** (Sales)
2. Haz clic en **Pedidos** (Orders)
3. Haz clic en **Líneas de Pedido (Cardex)**

## ✅ ¿Qué Deberías Ver?

Una tabla con las siguientes columnas:
- **Descripción** (name)
- **Cantidad** (product_uom_qty)
- **Precio Unitario** (price_unit)
- **Subtotal** (price_subtotal)
- **Impuestos** (price_tax)
- **Total** (price_total)

## ❓ Si No Ves Datos

Si la vista está vacía, necesitas crear pedidos de venta:

1. Ve a **Ventas** → **Pedidos** → **Presupuestos**
2. Haz clic en **Crear**
3. Selecciona un cliente
4. Agrega productos en las líneas de pedido
5. Haz clic en **Confirmar**
6. Vuelve a **Ventas** → **Pedidos** → **Líneas de Pedido (Cardex)**

## 🔄 Si Algo Sale Mal

### El módulo no aparece en Aplicaciones
```powershell
# Reinicia el contenedor
docker restart odoo-web-1

# Espera 15 segundos y vuelve a intentar
```

### El menú no aparece después de actualizar
1. Refresca la página (Ctrl + Shift + R)
2. Cierra sesión y vuelve a iniciar
3. Verifica que el módulo "Ventas" esté instalado

### Error al actualizar el módulo
1. Verifica los logs:
   ```powershell
   docker logs odoo-web-1 --tail 50
   ```
2. Asegúrate de que el módulo "Sales" esté instalado
3. Reinicia el contenedor y vuelve a intentar

## 📞 Información de Acceso

- **URL**: http://localhost:8070
- **Base de Datos**: inventario
- **Usuario**: 123456
- **Puerto**: 8070

## 📚 Más Información

- Lee `VISTA_SALE_ORDER_LINE.md` para documentación completa
- Lee `GUIA_ACTUALIZACION.md` para métodos alternativos de actualización
- Lee `RESUMEN_CAMBIOS.md` para ver todos los cambios realizados

---

**¿Necesitas ayuda?** Revisa los archivos de documentación o verifica los logs de Docker.
