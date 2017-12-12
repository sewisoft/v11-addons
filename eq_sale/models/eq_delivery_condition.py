# -*- coding: utf-8 -*-

from odoo import models, fields


class EqDeliverConditions(models.Model):
    _name = 'eq.delivery.conditions'
    _rec_name = 'eq_name'

    eq_name = fields.Char('Name', size=128)
