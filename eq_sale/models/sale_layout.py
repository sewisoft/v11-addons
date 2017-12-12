# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'
    _order = 'sequence'

    separator = fields.Boolean('Add separator', default=True)
