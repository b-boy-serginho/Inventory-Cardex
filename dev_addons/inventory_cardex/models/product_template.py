# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Campo computado para acceder al costo estándar
    cardex_standard_price = fields.Float(
        string='Costo (Cardex)',
        compute='_compute_cardex_standard_price',
        store=False,
        help='Costo estándar del producto para uso en Cardex'
    )

    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_cardex_standard_price(self):
        """
        Calcula el costo estándar desde la variante del producto.
        En Odoo, standard_price se almacena en product.product (variantes).
        """
        for template in self:
            # Obtener la primera variante (o la única si no hay variantes)
            if template.product_variant_ids:
                template.cardex_standard_price = template.product_variant_ids[0].standard_price
            else:
                template.cardex_standard_price = 0.0

    def get_current_cost(self):
        """
        Método helper para obtener el costo actual del producto.
        Retorna el costo de la primera variante.
        """
        self.ensure_one()
        if self.product_variant_ids:
            return self.product_variant_ids[0].standard_price
        return 0.0

    def get_cost_history(self, limit=10):
        """
        Obtiene el historial de costos del producto.
        Retorna una lista de diccionarios con fecha y costo.
        """
        self.ensure_one()
        history = []
        
        # Buscar en stock_valuation_layer si existe
        if hasattr(self.env, 'stock.valuation.layer'):
            layers = self.env['stock.valuation.layer'].search([
                ('product_id', 'in', self.product_variant_ids.ids)
            ], order='create_date desc', limit=limit)
            
            for layer in layers:
                history.append({
                    'date': layer.create_date,
                    'unit_cost': layer.unit_cost,
                    'quantity': layer.quantity,
                    'value': layer.value,
                    'description': layer.description or 'N/A'
                })
        
        return history

    def log_product_cost_info(self):
        """
        Método de debug para registrar información sobre el costo del producto.
        Útil para entender dónde se almacena el costo.
        """
        self.ensure_one()
        _logger.info("=" * 80)
        _logger.info(f"INFORMACIÓN DE COSTO - Producto: {self.name}")
        _logger.info("=" * 80)
        
        # Información básica
        _logger.info(f"ID Template: {self.id}")
        _logger.info(f"Nombre: {self.name}")
        
        # Información de variantes
        for variant in self.product_variant_ids:
            _logger.info(f"\nVariante ID: {variant.id}")
            _logger.info(f"  - Código: {variant.default_code}")
            _logger.info(f"  - Costo (standard_price): {variant.standard_price}")
            
            # Verificar si tiene valoración de inventario
            if hasattr(variant, 'stock_valuation_layer_ids'):
                _logger.info(f"  - Capas de valoración: {len(variant.stock_valuation_layer_ids)}")
                if variant.stock_valuation_layer_ids:
                    last_layer = variant.stock_valuation_layer_ids[0]
                    _logger.info(f"    * Última capa - Costo unitario: {last_layer.unit_cost}")
                    _logger.info(f"    * Última capa - Fecha: {last_layer.create_date}")
        
        _logger.info("=" * 80)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_cost_from_valuation_layers(self):
        """
        Obtiene el costo más reciente desde las capas de valoración.
        Útil cuando se usa valoración automática de inventario.
        """
        self.ensure_one()
        
        if hasattr(self, 'stock_valuation_layer_ids') and self.stock_valuation_layer_ids:
            # Obtener la capa más reciente
            latest_layer = self.stock_valuation_layer_ids.sorted('create_date', reverse=True)[0]
            return latest_layer.unit_cost
        
        # Si no hay capas, retornar el standard_price
        return self.standard_price

    def update_standard_price(self, new_price, reason=None):
        """
        Actualiza el costo estándar del producto de manera segura.
        
        :param new_price: Nuevo precio/costo
        :param reason: Razón del cambio (opcional)
        """
        self.ensure_one()
        
        old_price = self.standard_price
        self.standard_price = new_price
        
        _logger.info(f"Costo actualizado para {self.display_name}: {old_price} -> {new_price}")
        if reason:
            _logger.info(f"Razón: {reason}")
        
        return True
