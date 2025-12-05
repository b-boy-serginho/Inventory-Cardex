{
    'name': 'Inventory Cardex',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Custom Inventory Module',
    'description': """
        This module adds a Hello World message to the Inventory Picking form.
    """,
    # Dependencias necesarias:
    # - stock: modelo stock.move / stock.move.line
    # - sale: modelo sale.order / sale.order.line
    # - sale_stock: añade la relación stock.move.sale_line_id usada en este módulo
    # - purchase: modelo purchase.order / purchase.order.line
    # - purchase_stock: añade la relación stock.move.purchase_line_id usada en este módulo
    # - web: assets y vistas web
    'depends': ['stock', 'sale', 'sale_stock', 'purchase', 'purchase_stock', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_views.xml',
        # 'views/sale_order_line_views.xml',  # Temporalmente desactivado por error de esquema XML
        'views/assets.xml',
        'wizard/stock_cost_report_wizard_views.xml',
        'wizard/reporte_wizard_views.xml',
        # 'wizard/stock_move_line_report_wizard_views.xml',  # Comentado temporalmente
        'report/stock_cost_report_template.xml',
        'report/stock_move_line_cardex_report.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
}
