# -*- coding: utf-8 -*-
{
    'name': "Equitania Kontakt Optimierungen",
    'license': 'AGPL-3',
    'version': '11.0.1.0.0',
    'category': 'Partner',
    'description': """Extensions for res_partner""",
    'author': 'Equitania Software GmbH',
    'summary': 'Partner Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'pragma_supplier_number', 'pragma_customer_number'],
    'data': [
            "views/eq_res_partner_view.xml",
             ],
    "installable": True
}
