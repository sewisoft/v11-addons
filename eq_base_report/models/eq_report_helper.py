# -*- coding: utf-8 -*-

import datetime
from odoo import models


class EqReportHelper(models.TransientModel):
    _name = "eq_report_helper"

    def get_qty(self, value, language, param_name):
        precision = self.env['decimal.precision'].precision_get(param_name)
        string = ("%%5.%df" % precision)
        result = (string % value)

        # parse string and generate correct number format
        result = self.reformat_string(result, precision, language)

        return result

    def get_price(self, value, language, param_name, currency_id=False):
        precision = self.env['decimal.precision'].precision_get(param_name)
        string = ("%%5.%df" % precision)
        result = (string % value)

        # parse string and generate correct number format
        result = self.reformat_string(result, precision, language)
        # Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)

        return result

    def get_standard_price(self, object, language, currency_id=False):
        """
            Price formater - formats given number to default price format 1.000,00
        """

        precision = 2
        string = ("%%5.%df" % precision)
        result = (string % object)
        result = self.reformat_string(result, precision, language)
        # Currency Symbol is added
        if currency_id:
            result += (' %s' % currency_id.symbol)

        return result

    def get_gross_price_invoice(self, object, language, currency_id=False):
        """
            Calculate gross price a return result as string together with currency back
            @object: order line object
            @currency_id: Currency
            @return: Calculated gross price
        """

        gross_price = object.price_unit * object.quantity
        return self.get_standard_price(gross_price, language, currency_id)

    def get_gross_price(self, object, language, currency_id=False):
        """
            Calculate gross price a return result as string together with currency back
            @object: order line object
            @currency_id: Currency
            @return: Calculated gross price
        """

        gross_price = object.price_unit * object.product_uom_qty
        return self.get_standard_price(gross_price, language, currency_id)

    def _convert_string_to_date(self, date_as_string):
        """
            Convert date in string format like '2016-02-09' into date
            @date_as_string: date in string format
            @return: string converted into date

        """
        return datetime.datetime.strptime(date_as_string, '%Y-%m-%d')

    def _get_date_format_for_language(self, lang_code):
        """
            Get date format for actual language
            @lang_code: actual language code
            @return: Date forma for actual language
        """
        lang_obj = self.env['res.lang']
        languages = lang_obj.search([('code', '=', lang_code)])
        if languages:
            return languages[0].date_format

        return ''

    def reformat_string(self, data, precision, language):
        """
            Creates formated number with count of decimal positions from odd and puts hardcoded thousand separator on right place.
            We can chane both tags for decimal separator and thousand separator in our variables
            @data: number as string formated from odoo
            @precision: count of decimal positions from odoo
        """

        res_lang_obj = self.env["res.lang"]
        langauge_record = res_lang_obj.search([("code", "=", language)])
        DECIMAL_SEPARATOR_TAG = langauge_record.decimal_point
        THOUSAND_SEPARATOR_TAG = langauge_record.thousands_sep
        data = data.replace(".", DECIMAL_SEPARATOR_TAG)

        # delete all white spaces
        data = data.replace(" ", "")

        # finalResult = data
        tempData = ""
        decimal_part = ""

        # extract decimal part in case, that we have one in our string
        if precision > 0:
            startIndex = data.find(DECIMAL_SEPARATOR_TAG);
            endIndex = len(data)

            # get decimal part...example 1256,85 -> decimal_part = ,85
            decimal_part = data[startIndex:endIndex]

            tempdata = data[0:startIndex]
            data = tempdata

        # iterate our numbre from end to start and set THOUSAND_SEPARATOR_TAG on right place
        index = len(data)
        counter = 0
        finalResult = ""
        while index > 0:
            if counter == 3:
                finalResult += THOUSAND_SEPARATOR_TAG
                counter = 0

            finalResult += data[index - 1]
            index = index - 1
            counter = counter + 1

        # we're done here, let's reverse our string to get back to normal number
        finalResult = finalResult[::-1]

        # append decimal_part if we have one
        if len(decimal_part) > 0:
            finalResult += decimal_part

        return finalResult

    def get_sum_without_optional_positions(self, category_positions):
        """
        Berechnet die Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        :param category_positions: Alle Positionen einer Kategorie
        :return: Zwischensumme der Positionen einer Kategorie und ignoriert dabei alle Positionen, die als OPTIONAL definiert sind
        """
        result = 0
        for position in category_positions:
            if position.eq_optional is False:
                result = result + position.price_subtotal

        return result
