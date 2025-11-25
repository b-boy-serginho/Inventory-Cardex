# Guía para Actualizar el Módulo inventory_cardex

## ⚠️ IMPORTANTE: Debes actualizar el módulo desde la interfaz de Odoo

### Pasos para Actualizar:

1. **Activar Modo Desarrollador**
   - Ve a **Configuración** (Settings)
   - Desplázate hasta el final de la página
   - Click en **Activar el modo de desarrollador**
   - O usa la URL directa: `http://localhost:8069/web?debug=1`

2. **Ir a Aplicaciones**
   - Click en el menú principal (☰)
   - Selecciona **Aplicaciones** (Apps)

3. **Actualizar Lista de Aplicaciones**
   - Click en el menú de tres puntos (⋮) o en el botón de opciones
   - Selecciona **Actualizar lista de aplicaciones** (Update Apps List)
   - Click en **Actualizar** en el diálogo que aparece

4. **Buscar y Actualizar el Módulo**
   - En el buscador, escribe: `inventory_cardex`
   - Encuentra el módulo "Inventory Cardex"
   - Click en **Actualizar** (Upgrade)
   - Espera a que termine la actualización

5. **Verificar los Cambios**
   - Ve a **Inventario** → **Operaciones** → **Historial de Movimientos**
   - Deberías ver la nueva columna **"Costo Unit."**
   - Si no aparece, click en el icono de columnas (⋮) a la derecha
   - Activa la columna "Costo Unit." si está oculta

## 🔍 Si el campo NO aparece después de actualizar:

### Verificación 1: Comprobar que el módulo se cargó
1. Activa el modo desarrollador
2. Ve a **Configuración** → **Técnico** → **Modelos**
3. Busca el modelo `stock.move`
4. Click en el modelo
5. Ve a la pestaña **Campos**
6. Busca el campo `product_cost`
   - Si NO está, el módulo no se actualizó correctamente
   - Si SÍ está, el problema es en la vista

### Verificación 2: Comprobar la vista
1. Ve a **Configuración** → **Técnico** → **Vistas**
2. Busca: `stock.move.tree.inherit.cardex`
3. Si no existe, el módulo no se actualizó

### Verificación 3: Ver logs de error
1. Abre la consola del navegador (F12)
2. Ve a la pestaña **Console**
3. Busca errores en rojo
4. Comparte los errores si los hay

## 🐛 Solución de Problemas Comunes

### Problema: "El módulo no aparece en la lista"
**Solución**: 
- Asegúrate de que el módulo esté en la carpeta correcta
- Verifica que el archivo `__manifest__.py` sea válido
- Reinicia el contenedor: `docker-compose restart web`

### Problema: "Error al actualizar el módulo"
**Solución**:
- Revisa los logs: `docker logs odoo-web-1 --tail 100`
- Busca errores de sintaxis en Python o XML
- Verifica que todos los archivos tengan la codificación UTF-8

### Problema: "El campo aparece pero sin valores"
**Solución**:
- Verifica que los productos tengan un costo configurado
- Ve a **Inventario** → **Productos** → [Selecciona un producto]
- En la pestaña **Inventario**, verifica el campo **Costo**

## 📝 Comandos Útiles

```bash
# Ver logs en tiempo real
docker logs -f odoo-web-1

# Reiniciar Odoo
docker-compose restart web

# Entrar al contenedor
docker exec -it odoo-web-1 bash

# Ver archivos del módulo dentro del contenedor
docker exec odoo-web-1 ls -la /mnt/extra-addons/inventory_cardex/
```

## ✅ Checklist de Verificación

- [ ] Modo desarrollador activado
- [ ] Lista de aplicaciones actualizada
- [ ] Módulo "Inventory Cardex" actualizado
- [ ] Sin errores en la consola del navegador
- [ ] Campo `product_cost` existe en el modelo `stock.move`
- [ ] Vista `stock.move.tree.inherit.cardex` existe
- [ ] Columna "Costo Unit." visible en el historial de movimientos

---

**Nota**: Si después de seguir todos estos pasos el campo aún no aparece, puede haber un problema de permisos o de caché. En ese caso, intenta:
1. Limpiar la caché del navegador (Ctrl + Shift + Delete)
2. Abrir en modo incógnito
3. Verificar los permisos del usuario actual
