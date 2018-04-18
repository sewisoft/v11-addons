# -*- coding: utf-8 -*-
{
    'name': 'EQ Report Basis',
    'license': 'AGPL-3',
    'version': '1.0.6',
    'description': """
        Allgemeine Anpassungen für die Equitania Reports
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'eq_base', 'web', 'eq_res_partner'],
    'category': 'Report',
    'summary': 'Reports',
    'data': [
        'views/header.xml',
        'views/external_equitania_layout.xml',
        'views/footer.xml',
        'views/paper_format.xml',
        'views/report_external_layout.xml',
        'views/report_internal_layout.xml',
        'views/report_style.xml',
        'views/eq_res_config_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
