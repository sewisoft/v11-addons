# -*- coding: utf-8 -*-

from odoo import models, api


class ReportPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def get_tax(self, tax_id, language, currency_id):
        amount_net = 0
        for line in self.order_line:
            if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
                amount_net += line.price_subtotal

        tax_amount = 0
        for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
            tax_amount += tex['amount']
        return self.env["eq_report_helper"].get_price(tax_amount, language, 'Purchase Price Report [eq_purchase]', currency_id)

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Purchase Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Purchase Price Report [eq_purchase]', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Purchase Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Purchase Unit of Measure Report [eq_purchase]')

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


class ReportPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Purchase Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Purchase Price Report [eq_purchase]', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Purchase Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Purchase Unit of Measure Report [eq_purchase]')