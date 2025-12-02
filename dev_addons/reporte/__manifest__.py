# -*- coding:utf-8 -*-
{
    'name': 'Reportes Contables Empresas Oruro v18',
    'version': '1.0',
    'depends': [
        'base', 
        #'l10n_bo',
        'account',
        'purchase',
        'sale',
       
    ],
    'author': 'APPEX BOLIVIA SRL.',
    'summary': 'Reportes Contables Empresas Oruro v18',
    'data': [
      'reports/formato_papel.xml',
      'reports/boton_imprimir_pdf.xml',
      'reports/cabecera_pdf.xml',
      'reports/cuerpo_pdf.xml',
      'views/campo_adicional_razon_social_micelaneo.xml',
      'views/res_company_tree_view.xml',
      
    ],
    'installable': True,
}