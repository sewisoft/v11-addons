# -*- coding: utf-8 -*-

{
    'name': 'Equitania Dokumenten Bausteine',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'description': """
        Improves the odoo document templating, overwrites head- and foot-texttemplates
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup', 'website_quote', 'stock', 'sales_team', 'eq_sale', 'eq_purchase', 'eq_account'],
    'category': 'Reports',
    'summary': '',
    'data': [
            'security/ir.model.access.csv',
            'views/document_template_view.xml',
            'views/sale_view.xml',
            'views/purchase_view.xml',
            'views/stock_picking_view.xml',
            'views/account_invoice_view.xml',
            'views/res_partner_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
