# -*- coding: utf-8 -*-

from odoo import models, fields


class EqDocumentTemplate(models.Model):
    _name = "eq.document.template"
    
    name = fields.Char(string="Name", translate=True, required=True)
    eq_quote_line = fields.One2many('sale.quote.line', 'quote_id', 'Quote Template Lines', copy=True)
    eq_header = fields.Html(string="Header", translate=True)
    eq_footer = fields.Html(string="Footer", translate=True)
