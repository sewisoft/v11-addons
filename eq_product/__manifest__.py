# -*- coding: utf-8 -*-

{
    'name': "Equitania Produkt Optimierungen",
    'license': 'AGPL-3',
    'version': '11.0.2.0.0',
    'category': 'product',
    'description': """Extensions for product""",
    'author': 'Equitania Software GmbH',
    'summary': 'Product Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'product', 'sale_management'],
    'data': [
            'security/ir.model.access.csv',
            'data/ir_sequence_data.xml',
            'views/product_view.xml',
            'views/report_label_product_product_templates.xml',
             ],
    "active": False,
    "installable": True
}
