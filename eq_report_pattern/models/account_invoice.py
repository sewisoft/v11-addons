# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EqAccountInvoice(models.Model):
    _inherit = 'account.invoice'
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template')#TODO: readonly falls Rechnung nicht mehr editierbar?
    comment = fields.Html('Additional Information')

    @api.model
    def change_template_id(self, quote_template, partner=False, fiscal_position_id=False, order_lines=[]):
        if not quote_template:
            return True
        lines = []
        sale_order_line_obj = self.env['sale.order.line']
        for line in quote_template.eq_quote_line:
            res = sale_order_line_obj.product_id_change()
            data = res.get('value', {})
            if 'tax_id' in data:
                data['tax_id'] = [(6, 0, data['tax_id'])]
            data.update({
                'name': line.name,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
            })
            lines.append((0, 0, data))
        return lines

    @api.onchange('document_template_id')
    def onchange_document_template_id(self):
        """
        Übernahme der Texte beim Wechsel des Templates
        :return:
        """
        selected_template = self.document_template_id
        if self.partner_id and self.partner_id.lang and self.document_template_id:
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)

        if selected_template:
            self.eq_head_text = selected_template.eq_header
            self.comment = selected_template.eq_footer
