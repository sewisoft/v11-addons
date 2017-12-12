# -*- coding: utf-8 -*-

from odoo import models, api


class EqSaleQuoteLine(models.Model):
    _inherit = 'sale.quote.line'

    @api.model
    def create(self, values):
        if values['quote_id'] == 1:
            return super(EqSaleQuoteLine, self).create(values)
        else:
            quote_id = values['quote_id']
            quote_tmpl_obj = self.env['sale.quote.template'].search([('id','=',quote_id)])
            if len(quote_tmpl_obj):
                return super(EqSaleQuoteLine, self).create(values)
            else:
                tmpl_pool = self.env['sale.quote.template']
                create_vals = {
                    'number_of_days': 30,
                    'name': values['name'],
                    'website_description': values['website_description']
                }
                tmpl_obj = tmpl_pool.create(create_vals)
                values.update({'quote_id': tmpl_obj.id,})
                values = self._inject_quote_description(values)
                res = super(EqSaleQuoteLine, self).create(values)
                return res
