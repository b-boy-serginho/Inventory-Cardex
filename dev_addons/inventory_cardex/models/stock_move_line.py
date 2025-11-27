from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # Campos relacionados para acceder a las cantidades planificadas del producto
    incoming_qty = fields.Float(
        string='Cantidad Entrante',
        related='product_id.incoming_qty',
        readonly=True,
        help="Cantidad de productos entrantes planeados. Incluye los artículos que llegan a cualquier ubicación de existencias."
    )
    
    outgoing_qty = fields.Float(
        string='Cantidad Saliente',
        related='product_id.outgoing_qty',
        readonly=True,
        help="Cantidad de productos salientes planeados. Incluye los artículos que salen de las ubicaciones de existencias."
    )
    
    # ========== CAMPOS DE VENTA (sale_order_line) ==========
    # Relación con la línea de pedido de venta a través de stock.move
    sale_line_id = fields.Many2one(
        'sale.order.line',
        string='Línea de Venta',
        related='move_id.sale_line_id',
        readonly=True,
        store=True,
        help="Línea de pedido de venta relacionada con este movimiento de stock"
    )
    
    # Campos de la línea de venta
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Pedido de Venta',
        related='sale_line_id.order_id',
        readonly=True,
        store=True,
        help="Pedido de venta relacionado"
    )
    
    # En Odoo 17 el campo `sale.order.line.name` es de tipo Text, por lo que
    # este campo relacionado debe ser también Text para evitar errores de tipo.
    sale_product_name = fields.Text(
        string='Descripción Venta',
        related='sale_line_id.name',
        readonly=True,
        help="Descripción del producto en la línea de venta"
    )
    
    sale_product_uom_qty = fields.Float(
        string='Cantidad Vendida',
        related='sale_line_id.product_uom_qty',
        readonly=True,
        help="Cantidad en la línea de pedido de venta"
    )
    
    sale_price_unit = fields.Float(
        string='Precio Unit. Venta',
        related='sale_line_id.price_unit',
        readonly=True,
        help="Precio unitario de venta"
    )
    
    sale_price_subtotal = fields.Monetary(
        string='Subtotal Venta',
        related='sale_line_id.price_subtotal',
        readonly=True,
        currency_field='sale_currency_id',
        help="Subtotal sin impuestos de la línea de venta"
    )
    
    sale_price_tax = fields.Float(
        string='Impuestos Venta',
        related='sale_line_id.price_tax',
        readonly=True,
        help="Impuestos de la línea de venta"
    )
    
    sale_price_total = fields.Monetary(
        string='Total Venta',
        related='sale_line_id.price_total',
        readonly=True,
        currency_field='sale_currency_id',
        help="Total con impuestos de la línea de venta"
    )
    
    sale_currency_id = fields.Many2one(
        'res.currency',
        string='Moneda Venta',
        compute='_compute_sale_currency_id',
        readonly=True,
        store=False,
        help="Moneda del pedido de venta"
    )
    
    @api.depends('sale_line_id', 'sale_line_id.currency_id')
    def _compute_sale_currency_id(self):
        for line in self:
            if line.sale_line_id and line.sale_line_id.currency_id:
                line.sale_currency_id = line.sale_line_id.currency_id
            else:
                line.sale_currency_id = False
    
    sale_state = fields.Char(
        string='Estado Venta',
        compute='_compute_sale_state',
        readonly=True,
        store=False,
        help="Estado del pedido de venta"
    )
    
    @api.depends('sale_line_id', 'sale_line_id.order_id', 'sale_line_id.order_id.state')
    def _compute_sale_state(self):
        for line in self:
            if line.sale_line_id and line.sale_line_id.order_id:
                line.sale_state = line.sale_line_id.order_id.state or ''
            else:
                line.sale_state = ''
    
    # Campo para saber si este movimiento está relacionado con una venta
    has_sale = fields.Boolean(
        string='Tiene Venta',
        compute='_compute_has_sale',
        store=True,
        help="Indica si este movimiento está relacionado con un pedido de venta"
    )
    
    # Campo para saber si tiene venta con cantidad > 0 (para decoraciones)
    has_sale_qty = fields.Boolean(
        string='Tiene Venta con Cantidad',
        compute='_compute_has_sale_qty',
        store=False,
        help="Indica si este movimiento tiene venta con cantidad mayor a 0"
    )
    
    @api.depends('sale_line_id')
    def _compute_has_sale(self):
        for line in self:
            line.has_sale = bool(line.sale_line_id)
    
    @api.depends('sale_line_id', 'sale_product_uom_qty')
    def _compute_has_sale_qty(self):
        for line in self:
            if not line.sale_line_id:
                line.has_sale_qty = False
            else:
                try:
                    qty = getattr(line, 'sale_product_uom_qty', None) or 0.0
                    line.has_sale_qty = float(qty) > 0
                except (AttributeError, TypeError, ValueError):
                    line.has_sale_qty = False