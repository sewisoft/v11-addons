# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EqProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.one
    def _eq_sale_count(self):
        res = ''
        query = """select sum(product_uom_qty) from stock_move where sale_line_id in
        (select id from sale_order_line as sol where sol.product_id in
        (select id from product_product where product_tmpl_id = %d)
        and sol.state not in ('cancel')
        and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))
        and state not in ('sale', 'done', 'cancel')
        and picking_id is not null""" % (self.id)
        self._cr.execute(query)
        open = self._cr.fetchone()[0] or 0
        qry_all = """select sum(product_uom_qty) from sale_order_line where product_id in (select id from product_product where product_tmpl_id = %d) and state != 'cancel' and state != 'done' and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (
                self.id)
        self._cr.execute(qry_all)
        all = self._cr.fetchone()[0] or 0
        res = '%d / %d' % (open, all)
        self.eq_sale_count = res

    eq_sale_count = fields.Char(compute='_eq_sale_count', string="Sales")


class EqProductProduct(models.Model):
    _inherit = 'product.product'

    @api.one
    def _eq_sale_count(self):
        qry_open = """select sum(product_uom_qty) from stock_move where sale_line_id in
        (select id from sale_order_line as sol where sol.product_id  = %d
        and sol.state not in ('cancel', 'done') 
        and (select state from sale_order where id = sol.order_id) not in ('sent', 'draft'))
        and state not in ('done', 'cancel', 'sale')
        and picking_id is not null""" % (self.id)

        self._cr.execute(qry_open)
        open = self._cr.fetchone()[0] or 0

        qry_all = """select sum(product_uom_qty) from sale_order_line where product_id = %d and state != 'cancel'  and state != 'done' 
        and (select state from sale_order where id = order_id) not in ('sent', 'draft')""" % (self.id)

        self._cr.execute(qry_all)
        all = self._cr.fetchone()[0] or 0
        res = '%d / %d' % (open, all)
        self.eq_sale_count = res

    eq_sale_count = fields.Char(compute='_eq_sale_count', string="Sales")
    eq_rrp = fields.Float(string='RRP')
