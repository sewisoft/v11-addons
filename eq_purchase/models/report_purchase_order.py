# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2017-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import datetime
from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT

# Funktionen für Model, die über Report aufgerufen werden können

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

    def get_delivery_date_flag(self):
        """
        Anzeige geplantes Datum auf Basis der Checkbox 'Das geplante Datum in der Bestellung anzeigen [eq_purchase]' in der Konfiguration
        :param value:
        :param language:
        :return:
        """
        ir_values_obj = self.env['ir.values']
        show_delivery_date = ir_values_obj.get_default('purchase.order', 'show_planned_date')
        return show_delivery_date

    def get_delivery_date_kw_flag(self):
        """
        Anzeige geplante Datum auf Basis der Checkbox 'Das geplante Datum in der Bestellung anzeigen [eq_purchase] ' in der Konfiguration
        :param value:
        :param language:
        :return:
        """
        ir_values_obj = self.env['ir.values']
        show_calendar_week = ir_values_obj.get_default('purchase.order', 'use_calendar_week')
        return show_calendar_week

    def get_delivery_date_kw(self, delivery_date):
        """
        Anzeige geplante Datum als KW
        :param value:
        :param language:
        :return:
        """
        if delivery_date != False:
            new_date = delivery_date.split(' ')
            date = datetime.datetime.strptime(new_date[0], "%Y-%m-%d")
            year = date.year
            month = date.month
            day = date.day
            d = datetime.date(year, month, day)
            kw = d.isocalendar()[1]
            kw = str(kw)

            return kw

    def get_formatted_planned_date(self, planned_date):
        planned_date = planned_date.split(" ")
        planned_date = datetime.datetime.strptime(planned_date[0], OE_DFORMAT)
        planned_date = planned_date.strftime('%d.%m.%Y')
        return planned_date
