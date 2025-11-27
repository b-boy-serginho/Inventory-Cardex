# 🔄 Guía de Actualización del Módulo

## Problema Actual

El comando `docker exec odoo-web-1 odoo -u inventory_cardex -d inventario --stop-after-init` no funciona correctamente porque el comando `odoo` dentro del contenedor no puede conectarse a PostgreSQL (que está en otro contenedor llamado `db`).

## ✅ Solución: Actualizar desde la Interfaz Web

### Método 1: Actualizar desde Aplicaciones (Recomendado)

1. **Reinicia el contenedor de Odoo** (para que detecte los nuevos archivos):
   ```powershell
   docker restart odoo-web-1
   ```
   
2. **Espera 15-20 segundos** para que Odoo inicie completamente

3. **Accede a Odoo**:
   - URL: http://localhost:8070
   - Base de datos: `inventario`
   - Usuario: `123456`

4. **Activa el modo desarrollador**:
   - Ve a **Configuración** (Settings)
   - Busca "Activar modo desarrollador" (Activate Developer Mode)
   - Haz clic en "Activar"

5. **Actualiza el módulo**:
   - Ve a **Aplicaciones** (Apps)
   - Quita el filtro "Aplicaciones" para ver todos los módulos
   - Busca: `inventory_cardex`
   - Haz clic en el botón **Actualizar** (Upgrade)

### Método 2: Actualizar desde la línea de comandos (Alternativo)

Si prefieres usar la línea de comandos, puedes crear un archivo de configuración temporal:

```powershell
# 1. Crear un archivo de configuración temporal
docker exec odoo-web-1 bash -c "cat > /tmp/odoo_update.conf << EOF
[options]
db_host = db
db_port = 5432
db_user = odoo
db_password = myodoo
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
EOF"

# 2. Actualizar el módulo usando el archivo de configuración
docker exec odoo-web-1 odoo -c /tmp/odoo_update.conf -u inventory_cardex -d inventario --stop-after-init

# 3. Reiniciar el contenedor
docker restart odoo-web-1
```

### Método 3: Usando docker-compose exec

```powershell
# Desde el directorio c:\Mis-Documentos\Appex\odoo
docker-compose exec -e PGHOST=db web odoo -u inventory_cardex -d inventario --stop-after-init
docker-compose restart web
```

## 🎯 Script Rápido

He creado un script PowerShell que puedes ejecutar:

```powershell
cd c:\Mis-Documentos\Appex\odoo\dev_addons\inventory_cardex
.\reiniciar_odoo.ps1
```

Este script reinicia Odoo y te muestra las instrucciones para actualizar desde la interfaz web.

## 📋 Verificar que los Cambios se Aplicaron

Después de actualizar el módulo:

1. **Ve al menú de Ventas**:
   - **Ventas** → **Pedidos** → **Líneas de Pedido (Cardex)**

2. **Deberías ver**:
   - Una nueva opción de menú llamada "Líneas de Pedido (Cardex)"
   - Una vista con los campos: Descripción, Cantidad, Precio Unitario, Subtotal, Impuestos, Total

3. **Si no ves el menú**:
   - Refresca la página (Ctrl + Shift + R)
   - Cierra sesión y vuelve a iniciar sesión
   - Verifica que el módulo `sale` esté instalado

## 🐛 Solución de Problemas

### El módulo no se actualiza

**Problema**: Los cambios no aparecen después de actualizar.

**Solución**:
1. Limpia la caché del navegador (Ctrl + Shift + R)
2. Reinicia el contenedor: `docker restart odoo-web-1`
3. Verifica los logs: `docker logs odoo-web-1 --tail 50`

### Error: "Module not found"

**Problema**: Odoo no encuentra el módulo.

**Solución**:
1. Verifica que los archivos estén en: `c:\Mis-Documentos\Appex\odoo\dev_addons\inventory_cardex`
2. Verifica que el volumen esté montado: `docker inspect odoo-web-1 | Select-String "extra-addons"`
3. Reinicia el contenedor

### Error: "sale module not installed"

**Problema**: El módulo `sale` no está instalado.

**Solución**:
1. Ve a **Aplicaciones**
2. Busca "Sales" o "Ventas"
3. Haz clic en **Instalar**
4. Espera a que se instale
5. Actualiza `inventory_cardex` nuevamente

## 📊 Verificar Datos

Para verificar que hay datos en `sale_order_line`:

```sql
-- Conectarse a PostgreSQL
docker exec -it odoo-db-1 psql -U odoo -d inventario

-- Ver cuántas líneas de pedido hay
SELECT COUNT(*) FROM sale_order_line;

-- Ver algunas líneas de ejemplo
SELECT name, product_uom_qty, price_unit, price_subtotal, price_tax, price_total 
FROM sale_order_line 
LIMIT 5;

-- Salir
\q
```

Si no hay datos, necesitas crear algunos pedidos de venta primero:
1. Ve a **Ventas** → **Pedidos** → **Presupuestos**
2. Crea un nuevo presupuesto
3. Agrega productos
4. Confirma el pedido

## 🔍 Logs Útiles

Para ver los logs de Odoo en tiempo real:

```powershell
# Ver los últimos 50 logs
docker logs odoo-web-1 --tail 50

# Seguir los logs en tiempo real
docker logs odoo-web-1 --follow

# Ver solo errores
docker logs odoo-web-1 2>&1 | Select-String "ERROR"
```

## ✅ Checklist de Verificación

- [ ] Archivos creados correctamente en `dev_addons/inventory_cardex/`
- [ ] `__manifest__.py` actualizado con dependencia `sale`
- [ ] Contenedor reiniciado: `docker restart odoo-web-1`
- [ ] Módulo actualizado desde la interfaz web
- [ ] Navegador refrescado (Ctrl + Shift + R)
- [ ] Menú "Líneas de Pedido (Cardex)" visible en Ventas
- [ ] Vista muestra los campos correctos

## 📞 Información de Conexión

- **URL Odoo**: http://localhost:8070
- **Base de Datos**: inventario
- **Usuario DB**: 123
- **Contraseña DB**: 123
- **Usuario Maestro Odoo**: 123456
- **Puerto PostgreSQL**: 5432 (interno), no expuesto externamente
