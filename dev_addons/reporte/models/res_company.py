from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    is_cd = fields.Boolean(
        string='Mostrar "CD" en Comprobante de Diario',
        default=False,
        help='Si está activado, se mostrará "COMPROBANTE DE DIARIO" con el código CD en los reportes'
    )

