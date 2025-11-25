# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import io
import base64
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class StockCostReportWizard(models.TransientModel):
    _name = 'stock.cost.report.wizard'
    _description = 'Wizard para Reportes de Costos de Inventario'

    date_from = fields.Date(
        string='Fecha Desde',
        required=True,
        default=fields.Date.context_today
    )
    date_to = fields.Date(
        string='Fecha Hasta',
        required=True,
        default=fields.Date.context_today
    )
    report_type = fields.Selection([
        ('pdf', 'Reporte PDF'),
        ('excel', 'Exportar a Excel'),
    ], string='Tipo de Reporte', default='pdf', required=True)
    
    product_ids = fields.Many2many(
        'product.product',
        string='Productos',
        help='Dejar vacío para incluir todos los productos'
    )
    
    location_ids = fields.Many2many(
        'stock.location',
        string='Ubicaciones',
        help='Dejar vacío para incluir todas las ubicaciones'
    )
    
    include_zero_cost = fields.Boolean(
        string='Incluir productos con costo cero',
        default=False
    )

    def action_generate_report(self):
        """Generar el reporte según el tipo seleccionado"""
        self.ensure_one()
        
        if self.report_type == 'pdf':
            return self.action_print_pdf()
        else:
            return self.action_export_excel()

    def _get_report_data(self):
        """Obtener datos para el reporte"""
        self.ensure_one()
        
        # Construir dominio de búsqueda
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('state', '=', 'done'),
        ]
        
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))
        
        if self.location_ids:
            domain.append(('location_id', 'in', self.location_ids.ids))
        
        if not self.include_zero_cost:
            domain.append(('product_cost', '>', 0))
        
        # Obtener movimientos
        moves = self.env['stock.move'].search(domain, order='date desc, id desc')
        
        # Calcular totales
        total_quantity = sum(moves.mapped('product_qty'))
        total_cost = sum(move.product_cost * move.product_qty for move in moves)
        
        return {
            'moves': moves,
            'total_quantity': total_quantity,
            'total_cost': total_cost,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }

    def action_print_pdf(self):
        """Generar reporte PDF"""
        self.ensure_one()
        return self.env.ref('inventory_cardex.action_report_stock_cost').report_action(self)

    def action_export_excel(self):
        """Exportar datos a Excel"""
        self.ensure_one()
        
        # Obtener datos
        data = self._get_report_data()
        moves = data['moves']
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Reporte de Costos')
        
        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yyyy',
            'border': 1
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1
        })
        
        number_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })
        
        total_format = workbook.add_format({
            'bold': True,
            'bg_color': '#E7E6E6',
            'border': 1,
            'num_format': '$#,##0.00'
        })
        
        # Título
        worksheet.merge_range('A1:H1', 'REPORTE DE COSTOS DE INVENTARIO', title_format)
        
        # Información del reporte
        worksheet.write('A2', 'Período:', workbook.add_format({'bold': True}))
        worksheet.write('B2', f"{self.date_from.strftime('%d/%m/%Y')} - {self.date_to.strftime('%d/%m/%Y')}")
        
        worksheet.write('A3', 'Generado:', workbook.add_format({'bold': True}))
        worksheet.write('B3', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        # Encabezados
        row = 5
        headers = [
            'ID', 'Fecha', 'Referencia', 'Producto', 
            'Cantidad', 'Costo Unit.', 'Costo Total', 'Estado'
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(row, col, header, header_format)
        
        # Ajustar anchos de columna
        worksheet.set_column('A:A', 8)   # ID
        worksheet.set_column('B:B', 12)  # Fecha
        worksheet.set_column('C:C', 25)  # Referencia
        worksheet.set_column('D:D', 35)  # Producto
        worksheet.set_column('E:E', 12)  # Cantidad
        worksheet.set_column('F:F', 12)  # Costo Unit
        worksheet.set_column('G:G', 14)  # Costo Total
        worksheet.set_column('H:H', 12)  # Estado
        
        # Datos
        row += 1
        for move in moves:
            total_cost_move = move.product_cost * move.product_qty
            
            worksheet.write(row, 0, move.id, cell_format)
            worksheet.write(row, 1, move.date, date_format)
            worksheet.write(row, 2, move.name or '', cell_format)
            worksheet.write(row, 3, move.product_id.display_name or '', cell_format)
            worksheet.write(row, 4, move.product_qty, number_format)
            worksheet.write(row, 5, move.product_cost, currency_format)
            worksheet.write(row, 6, total_cost_move, currency_format)
            worksheet.write(row, 7, dict(move._fields['state'].selection).get(move.state, ''), cell_format)
            
            row += 1
        
        # Totales
        row += 1
        worksheet.merge_range(row, 0, row, 3, 'TOTALES:', workbook.add_format({'bold': True, 'align': 'right'}))
        worksheet.write(row, 4, data['total_quantity'], workbook.add_format({'bold': True, 'num_format': '#,##0.00', 'bg_color': '#E7E6E6', 'border': 1}))
        worksheet.write(row, 5, '', total_format)
        worksheet.write(row, 6, data['total_cost'], total_format)
        
        # Cerrar archivo
        workbook.close()
        output.seek(0)
        
        # Crear attachment
        filename = f"reporte_costos_{self.date_from}_{self.date_to}.xlsx"
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
