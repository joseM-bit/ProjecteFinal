# -*- coding: utf-8 -*-
{
    'name': "Taller",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','base','contacts', 'account', 'stock','sale','product'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
         'views/vehiculo_views.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/orden_views.xml',
        'views/ordenrepuestoline_views.xml',
        'views/facturas_no_pagadas.xml',
        'views/factura_views.xml',
        'views/presupuesto_views.xml',
        'views/productos.xml',
        'views/stock.xml',
        'views/res_partner.xml',
        'views/plantillafactura.xml',
        'views/empleados_views.xml',
        
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
