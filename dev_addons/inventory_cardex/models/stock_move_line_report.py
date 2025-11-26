from odoo import models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.model
    def generate_dynamic_report(self, record_ids, visible_fields):
        """
        Genera un reporte PDF con las columnas visibles especificadas
        
        :param record_ids: IDs de los registros a imprimir
        :param visible_fields: Lista de nombres técnicos de campos visibles
        :return: Acción de reporte
        """
        records = self.browse(record_ids)
        
        # Mapeo de nombres técnicos a nombres legibles (en el orden deseado)
        field_labels = {
            'date': 'Fecha',
            'reference': 'Referencia',
            'location_id': 'Desde',
            'location_dest_id': 'A',
            'product_id': 'Producto',
            'quantity': 'Cantidad',
            'product_cost': 'Costo Unitario',
            'line_cost': 'Costo Total',
            'state': 'Estado',
            # Campos opcionales
            'product_uom_id': 'UdM',
            'incoming_qty': 'Qty Entrante',
            'outgoing_qty': 'Qty Saliente',
            'lot_id': 'Número de serie/lote',
            'picking_id': 'Transferir',
            'package_id': 'Paquete Origen',
            'result_package_id': 'Paquete Destino',
            'owner_id': 'Propietario',
            'company_id': 'Empresa',
            'company_currency_id': 'Currency',
            'product_uom_category_id': 'Categoría',
        }
        
        # Filtrar solo los campos visibles
        visible_field_data = []
        for field in visible_fields:
            if field in field_labels:
                visible_field_data.append({
                    'technical_name': field,
                    'label': field_labels[field]
                })
        
        # Pasar los datos al contexto del reporte
        return self.env.ref('inventory_cardex.action_report_stock_move_line_cardex').report_action(
            records,
            data={
                'visible_fields': visible_field_data,
                'record_ids': record_ids
            }
        )
