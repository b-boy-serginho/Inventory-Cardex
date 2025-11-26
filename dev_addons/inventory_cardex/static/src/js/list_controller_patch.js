/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";

patch(ListController.prototype, {
    /**
     * Sobrescribir la acción de imprimir para capturar columnas visibles
     */
    async onClickPrint() {
        const recordIds = await this.getSelectedResIds();

        if (this.props.resModel === 'stock.move.line' && recordIds.length > 0) {
            // Obtener las columnas visibles
            const visibleFields = [];
            const columns = this.model.root.columns;

            for (const column of columns) {
                if (column.type === 'field' && !column.column_invisible) {
                    visibleFields.push(column.name);
                }
            }

            console.log('Columnas visibles:', visibleFields);
            console.log('IDs seleccionados:', recordIds);

            // Llamar al método del backend para generar el reporte con columnas dinámicas
            const action = await this.orm.call(
                'stock.move.line',
                'generate_dynamic_report',
                [recordIds, visibleFields]
            );

            return this.actionService.doAction(action);
        }

        return super.onClickPrint(...arguments);
    },
});
