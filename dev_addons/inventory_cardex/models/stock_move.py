# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Campo relacionado para mostrar el costo del producto
    product_cost = fields.Float(
        string='Costo',
        related='product_id.standard_price',
        readonly=True,
        store=True,  # Guardado en BD para mantener histórico
        help='Costo estándar del producto en el momento de la consulta'
    )

    # Campo computado para el costo total del movimiento
    total_cost = fields.Monetary(
        string='Costo Total',
        compute='_compute_total_cost',
        store=False,
        currency_field='company_currency_id',
        help='Costo total = Cantidad * Costo unitario'
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        string='Moneda de la Compañía',
        readonly=True
    )

    @api.depends('product_id', 'product_id.standard_price', 'product_qty')
    def _compute_total_cost(self):
        """
        Calcula el costo total del movimiento.
        Costo Total = Cantidad * Costo Unitario
        """
        for move in self:
            if move.product_id and move.product_qty:
                move.total_cost = move.product_id.standard_price * move.product_qty
            else:
                move.total_cost = 0.0

    # Método alternativo: obtener el costo en el momento del movimiento
    def get_cost_at_move_date(self):
        """
        Obtiene el costo del producto en la fecha del movimiento.
        Útil para obtener el costo histórico real.
        """
        self.ensure_one()
        
        # Si el movimiento tiene capas de valoración, usar ese costo
        if hasattr(self, 'stock_valuation_layer_ids') and self.stock_valuation_layer_ids:
            layer = self.stock_valuation_layer_ids[0]
            return layer.unit_cost
        
        # Si no, retornar el costo actual
        return self.product_id.standard_price


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # Campo relacionado para mostrar el costo en las líneas de movimiento
    product_cost = fields.Float(
        string='Costo Unitario',
        related='product_id.standard_price',
        readonly=True,
        store=True  # Guardado en BD para mantener histórico
    )

    # Costo total de la línea
    line_cost = fields.Monetary(
        string='Costo Total Línea',
        compute='_compute_line_cost',
        store=False,
        currency_field='company_currency_id'
    )

    company_currency_id = fields.Many2one(
        'res.currency',
        related='company_id.currency_id',
        readonly=True
    )

    @api.depends('product_id', 'product_id.standard_price', 'quantity')
    def _compute_line_cost(self):
        """
        Calcula el costo total de la línea.
        """
        for line in self:
            if line.product_id and line.quantity:
                line.line_cost = line.product_id.standard_price * line.quantity
            else:
                line.line_cost = 0.0
