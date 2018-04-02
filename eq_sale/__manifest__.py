# -*- coding: utf-8 -*-

{
    'name': "Equitania Sale",
    'license': 'AGPL-3',
    'version': '1.0.6',
    'category': 'sale',
    'description': """Extensions for sale""",
    'author': 'Equitania Software GmbH',
    'summary': 'Sale Extension',
    'website': 'www.myodoo.de',
    "depends": ['base_setup', 'crm', 'sale', 'product', 'sales_team', 'sale_stock', 'delivery', 'eq_res_partner', 'eq_base_report','website_quote', 'eq_mail_extension'],
    'data': [
            'security/equitania_security.xml',
            'security/ir.model.access.csv',
            'data/template_sale_order_notification.xml',
            'data/email_template_function.xml',
            'data/decimal_precision.xml',
            'data/ir_values_defaults.xml',
            'data/sales_order_send_by_email.xml',
            # 'views/sale_templates.xml',
            'views/report_sale_order.xml',
            'views/product_view.xml',
            'views/res_partner_view.xml',
            'views/sale_views.xml',
            'views/sale_layout_category_view.xml',
             ],
    "active": False,
    "installable": True
}
