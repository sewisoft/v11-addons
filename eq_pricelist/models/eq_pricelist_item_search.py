# -*- coding: utf-8 -*-

from odoo import models, api, _


class EqProductPricelistItemSearchItem(models.Model):
    _inherit = 'product.pricelist.item'

    @api.one
    def delete(self):
        self.unlink()
        return True

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = _("%s, Min. %s New Price %s") % (record.name, record.min_quantity, record.price_surcharge)
            res.append((record.id, name))
        return res
