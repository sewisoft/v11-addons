# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EqHrResUsers(models.Model):
    _inherit = 'res.users'

    eq_employee_id = fields.Many2one('hr.employee', 'Employee', copy=False)

    @api.model
    def create(self, values):
        context_new = {}
        if self._context:
            context_new = dict(self._context)
        res = super(EqHrResUsers, self).create(values)
        if 'eq_employee_id' in values and 'do_not_repeat' not in self._context:
            if values['eq_employee_id']:
                emp_obj = self.env['hr.employee']
                # Removes the user from all employees, except the selected one.
                user_ids_to_del = self.search([('eq_employee_id', '=', values['eq_employee_id'])])  # SUPERUSER_ID
                if len(user_ids_to_del) != 0:
                    for user_id in user_ids_to_del:
                        if user_id.id != res.id:
                            user_id.write({'eq_employee_id': False})  # SUPERUSER_ID
                # Sets the user_id in the employee. do_not_repeat in context so that the employee
                # does not set the employee_id for the user.
                emp_to_update = emp_obj.browse(values['eq_employee_id'])
                if emp_to_update:
                    context_new['do_not_repeat'] = True
                    emp_to_update.with_context(context_new).write({'user_id': res.id})
        return res

    @api.one
    def write(self, values):
        context_new = {}
        if self._context:
            context_new = dict(self._context)
        context_new['do_not_repeat'] = True

        if 'eq_employee_id' in values and 'do_not_repeat' not in self._context:
            emp_obj = self.env['hr.employee']
            if values['eq_employee_id']:
                if values['eq_employee_id'] != self.eq_employee_id.id:
                    # Removes the user from all employees, except the selected one
                    user_ids_to_del = self.search([('eq_employee_id', '=', values['eq_employee_id'])])
                    if len(user_ids_to_del) != 0:
                        for user_id in user_ids_to_del:
                            if user_id.id != self.id:
                                user_id.write({'eq_employee_id': False})

                    # Benutzerfeld für Mitarbeiter leeren, für die bisher der aktuelle Benutzer gesetzt war
                    employees_to_clear = emp_obj.search([('user_id', '=', self.id)])
                    if len(employees_to_clear) != 0:
                        employees_to_clear.with_context(context_new).write({'user_id': False})

                    # Sets the user_id in the employee
                    emp_to_update = emp_obj.browse(values['eq_employee_id'])
                    emp_to_update.with_context(context_new).write({'user_id': self.id})
            else:
                # Removes the user from all employees
                employees_to_clear = emp_obj.search([('user_id', '=', self.id)])
                if employees_to_clear:
                    employees_to_clear.with_context(context_new).write({'user_id': False})
        return super(EqHrResUsers, self).write(values)
