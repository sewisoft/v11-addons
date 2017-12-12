# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
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

import base64
import odoo
from odoo import models, fields, api, _


class EqPrintWizard(models.TransientModel):
    _name = 'eq.print.wiz'
    
    def _get_default_printer(self):
        user = self.env['res.users'].browse(self._uid)
        if user.eq_default_printer_id:
            return user.eq_default_printer_id.id
        else:
            return False
    
    def _get_default_user(self):
        if self._uid:
            return self._uid
        else:
            return False
    
    eq_printer_id = fields.Many2one(string="Printer", comodel_name="eq.printer",
                                    default=_get_default_printer, required=True)
    eq_copies = fields.Integer(string="Copies", default=1, required=True)
    eq_user_id = fields.Many2one(string="User", comodel_name="res.users",
                                 default=_get_default_user, required=True)
    
    @api.multi
    def print_document(self):
        active_ids = self.env.context['active_ids']
        # Anpassung für Pentaho
        act_report_xml_obj = self.env['ir.actions.report']
        found_report = None
        if 'params' in self.env.context:
            if 'action' in self.env.context['params']:
                action = self.env.context['params']['action']
                seach_rep = act_report_xml_obj.search([('eq_report_wiz_action', '=', action)])
                if seach_rep:
                    found_report = act_report_xml_obj.browse(seach_rep.id)
        if found_report and found_report != None:
            pdf_binary = found_report.render_qweb_pdf(active_ids)
        else:
            pdf_binary = act_report_xml_obj.search([('report_name', '=', self.env.context['report_name'])]).render_qweb_pdf(active_ids)
        encoded_pdf_binary = base64.b64encode(pdf_binary[0])
        current_obj = self.env[self._context['active_model']]
        current_obj_rec_name = current_obj._rec_name
        current_records = current_obj.browse(active_ids)
        document_name = ""
        if len(current_records) == 1:
            document_name = getattr(current_records, current_obj_rec_name)
        elif len(current_records) > 1:
            document_name = "%sx %s" % (len(current_records), current_obj._description)
        spooltable_vals = {
                           'eq_printer_id': self.eq_printer_id.id,
                           'eq_user_id': self.eq_user_id.id,
                           'eq_copies': self.eq_copies,
                           'eq_file': encoded_pdf_binary,
                           'eq_document_name': document_name,
                           'state': 'open',
                           }
        self.env['eq.spooltable'].create(spooltable_vals)
        return True
