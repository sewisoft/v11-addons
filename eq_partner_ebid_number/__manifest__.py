# -*- coding: utf-8 -*-

{
    'name': 'Equitania EBID Integration Unternehmensverzeichnis.org',
    'version': '11.0.1.0.0',
    'description': """
        Equitania Software GmbH
    """,
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'sales_team'],
    'category': 'General Improvements',
    'summary': '',
    'data': [
        'security/ir.model.access.csv',
        'views/partner_view.xml',
        'views/eq_ebid_config_view.xml',
        'views/eq_ebid_check_job.xml',
        'views/eq_ebid_protocol_view.xml',
        
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
