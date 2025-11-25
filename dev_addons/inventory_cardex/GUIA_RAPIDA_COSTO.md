# 💰 Guía Rápida: Campo de Costo en Historial de Movimientos

## ✅ Estado Actual

El campo de costo **YA ESTÁ IMPLEMENTADO** en tu módulo `inventory_cardex`.

## 🎯 Dónde Ver el Campo de Costo

### Ruta en Odoo:
```
Inventario → Stock → Historial de Movimientos
(Inventory → Stock → History of Movements)
```

### Campos Disponibles:
| Campo | Nombre Técnico | Descripción | Visible por Defecto |
|-------|---------------|-------------|---------------------|
| **Costo Unit.** | `product_cost` | Costo estándar del producto | ✅ Sí |
| **Costo Total** | `total_cost` | Cantidad × Costo unitario | ❌ No (activar manualmente) |

## 📋 Pasos para Ver el Campo

### 1️⃣ Actualizar el Módulo

**Opción A: Desde la Interfaz (Recomendado)**
1. Ir a **Configuración** → Activar **Modo Desarrollador**
2. Ir a **Aplicaciones**
3. Buscar: `inventory_cardex`
4. Clic en **Actualizar** (Upgrade)

**Opción B: Reiniciar Docker**
```bash
cd c:\Mis-Documentos\Appex\odoo
docker-compose restart
```

### 2️⃣ Ir al Historial de Movimientos
1. Abrir Odoo: http://localhost:8070
2. Ir a: **Inventario → Operaciones → Historial de Movimientos**
3. Buscar la columna **"Costo Unit."** después de "Producto"

### 3️⃣ Activar Columnas Adicionales (Opcional)
1. Clic en el icono de columnas (☰) en la esquina superior derecha
2. Marcar **"Costo Total"** para verlo también

## 🔍 Filtros Disponibles

En el historial de movimientos, puedes filtrar por:
- **Costo Alto**: Productos con costo > 100
- **Costo Medio**: Productos con costo entre 10-100
- **Costo Bajo**: Productos con costo < 10

## 📊 Ejemplo de Vista

```
┌─────────────────────────────────────────────────────────────────┐
│ Historial de movimientos                                        │
├─────────┬──────────────┬─────────────┬────────────┬────────────┤
│ Fecha   │ Referencia   │ Producto    │ Costo Unit.│ Cantidad   │
├─────────┼──────────────┼─────────────┼────────────┼────────────┤
│ 24/11   │ WH/OUT/00055 │ Office Chair│ $150.00    │ 3.00       │
│ 24/11   │ WH/OUT/00054 │ Office Chair│ $150.00    │ 4.00       │
│ 24/11   │ WH/OUT/00053 │ Office Chair│ $150.00    │ 3.00       │
└─────────┴──────────────┴─────────────┴────────────┴────────────┘
```

## 🛠️ Archivos Modificados

### Backend (Python)
- `models/stock_move.py`
  - Campo `product_cost`: Relacionado con `product_id.standard_price`
  - Campo `total_cost`: Calculado automáticamente
  - Campo `company_currency_id`: Para formato de moneda

### Frontend (XML)
- `views/stock_move_views.xml`
  - Vista de árbol extendida
  - Vista de formulario extendida
  - Filtros de búsqueda

## 🐛 Solución de Problemas

### ❌ No veo la columna "Costo Unit."
**Solución:**
1. Actualizar el módulo desde Aplicaciones
2. Limpiar caché del navegador (Ctrl+Shift+Del)
3. Recargar la página (Ctrl+F5)

### ❌ Los costos aparecen en $0.00
**Solución:**
1. Ir a **Inventario → Productos**
2. Abrir el producto
3. Pestaña **"Inventario"**
4. Verificar que el campo **"Costo"** tenga un valor

### ❌ El módulo no aparece en Aplicaciones
**Solución:**
1. Modo Desarrollador activado
2. **Aplicaciones** → Menú (☰) → **"Actualizar lista de aplicaciones"**
3. Buscar nuevamente

## 📝 Notas Técnicas

### ¿De dónde viene `standard_price`?
- Tabla: `product_product`
- Campo: `standard_price`
- Ubicación en UI: Producto → Pestaña "Inventario" → Campo "Costo"

### ¿Por qué no se puede hacer solo con JavaScript?
- El campo `standard_price` NO existe en `stock.move`
- Necesita una relación entre modelos (`product_id.standard_price`)
- Requiere cálculos del lado del servidor
- Debe respetar permisos de acceso

## ✨ Características Adicionales

✅ Formato de moneda automático  
✅ Cálculo de costo total  
✅ Filtros por rango de costo  
✅ Visible en todas las vistas de movimientos  
✅ Compatible con multi-moneda  

---

**Versión del módulo**: 1.0  
**Última actualización**: 2025-11-24  
**Autor**: Antigravity AI
