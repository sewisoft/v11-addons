# -*- coding: utf-8 -*-

{
    'name': "Equitania Verkauf & Lager",
    'license': 'AGPL-3',
    'version': '11.0.2.0.0',
    'category': 'sale_stock',
    'description': """ Improved view for order items""",
    'author': 'Equitania Software GmbH',
    'summary': ' Erweiterung Verkauf / Lager',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'eq_stock', 'sales_team', 'sale_stock', 'eq_product', 'eq_sale'],
    'data': [
            'security/ir.model.access.csv',
            'views/eq_open_sale_order_line_view.xml',
             ],
    "active": False,
    "installable": True
}
