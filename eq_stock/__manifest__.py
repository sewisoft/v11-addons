# -*- coding: utf-8 -*-

{
    'name': 'Equitania Stock',
    'license': 'AGPL-3',
    'version': '11.0.3.0.0',
    'description': """
        Erweiterung für Lager
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base', 'base_setup', 'delivery', 'stock', 'eq_res_partner', 'eq_base_report'],
    'category': 'stock',
    'summary': 'Equitania Lager Erweiterung',
    'data': [
        "views/stock_picking_view.xml",
        "views/report_stock_picking.xml",
        "views/report_stock_picking_packaging.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
