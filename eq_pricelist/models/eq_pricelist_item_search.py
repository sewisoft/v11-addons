# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2017-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
