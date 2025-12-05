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
        """Generar reporte Excel"""
        if move_lines is None:
            move_lines = self._get_move_lines()
        record_ids = move_lines.ids
        
        # Obtener todas las columnas comunes
        visible_fields = [
            'date', 'reference', 'location_id', 'location_dest_id', 
            'product_id', 'quantity', 'product_cost', 'line_cost', 'state',
            'has_sale', 'sale_order_id', 'sale_product_name', 'sale_product_uom_qty',
            'sale_price_unit', 'sale_price_subtotal', 'sale_price_tax', 'sale_price_total', 'sale_state',
            'has_purchase', 'purchase_order_id', 'purchase_product_name', 'purchase_product_qty',
            'purchase_price_unit', 'purchase_price_subtotal', 'purchase_price_tax', 'purchase_price_total', 'purchase_state',
            'product_uom_id', 'lot_id', 'picking_id'
        ]
        
        return self.env['stock.move.line'].generate_dynamic_excel(record_ids, visible_fields)

    def _generate_csv(self, move_lines=None):
        """Generar reporte CSV"""
        if move_lines is None:
            move_lines = self._get_move_lines()
        records = move_lines
        
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
        
        # Crear el archivo CSV
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_ALL)
        
        # Encabezados
        headers = [
            'Fecha', 'Referencia', 'Producto', 'Cantidad', 
            'Costo Unitario', 'Costo Total', 'Estado'
        ]
        writer.writerow(headers)
        
        # Función auxiliar para obtener el valor de un campo
        def get_field_value(record, field_name):
            """Obtiene el valor de un campo de un registro y lo formatea"""
            if not hasattr(record, field_name):
                return ''
            
            value = getattr(record, field_name, None)
            
            if value is None or value is False:
                return ''
            
            # Many2one fields
            if hasattr(value, 'display_name') and hasattr(value, '_name'):
                return value.display_name or ''
            
            # Boolean fields
            if isinstance(value, bool):
                return 'Sí' if value else 'No'
            
            # Selection fields
            if field_name in record._fields:
                field_def = record._fields[field_name]
                if hasattr(field_def, 'selection') and field_def.selection:
                    selection = field_def.selection
                    try:
                        if callable(selection):
                            selection_list = selection(record)
                        else:
                            selection_list = selection
                        
                        if selection_list:
                            selection_dict = dict(selection_list)
                            return selection_dict.get(value, str(value))
                    except:
                        pass
            
            return str(value) if value else ''
        
        # Datos
        for record in records:
            row = [
                record.date.strftime('%Y-%m-%d %H:%M:%S') if record.date else '',
                record.reference or '',
                record.product_id.display_name if record.product_id else '',
                str(record.quantity or 0.0),
                str(record.product_cost or 0.0),
                str(record.line_cost or 0.0),
                get_field_value(record, 'state')
            ]
            writer.writerow(row)
        
        # Preparar archivo para descarga
        output.seek(0)
        filename = 'Cardex_%s.csv' % datetime.now().strftime('%Y%m%d_%H%M%S')
        
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

