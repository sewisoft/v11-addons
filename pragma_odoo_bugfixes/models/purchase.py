# -*- coding: utf-8 -*-

from odoo import models, fields, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], related='order_id.state', string=_('Order Status'), readonly=True, copy=False, store=True, default='draft')
