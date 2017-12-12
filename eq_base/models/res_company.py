# -*- coding: utf-8 -*-

from odoo import models, fields


class EqModuleTemplate(models.Model):
    _inherit = 'res.company'

    eq_ceo_title = fields.Char('Eq ceo title', translate=True)
    eq_ceo_01 = fields.Char('CEO 1')
    eq_ceo_02 = fields.Char('CEO 2')
    eq_ceo_03 = fields.Char('CEO 3')
