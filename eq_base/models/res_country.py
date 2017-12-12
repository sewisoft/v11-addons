# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCountry(models.Model):
    _inherit = 'res.country'

    eq_active = fields.Boolean(string="Active", default=True)
