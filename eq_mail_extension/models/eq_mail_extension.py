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

import logging
try:
    import io
except ImportError:
    import io

from odoo import fields, models, exceptions
from odoo import api
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)
MAX_POP_MESSAGES = 50


class EqFetchmailServer(models.Model):
    _inherit = "fetchmail.server"

    user_id = fields.Many2one('res.users', string="Owner")
    
    # Copy and Pasted form original fetchmail.server and removed the remove E-Mail for pop mail servers.
    @api.multi
    def fetch_mail(self):
        """ WARNING: meant for cron usage only - will commit() after each email! """
        additionnal_context = {
            'fetchmail_cron_running': True
        }
        MailThread = self.env['mail.thread']
        for server in self:
            _logger.info('start checking for new emails on %s server %s', server.type, server.name)
            additionnal_context['fetchmail_server_id'] = server.id
            additionnal_context['server_type'] = server.type
            count, failed = 0, 0
            imap_server = None
            pop_server = None
            if server.type == 'imap':
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    result, data = imap_server.search(None, '(UNSEEN)')
                    for num in data[0].split():
                        res_id = None
                        result, data = imap_server.fetch(num, '(RFC822)')
                        imap_server.store(num, '-FLAGS', '\\Seen')
                        try:
                            res_id = MailThread.with_context(**additionnal_context).message_process(
                                server.object_id.model, data[0][1], save_original=server.original,
                                strip_attachments=(not server.attach))
                        except Exception:
                            _logger.info('Failed to process mail from %s server %s.', server.type, server.name,
                                         exc_info=True)
                            failed += 1
                        if res_id and server.action_id:
                            server.action_id.with_context({
                                'active_id': res_id,
                                'active_ids': [res_id],
                                'active_model': self.env.context.get("thread_model", server.object_id.model)
                            }).run()
                        imap_server.store(num, '+FLAGS', '\\Seen')
                        self._cr.commit()
                        count += 1
                    _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", count, server.type,
                                 server.name, (count - failed), failed)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type,
                                 server.name, exc_info=True)
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
            elif server.type == 'pop':
                try:
                    while True:
                        pop_server = server.connect()
                        (num_messages, total_size) = pop_server.stat()
                        pop_server.list()
                        for num in range(1, min(MAX_POP_MESSAGES, num_messages) + 1):
                            (header, messages, octets) = pop_server.retr(num)
                            message = '\n'.join(messages)
                            res_id = None
                            try:
                                res_id = MailThread.with_context(**additionnal_context).message_process(
                                    server.object_id.model, message, save_original=server.original,
                                    strip_attachments=(not server.attach))
                                # pop_server.dele(num)
                            except Exception:
                                _logger.info('Failed to process mail from %s server %s.', server.type, server.name,
                                             exc_info=True)
                                failed += 1
                            if res_id and server.action_id:
                                server.action_id.with_context({
                                    'active_id': res_id,
                                    'active_ids': [res_id],
                                    'active_model': self.env.context.get("thread_model", server.object_id.model)
                                }).run()
                            self.env.cr.commit()
                        if num_messages < MAX_POP_MESSAGES:
                            break
                        pop_server.quit()
                        _logger.info("Fetched %d email(s) on %s server %s; %d succeeded, %d failed.", num_messages,
                                     server.type, server.name, (num_messages - failed), failed)
                except Exception:
                    _logger.info("General failure when trying to fetch mail from %s server %s.", server.type,
                                 server.name, exc_info=True)
                finally:
                    if pop_server:
                        pop_server.quit()
            server.write({'date': fields.Datetime.now()})
        return True


class EqIrMailServer(models.Model):
    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="Owner")


class EqMailMail(models.Model):
    _inherit = 'mail.mail'

    mail_server_id = fields.Many2one('ir.mail_server', "Default Mail Server")
    mail_server_address = fields.Char('Default Mail Server Address')


class EqResUserExtension(models.Model):
    _inherit = 'res.users'

    @api.multi
    def open_change_email(self):
        mod_obj = self.env['ir.model.data']
        res = mod_obj.get_object_reference('eq_mail_extension', 'eq_mail_password_change_form')
        return {
                'name': 'Neue Version',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [res and res[1] or False],
                'res_model': 'eq_mail.password_change',                
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'context': "{}",
                'res_id': False,
            }


class EqMailPasswordChange(models.TransientModel):
    _name = "eq_mail.password_change"
    
    eq_old_password = fields.Char('Old password', size=64)
    eq_password = fields.Char('New password', size=64)
    eq_compare_password = fields.Char('Repeat new password', size=64)

    @api.multi
    def button_confirm(self):
        # ir.mail_server Object and Dataset id for the user.
        ir_mail_server_obj = self.env['ir.mail_server']
        ir_mail_server_id = ir_mail_server_obj.search([('user_id', '=', self._uid)])
        # fetchmail.server Object and Dataset id for the user.
        fetchmail_server_obj = self.env['fetchmail.server']
        fetchmail_server_id = fetchmail_server_obj.search([('user_id', '=', self._uid)])
        # eq_mail.password_change Dataset
        password = self.browse(self.ids)
        # ir.mail_server Dataset
        ir_mail_server = ir_mail_server_id
        if len(ir_mail_server_id) == 0 and len(fetchmail_server_id) == 0:
            raise exceptions.UserError(_('There is no incoming and outgoing mailserver for this user.Please contact '
                                         'an administrator.'))
        elif len(ir_mail_server_id) == 0:
            raise exceptions.UserError(_('There is no outgoing mailserver for this user.'
                                         'Please contact an administrator.'))
        else:
            if password.eq_old_password != ir_mail_server.smtp_pass:
                raise exceptions.UserError(_('The old password does not match.'))
            else:
                if password.eq_password != password.eq_compare_password:
                    raise exceptions.UserError(_('The two new passwords do not match.'))
                else:
                    # Set password for ir_mail_server
                    ir_mail_server_values = {
                              'smtp_pass': password.eq_password
                              }
                    ir_mail_server.write(ir_mail_server_values)
                    if len(fetchmail_server_id) != 0:
                        # Set password for fetchmail_server
                        fetchmail_server_values = {
                                  'password': password.eq_password,
                                  }
                        fetchmail_server_id.write(fetchmail_server_values)
                    return True
