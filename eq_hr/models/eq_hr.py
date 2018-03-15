# -*- coding: utf-8 -*-

from odoo import models, api


class EqHrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def create(self, values):
        context_new = {}
        if self._context:
            context_new = dict(self._context)
        context_new['do_not_repeat'] = True

        res = super(EqHrEmployee, self).create(values)
        if 'user_id' in values and 'do_not_repeat' not in self._context:
            if values['user_id']:
                user_obj = self.env['res.users']
                cur_user = user_obj.browse(values['user_id'])
                emp_ids_to_del = self.search([('user_id', '=', values['user_id']), ('id', '!=', res.id)])
                if len(emp_ids_to_del) != 0:
                    emp_ids_to_del.write({'user_id': False})
                if cur_user:
                    cur_user.with_context(context_new).write({'eq_employee_id': res.id})
        return res

    @api.one
    def write(self, values):
        context_new = {}
        if self._context:
            context_new = dict(self._context)
        context_new['do_not_repeat'] = True
        if 'user_id' in values and 'do_not_repeat' not in self._context:
            user_obj = self.env['res.users']
            if values['user_id']:
                if values['user_id'] != self.user_id.id:
                    # Removes the employee from all users, except the current one.
                    emp_ids_to_del = self.search([('user_id', '=', values['user_id'])])
                    if len(emp_ids_to_del) != 0:
                        for emp_id in emp_ids_to_del:
                            if emp_id.id != self.id:
                                emp_id.write({'user_id': False})
                    user_ids_to_clear = user_obj.search([('eq_employee_id', '=', self.id)])
                    if len(user_ids_to_clear) != 0:
                        user_ids_to_clear.with_context(context_new).write({'eq_employee_id': False})

                    # Sets the employee_id for the user.
                    user_to_update = user_obj.browse(values['user_id'])
                    if user_to_update:
                        user_to_update.with_context(context_new).write({'eq_employee_id': self.id})
            else:
                # Removes the employee from all the users.
                user_ids_to_clear = user_obj.search([('eq_employee_id', '=', self.id)])
                if user_ids_to_clear:
                    user_ids_to_clear.with_context(context_new).write({'eq_employee_id': False})

        res = super(EqHrEmployee, self).write(values)
        return res