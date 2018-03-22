# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EqResCompanyConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    eq_report_logo = fields.Binary('Company Report Logo')

    @api.multi
    def get_values(self):
        res = super(EqResCompanyConfig, self).get_values()
        user = self.env['res.users'].browse(self._uid)
        found_company = False
        if user:
            found_company = user.company_id
        if found_company:
            result = found_company.eq_report_logo
            if result:
                res.update(eq_report_logo=result)
                return res
        res.update(eq_report_logo=None)
        return res

    @api.multi
    def set_values(self):
        super(EqResCompanyConfig, self).set_values()
        for record in self:
            record.company_id.eq_report_logo = record.eq_report_logo
