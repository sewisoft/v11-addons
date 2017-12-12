# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EqResPartner(models.Model):
    _inherit = 'res.partner'

    eq_firstname = fields.Char('Firstname')
    eq_name2 = fields.Char('Name2')
    eq_name3 = fields.Char('Name3')

    eq_house_no = fields.Char('House number')
    eq_citypart = fields.Char('District')
    eq_birthday = fields.Date('Birthday')
    eq_letter_salutation = fields.Char('Salutation')
    eq_foreign_ref = fields.Char('Foreign reference')
    eq_foreign_ref_purchase = fields.Char('Foreign reference purchase')

    eq_email2 = fields.Char('E-Mail (additional)')
    eq_phone2 = fields.Char('Phone (additional)')

    eq_deb_cred_number = fields.Char(compute="_show_deb_cred_number", store=False)

    @api.model
    def _address_fields(self):
        res = super(EqResPartner, self)._address_fields()
        res.extend(("eq_house_no", "eq_citypart"))
        return res

    @api.multi
    def _show_deb_cred_number(self):
        for partner in self:
            deb_cred = False
            if partner.customer_number != 'False' and partner.customer_number and partner.supplier_number != 'False' and partner.supplier_number:
                deb_cred = partner.customer_number + ' / ' + partner.supplier_number
            elif partner.customer_number != 'False' and partner.customer_number:
                deb_cred = partner.customer_number
            elif partner.supplier_number != 'False' and partner.supplier_number:
                deb_cred = partner.supplier_number
            partner.eq_deb_cred_number = deb_cred
