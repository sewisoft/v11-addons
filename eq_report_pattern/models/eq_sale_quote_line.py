# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2017-now Equitania Software GmbH(<http://www.equitania.de>).
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
