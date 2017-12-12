# -*- coding: utf-8 -*-

from odoo import models, fields

"""
Hilfsklassen für die Anzeige von Meldungen in Odoo
"""


class EqMessage(models.TransientModel):
    _name = "eq_message"
    
    eq_info = fields.Char("Info")
    eq_message_text = fields.Char("Message")
    
    
class EqProtMessage(models.TransientModel):
    _inherit = ['eq_message']
    
    eq_res_id = fields.Many2one('eq.ebid.protocol', string='Protocol', required=False)
