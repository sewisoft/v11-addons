# -*- coding: utf-8 -*-
{
    'name': "Equitania Finanzen",
    'license': 'AGPL-3',
    'version': '1.0.1',
    'category': 'Accounting',
    'description': """Extensions for account""",
    'author': 'Equitania Software GmbH',
    'summary': 'Account Extension',
    'website': 'www.myodoo.de',
    "depends": ['base', 'base_setup', 'account', 'stock', 'eq_sale_stock', 'sale_stock'],
    'data': [
            'security/ir.model.access.csv',
            'data/template_account_invoice_notification.xml',
            'data/invoice_send_by_email.xml',
            'data/email_template_function.xml',
            'views/account_invoice_view.xml',
            'views/report_invoice.xml',
            'data/invoice_send_by_email.xml',
             ],
    "active": False,
    "installable": True
}
