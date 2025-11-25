# 📊 GUÍA DE REPORTES - INVENTORY CARDEX

## 🎯 Funcionalidades Implementadas

Tu módulo ahora incluye dos potentes herramientas de reportes:

1. **📄 Reporte PDF** - Documento profesional con costos de inventario
2. **📊 Exportar a Excel** - Archivo .xlsx para análisis detallado

---

## 🚀 CÓMO USAR LOS REPORTES

### Opción 1: Desde el Menú Principal

1. Abre Odoo: **http://localhost:8070**
2. Ve al módulo **Inventario**
3. En el menú, busca: **Operaciones → Reporte de Costos**
4. Se abrirá el wizard de generación de reportes

### Opción 2: Desde Movimientos de Stock

1. Ve a **Inventario → Operaciones → Todos los Movimientos**
2. En la parte superior, verás el botón **"Reporte de Costos"**
3. Haz clic para abrir el wizard

---

## 🎨 CARACTERÍSTICAS DEL WIZARD

### 📅 Filtros Disponibles:

| Campo | Descripción | Requerido |
|-------|-------------|-----------|
| **Fecha Desde** | Fecha inicial del período | ✅ Sí |
| **Fecha Hasta** | Fecha final del período | ✅ Sí |
| **Tipo de Reporte** | PDF o Excel | ✅ Sí |
| **Productos** | Filtrar productos específicos | ❌ Opcional |
| **Ubicaciones** | Filtrar ubicaciones específicas | ❌ Opcional |
| **Incluir costo cero** | Mostrar productos sin costo | ❌ Opcional |

---

## 📄 REPORTE PDF

### Características:
- ✅ Diseño profesional con colores corporativos
- ✅ Resumen ejecutivo en la parte superior
- ✅ Tabla detallada de todos los movimientos
- ✅ Totalizadores automáticos
- ✅ Información del período y fecha de generación
- ✅ Notas al pie explicativas

### Contenido del PDF:

#### 📈 Resumen Ejecutivo:
- Total de Movimientos
- Cantidad Total
- Valor Total (Costo Total)

#### 📋 Tabla de Datos:
- ID del movimiento
- Fecha
- Referencia
- Producto
- Cantidad
- Costo Unitario
- Costo Total

### Ejemplo de uso:

```
1. Selecciona tipo: "Reporte PDF"
2. Define período: 01/11/2025 - 30/11/2025
3. (Opcional) Selecciona productos específicos
4. Clic en "Generar Reporte"
5. El PDF se descargará automáticamente
```

---

## 📊 EXPORTAR A EXCEL

### Características:
- ✅ Formato .xlsx compatible con Excel, LibreOffice, Google Sheets
- ✅ Encabezados formateados con colores
- ✅ Celdas con formato de moneda ($)
- ✅ Formato de fecha (dd/mm/yyyy)
- ✅ Columnas auto-ajustadas
- ✅ Fila de totales con fondo gris
- ✅ Título y metadata del reporte

### Estructura del archivo Excel:

#### Fila 1: Título
```
REPORTE DE COSTOS DE INVENTARIO
```

#### Filas 2-3: Información
```
Período: 01/11/2025 - 30/11/2025
Generado: 25/11/2025 10:30:45
```

#### Fila 5: Encabezados (con formato azul)
```
ID | Fecha | Referencia | Producto | Cantidad | Costo Unit. | Costo Total | Estado
```

#### Filas 6+: Datos
```
37 | 24/11/2025 | WH/IN/00001 | [AUR-001] Auriculares Sony | 10.00 | $180.00 | $1,800.00 | Hecho
```

#### Última fila: Totales (fondo gris)
```
TOTALES: | | | | 150.00 | | $45,250.00
```

### Ejemplo de uso:

```
1. Selecciona tipo: "Exportar a Excel"
2. Define período: 01/11/2025 - 30/11/2025
3. (Opcional) Filtra por ubicaciones
4. Clic en "Generar Reporte"
5. El archivo .xlsx se descargará automáticamente
```

---

## 🎯 CASOS DE USO COMUNES

### Caso 1: Reporte mensual completo
```
Fecha Desde: 01/11/2025
Fecha Hasta: 30/11/2025
Tipo: PDF
Productos: (todos)
Ubicaciones: (todas)
Incluir costo cero: No
```

### Caso 2: Análisis de productos específicos
```
Fecha Desde: 01/01/2025
Fecha Hasta: 31/12/2025
Tipo: Excel
Productos: Seleccionar productos a analizar
Ubicaciones: (todas)
Incluir costo cero: Sí
```

