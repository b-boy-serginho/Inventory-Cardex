# 📦 Cómo Cargar Datos en Inventory Cardex

## Método 1: Datos de Demostración Automáticos (XML) ✅ RECOMENDADO

### Paso 1: Desinstalar y Reinstalar el Módulo
Los datos demo solo se cargan en la **instalación inicial**:

1. Ve a **Aplicaciones** (Apps)
2. Busca "Inventory Cardex"
3. Click en **Desinstalar**
4. Vuelve a **Instalar** el módulo
5. ✅ Los datos se cargarán automáticamente

### Paso 2: Verificar los Datos
Después de reinstalar, verifica:

- **Productos**: Inventario → Productos → Productos
  - Laptop Dell Inspiron
  - Mouse Logitech MX Master
  - Teclado Mecánico RGB
  - Monitor LG 27 pulgadas

- **Contactos**: Contactos
  - Empresa Demo S.A. (Cliente)
  - Proveedor Tech S.A. (Proveedor)

- **Operaciones**: Inventario → Operaciones
  - Recepciones (con productos del proveedor)
  - Órdenes de Entrega (entregas a clientes)

---

## Método 2: Importar CSV Manualmente

### Productos desde CSV:

1. Ve a **Inventario → Productos → Productos**
2. Click en el icono de **lista** (arriba derecha)
3. Click en **⚙️ Favoritos → Importar registros**
4. Selecciona el archivo: `data/productos_ejemplo.csv`
5. Mapea las columnas si es necesario
6. Click en **Importar**  

---

## Método 3: Crear Datos Manualmente

### Crear un Producto:
1. **Inventario → Productos → Productos**
2. Click en **Crear**
3. Completa:
   - Nombre del producto
   - Tipo de producto: "Producto almacenable"
   - Precio de venta
   - Costo
   - Referencia interna
   - Código de barras
4. **Guardar**

### Crear una Recepción de Mercancía:
1. **Inventario → Operaciones → Recepciones**
2. Click en **Crear**
3. Selecciona el **Proveedor**
4. Click en **Agregar una línea**
5. Selecciona el **Producto** y la **Cantidad**
6. **Guardar**
7. Click en **Validar** para confirmar la recepción

### Crear una Orden de Entrega:
1. **Inventario → Operaciones → Órdenes de Entrega**
2. Click en **Crear**
3. Selecciona el **Cliente**
4. Click en **Agregar una línea**
5. Selecciona el **Producto** y la **Cantidad**
6. **Guardar**
7. Click en **Validar** para confirmar la entrega

---

## Método 4: Ajuste de Inventario (Stock Inicial)

Si solo necesitas agregar stock existente:

1. **Inventario → Operaciones → Ajustes de Inventario**
2. Click en **Crear**
3. Selecciona la **Ubicación** (ej: WH/Stock)
4. Click en **Agregar una línea**
5. Selecciona el **Producto**
6. Ingresa la **Cantidad Contada**
7. **Guardar** y **Validar**

---

## 🔄 Actualizar el Módulo (Sin Perder Datos)

Si solo modificas vistas XML (no datos):

1. **Aplicaciones → Inventory Cardex**
2. Click en **Actualizar**
3. ✅ Los datos existentes se mantienen

---

## 🗑️ Limpiar Datos de Prueba

Para eliminar todos los datos demo:

1. **Configuración → Técnico → Datos externos → ID externos**
2. Busca: `inventory_cardex.`
3. Selecciona todos los registros
4. **Acción → Eliminar**

---

## 📊 Datos Incluidos en demo_data.xml

- ✅ 4 Productos (Laptop, Mouse, Teclado, Monitor)
- ✅ 1 Cliente (Empresa Demo S.A.)
- ✅ 1 Proveedor (Proveedor Tech S.A.)
- ✅ 2 Ubicaciones de almacén (Estante A y B)
- ✅ 1 Recepción de mercancía (10 laptops, 25 mouse)
- ✅ 1 Orden de entrega (3 laptops)

---

## ⚠️ Notas Importantes

1. **Los datos demo solo se cargan en instalación inicial**, no en actualizaciones
2. **Para recargar datos demo**: Desinstalar → Reinstalar
3. **En producción**: Usa `'data': []` en lugar de `'demo': []`
4. **Para datos permanentes**: Mueve archivos de `'demo'` a `'data'` en __manifest__.py

---

## 🆘 Solución de Problemas

### "No veo los datos después de instalar"
- Verifica que instalaste con datos de demostración habilitados
- Revisa los logs de Odoo para errores en el XML

### "Error al instalar el módulo"
- Verifica la sintaxis del XML
- Asegúrate de que las referencias (`ref=""`) existan
- Revisa que los modelos y campos sean correctos

### "Los productos no tienen stock"
- Los movimientos de stock necesitan ser validados
- Crea un ajuste de inventario manual
- O valida las recepciones pendientes
