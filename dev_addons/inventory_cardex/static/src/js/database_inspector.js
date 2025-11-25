/** @odoo-module **/

// Script sencillo para inspeccionar datos desde consola del navegador
// Compatible con Odoo 17

console.log("🔍 Inspector de Base de Datos - Inventory Cardex CARGADO");

// Función simple para inspeccionar stock.move
window.inspectStockMove = function (limit) {
    limit = limit || 10;

    var rpcPromise = $.ajax({
        url: '/web/dataset/call_kw/stock.move/search_read',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                model: 'stock.move',
                method: 'search_read',
                args: [[]],
                kwargs: {
                    fields: ['id', 'name', 'product_id', 'product_cost', 'total_cost', 'product_qty', 'date'],
                    limit: limit,
                    order: 'id desc'
                }
            },
            id: new Date().getTime()
        })
    });

    rpcPromise.done(function (response) {
        if (response.result) {
            console.log("✅ Datos de stock.move (últimos " + limit + " registros):");
            console.table(response.result);
            console.log("📋 Tabla en PostgreSQL: stock_move");
            console.log("📋 Campo en BD: product_cost");
            console.log("📊 Total registros:", response.result.length);
        }
    }).fail(function (error) {
        console.error("❌ Error:", error);
    });

    return rpcPromise;
};

// Función simple para inspeccionar stock.move.line
window.inspectStockMoveLine = function (limit) {
    limit = limit || 10;

    var rpcPromise = $.ajax({
        url: '/web/dataset/call_kw/stock.move.line/search_read',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                model: 'stock.move.line',
                method: 'search_read',
                args: [[]],
                kwargs: {
                    fields: ['id', 'product_id', 'product_cost', 'line_cost', 'quantity', 'date'],
                    limit: limit,
                    order: 'id desc'
                }
            },
            id: new Date().getTime()
        })
    });

    rpcPromise.done(function (response) {
        if (response.result) {
            console.log("✅ Datos de stock.move.line (últimos " + limit + " registros):");
            console.table(response.result);
            console.log("📋 Tabla en PostgreSQL: stock_move_line");
            console.log("📋 Campo en BD: product_cost");
            console.log("📊 Total registros:", response.result.length);
        }
    }).fail(function (error) {
        console.error("❌ Error:", error);
    });

    return rpcPromise;
};

// Función para verificar si el campo está guardado en BD
window.checkFieldInDB = function (model_name) {
    var rpcPromise = $.ajax({
        url: '/web/dataset/call_kw/ir.model.fields/search_read',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            jsonrpc: '2.0',
            method: 'call',
            params: {
                model: 'ir.model.fields',
                method: 'search_read',
                args: [[['model', '=', model_name], ['name', '=', 'product_cost']]],
                kwargs: {
                    fields: ['name', 'field_description', 'ttype', 'store', 'model']
                }
            },
            id: new Date().getTime()
        })
    });

    rpcPromise.done(function (response) {
        if (response.result && response.result.length > 0) {
            console.log("✅ Campo 'product_cost' en modelo '" + model_name + "':");
            console.table(response.result);

            if (response.result[0].store) {
                console.log("✅ El campo SÍ está guardado en BD (store=True)");
            } else {
                console.log("⚠️ El campo NO está guardado en BD (store=False)");
            }
        } else {
            console.log("❌ Campo no encontrado en el modelo " + model_name);
        }
    }).fail(function (error) {
        console.error("❌ Error:", error);
    });

    return rpcPromise;
};

// Función de ayuda
window.showDBInspectorHelp = function () {
    console.log("╔════════════════════════════════════════════════════════════╗");
    console.log("║           🔍 DATABASE INSPECTOR - COMANDOS                 ║");
    console.log("╠════════════════════════════════════════════════════════════╣");
    console.log("║                                                            ║");
    console.log("║  inspectStockMove(10)      - Ver últimos 10 stock.move    ║");
    console.log("║  inspectStockMoveLine(10)  - Ver últimos 10 move lines    ║");
    console.log("║  checkFieldInDB('stock.move') - Verificar campo en BD     ║");
    console.log("║  showDBInspectorHelp()     - Mostrar esta ayuda           ║");
    console.log("║                                                            ║");
    console.log("║  📋 Tablas en PostgreSQL:                                 ║");
    console.log("║     • stock_move       → Campo: product_cost              ║");
    console.log("║     • stock_move_line  → Campo: product_cost              ║");
    console.log("║                                                            ║");
    console.log("╚════════════════════════════════════════════════════════════╝");
};

// Mostrar ayuda inicial
console.log("✅ Funciones disponibles:");
console.log("   • inspectStockMove(10)");
console.log("   • inspectStockMoveLine(10)");
console.log("   • checkFieldInDB('stock.move')");
console.log("   • showDBInspectorHelp()");
console.log("");
console.log("💡 Ejecuta: showDBInspectorHelp() para ver ayuda completa");
