# -*- coding: utf-8 -*-
{
    'name': 'Equitania Base',
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'description': """Basic fields for more EQ Modules""",
    'author': 'Equitania Software GmbH',
    'website': 'www.myodoo.de',
    'depends': ['base_setup', 'base'],
    'category': 'General Improvements',
    'summary': 'Base extension',
    'data': [
         "views/res_company_view.xml",
         "views/res_country_view.xml",
         "views/eq_res_users_view.xml",
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
