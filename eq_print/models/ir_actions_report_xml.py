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

from odoo import models, fields, api, _


class EqIrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report'

    eq_direct_print = fields.Boolean(string="Remote Print")
    eq_report_wiz_action = fields.Many2one(string="Report Wizard Action", comodel_name="ir.actions.act_window")

    @api.onchange('report_type')
    def _onchange_report_type(self):
        self.eq_direct_print = False
        
    @api.multi
    def _get_wiz_action(self):
        self.ensure_one()
        if self.eq_report_wiz_action:
            return self.eq_report_wiz_action.id
        else:
            act_window_obj = self.env['ir.actions.act_window']
            
            rep_wiz_action_id = self.env['ir.model.data'].xmlid_to_res_id('eq_print.eq_print_wiz_action', raise_if_not_found=True)
            act = act_window_obj.browse(rep_wiz_action_id)

            copied_data_list = act.copy_data([])
            rep_wiz_action_vals = copied_data_list[0]
            rep_wiz_action_vals['name'] = self.name + ' Remote Print'
            rep_wiz_action_vals['context'] = "{'report_name': '" + self.report_name + "' }"
            rep_wiz_action_vals['id'] = "action_print_menu"
            rep_wiz_action_vals['binding_model_id'] = self.binding_model_id.id
            rep_wiz_action_vals["binding_type"] = 'report'
            new_rep_wiz_action_id = act_window_obj.create(rep_wiz_action_vals)
            self.update({'eq_report_wiz_action': new_rep_wiz_action_id.id})
            return new_rep_wiz_action_id.id
    
    @api.multi
    def _update_ir_values(self):
        for rep in self:
            if rep.eq_direct_print:
                action = rep._get_wiz_action()
            else:
                rep.eq_report_wiz_action.unlink()

    @api.model
    def create(self, vals):
        res = super(EqIrActionsReportXml, self).create(vals)
        self._update_ir_values()
        return res
 
    @api.multi
    def write(self, vals):
        res = super(EqIrActionsReportXml, self).write(vals)
        self._update_ir_values()
        return res
