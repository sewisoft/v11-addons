# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon Kontenrahmen SKR04',
    'version': '10.0.1.1',
    'author': 'Mathias Neef',
    'website': 'https://syscoon.com',
    'category': 'Localization/Account Charts',
    'description': """
Dieses  Modul beinhaltet einen deutschen Kontenrahmen basierend auf dem SKR04.
==============================================================================

German accounting chart and localization.
    """,
    'depends': ['l10n_de', 'eq_syscoon'],
    'category': 'Localization',
    'demo': [],
    'data': [
        'account_chart.xml',
        'account_tax_fiscal_position.xml',
        'account.chart.template.yml',
    ],
    'installable': True,
}
