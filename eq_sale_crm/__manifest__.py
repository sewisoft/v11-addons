# -*- coding: utf-8 -*-

{
    'name': 'Equitania Sale_CRM',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'description': """
        Extensions for sale_crm
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base', 'sale_crm'],
    'category': 'CRM Sale',
    'summary': 'Sale_crm extensions',
    'data': [
        "views/crm_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
