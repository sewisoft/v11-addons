# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EqSaleOrderTemplate(models.Model):
    _inherit = 'sale.order'
   
    document_template_id = fields.Many2one(comodel_name='eq.document.template', string='Document Template', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    # Automatischen Test anlegen
    @api.model
    def change_template_id(self, quote_template, partner=False, fiscal_position_id=False, order_lines=[]):
        if not quote_template:
            return True
        lines = []
        sale_order_line_obj = self.env['sale.order.line']
        for line in quote_template.eq_quote_line:
            data = {}
            try:
                fpos = self.fiscal_position_id or self.partner_id.property_account_position_id
                # If company_id is set, always filter taxes by the company
                taxes = line.product_id.taxes_id.filtered(lambda r: not self.company_id or r.company_id == self.company_id)
                data['tax_id'] = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id) if fpos else taxes
            except:
                pass

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
        selected_template = self.document_template_id
        if self.partner_id and self.partner_id.lang and self.document_template_id:
            selected_template = self.document_template_id.with_context(lang=self.partner_id.lang)

        if selected_template:
            self.eq_head_text = selected_template.eq_header
            self.note = selected_template.eq_footer
            partner_id = False
            if self.partner_id:
                partner_id = self.partner_id.id
            if self.document_template_id:
                res = self.change_template_id(selected_template, partner_id, self.fiscal_position_id,
                                                         self.order_line)
                if res:
                    self.order_line = res
        self.eq_header = selected_template.eq_header
        self.note = selected_template.eq_footer

    @api.multi
    def _prepare_invoice(self):
        """
        Überschrieben zum Setzen der Dokumentenvorlage
        :return:
        """
        result = super(EqSaleOrderTemplate, self)._prepare_invoice()
        if self.document_template_id:
            result['document_template_id'] = self.document_template_id.id
        return result
