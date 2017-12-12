# -*- coding: utf-8 -*-

from odoo import models, fields


class EqProductTemplateBlock(models.Model):
    _inherit = "product.template"

    eq_website_description = fields.Html(translate=True)
    website_description = fields.Html(translate=True)
