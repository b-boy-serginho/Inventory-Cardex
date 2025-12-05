/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(ListController.prototype, {
    /**
     * Sobrescribir la acción de imprimir para capturar columnas visibles
     * y permitir elegir entre PDF y Excel
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

            // Mostrar diálogo para elegir formato usando confirmación de Odoo
            const useExcel = window.confirm(
                _t("¿Desea exportar a Excel?\n\nClic en Aceptar para Excel\nClic en Cancelar para PDF")
            );

            let action;
            if (useExcel) {
                // Generar Excel
                action = await this.orm.call(
                    'stock.move.line',
                    'generate_dynamic_excel',
                    [recordIds, visibleFields]
                );
            } else {
                // Generar PDF (por defecto)
                action = await this.orm.call(
                'stock.move.line',
                'generate_dynamic_report',
                [recordIds, visibleFields]
            );
            }

            return this.actionService.doAction(action);
        }

        return super.onClickPrint(...arguments);
    },
});
