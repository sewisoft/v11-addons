# -*- coding: utf-8 -*-

from odoo import models, fields


class EqCrmLead(models.Model):
    _inherit = 'crm.lead'

    def compute_quot_crm_count(self):
        sale_order_obj = self.env['sale.order']
        for crm in self:
            record = sale_order_obj.search([('partner_id', '=', crm.partner_id.id),
                                            ('state', 'in', ['draft', 'sent', 'cancel'])])
            crm_quot_count = len(record)
            crm.total_quot_crm = str(crm_quot_count)

    total_quot_crm = fields.Char(compute='compute_quot_crm_count', string="Quotations")
