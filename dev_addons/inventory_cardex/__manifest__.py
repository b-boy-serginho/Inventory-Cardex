{
    'name': 'Inventory Cardex',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Custom Inventory Module',
    'description': """
        This module adds a Hello World message to the Inventory Picking form.
    """,
    'depends': ['stock', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_views.xml',
        'views/assets.xml',
        'wizard/stock_cost_report_wizard_views.xml',
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
