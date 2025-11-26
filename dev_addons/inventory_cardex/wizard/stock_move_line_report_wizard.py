from odoo import models, fields, api
import io
import xlsxwriter
import base64
from datetime import datetime


class StockMoveLineReportWizard(models.TransientModel):
    _name = 'stock.move.line.report.wizard'
    _description = 'Asistente de Reportes de Movimientos Detallados (Cardex)'

    # Filtros
    date_from = fields.Date(string='Fecha Desde')
    date_to = fields.Date(string='Fecha Hasta')
    product_ids = fields.Many2many('product.product', string='Productos')
    location_id = fields.Many2one('stock.location', string='Ubicación Origen')
    location_dest_id = fields.Many2one('stock.location', string='Ubicación Destino')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('waiting', 'Esperando'),
        ('confirmed', 'Confirmado'),
        ('assigned', 'Disponible'),
        ('done', 'Hecho'),
        ('cancel', 'Cancelado')
    ], string='Estado')
    picking_id = fields.Many2one('stock.picking', string='Transferencia')
    company_id = fields.Many2one('res.company', string='Compañía', 
                                  default=lambda self: self.env.company)

    # Archivo de salida para Excel
    excel_file = fields.Binary(string='Archivo Excel', readonly=True)
    excel_filename = fields.Char(string='Nombre de Archivo', readonly=True)
    
    def _get_domain(self):
        """Construye el dominio basado en los filtros seleccionados"""
        domain = []
        
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))
        if self.location_id:
            domain.append(('location_id', '=', self.location_id.id))
        if self.location_dest_id:
            domain.append(('location_dest_id', '=', self.location_dest_id.id))
        if self.state:
            domain.append(('state', '=', self.state))
        if self.picking_id:
            domain.append(('picking_id', '=', self.picking_id.id))
        if self.company_id:
            domain.append(('company_id', '=', self.company_id.id))
            
        return domain

    def action_generate_pdf(self):
        """Genera el reporte PDF con los filtros aplicados"""
        domain = self._get_domain()
        move_lines = self.env['stock.move.line'].search(domain, order='date desc, product_id')
        
        if not move_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin datos',
                    'message': 'No se encontraron movimientos con los filtros seleccionados.',
                    'type': 'warning',
                }
            }
        
        # Retorna la acción del reporte PDF con los registros filtrados
        return self.env.ref('inventory_cardex.action_report_stock_move_line_cardex').report_action(move_lines)

    def action_generate_excel(self):
        """Genera el reporte Excel con los filtros aplicados"""
        domain = self._get_domain()
        move_lines = self.env['stock.move.line'].search(domain, order='date desc, product_id')
        
        if not move_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin datos',
                    'message': 'No se encontraron movimientos con los filtros seleccionados.',
                    'type': 'warning',
                }
            }
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Movimientos Cardex')
        
        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4F81BD',
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
        
        # Encabezados
        headers = [
            'Producto',
            'Costo Unitario',
            'Costo Total',
            'Cantidad',
            'UdM',
            'Ubicación Origen',
            'Ubicación Destino',
            'Lote/Serie',
            'Paquete',
            'Transferencia',
            'Estado',
            'Fecha',
            'Referencia'
        ]
        
        # Escribir encabezados
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        # Ajustar anchos de columna
        worksheet.set_column('A:A', 30)  # Producto
        worksheet.set_column('B:C', 15)  # Costos
        worksheet.set_column('D:D', 12)  # Cantidad
        worksheet.set_column('E:E', 10)  # UdM
        worksheet.set_column('F:G', 25)  # Ubicaciones
        worksheet.set_column('H:I', 20)  # Lote/Paquete
        worksheet.set_column('J:J', 20)  # Transferencia
        worksheet.set_column('K:K', 12)  # Estado
        worksheet.set_column('L:L', 18)  # Fecha
        worksheet.set_column('M:M', 20)  # Referencia
        
        # Escribir datos
        row = 1
        total_cost = 0.0
        
        for line in move_lines:
            worksheet.write(row, 0, line.product_id.display_name or '', text_format)
            worksheet.write(row, 1, line.product_cost or 0.0, currency_format)
            worksheet.write(row, 2, line.line_cost or 0.0, currency_format)
            worksheet.write(row, 3, line.quantity or 0.0, number_format)
            worksheet.write(row, 4, line.product_uom_id.name or '', text_format)
            worksheet.write(row, 5, line.location_id.complete_name or '', text_format)
            worksheet.write(row, 6, line.location_dest_id.complete_name or '', text_format)
            worksheet.write(row, 7, line.lot_id.name or '', text_format)
            worksheet.write(row, 8, line.package_id.name or '', text_format)
            worksheet.write(row, 9, line.picking_id.name or '', text_format)
            worksheet.write(row, 10, dict(line._fields['state'].selection).get(line.state, ''), text_format)
            
            if line.date:
                worksheet.write_datetime(row, 11, line.date, date_format)
            else:
                worksheet.write(row, 11, '', text_format)
                
            worksheet.write(row, 12, line.reference or '', text_format)
            
            total_cost += line.line_cost or 0.0
            row += 1
        
        # Totales
        row += 1
        total_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9E1F2',
            'border': 1,
            'align': 'right'
        })
        
        worksheet.write(row, 0, 'TOTALES:', total_format)
        worksheet.write(row, 1, '', total_format)
        worksheet.write(row, 2, total_cost, currency_format)
        
        # Guardar
        workbook.close()
        output.seek(0)
        
        # Generar nombre de archivo
        filename = 'Cardex_Detallado_%s.xlsx' % datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Actualizar el wizard con el archivo generado
        self.write({
            'excel_file': base64.b64encode(output.read()),
            'excel_filename': filename,
        })
        
        # Retornar acción para descargar el archivo
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content?model=stock.move.line.report.wizard&id=%s&field=excel_file&download=true&filename=%s' % (self.id, filename),
            'target': 'self',
        }
