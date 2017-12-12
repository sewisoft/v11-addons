# -*- coding: utf-8 -*-
{
    'name': 'EQ Report Basis',
    'license': 'AGPL-3',
    'version': '11.0.3.0.0',
    'description': """
        Allgemeine Anpassungen für die Equitania Reports
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'eq_base', 'web', 'eq_res_partner'],
    'category': 'Report',
    'summary': 'Reports',
    'data': [
        'views/report_external_layout.xml',
        'views/external_equitania_layout.xml',
        'eq_res_config_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
