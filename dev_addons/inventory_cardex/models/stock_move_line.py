from odoo import models, fields


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
