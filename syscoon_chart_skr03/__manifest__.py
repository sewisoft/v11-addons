# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon SKR03 - Accounting',
    'version': '10.0.1.1',
    'author': 'Mathias Neef',
    'website': 'https://syscoon.com',
    'category': 'Localization/Account Charts',
    'description': """
Dieses  Modul beinhaltet einen deutschen Kontenrahmen basierend auf dem SKR03.
==============================================================================

German accounting chart and localization.
    """,
    'category': 'Localization',
    'depends': ['l10n_de', 'eq_syscoon'],
    'demo': [],
    'data': [
       # 'data/data.xml',
        #'data/tags.xml',
        'account_chart.xml',
        'account_tax_fiscal_position.xml',
        'account.chart.template.yml',
    ],
    'installable': True,
}
