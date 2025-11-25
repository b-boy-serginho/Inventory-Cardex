# 🗄️ CONSULTAS SQL ÚTILES - INVENTORY CARDEX

## 📋 Información de Conexión

```bash
# Conectarse a PostgreSQL desde el contenedor
docker exec -it odoo-db-1 bash
psql -U odoo -d inventario
```

**Datos de conexión:**
- Usuario: `odoo`
- Base de datos: `inventario`
- Contraseña: `123`

---

## 📊 CONSULTAS PARA `stock_move`

### Ver últimos 10 movimientos con costo
```sql
SELECT id, name, product_cost, product_qty,
       (product_cost * product_qty) as total_cost_calculado,
       date
FROM stock_move
WHERE product_cost IS NOT NULL
ORDER BY id DESC
LIMIT 10;
```

### Ver movimientos con costo mayor a 100
```sql
SELECT id, name, product_cost, product_qty,
       (product_cost * product_qty) as total_cost
FROM stock_move
WHERE product_cost > 100
ORDER BY product_cost DESC;
```

### Estadísticas de costos
```sql
SELECT 
    COUNT(*) as total_movimientos,
    ROUND(AVG(product_cost), 2) as costo_promedio,
    ROUND(MIN(product_cost), 2) as costo_minimo,
    ROUND(MAX(product_cost), 2) as costo_maximo,
    ROUND(SUM(product_cost * product_qty), 2) as valor_total_inventario
FROM stock_move
WHERE product_cost IS NOT NULL;
```

### Movimientos por rango de fecha
```sql
SELECT id, name, product_cost, product_qty,
       (product_cost * product_qty) as total_cost,
       date::date as fecha
FROM stock_move
WHERE product_cost IS NOT NULL
  AND date >= '2025-11-20'
  AND date <= '2025-11-25'
ORDER BY date DESC;
```

### Top 10 movimientos más costosos
```sql
SELECT id, name, product_cost, product_qty,
       (product_cost * product_qty) as total_cost
FROM stock_move
WHERE product_cost IS NOT NULL
ORDER BY (product_cost * product_qty) DESC
LIMIT 10;
```

---

## 📊 CONSULTAS PARA `stock_move_line`

### Ver últimas 10 líneas con costo
```sql
SELECT id, product_cost, quantity,
       (product_cost * quantity) as line_cost_calculado,
       date
FROM stock_move_line
WHERE product_cost IS NOT NULL
ORDER BY id DESC
LIMIT 10;
```

### Ver líneas con costo total mayor a 1000
```sql
SELECT id, product_cost, quantity,
       (product_cost * quantity) as line_cost
FROM stock_move_line
WHERE product_cost IS NOT NULL
  AND (product_cost * quantity) > 1000
ORDER BY (product_cost * quantity) DESC;
```

### Estadísticas de líneas de movimiento
```sql
SELECT 
    COUNT(*) as total_lineas,
    ROUND(AVG(product_cost), 2) as costo_promedio,
    ROUND(MIN(product_cost), 2) as costo_minimo,
    ROUND(MAX(product_cost), 2) as costo_maximo,
    ROUND(SUM(product_cost * quantity), 2) as valor_total
FROM stock_move_line
WHERE product_cost IS NOT NULL;
```

---

## 🔍 CONSULTAS DE VERIFICACIÓN

### Ver estructura de tabla stock_move
```sql
\d stock_move
```

### Ver estructura de tabla stock_move_line
```sql
\d stock_move_line
```

### Ver todas las columnas de stock_move
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'stock_move' 
ORDER BY column_name;
```

### Ver todas las columnas de stock_move_line
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'stock_move_line' 
ORDER BY column_name;
```

### Verificar campo product_cost
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name IN ('stock_move', 'stock_move_line')
  AND column_name = 'product_cost';
```

### Contar registros con costo
```sql
-- En stock_move
SELECT COUNT(*) as registros_con_costo
FROM stock_move
WHERE product_cost IS NOT NULL AND product_cost > 0;

-- En stock_move_line
SELECT COUNT(*) as registros_con_costo
FROM stock_move_line
WHERE product_cost IS NOT NULL AND product_cost > 0;
```

---

## 📈 REPORTES AVANZADOS

### Resumen diario de movimientos
```sql
SELECT 
    date::date as fecha,
    COUNT(*) as num_movimientos,
    ROUND(SUM(product_cost * product_qty), 2) as valor_total_dia,
    ROUND(AVG(product_cost), 2) as costo_promedio_dia
FROM stock_move
WHERE product_cost IS NOT NULL
GROUP BY date::date
ORDER BY fecha DESC
LIMIT 30;
```

### Productos con mayor valor en inventario
```sql
SELECT 
    product_id,
    COUNT(*) as num_movimientos,
    ROUND(SUM(product_qty), 2) as cantidad_total,
    ROUND(AVG(product_cost), 2) as costo_promedio,
    ROUND(SUM(product_cost * product_qty), 2) as valor_total
FROM stock_move
WHERE product_cost IS NOT NULL
GROUP BY product_id
ORDER BY valor_total DESC
LIMIT 20;
```

### Movimientos con costo cero (posibles errores)
```sql
SELECT id, name, product_cost, product_qty, date
FROM stock_move
WHERE product_cost = 0 OR product_cost IS NULL
ORDER BY date DESC
LIMIT 10;
```

---

## 🛠️ COMANDOS ÚTILES DE POSTGRESQL

```sql
-- Salir de psql
\q

-- Listar todas las bases de datos
\l

-- Cambiar de base de datos
\c nombre_bd

-- Listar todas las tablas
\dt

-- Ver índices de una tabla
\di stock_move

-- Ver tamaño de las tablas
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE tablename IN ('stock_move', 'stock_move_line')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ejecutar un script SQL desde archivo
\i /path/to/file.sql

-- Activar timing (ver cuánto tarda cada query)
\timing

-- Ver historial de comandos
\s
```

---

## 📊 EXPORTAR DATOS

### Exportar a CSV
```sql
-- Desde psql
\copy (SELECT id, name, product_cost, product_qty, (product_cost * product_qty) as total FROM stock_move WHERE product_cost IS NOT NULL) TO '/tmp/stock_move_export.csv' WITH CSV HEADER;
```

### Desde bash (fuera de psql)
```bash
docker exec odoo-db-1 psql -U odoo -d inventario -c "COPY (SELECT id, name, product_cost, product_qty FROM stock_move WHERE product_cost IS NOT NULL) TO STDOUT WITH CSV HEADER" > stock_move_export.csv
```

---

## ⚠️ IMPORTANTE

1. **Campos computados NO en BD:**
   - `total_cost` (en stock_move) - Se calcula como `product_cost * product_qty`
   - `line_cost` (en stock_move_line) - Se calcula como `product_cost * quantity`

2. **Campo guardado en BD:**
   - ✅ `product_cost` - Almacena el costo histórico del producto

3. **Para hacer cálculos:**
   - Usa `(product_cost * product_qty)` para total_cost
   - Usa `(product_cost * quantity)` para line_cost

---

## 🔗 Recursos Adicionales

- [Documentación PostgreSQL](https://www.postgresql.org/docs/)
- [Documentación Odoo ORM](https://www.odoo.com/documentation/17.0/developer/reference/backend/orm.html)
- Archivo relacionado: `GUIA_BASE_DE_DATOS.md`
- Script JS: `static/src/js/database_inspector.js`

---

📝 **Última actualización:** 2025-11-25
