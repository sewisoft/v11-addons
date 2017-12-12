# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    eq_planned_date_type_purchase = fields.Selection([('cw', 'Calendar week'), ('date', 'Date')],
                                                     string="Planned Date Purchase",
                                                     help="If nothing is selected, the default from the "
                                                          "settings will be used.")
