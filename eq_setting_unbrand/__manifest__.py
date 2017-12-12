# -*- coding: utf-8 -*-

{
    'name': "Equitania Setting Unbrand",
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'category': 'Tools',
    'description': """ Entfernt die Odoo Brandings und ersetzt Sie durch MyOdoo Links und Wiki-links """,
    'author': 'Equitania Software GmbH',
    'summary': 'Unbrand Extension',
    'website': 'www.myodoo.de',
    'depends': ['web_settings_dashboard', 'base_setup', 'web'],
    'data': ['views/report_settings.xml'],
    'qweb': ['static/src/xml/dashboard_extension.xml'],
    "active": False,
    "installable": True
}
