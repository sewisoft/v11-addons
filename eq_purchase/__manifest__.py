# -*- coding: utf-8 -*-
{
    'name': "Equitania Einkauf Optimierungen",
    'license': 'AGPL-3',
    'version': '11.0.4.0.0',
    'category': 'purchase',
    'description': """Extensions for purchase""",
    'author': 'Equitania Software GmbH',
    'summary': 'Purchase Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'purchase', 'eq_res_partner', 'eq_mail_extension'],
    'data': [
        'security/ir.model.access.csv',
        'data/decimal_precision.xml',
        'data/email_template_function.xml',
        'data/purchase_order_send_by_email.xml',
        'data/rfq_send_by_email.xml',
        'views/purchase_view.xml',
        'views/report_purchase_order.xml',
        'views/report_purchase_quotation.xml',
        'views/eq_res_partner_view.xml',
             ],
    "active": False,
    "installable": True
}
