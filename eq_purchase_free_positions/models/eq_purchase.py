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
from ast import literal_eval
from odoo import models, fields, api


class eq_purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    def _generate_default_tax(self):
        ir_values_obj = self.env['ir.default']
        account_tax_id = ir_values_obj.get('purchase.order', 'eq_default_tax_purchase_order')
        account_tax_obj = self.browse(account_tax_id)

        if len(account_tax_obj) > 0:
            tax_obj = account_tax_obj[0]
            return tax_obj
        else:
            pass

    taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False),
                                                                       ('active', '=', True)],
                                default=_generate_default_tax)
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)],
                                 change_default=True, required=False)


class eq_purchase_configuration_address(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.multi
    def set_values(self):
        super(eq_purchase_configuration_address, self).set_values()
        IrDefault = self.env['ir.config_parameter'].sudo()
        IrDefault.set_param('eq_purchase_free_positions.eq_default_tax_purchase_order', self.eq_default_tax_purchase_order.id)

    @api.model
    def get_values(self):
        res = super(eq_purchase_configuration_address, self).get_values()
        ir_values_obj = self.env['ir.config_parameter'].sudo()
        default_tax_purchase_order = literal_eval(ir_values_obj.get_param('eq_purchase_free_positions.eq_default_tax_purchase_order', default='False'))
        res.update(
            eq_default_tax_purchase_order=default_tax_purchase_order
        )
        return res

    eq_default_tax_purchase_order = fields.Many2one('account.tax', string='Free position default tax in po '
                                                                          '[eq_purchase_free_positions]',
                                                    domain="[('type_tax_use', '=', 'purchase')]")
