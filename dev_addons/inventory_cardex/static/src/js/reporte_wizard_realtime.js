/** @odoo-module **/

import { FormController } from "@web/views/form/form_controller";
import { patch } from "@web/core/utils/patch";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        // Solo aplicar para el wizard de reporte
        if (this.props.resModel === 'reporte.wizard') {
            this._setupRealtimeUpdate();
        }
    },

    async onWillStart() {
        await super.onWillStart?.();
        // Asegurar que el campo computado se calcule al cargar el wizard
        if (this.props.resModel === 'reporte.wizard') {
            const record = this.model.root;
            if (record) {
                // Esperar a que el registro se cargue completamente
                await record.load();
                // Forzar el cálculo del campo computado
                if (record.data && record.data.move_line_ids) {
                    const count = Array.isArray(record.data.move_line_ids) 
                        ? record.data.move_line_ids.length 
                        : 0;
                    record.update({ moves_count: count });
                }
            }
        }
    },

    _setupRealtimeUpdate() {
        // Interceptar el método que maneja las acciones de botones
        const originalOnButtonClicked = this.onButtonClicked;
        this.onButtonClicked = async (params) => {
            // Si se ejecutó la acción de limpiar movimientos
            if (params.name === 'action_clear_movements') {
                const record = this.model.root;
                if (record) {
                    // Actualizar inmediatamente en el cliente
                    record.update({ 
                        move_line_ids: [],
                        moves_count: 0
                    });
                    
                    // Forzar el renderizado inmediato
                    this.render();
                    
                    // Ejecutar la acción del servidor
                    try {
                        await originalOnButtonClicked.call(this, params);
                        // Recargar después de que el servidor procese
                        await record.load();
                        this.render();
                    } catch (err) {
                        console.error('Error al limpiar movimientos:', err);
                    }
                    
                    return false;
                }
            }
            
            // Llamar al método original para otras acciones
            return await originalOnButtonClicked.call(this, params);
        };
    },
});

