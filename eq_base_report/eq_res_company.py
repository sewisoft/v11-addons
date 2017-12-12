# -*- coding: utf-8 -*-

from odoo import models, fields


class EqResCompany(models.Model):
    _inherit = 'res.company'

    eq_report_logo = fields.Binary('Company Report Logo')
    external_report_layout = fields.Selection([
        ('background', 'Background'),
        ('boxed', 'Boxed'),
        ('clean', 'Clean'),
        ('standard', 'Standard'),
        ('equitania', 'Equitania'),
    ], string='Document Template')
