# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EqStockPickingExtension(models.Model):
    _inherit = 'stock.picking'

    eq_sale_order_id = fields.Many2one('sale.order', 'SaleOrder')

    @api.model
    def create(self, vals):
        """
            Extended version of create method. We're using this in process "Confirm an order" to be able to set
            link between sale order and stock_picking.
            It's a simple solution to save sale_order_id defined as many2one field eq_sale_order_id.
            @vals: values to be saved
            @return: defaul result
        """
        sale_order_obj = self.env['sale.order']
        if 'origin' in vals:
            sale_order_ids = sale_order_obj.search([("name", "=", vals["origin"])])
            if sale_order_ids and len(sale_order_ids) > 0:
                found_sale_order = sale_order_ids[0]
                vals['eq_sale_order_id'] = found_sale_order.id
                vals['eq_header_text'] = found_sale_order.eq_head_text
                vals['eq_footer_text'] = found_sale_order.note
        return super(EqStockPickingExtension, self).create(vals)
