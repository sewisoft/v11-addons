# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EqStockPicking(models.Model):
    _inherit = 'stock.picking'
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template')#TODO: readonly falls Rechnung nicht mehr editierbar?

    # account.invoice enthaelt die selbe Methode und ist auf die selbe Art ueberschrieben
    @api.onchange('document_template_id')
    def onchange_document_template_id(self):
        selected_template = self.document_template_id
        if self.partner_id and self.partner_id.lang and self.document_template_id:
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)
        if selected_template:
            self.eq_header_text = selected_template.eq_header
            self.eq_footer_text = selected_template.eq_footer

    @api.model
    def create(self, vals):
        """
        Überschrieben zur Übernahme der Dokumentenvorlage aus dem Auftrag
        :param vals:
        :return:
        """
        sale_order_obj = self.env['sale.order']
        sale_order_ids = sale_order_obj.search([("name", "=", vals["origin"])])
        if sale_order_ids:
            sale_order_origin = sale_order_ids[0]
            if sale_order_origin:
                vals['document_template_id'] = sale_order_origin.document_template_id.id
        
        return super(EqStockPicking, self).create(vals)
