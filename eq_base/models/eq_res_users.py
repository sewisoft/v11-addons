# -*- coding: utf-8 -*-

from odoo import models, fields


class EqResUsers(models.Model):
    _inherit = 'res.users'

    eq_signature = fields.Binary(string='Signature')
