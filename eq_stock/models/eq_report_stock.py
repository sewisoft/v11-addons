# -*- coding: utf-8 -*-

from odoo import models, api


class ReportStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def html_text_is_set(self, value):
        if not value:
            return False
        value = value.replace('<br>', '')
        value = value.replace('<p>', '')
        value = value.replace('</p>', '')
        value = value.replace('<', '')
        value = value.replace('>', '')
        value = value.replace('/', '')
        value = value.strip()
        return value != ''
