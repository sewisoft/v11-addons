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
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp


class EqProductProduct(models.Model):
    _inherit = 'product.product'

    _sql_constraints = [('default_code_unique', 'unique(default_code)', 'This Product No. is already in use !')]

    def _generate_ean(self, company_ean, sequence):
        ean_without_checksum = company_ean + sequence[-5:]

        oddsum = 0
        evensum = 0
        for i in range(0, len(ean_without_checksum)):
            if i % 2 == 0:
                oddsum += int(ean_without_checksum[i])
            else:
                evensum += int(ean_without_checksum[i])
        total = oddsum + (evensum * 3)
        checksum = int(10 - total % 10.0) % 10
        if checksum == 10:
            checksum == 0
        ean13 = ean_without_checksum + str(checksum)
        self.write({'ean13': ean13})

    @api.model
    def create(self, vals):
        """
        Unsere Erweiterung der CREATE Methode
        :param vals:
        :return:
        """
        res = super(EqProductProduct, self).create(vals)
        # Nummer wurde nicht eingegeben, wir müssen sie generieren
        if 'default_code' not in vals or vals['default_code'] is False:
            self.eq_product_number_update(res)
            res.barcode = res.default_code
        return res

    @api.multi
    def eq_product_number_update(self, res):
        if self.id is False:
            self = res
        product_product_obj = self.env['product.product'].browse(self.id)
        seq = self.env['ir.sequence'].next_by_code('eq_product_no')
        vals = {'default_code': seq}
        product_product_obj.write(vals)


class EqProductTemplate(models.Model):
    _inherit = 'product.template'

    _sql_constraints = [('default_code_unique', 'unique(default_code)', 'This Product No. is already in use !')]

    @api.multi
    def write(self, vals):
        if 'standard_price' in vals:
            old_price = self.standard_price
            new_price = vals['standard_price']
            history_vals = {
                'eq_product_id': self.id,
                'eq_old_price': old_price,
                'eq_new_price': new_price,
            }
            self.env['product.template.standard_price_history'].create(history_vals)
        res = super(EqProductTemplate, self).write(vals)

        # Korrektur der Lokalisierung für das Feld name, damit wir kein Problem mehr mit dem Modul web_translate haben
        if self._context is not None:
            if 'lang' in self._context and 'name' in vals:  # sehr wichtig ! die Write-Methode wird ausgeführt auch wenn man in den Einstellungen etwas speichert !
                actual_language = self._context['lang']
                text_to_be_set = vals['name']
                ir_translation_obj = self.env['ir.translation']
                ir_translation_record = ir_translation_obj.sudo().search([('res_id', '=', self.id), (
                    'lang', '=', actual_language), ('name', '=', 'product.template,name')])
                if ir_translation_record:
                    ir_translation_record.value = text_to_be_set

        return res

    def _generate_ean(self, prod_variant, company_ean, sequence):
        ean_without_checksum = company_ean + sequence[-5:]

        oddsum = 0
        evensum = 0
        for i in range(0, len(ean_without_checksum)):
            if i % 2 == 0:
                oddsum += int(ean_without_checksum[i])
            else:
                evensum += int(ean_without_checksum[i])
        total = oddsum + (evensum * 3)
        checksum = int(10 - total % 10.0) % 10
        if checksum == 10:
            checksum == 0
        ean13 = ean_without_checksum + str(checksum)
        prod_variant.write({'ean13': ean13})


class EqProductTemplateStandardPriceHistory(models.Model):
    _name = 'product.template.standard_price_history'

    eq_product_id = fields.Many2one('product.template', string="Product")
    eq_old_price = fields.Float(string="Old Price", digits=dp.get_precision('Product Price Purchase'))
    eq_new_price = fields.Float(string="New Price", digits=dp.get_precision('Product Price Purchase'))
    create_uid = fields.Many2one('res.users', string="User")
    create_date = fields.Datetime(string="Create Date")

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, _('Change ') + self.create_date))
        return res


class eq_sale_config_product(models.TransientModel):
    _inherit = 'res.config.settings'

    default_eq_min_prefix_count = fields.Integer('Min prefix lenght [equitania]')
    default_eq_max_prefix_count = fields.Integer('Max prefix lenght [equitania]')
    default_eq_prod_num_lenght = fields.Integer('Product number lenght [equitania]')
    default_eq_seperator = fields.Char('Seperator [equitania]')

    @api.model
    def get_values(self):
        res = super(eq_sale_config_product, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            default_eq_min_prefix_count=ICPSudo.get_param('eq_product.default_eq_min_prefix_count'),
            default_eq_max_prefix_count=ICPSudo.get_param('eq_product.default_eq_max_prefix_count'),
            default_eq_prod_num_lenght=ICPSudo.get_param('eq_product.default_eq_prod_num_lenght'),
            default_eq_seperator=ICPSudo.get_param('eq_product.default_eq_seperator'),
        )
        return res

    @api.multi
    def set_values(self):
        super(eq_sale_config_product, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("eq_product.default_eq_min_prefix_count", self.default_eq_min_prefix_count)
        ICPSudo.set_param("eq_product.default_eq_max_prefix_count", self.default_eq_max_prefix_count)
        ICPSudo.set_param("eq_product.default_eq_prod_num_lenght", self.default_eq_prod_num_lenght)
        ICPSudo.set_param("eq_product.default_eq_seperator", self.default_eq_seperator)

