# 🗄️ GUÍA COMPLETA - CAMPO COSTO EN BASE DE DATOS

## ✅ CAMBIOS REALIZADOS

### 1. Modificaciones en el Modelo Python
**Archivo:** `models/stock_move.py`

Se cambió `store=False` a `store=True` en:
- Clase `StockMove` → campo `product_cost` (línea 13)
- Clase `StockMoveLine` → campo `product_cost` (línea 69)

Esto significa que ahora los valores se **GUARDARÁN EN LA BASE DE DATOS**.

---

## 📊 TABLAS EN POSTGRESQL

### Tabla 1: `stock_move`
```sql
-- Nombre de tabla en PostgreSQL
Tabla: stock_move

-- Campo agregado
Columna: product_cost
Tipo: NUMERIC o DOUBLE PRECISION
```

### Tabla 2: `stock_move_line`
```sql
-- Nombre de tabla en PostgreSQL
Tabla: stock_move_line

-- Campo agregado
Columna: product_cost
Tipo: NUMERIC o DOUBLE PRECISION
```

---

## 🔄 ACTUALIZAR EL MÓDULO EN DOCKER

### Opción 1: Desde la interfaz web de Odoo
1. Ve a **Aplicaciones** (Apps)
2. Activa el **Modo Desarrollador** si no está activo
3. Busca el módulo **"Inventory Cardex"** o **"inventory_cardex"**
4. Haz clic en **"Actualizar"** (Upgrade)

### Opción 2: Reiniciar el contenedor (ya ejecutado)
```powershell
docker restart odoo-web-1
```

### Opción 3: Actualizar desde línea de comandos
Después de reiniciar, conéctate a:
- URL: http://localhost:8070
- Base de datos: **inventario**
- Usuario: admin
- Contraseña: **123**

Y actualiza el módulo desde Apps.

---

## 🌐 VERIFICAR EN EL NAVEGADOR CON JAVASCRIPT

### Paso 1: Abrir la consola del navegador
1. Abre Odoo en tu navegador: `http://localhost:8070`
2. Inicia sesión con la base de datos **inventario**
3. Presiona `F12` o clic derecho → "Inspeccionar" → pestaña **Console**

### Paso 2: Ejecutar comandos de inspección

#### Comando 1: Ver ayuda
```javascript
showDBInspectorHelp()
```

#### Comando 2: Inspeccionar tabla stock_move
```javascript
// Ver últimos 10 registros de stock.move
await inspectStockMove(10)

// Ver últimos 50 registros
await inspectStockMove(50)
```

**Resultado esperado:**
```
✅ Datos de stock.move (últimos 10 registros):
┌─────────┬────┬────────────┬────────────┬──────────────┬──────────────┬─────────┐
│ (index) │ id │    name    │ product_id │ product_cost │ total_cost   │ qty     │
├─────────┼────┼────────────┼────────────┼──────────────┼──────────────┼─────────┤
│    0    │ 5  │  'WH/IN/...'│  [15, "..."]│   45.50     │   227.50     │   5.0   │
│    1    │ 4  │  'WH/OUT/..'│  [12, "..."]│   30.00     │    90.00     │   3.0   │
└─────────┴────┴────────────┴────────────┴──────────────┴──────────────┴─────────┘
📋 Tabla en PostgreSQL: stock_move
📋 Campo en BD: product_cost (tipo: numeric/float)
```

#### Comando 3: Inspeccionar tabla stock_move_line
```javascript
// Ver últimos 10 registros de stock.move.line
await inspectStockMoveLine(10)
```

**Resultado esperado:**
```
✅ Datos de stock.move.line (últimos 10 registros):
┌─────────┬────┬────────────┬──────────────┬────────────┬──────────┐
│ (index) │ id │ product_id │ product_cost │ line_cost  │ quantity │
├─────────┼────┼────────────┼──────────────┼────────────┼──────────┤
│    0    │ 8  │  [15, ".."]│    45.50     │   227.50   │   5.0    │
└─────────┴────┴────────────┴──────────────┴────────────┴──────────┘
📋 Tabla en PostgreSQL: stock_move_line
📋 Campo en BD: product_cost (tipo: numeric/float)
```

#### Comando 4: Verificar si el campo está en la BD
```javascript
// Verificar stock.move
await checkFieldInDB('stock.move')

// Verificar stock.move.line
await checkFieldInDB('stock.move.line')
```

**Resultado esperado:**
```
✅ Configuración del campo 'product_cost':
┌─────────┬──────────────┬────────────────────┬─────────┬──────────┐
│ (index) │     name     │ field_description  │  ttype  │  store   │
├─────────┼──────────────┼────────────────────┼─────────┼──────────┤
│    0    │'product_cost'│      'Costo'       │ 'float' │   true   │
└─────────┴──────────────┴────────────────────┴─────────┴──────────┘
✅ El campo SÍ está guardado en la base de datos (store=True)
```

#### Comando 5: Ver estadísticas de costos
```javascript
await getCostStats()
```

**Resultado esperado:**
```
📊 Estadísticas de Costos:
┌──────────────────┬─────────┐
│     (index)      │ Values  │
├──────────────────┼─────────┤
│ total_registros  │   156   │
│ costo_promedio   │ '38.75' │
│ costo_minimo     │ '5.00'  │
│ costo_maximo     │ '250.00'│
│ total_acumulado  │'6045.00'│
└──────────────────┴─────────┘
```

---

## 🔍 CONSULTAS SQL DIRECTAS (OPCIONAL)

Si quieres consultar directamente en PostgreSQL:

```sql
-- Conectarse al contenedor de base de datos
docker exec -it odoo-db-1 psql -U odoo -d inventario

-- Ver estructura de la tabla stock_move
\d stock_move

-- Ver registros con costo
SELECT id, name, product_cost, total_cost, product_qty
FROM stock_move
WHERE product_cost IS NOT NULL
LIMIT 10;

-- Ver estructura de la tabla stock_move_line
\d stock_move_line

-- Ver registros con costo en líneas
SELECT id, product_cost, line_cost, quantity
FROM stock_move_line
WHERE product_cost IS NOT NULL
LIMIT 10;

-- Salir de PostgreSQL
\q
```

---

## 📝 RESUMEN DE INFORMACIÓN

| Concepto | Valor |
|----------|-------|
| **Base de datos** | inventario |
| **Contraseña BD** | 123 |
| **Contraseña Master** | 123456 |
| **Tabla 1** | stock_move |
| **Tabla 2** | stock_move_line |
| **Campo guardado** | product_cost |
| **Tipo de dato** | NUMERIC / FLOAT |
| **Store en BD** | ✅ SÍ (True) |

---

## ⚠️ IMPORTANTE

1. **Valores históricos**: Ahora que `store=True`, cada registro guardará el costo en el momento de la creación.

2. **Actualización**: Debes actualizar el módulo para que Odoo cree las columnas en la BD.

3. **Registros existentes**: Los registros antiguos recibirán el costo actual del producto al actualizar el módulo.

4. **JavaScript**: Los scripts de inspección se cargarán automáticamente al abrir Odoo en el navegador.

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Reiniciar contenedor (Ya hecho)
2. 🔄 Actualizar módulo desde Odoo Apps
3. 🌐 Abrir navegador y probar comandos JS
4. ✅ Verificar datos en la consola

¿Necesitas ayuda con alguno de estos pasos?
