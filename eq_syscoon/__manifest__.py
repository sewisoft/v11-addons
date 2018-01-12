# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'equitania syscoon ',
    'version': '1.0.1',
    'author': '',
	'website': '',
    'category': 'Localization/Account Charts',
    'description': """
Dieses Modul beinhaltet neue Dateien für die  deutschen Kontenrahmen IKR, skr03, skr04.
==========================================================================================================================
	




    """,
    'depends': [
		'l10n_de'
	],
    'category': 'Localization',
    'demo': [],
    'data': [
        'data/data.xml',
        'data/tags.xml',
    ],
    'installable': True,
}

