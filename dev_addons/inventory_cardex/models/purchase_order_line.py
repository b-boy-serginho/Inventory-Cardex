# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # ========== CAMPOS DE COMPRA (purchase_order_line) ==========
    # Relación con la línea de pedido de compra a través de stock.move
    purchase_line_id = fields.Many2one(
        'purchase.order.line',
        string='Línea de Compra',
        related='move_id.purchase_line_id',
        readonly=True,
        store=True,
        help="Línea de pedido de compra relacionada con este movimiento de stock"
    )
    
    # Campos de la línea de compra
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Pedido de Compra',
        related='purchase_line_id.order_id',
        readonly=True,
        store=True,
        help="Pedido de compra relacionado"
    )
    
    # En Odoo 17 el campo `purchase.order.line.name` es de tipo Text
    purchase_product_name = fields.Text(
        string='Descripción Compra',
        related='purchase_line_id.name',
        readonly=True,
        help="Descripción del producto en la línea de compra"
    )
    
    purchase_product_qty = fields.Float(
        string='Cantidad Comprada',
        related='purchase_line_id.product_qty',
        readonly=True,
        help="Cantidad en la línea de pedido de compra"
    )
    
    purchase_price_unit = fields.Float(
        string='Precio Unit. Compra',
        related='purchase_line_id.price_unit',
        readonly=True,
        help="Precio unitario de compra"
    )
    
    purchase_price_subtotal = fields.Monetary(
        string='Subtotal Compra',
        related='purchase_line_id.price_subtotal',
        readonly=True,
        currency_field='purchase_currency_id',
        help="Subtotal sin impuestos de la línea de compra"
    )
    
    purchase_price_tax = fields.Float(
        string='Impuestos Compra',
        related='purchase_line_id.price_tax',
        readonly=True,
        help="Impuestos de la línea de compra"
    )
    
    purchase_price_total = fields.Monetary(
        string='Total Compra',
        related='purchase_line_id.price_total',
        readonly=True,
        currency_field='purchase_currency_id',
        help="Total con impuestos de la línea de compra"
    )
    
    purchase_currency_id = fields.Many2one(
        'res.currency',
        string='Moneda Compra',
        compute='_compute_purchase_currency_id',
        readonly=True,
        store=False,
        help="Moneda del pedido de compra"
    )
    
    @api.depends('purchase_line_id', 'purchase_line_id.currency_id')
    def _compute_purchase_currency_id(self):
        for line in self:
            if line.purchase_line_id and line.purchase_line_id.currency_id:
                line.purchase_currency_id = line.purchase_line_id.currency_id
            else:
                line.purchase_currency_id = False
    
    purchase_state = fields.Char(
        string='Estado Compra',
        compute='_compute_purchase_state',
        readonly=True,
        store=False,
        help="Estado del pedido de compra"
    )
    
    @api.depends('purchase_line_id', 'purchase_line_id.order_id', 'purchase_line_id.order_id.state')
    def _compute_purchase_state(self):
        for line in self:
            if line.purchase_line_id and line.purchase_line_id.order_id:
                line.purchase_state = line.purchase_line_id.order_id.state or ''
            else:
                line.purchase_state = ''
    
    # Campo para saber si este movimiento está relacionado con una compra
    has_purchase = fields.Boolean(
        string='Tiene Compra',
        compute='_compute_has_purchase',
        store=True,
        help="Indica si este movimiento está relacionado con un pedido de compra"
    )
    
    # Campo para saber si tiene compra con cantidad > 0 (para decoraciones)
    has_purchase_qty = fields.Boolean(
        string='Tiene Compra con Cantidad',
        compute='_compute_has_purchase_qty',
        store=False,
        help="Indica si este movimiento tiene compra con cantidad mayor a 0"
    )
    
    @api.depends('purchase_line_id')
    def _compute_has_purchase(self):
        for line in self:
            line.has_purchase = bool(line.purchase_line_id)
    
    @api.depends('purchase_line_id', 'purchase_product_qty')
    def _compute_has_purchase_qty(self):
        for line in self:
            if not line.purchase_line_id:
                line.has_purchase_qty = False
            else:
                try:
                    qty = getattr(line, 'purchase_product_qty', None) or 0.0
                    line.has_purchase_qty = float(qty) > 0
                except (AttributeError, TypeError, ValueError):
                    line.has_purchase_qty = False