### Caso 3: Auditoría de ubicación
```
Fecha Desde: 01/11/2025
Fecha Hasta: 25/11/2025
Tipo: PDF
Productos: (todos)
Ubicaciones: Seleccionar ubicación específica
Incluir costo cero: No
```

---

## 📂 ARCHIVOS GENERADOS

### PDF:
- **Nombre:** `Reporte_Costos_2025-11-01_2025-11-30.pdf`
- **Ubicación:** Descarga automática en navegador
- **Tamaño:** Varía según datos (típicamente 50-500 KB)

### Excel:
- **Nombre:** `reporte_costos_2025-11-01_2025-11-30.xlsx`
- **Ubicación:** Descarga automática en navegador
- **Tamaño:** Varía según datos (típicamente 20-200 KB)

---

## 🔧 ACTUALIZAR EL MÓDULO

Después de agregar estos archivos, DEBES actualizar el módulo:

### Desde la Interfaz Web:
1. Ve a **Aplicaciones** (Apps)
2. Activa **Modo Desarrollador** (si no lo está)
3. Busca **"Inventory Cardex"**
4. Clic en **"Actualizar"**

### Desde Docker (alternativa):
```bash
docker restart odoo-web-1
```

Espera 10-15 segundos y actualiza desde Apps.

---

## ✅ VERIFICACIÓN

Después de actualizar, verifica que todo funcione:

### 1. Verificar menú:
```
Inventario → Operaciones → Reporte de Costos
```

### 2. Verificar wizard:
- Debe mostrar todos los campos
- Debe tener botón "Generar Reporte"

### 3. Probar PDF:
- Selecciona período
- Tipo: PDF
- Genera y verifica descarga

### 4. Probar Excel:
- Selecciona período  
- Tipo: Excel
- Genera y verifica descarga

---

## 🎨 PERSONALIZACIÓN

### Cambiar colores del PDF:
Edita: `report/stock_cost_report_template.xml`
```xml
<!-- Cambiar color del encabezado -->
<h2 style="color: #TU_COLOR;">
```

### Cambiar colores del Excel:
Edita: `wizard/stock_cost_report_wizard.py`
```python
header_format = workbook.add_format({
    'bg_color': '#TU_COLOR',  # Cambia aquí
})
```

### Agregar más campos:
1. Modifica la consulta en `_get_report_data()`
2. Agrega columnas en la plantilla PDF
3. Agrega columnas en el código de Excel

---

## 📊 DATOS INCLUIDOS

### Solo se incluyen movimientos:
- ✅ Con estado = "Hecho" (done)
- ✅ Dentro del rango de fechas
- ✅ Con costo > 0 (si no incluyes costo cero)
- ✅ De productos/ubicaciones seleccionados (si aplica)

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Error: "Module xlsxwriter not found"
```bash
# Entrar al contenedor
docker exec -it odoo-web-1 bash

# Instalar xlsxwriter
pip3 install xlsxwriter

# Salir y reiniciar
exit
docker restart odoo-web-1
```

### El menú no aparece:
1. Verifica que actualizaste el módulo
2. Limpia caché del navegador (Ctrl + Shift + R)
3. Cierra sesión y vuelve a entrar

### El PDF está en blanco:
- Verifica que hay datos en el rango de fechas seleccionado
- Revisa los filtros (puede que estén muy restrictivos)

### El Excel no descarga:
- Verifica que xlsxwriter esté instalado
- Revisa logs del servidor: `log/odoo-server.log`

---

## 📚 ARCHIVOS DEL MÓDULO

```
inventory_cardex/
├── wizard/
│   ├── __init__.py
│   ├── stock_cost_report_wizard.py          ← Lógica del wizard
│   └── stock_cost_report_wizard_views.xml   ← Vista del formulario
├── report/
│   └── stock_cost_report_template.xml       ← Plantilla PDF
├── models/
│   └── stock_move.py                         ← Modelo con product_cost
└── __manifest__.py                           ← Registro de archivos
```

---

## 🎓 PRÓXIMOS PASOS

Mejoras que puedes agregar:

1. **Gráficos en PDF** - Agregar pie charts o bar charts
2. **Envío por email** - Enviar reporte automáticamente
3. **Programar reportes** - Generar automáticamente cada mes
4. **Dashboard** - Vista gráfica de costos
5. **Comparación de períodos** - Comparar mes actual vs anterior

---

## 📞 AYUDA Y SOPORTE

Si encuentras errores:
1. Revisa `log/odoo-server.log`
2. Verifica que xlsxwriter esté instalado
3. Asegúrate de que el módulo esté actualizado
4. Consulta la documentación de Odoo: https://www.odoo.com/documentation/17.0/

---

📝 **Última actualización:** 2025-11-25  
✅ **Compatible con:** Odoo 17  
🐳 **Docker:** Soportado
