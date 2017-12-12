# -*- coding: utf-8 -*-

from odoo import models, fields


class EqStockPicking(models.Model):
    _inherit = 'stock.picking'

    eq_header_text = fields.Html(string="Header")
    eq_footer_text = fields.Html(string="Footer")
    eq_use_page_break_after_header = fields.Boolean(string='Page break after header text')
    eq_use_page_break_before_footer = fields.Boolean(string='Page break before footer text')
