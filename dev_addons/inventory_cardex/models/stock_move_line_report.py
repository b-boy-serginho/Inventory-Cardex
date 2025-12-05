from odoo import models, api
import io
import base64
from datetime import datetime
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


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
            # Campos de inventario
            'date': 'Fecha',
            'reference': 'Referencia',
            'location_id': 'Desde',
            'location_dest_id': 'A',
            'product_id': 'Producto',
            'quantity': 'Cantidad',
            'product_cost': 'Costo Unitario',
            'line_cost': 'Costo Total',
            'state': 'Estado',
            
            # Campos de venta (sale_order_line)
            'has_sale': 'Tiene Venta',
            'sale_order_id': 'Pedido Venta',
            'sale_product_name': 'Descripción Venta',
            'sale_product_uom_qty': 'Cantidad Vendida',
            'sale_price_unit': 'Precio Unit. Venta',
            'sale_price_subtotal': 'Subtotal Venta',
            'sale_price_tax': 'Impuestos Venta',
            'sale_price_total': 'Total Venta',
            'sale_state': 'Estado Venta',
            
            # Campos de compra (purchase_order_line)
            'has_purchase': 'Tiene Compra',
            'purchase_order_id': 'Pedido Compra',
            'purchase_product_name': 'Descripción Compra',
            'purchase_product_qty': 'Cantidad Comprada',
            'purchase_price_unit': 'Precio Unit. Compra',
            'purchase_price_subtotal': 'Subtotal Compra',
            'purchase_price_tax': 'Impuestos Compra',
            'purchase_price_total': 'Total Compra',
            'purchase_state': 'Estado Compra',
            
            # Campos opcionales de inventario
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

    @api.model
    def generate_dynamic_excel(self, record_ids, visible_fields):
        """
        Genera un reporte Excel con las columnas visibles especificadas
        
        :param record_ids: IDs de los registros a exportar
        :param visible_fields: Lista de nombres técnicos de campos visibles
        :return: Acción para descargar el archivo Excel
        """
        records = self.browse(record_ids)
        
        if not records:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin datos',
                    'message': 'No hay registros para exportar.',
                    'type': 'warning',
                }
            }
        
        # Mapeo de nombres técnicos a nombres legibles
        field_labels = {
            # Campos de inventario
            'date': 'Fecha',
            'reference': 'Referencia',
            'location_id': 'Desde',
            'location_dest_id': 'A',
            'product_id': 'Producto',
            'quantity': 'Cantidad',
            'product_cost': 'Costo Unitario',
            'line_cost': 'Costo Total',
            'state': 'Estado',
            
            # Campos de venta (sale_order_line)
            'has_sale': 'Tiene Venta',
            'sale_order_id': 'Pedido Venta',
            'sale_product_name': 'Descripción Venta',
            'sale_product_uom_qty': 'Cantidad Vendida',
            'sale_price_unit': 'Precio Unit. Venta',
            'sale_price_subtotal': 'Subtotal Venta',
            'sale_price_tax': 'Impuestos Venta',
            'sale_price_total': 'Total Venta',
            'sale_state': 'Estado Venta',
            
            # Campos de compra (purchase_order_line)
            'has_purchase': 'Tiene Compra',
            'purchase_order_id': 'Pedido Compra',
            'purchase_product_name': 'Descripción Compra',
            'purchase_product_qty': 'Cantidad Comprada',
            'purchase_price_unit': 'Precio Unit. Compra',
            'purchase_price_subtotal': 'Subtotal Compra',
            'purchase_price_tax': 'Impuestos Compra',
            'purchase_price_total': 'Total Compra',
            'purchase_state': 'Estado Compra',
            
            # Campos opcionales de inventario
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
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Cardex Valorizado')
        
        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#7b68ab',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })
        
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yyyy hh:mm',
            'border': 1
        })
        
        text_format = workbook.add_format({
            'border': 1
        })
        
        boolean_format = workbook.add_format({
            'border': 1,
            'align': 'center'
        })
        
        # Escribir encabezados
        headers = [field_data['label'] for field_data in visible_field_data]
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        # Ajustar anchos de columna (ajustar según el contenido)
        for col, field_data in enumerate(visible_field_data):
            field_name = field_data['technical_name']
            # Ajustar ancho según el tipo de campo
            if field_name in ['product_id', 'sale_product_name', 'purchase_product_name', 'reference']:
                worksheet.set_column(col, col, 35)
            elif field_name in ['location_id', 'location_dest_id', 'picking_id']:
                worksheet.set_column(col, col, 25)
            elif field_name in ['date']:
                worksheet.set_column(col, col, 18)
            elif field_name in ['product_cost', 'line_cost', 'sale_price_unit', 'sale_price_subtotal', 
                               'sale_price_total', 'purchase_price_unit', 'purchase_price_subtotal',
                               'purchase_price_total']:
                worksheet.set_column(col, col, 15)
            elif field_name in ['quantity', 'sale_product_uom_qty', 'purchase_product_qty']:
                worksheet.set_column(col, col, 12)
            else:
                worksheet.set_column(col, col, 15)
        
        # Función auxiliar para obtener el valor formateado de un campo
        def get_field_value(record, field_name):
            """Obtiene el valor de un campo de un registro y lo formatea"""
            if not hasattr(record, field_name):
                return ''
            
            value = getattr(record, field_name, None)
            
            # Manejar diferentes tipos de campos
            if value is None or value is False:
                return ''
            
            # Many2one fields (verificar si es un recordset de Odoo)
            if hasattr(value, 'display_name') and hasattr(value, '_name'):
                return value.display_name or ''
            
            # Boolean fields
            if isinstance(value, bool):
                return 'Sí' if value else 'No'
            
            # Selection fields (estado y otros campos con selection)
            # Verificar si el campo tiene selection antes de intentar acceder
            if field_name in record._fields:
                field_def = record._fields[field_name]
                if hasattr(field_def, 'selection') and field_def.selection:
                    selection = field_def.selection
                    # Selection puede ser una lista/tupla o una función
                    try:
                        if callable(selection):
                            # Si es una función, llamarla con el recordset
                            selection_list = selection(record)
                        else:
                            # Si es una lista/tupla, usarla directamente
                            selection_list = selection
                        
                        if selection_list:
                            selection_dict = dict(selection_list)
                            return selection_dict.get(value, str(value))
                    except (TypeError, ValueError):
                        # Si hay error al procesar selection, continuar con el valor original
                        pass
            
            return value
        
        # Escribir datos
        for row, record in enumerate(records, start=1):
            for col, field_data in enumerate(visible_field_data):
                field_name = field_data['technical_name']
                
                # Obtener valor directo del campo
                if not hasattr(record, field_name):
                    worksheet.write(row, col, '', text_format)
                    continue
                
                raw_value = getattr(record, field_name, None)
                
                # Determinar formato según el tipo de campo
                if field_name == 'date':
                    if raw_value:
                        try:
                            worksheet.write_datetime(row, col, raw_value, date_format)
                        except:
                            worksheet.write(row, col, str(raw_value), text_format)
                    else:
                        worksheet.write(row, col, '', text_format)
                elif field_name in ['product_cost', 'line_cost', 'sale_price_unit', 'sale_price_subtotal',
                                   'sale_price_total', 'purchase_price_unit', 'purchase_price_subtotal',
                                   'purchase_price_total', 'sale_price_tax', 'purchase_price_tax']:
                    try:
                        # Manejar campos monetary que pueden ser float o recordset
                        if hasattr(raw_value, '__float__'):
                            float_value = float(raw_value)
                        elif isinstance(raw_value, (int, float)):
                            float_value = float(raw_value)
                        else:
                            float_value = 0.0
                        worksheet.write(row, col, float_value, currency_format)
                    except (ValueError, TypeError, AttributeError):
                        worksheet.write(row, col, get_field_value(record, field_name), text_format)
                elif field_name in ['quantity', 'sale_product_uom_qty', 'purchase_product_qty',
                                   'incoming_qty', 'outgoing_qty']:
                    try:
                        if isinstance(raw_value, (int, float)):
                            float_value = float(raw_value)
                        else:
                            float_value = 0.0
                        worksheet.write(row, col, float_value, number_format)
                    except (ValueError, TypeError):
                        worksheet.write(row, col, get_field_value(record, field_name), text_format)
                elif field_name in ['has_sale', 'has_purchase']:
                    bool_value = get_field_value(record, field_name)
                    worksheet.write(row, col, bool_value, boolean_format)
                else:
                    # Para campos de texto y relaciones
                    value = get_field_value(record, field_name)
                    worksheet.write(row, col, str(value) if value else '', text_format)
        
        # Cerrar workbook
        workbook.close()
        output.seek(0)
        
        # Crear nombre de archivo
        product_name = records[0].product_id.name if records and records[0].product_id else 'Cardex'
        filename = 'Cardex_Valorizado_%s_%s.xlsx' % (
            product_name.replace('/', '_').replace('\\', '_')[:50],
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        
        # Crear attachment
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'store_fname': filename,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        
        # Retornar acción para descargar
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
