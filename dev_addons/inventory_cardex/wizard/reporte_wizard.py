# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import io
import base64
import csv
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class ReporteWizard(models.TransientModel):
    _name = 'reporte.wizard'
    _description = 'Wizard de Reporte del Kardex'

    move_line_ids = fields.Many2many(
        'stock.move.line',
        string='Movimientos Seleccionados'
    )
    
    moves_count = fields.Integer(
        string='Cantidad de Movimientos',
        compute='_compute_moves_count',
        store=False,
        default=0
    )
    
    date_from = fields.Date(
        string='Fecha Desde',
        default=fields.Date.context_today
    )
    
    date_to = fields.Date(
        string='Fecha Hasta',
        default=fields.Date.context_today
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        help='Dejar vacío para incluir todos los productos'
    )
    
    is_wizard = fields.Boolean(
        string='Habilitar Filtros',
        default=False,
        help='Activar para habilitar los campos de fecha y producto'
    )
    
    @api.depends('is_wizard')
    def _compute_not_is_wizard(self):
        """Campo computado inverso de is_wizard para usar en readonly"""
        for record in self:
            record.not_is_wizard = not record.is_wizard
    
    not_is_wizard = fields.Boolean(
        string='Not Is Wizard',
        compute='_compute_not_is_wizard',
        store=False
    )
    
    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ], string='Tipo de reporte', default='pdf', required=True)

    @api.depends('move_line_ids')
    def _compute_moves_count(self):
        for wizard in self:
            # Calcular el número de movimientos
            wizard.moves_count = len(wizard.move_line_ids) if wizard.move_line_ids else 0

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Obtener los IDs del contexto si vienen de una selección
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['move_line_ids'] = [(6, 0, active_ids)]
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribir create para calcular moves_count al crear"""
        wizards = super().create(vals_list)
        # Forzar el cálculo del campo computado después de crear
        for wizard in wizards:
            wizard._compute_moves_count()
        return wizards

    def write(self, vals):
        """Sobrescribir write para recalcular moves_count cuando cambia move_line_ids o product_id"""
        result = super().write(vals)
        if 'move_line_ids' in vals or 'product_id' in vals:
            # Forzar el recálculo del campo computado
            self._compute_moves_count()
        return result
    
    @api.onchange('product_id', 'date_from', 'date_to')
    def _onchange_product_or_dates(self):
        """Actualizar los movimientos cuando cambia el producto o las fechas"""
        if self.product_id:
            # Buscar todos los movimientos del producto
            domain = [('product_id', '=', self.product_id.id)]
            if self.date_from:
                domain.append(('date', '>=', self.date_from))
            if self.date_to:
                domain.append(('date', '<=', self.date_to))
            
            # Ordenar de más antiguo a más reciente
            move_lines = self.env['stock.move.line'].search(domain, order='date asc, id asc')
            self.move_line_ids = move_lines
            self._compute_moves_count()

    def read(self, fields=None, load='_classic_read'):
        """Sobrescribir read para asegurar que moves_count se calcule"""
        result = super().read(fields, load)
        # Si se está leyendo moves_count o move_line_ids, forzar el cálculo
        if fields is None or 'moves_count' in fields or 'move_line_ids' in fields:
            for record in self:
                record._compute_moves_count()
        return result

    def action_clear_movements(self):
        """Limpiar los movimientos seleccionados"""
        self.ensure_one()
        self.move_line_ids = [(5, 0, 0)]  # Limpiar todos los registros
        # El campo computado moves_count se actualizará automáticamente
        # debido al decorador @api.depends('move_line_ids')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Movimientos limpiados',
                'message': 'Los movimientos seleccionados han sido limpiados.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_generate_report(self):
        """Generar el reporte según el tipo seleccionado"""
        self.ensure_one()
        
        # Obtener los movimientos según los filtros
        move_lines = self._get_move_lines()
        
        if not move_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin movimientos',
                    'message': 'No se encontraron movimientos con los filtros seleccionados. Por favor, seleccione movimientos o un producto para generar el reporte.',
                    'type': 'warning',
                }
            }
        
        if self.report_type == 'pdf':
            return self._generate_pdf(move_lines)
        elif self.report_type == 'excel':
            return self._generate_excel(move_lines)
        elif self.report_type == 'csv':
            return self._generate_csv(move_lines)

    def _get_move_lines(self):
        """Obtener los movimientos según los filtros aplicados"""
        self.ensure_one()
        
        # Si hay un producto seleccionado, buscar TODOS los movimientos de ese producto
        # (esto tiene prioridad sobre los movimientos seleccionados manualmente)
        if self.product_id:
            domain = [('product_id', '=', self.product_id.id)]
            
            # Si hay fechas seleccionadas, filtrar por rango de fechas
            if self.date_from:
                domain.append(('date', '>=', self.date_from))
            if self.date_to:
                domain.append(('date', '<=', self.date_to))
            
            # Buscar todos los movimientos del producto (ordenados de más antiguo a más reciente)
            move_lines = self.env['stock.move.line'].search(domain, order='date asc, id asc')
        elif self.move_line_ids:
            # Si no hay producto pero hay movimientos seleccionados, usar esos
            domain = [('id', 'in', self.move_line_ids.ids)]
            
            # Si hay fechas seleccionadas, también filtrar por fechas
            if self.date_from:
                domain.append(('date', '>=', self.date_from))
            if self.date_to:
                domain.append(('date', '<=', self.date_to))
            
            # Ordenar de más antiguo a más reciente
            move_lines = self.env['stock.move.line'].search(domain, order='date asc, id asc')
        else:
            # Si no hay filtros, retornar vacío
            move_lines = self.env['stock.move.line']
        
        return move_lines

    def _generate_pdf(self, move_lines=None):
        """Generar reporte PDF"""
        if move_lines is None:
            move_lines = self._get_move_lines()
        return self.env.ref('inventory_cardex.action_report_stock_move_line_cardex').report_action(move_lines)

    def _generate_excel(self, move_lines=None):
        """Generar reporte Excel con la misma estructura que el PDF"""
        if move_lines is None:
            move_lines = self._get_move_lines()
        
        if not move_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin datos',
                    'message': 'No hay registros para exportar.',
                    'type': 'warning',
                }
            }
        
        # Crear archivo Excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Kardex Valorizado')
        
        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#7b68ab',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        subheader_format = workbook.add_format({
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
        
        integer_format = workbook.add_format({
            'num_format': '#,##0',
            'border': 1
        })
        
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yyyy hh:mm',
            'border': 1
        })
        
        text_format = workbook.add_format({
            'border': 1
        })
        
        purchase_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1,
            'font_color': '#00b050',
            'bold': True
        })
        
        purchase_currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1,
            'font_color': '#00b050',
            'bold': True
        })
        
        sale_format = workbook.add_format({
            'num_format': '#,##0.00',
            'border': 1,
            'font_color': '#ff0000',
            'bold': True
        })
        
        sale_currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1,
            'font_color': '#ff0000',
            'bold': True
        })
        
        total_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1
        })
        
        total_currency_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1,
            'num_format': '$#,##0.00'
        })
        
        total_number_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1,
            'num_format': '#,##0.00'
        })
        
        total_integer_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1,
            'num_format': '#,##0'
        })
        
        # Escribir encabezados principales (fila 0)
        worksheet.merge_range(0, 0, 0, 1, '', header_format)  # Fecha y Referencia
        worksheet.merge_range(0, 2, 0, 4, 'ENTRADA', header_format)
        worksheet.merge_range(0, 5, 0, 7, 'SALIDA', header_format)
        worksheet.merge_range(0, 8, 0, 10, 'SALDO FINAL', header_format)
        
        # Escribir encabezados de columnas (fila 1)
        headers = [
            'Fecha', 'REFERENCIA',
            'CANTIDAD', 'PRECIO', 'SUBTOTAL',  # ENTRADA
            'CANTIDAD', 'PRECIO', 'SUBTOTAL',  # SALIDA
            'CANTIDAD', 'COSTO PROMEDIO', 'VALOR TOTAL'  # SALDO FINAL
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(1, col, header, subheader_format)
        
        # Ajustar anchos de columna
        worksheet.set_column('A:A', 18)  # Fecha
        worksheet.set_column('B:B', 25)  # Referencia
        worksheet.set_column('C:E', 15)  # Entrada
        worksheet.set_column('F:H', 15)  # Salida
        worksheet.set_column('I:K', 15)  # Saldo Final
        
        # Inicializar variables de saldo (igual que en el PDF)
        balance_qty = 0.0
        balance_total_cost = 0.0
        balance_avg_cost = 0.0
        last_avg_cost = 0.0
        total_purchase_qty = 0.0
        total_purchase_subtotal = 0.0
        total_sale_qty = 0.0
        total_sale_subtotal = 0.0
        first_sale_qty = 0.0
        first_sale_subtotal = 0.0
        is_first_sale = True
        
        # Escribir datos (empezar en fila 2)
        row = 2
        for line in move_lines:
            # Obtener valores de compra
            purchase_qty = line.purchase_product_qty or 0.0
            purchase_price = line.purchase_price_unit or 0.0
            purchase_subtotal = line.purchase_price_subtotal or 0.0
            
            # Obtener valores de venta
            sale_qty = line.sale_product_uom_qty or 0.0
            sale_price = line.sale_price_unit or 0.0
            sale_subtotal = line.sale_price_subtotal or 0.0
            
            # Calcular costo promedio actual antes de la transacción
            current_avg_cost = balance_total_cost / balance_qty if balance_qty != 0 else last_avg_cost
            
            # Actualizar saldo: compras aumentan, ventas disminuyen
            if purchase_qty > 0:
                balance_qty += purchase_qty
                balance_total_cost += purchase_subtotal
            
            if sale_qty > 0:
                balance_qty -= sale_qty
                cost_to_subtract = sale_qty * current_avg_cost
                balance_total_cost -= cost_to_subtract
            
            # Calcular costo promedio del saldo después de la transacción
            if balance_qty != 0:
                balance_avg_cost = balance_total_cost / balance_qty
                last_avg_cost = balance_avg_cost
            else:
                balance_avg_cost = last_avg_cost
            
            # Escribir Fecha
            if line.date:
                worksheet.write_datetime(row, 0, line.date, date_format)
            else:
                worksheet.write(row, 0, '', text_format)
            
            # Escribir Referencia
            worksheet.write(row, 1, line.reference or '', text_format)
            
            # ENTRADA - CANTIDAD, PRECIO, SUBTOTAL
            if purchase_qty > 0:
                worksheet.write(row, 2, purchase_qty, purchase_format)
                worksheet.write(row, 3, purchase_price, purchase_currency_format)
                worksheet.write(row, 4, purchase_subtotal, purchase_currency_format)
            else:
                worksheet.write(row, 2, '', text_format)
                worksheet.write(row, 3, '', text_format)
                worksheet.write(row, 4, '', text_format)
            
            # SALIDA - CANTIDAD, PRECIO, SUBTOTAL
            if sale_qty > 0:
                worksheet.write(row, 5, -sale_qty, sale_format)
                worksheet.write(row, 6, sale_price, sale_currency_format)
                worksheet.write(row, 7, -sale_subtotal, sale_currency_format)
            else:
                worksheet.write(row, 5, '', text_format)
                worksheet.write(row, 6, '', text_format)
                worksheet.write(row, 7, '', text_format)
            
            # SALDO FINAL - CANTIDAD, COSTO PROMEDIO, VALOR TOTAL
            worksheet.write(row, 8, int(balance_qty), integer_format)
            if balance_qty != 0:
                worksheet.write(row, 9, balance_avg_cost, currency_format)
                worksheet.write(row, 10, balance_total_cost, currency_format)
            else:
                worksheet.write(row, 9, '', text_format)
                worksheet.write(row, 10, '', text_format)
            
            # Acumular totales
            total_purchase_qty += purchase_qty
            total_purchase_subtotal += purchase_subtotal
            
            if sale_qty > 0:
                if is_first_sale:
                    first_sale_qty = sale_qty
                    first_sale_subtotal = sale_subtotal
                    is_first_sale = False
                else:
                    total_sale_qty += sale_qty
                    total_sale_subtotal += sale_subtotal
            
            row += 1
        
        # Escribir fila de TOTALES
        row += 1
        worksheet.write(row, 0, 'Totales', total_format)
        worksheet.write(row, 1, '', total_format)
        
        # TOTALES ENTRADA
        worksheet.write(row, 2, int(total_purchase_qty), total_integer_format)
        worksheet.write(row, 3, '', total_format)
        worksheet.write(row, 4, total_purchase_subtotal, total_currency_format)
        
        # TOTALES SALIDA
        final_sale_qty = first_sale_qty - total_sale_qty if first_sale_qty > 0 else -total_sale_qty
        final_sale_subtotal = first_sale_subtotal - total_sale_subtotal if first_sale_subtotal > 0 else -total_sale_subtotal
        worksheet.write(row, 5, int(final_sale_qty), total_integer_format)
        worksheet.write(row, 6, '', total_format)
        worksheet.write(row, 7, final_sale_subtotal, total_currency_format)
        
        # TOTALES SALDO FINAL
        worksheet.write(row, 8, int(balance_qty), total_integer_format)
        if balance_qty != 0:
            worksheet.write(row, 9, balance_avg_cost, total_currency_format)
            worksheet.write(row, 10, balance_total_cost, total_currency_format)
        else:
            worksheet.write(row, 9, '', total_format)
            worksheet.write(row, 10, '', total_format)
        
        # Cerrar workbook
        workbook.close()
        output.seek(0)
        
        # Crear nombre de archivo
        product_name = move_lines[0].product_id.name if move_lines and move_lines[0].product_id else 'Kardex'
        filename = 'Kardex_Valorizado_%s_%s.xlsx' % (
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

    def _generate_csv(self, move_lines=None):
        """Generar reporte CSV con la misma estructura que el PDF y Excel"""
        if move_lines is None:
            move_lines = self._get_move_lines()
        
        if not move_lines:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin datos',
                    'message': 'No hay registros para exportar.',
                    'type': 'warning',
                }
            }
        
        # Crear el archivo CSV
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_ALL)
        
        # Encabezados principales (igual que PDF y Excel)
        writer.writerow([''])  # Fila vacía para el encabezado principal
        writer.writerow([
            'Fecha', 'REFERENCIA',
            'ENTRADA - CANTIDAD', 'ENTRADA - PRECIO', 'ENTRADA - SUBTOTAL',
            'SALIDA - CANTIDAD', 'SALIDA - PRECIO', 'SALIDA - SUBTOTAL',
            'SALDO FINAL - CANTIDAD', 'SALDO FINAL - COSTO PROMEDIO', 'SALDO FINAL - VALOR TOTAL'
        ])
        
        # Inicializar variables de saldo (igual que en el PDF y Excel)
        balance_qty = 0.0
        balance_total_cost = 0.0
        balance_avg_cost = 0.0
        last_avg_cost = 0.0
        total_purchase_qty = 0.0
        total_purchase_subtotal = 0.0
        total_sale_qty = 0.0
        total_sale_subtotal = 0.0
        first_sale_qty = 0.0
        first_sale_subtotal = 0.0
        is_first_sale = True
        
        # Escribir datos
        for line in move_lines:
            # Obtener valores de compra
            purchase_qty = line.purchase_product_qty or 0.0
            purchase_price = line.purchase_price_unit or 0.0
            purchase_subtotal = line.purchase_price_subtotal or 0.0
            
            # Obtener valores de venta
            sale_qty = line.sale_product_uom_qty or 0.0
            sale_price = line.sale_price_unit or 0.0
            sale_subtotal = line.sale_price_subtotal or 0.0
            
            # Calcular costo promedio actual antes de la transacción
            current_avg_cost = balance_total_cost / balance_qty if balance_qty != 0 else last_avg_cost
            
            # Actualizar saldo: compras aumentan, ventas disminuyen
            if purchase_qty > 0:
                balance_qty += purchase_qty
                balance_total_cost += purchase_subtotal
            
            if sale_qty > 0:
                balance_qty -= sale_qty
                cost_to_subtract = sale_qty * current_avg_cost
                balance_total_cost -= cost_to_subtract
            
            # Calcular costo promedio del saldo después de la transacción
            if balance_qty != 0:
                balance_avg_cost = balance_total_cost / balance_qty
                last_avg_cost = balance_avg_cost
            else:
                balance_avg_cost = last_avg_cost
            
            # Formatear fecha
            fecha_str = line.date.strftime('%Y-%m-%d %H:%M:%S') if line.date else ''
            
            # Preparar fila de datos
            row = [
                fecha_str,
                line.reference or '',
                # ENTRADA
                int(purchase_qty) if purchase_qty > 0 else '',
                '{:,.2f}'.format(purchase_price) if purchase_qty > 0 else '',
                '{:,.2f}'.format(purchase_subtotal) if purchase_qty > 0 else '',
                # SALIDA
                int(-sale_qty) if sale_qty > 0 else '',
                '{:,.2f}'.format(sale_price) if sale_qty > 0 else '',
                '{:,.2f}'.format(-sale_subtotal) if sale_qty > 0 else '',
                # SALDO FINAL
                int(balance_qty),
                '{:,.2f}'.format(balance_avg_cost) if balance_qty != 0 else '',
                '{:,.2f}'.format(balance_total_cost) if balance_qty != 0 else ''
            ]
            writer.writerow(row)
            
            # Acumular totales
            total_purchase_qty += purchase_qty
            total_purchase_subtotal += purchase_subtotal
            
            if sale_qty > 0:
                if is_first_sale:
                    first_sale_qty = sale_qty
                    first_sale_subtotal = sale_subtotal
                    is_first_sale = False
                else:
                    total_sale_qty += sale_qty
                    total_sale_subtotal += sale_subtotal
        
        # Escribir fila de TOTALES
        writer.writerow([''])  # Fila vacía
        final_sale_qty = first_sale_qty - total_sale_qty if first_sale_qty > 0 else -total_sale_qty
        final_sale_subtotal = first_sale_subtotal - total_sale_subtotal if first_sale_subtotal > 0 else -total_sale_subtotal
        
        totales_row = [
            'Totales',
            '',
            # TOTALES ENTRADA
            int(total_purchase_qty),
            '',
            '{:,.2f}'.format(total_purchase_subtotal),
            # TOTALES SALIDA
            int(final_sale_qty),
            '',
            '{:,.2f}'.format(final_sale_subtotal),
            # TOTALES SALDO FINAL
            int(balance_qty),
            '{:,.2f}'.format(balance_avg_cost) if balance_qty != 0 else '',
            '{:,.2f}'.format(balance_total_cost) if balance_qty != 0 else ''
        ]
        writer.writerow(totales_row)
        
        # Preparar archivo para descarga
        output.seek(0)
        product_name = move_lines[0].product_id.name if move_lines and move_lines[0].product_id else 'Kardex'
        filename = 'Kardex_Valorizado_%s_%s.csv' % (
            product_name.replace('/', '_').replace('\\', '_')[:50],
            datetime.now().strftime('%Y%m%d_%H%M%S')
        )
        
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(output.getvalue().encode('utf-8')),
            'store_fname': filename,
            'mimetype': 'text/csv',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

