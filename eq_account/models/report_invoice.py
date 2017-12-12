# -*- coding: utf-8 -*-

from odoo import api, models, fields


class ReportAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    eq_ref_number = fields.Char('Sale Order Referenc', size=64)

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Quantity Report')

    @api.multi
    def html_text_is_set(self, value):
        """
        Workaround für HTML-Texte: Autom. Inhalt nach Speichern ohne Inhalt <p><br></p>
        :param value:
        :return:
        """
        if not value:
            return False

        value = value.replace('<br>', '')
        value = value.replace('<p>', '')
        value = value.replace('</p>', '')
        value = value.replace('<', '')
        value = value.replace('>', '')
        value = value.replace('/', '')
        value = value.strip()
        return value != ''


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    move_ids = fields.One2many(
            comodel_name='stock.move',
            inverse_name='sale_line_id',
            string='Ralated Moves',
            readonly=True,
            ondelete='set null'
    )


class ReportAccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    eq_move_ids = fields.Many2many('stock.move', string="Move") #Notwendig bei Teillieferungen
    eq_move_id = fields.Many2one('stock.move', string="Move")   #Funktioniert, nur nicht bei Teillieferungen

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report [eq_sale]',
                                                      currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Unit of Measure Report [eq_sale]')

    @api.multi
    def create(self, vals):
        """
            let's get original sequence no from deliverynote and save it for every position on delivery note
            @cr: cursor
            @use: actual user
            @vals: alle values to be saved
            @context: context
        """

        res = super(ReportAccountInvoiceLine, self).create(vals)
        stock_move_list = []
        account_invoice_line = res
        sale_line_id = account_invoice_line.sale_line_ids.id
        if sale_line_id:
            stock_move_objs = self.env['stock.move'].search([('sale_line_id', '=', sale_line_id),('state','=','done')])
            for stock_move_obj in stock_move_objs:
                if len(stock_move_obj.origin_returned_move_id) == 0:
                    stock_move_list.append(stock_move_obj.id)
                    # Obsolete sobald Report angepasst wurde
                    res.update({'eq_move_id': stock_move_obj.id})
                else:
                    pass
            if len(stock_move_list) > 0:
                res.update({'eq_move_ids': [(6, 0, stock_move_list)]})
        return res


class EqReportExtensionStockPicking(models.Model):
    _inherit = "stock.picking"

    eq_ref_number = fields.Char('Sale Order Referenc', size=64)

    @api.model
    def create(self, vals):
        """
            Adds the customer ref number to the picking list. Gets data from context which is set in the method action_ship_create of the sale.order
            @cr: cursor
            @user: actual user
            @vals: values to be saved - we'll append eq_ref_number here
            @context: context
            @return: result of super method
        """
        res = super(EqReportExtensionStockPicking, self).create(vals)
        sale_order_obj = res.eq_sale_order_id
        client_order_ref = sale_order_obj.client_order_ref

        res.update({'eq_ref_number': client_order_ref})

        return res
