# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon Kontenrahmen IKR',
    'version': '11.0.1.0',
    'author': 'copado MEDIA',
	'website': 'http://www.copado.de',
    'category': 'Localization/Account Charts',
    'description': """
Dieses Modul beinhaltet den deutschen Kontenrahmen IKR (Industriekontenrahmen) angelehnt an den Schulkontenrahmen der IHK.
==========================================================================================================================
	* Letzte Überarbeitung IKR: 06/2016


English:
German accounting chart and localization (Industry Chart Temlate (IKR)) relating to the school-chart-template of the IHK (Industry and Trade Chamber).
	* Last change IKR: 06/2016

    """,
    'depends': [
		'l10n_de',
	],
    'category': 'Localization',
    'demo': [],
    'data': [
        'account_chart.xml', 
        'account_tax_fiscal_position_ikr.xml',		
    ],
    'installable': False,
}

