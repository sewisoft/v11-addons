# -*- coding: utf-8 -*-
import datetime
from odoo import api, models


class ReportSaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_tax(self, tax_id, language, currency_id):
        """
        Berechnet MwSt für die aktuelle Sprache und liefert den Wert zurück
        :param tax_id: MwSt-ID
        :param language: Aktuelle Sprache
        :param currency_id: Aktuelle Währung
        :return: MwSt für die aktuelle Sprache
        """
        amount_net = 0;
        for line in self.order_line:
            if tax_id.id in [x.id for x in line.tax_id] and not line.eq_optional:
                amount_net += line.price_subtotal
        tax_amount = 0
        for tex in self.env['account.tax']._compute([tax_id], amount_net, 1):
            tax_amount += tex['amount']
        return self.env["eq_report_helper"].get_price(tax_amount, language, 'Sale Price Report', currency_id)

    @api.multi
    def get_sum_without_optional_positions(self, category_id):
        """
        Berechnet die Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        :param category_positions: Alle Positionen einer Kategorie
        :return: Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        """
        return self.env["eq_report_helper"].get_sum_without_optional_positions(category_id)

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
        Workaround für HTML-Texte: Autom. Inhalt nach Speichern ohne Inhalt: <p><br></p>
        Entfernen der Zeilenumbrüche und Paragraphen für Test, ob ein Inhalt gesetzt wurde
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


class ReportSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def get_price(self, value, currency_id, language):
        """
        Formatierung eines Preises mit Berücksichtigung der Einstellung Dezimalstellen Sale Price Report
        :param value:
        :param currency_id:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_price(value, language, 'Sale Price Report [eq_sale]', currency_id)

    @api.multi
    def get_qty(self, value, language):
        """
        Formatierung für Mengenangabe mit Berücksichtigung der Einstellung Dezimalstellen Sale Quantity Report
        :param value:
        :param language:
        :return:
        """
        return self.env["eq_report_helper"].get_qty(value, language, 'Sale Unit of Measure Report [eq_sale]')

    def get_delivery_date_flag(self):
        """
        Anzeige Lieferdatum auf Basis der Checkbox 'Liefertermin auf Angebot und Auftragsbestätigung anzeigen [eq_sale]' in der Konfiguration
        :param value:
        :param language:
        :return:
        """
        ir_values_obj = self.env['ir.values']
        show_delivery_date = ir_values_obj.get_default('sale.order', 'show_delivery_date')
        return show_delivery_date

    def get_delivery_date_kw_flag(self):
        """
        Anzeige Lieferdatum auf Basis der Checkbox 'Liefertermin als Kalenderwoche anzeigen [eq_sale] ' in der Konfiguration
        :param value:
        :param language:
        :return:
        """
        ir_values_obj = self.env['ir.values']
        show_calendar_week = ir_values_obj.get_default('sale.order', 'use_calendar_week')
        return show_calendar_week

    def get_delivery_date_kw(self, delivery_date):
        """
        Anzeige Lieferdatum als KW
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
