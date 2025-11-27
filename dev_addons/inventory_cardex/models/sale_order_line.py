# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Los campos que quieres mostrar ya existen en el modelo sale.order.line:
    # - name: Descripción del producto
    # - product_uom_qty: Cantidad
    # - price_unit: Precio unitario
    # - price_subtotal: Subtotal (sin impuestos)
    # - price_tax: Impuestos
    # - price_total: Total (con impuestos)
    
    # Puedes agregar campos computados adicionales aquí si lo necesitas en el futuro
    # Por ejemplo:
    
    # @api.depends('product_uom_qty', 'price_unit')
    # def _compute_custom_field(self):
    #     for line in self:
    #         line.custom_field = line.product_uom_qty * line.price_unit
