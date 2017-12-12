# -*- coding: utf-8 -*-

from odoo import models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def reflect_code_digits_change(self, digits):
        accounts = self.env['account.account'].search([('company_id', '=', self.id)], order='code asc')
        for account in accounts:
            if len(account.code) == digits:
                account.write({'code': account.code.ljust(digits, '0')})
