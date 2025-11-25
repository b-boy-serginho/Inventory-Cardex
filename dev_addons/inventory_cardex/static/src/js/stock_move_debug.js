/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";

/**
 * Widget de Debug para verificar campos en stock.move
 * Este widget se carga automáticamente y muestra información en la consola
 */
export class StockMoveDebugController extends ListController {
    
    setup() {
        super.setup();
        
        // Debug: Verificar información del modelo cuando se carga la vista
        console.log("=".repeat(80));
        console.log("🔍 DEBUG: Stock Move List View");
        console.log("=".repeat(80));
        
        // Información del modelo
        console.log("📋 Modelo:", this.props.resModel);
        
        // Verificar si estamos en la vista de stock.move
        if (this.props.resModel === 'stock.move') {
            this.debugStockMoveFields();
        }
    }
    
    debugStockMoveFields() {
        console.log("\n🔎 Verificando campos disponibles en stock.move...\n");
        
        // Obtener los campos de la vista
        const fields = this.props.fields;
        
        console.log("📊 Total de campos en la vista:", Object.keys(fields).length);
        
        // Buscar campos relacionados con costo
        const costFields = Object.keys(fields).filter(field => 
            field.includes('cost') || field.includes('price')
        );
        
        console.log("\n💰 Campos relacionados con costo/precio:");
        if (costFields.length > 0) {
            costFields.forEach(field => {
                console.log(`  ✓ ${field}:`, fields[field]);
            });
        } else {
            console.log("  ⚠️ No se encontraron campos de costo");
        }
        
        // Verificar específicamente los campos que agregamos
        const ourFields = ['product_cost', 'total_cost', 'company_currency_id'];
        console.log("\n🎯 Verificando campos personalizados:");
        ourFields.forEach(fieldName => {
            if (fields[fieldName]) {
                console.log(`  ✅ ${fieldName}: EXISTE`);
                console.log(`     Tipo: ${fields[fieldName].type}`);
                console.log(`     String: ${fields[fieldName].string}`);
            } else {
                console.log(`  ❌ ${fieldName}: NO EXISTE`);
            }
        });
        
        // Listar TODOS los campos disponibles
        console.log("\n📝 Lista completa de campos:");
        Object.keys(fields).sort().forEach(field => {
            console.log(`  - ${field} (${fields[field].type})`);
        });
        
        console.log("\n" + "=".repeat(80));
        console.log("💡 Si 'product_cost' NO existe, el módulo no se actualizó correctamente");
        console.log("💡 Si 'product_cost' SÍ existe pero no se ve, es un problema de vista");
        console.log("=".repeat(80) + "\n");
    }
}

// Registrar el controlador personalizado
export const stockMoveDebugListView = {
    ...listView,
    Controller: StockMoveDebugController,
};

registry.category("views").add("stock_move_debug_tree", stockMoveDebugListView);
