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

from odoo import fields, models, api


class EqMailConfigSettings(models.TransientModel):
    _name = 'eq_mail_config.settings'
    _inherit = 'res.config.settings'    

    def set_values(self):
        super(EqMailConfigSettings, self).set_values()
        ir_default = self.env['ir.default']
        config = self.browse(self.ids)
        ir_default.set('mail.mail', 'mail_server_id', config.mail_server_id and config.mail_server_id.id or False)
        ir_default.set('mail.mail', 'mail_server_address', config.mail_server_address or False)

    @api.model
    def get_values(self):
        res = super(EqMailConfigSettings, self).get_values()
        ir_default = self.env['ir.default']
        receivable = ir_default.get('mail.mail', 'mail_server_id')
        existing_ir_mail_server = self.env['ir.mail_server'].search([('id', '=', receivable)])

        if len(existing_ir_mail_server) > 0:
            address = self.env['ir.mail_server'].browse(receivable)
            receivable = existing_ir_mail_server[0]
        else:
            address = False
            receivable = False
        res.update(
                mail_server_id=existing_ir_mail_server.id if receivable else "",
                mail_server_address=address.smtp_user if address else "",
        )
        return res

    mail_server_id = fields.Many2one('ir.mail_server', 'Default Mail Server',
                                     help="""The outgoing mail server that the system
                                     should user for sending e-mails.""")
    mail_server_address = fields.Char('Default Mails Server Address')

    @api.onchange('mail_server_id')
    def on_change_mail_server(self):
        address = self.env['ir.mail_server'].browse(self.mail_server_id.id)
        values = {'mail_server_address': address.smtp_user}
        return {'value': values}
