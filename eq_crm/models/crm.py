# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools


class EqCrmLead(models.Model):
    _inherit = 'crm.lead'

    firstname = fields.Char('Firstname')
    lastname = fields.Char('Lastname')
    category_ids = fields.Many2many('res.partner.category', string='Tags')
    birthdate = fields.Date('Birthday')
    eq_citypart = fields.Char('District')
    eq_house_no = fields.Char('House Number')

    @api.multi
    def _create_lead_partner_data(self, firstname, name, is_company, parent_id=False):
        """ extract data from lead to create a partner
            :param name : furtur name of the partner
            :param is_company : True if the partner is a company
            :param parent_id : id of the parent partner (False if no parent)
            :returns res.partner record
        """
        email_split = tools.email_split(self.email_from)
        if is_company:
            values = {
                'name': name,
                'user_id': self.env.context.get('default_user_id') or self.user_id.id,
                'comment': self.description,
                'team_id': self.team_id.id,
                'parent_id': parent_id,
                'phone': self.phone,
                'mobile': self.mobile,
                'email': email_split[0] if email_split else False,
                'street': self.street,
                'street2': self.street2,
                'zip': self.zip,
                'city': self.city,
                'country_id': self.country_id.id,
                'state_id': self.state_id.id,
                'is_company': is_company,
                'eq_house_no': self.eq_house_no,
                'type': 'contact',
                'website': self.website
            }

        else:
            values = {
                'name': name,
                'user_id': self.env.context.get('default_user_id') or self.user_id.id,
                'comment': self.description,
                'team_id': self.team_id.id,
                'parent_id': parent_id,
                'phone': self.phone,
                'mobile': self.mobile,
                'email': email_split[0] if email_split else False,
                'title': self.title.id,
                'function': self.function,
                'street': self.street,
                'street2': self.street2,
                'zip': self.zip,
                'city': self.city,
                'country_id': self.country_id.id,
                'state_id': self.state_id.id,
                'is_company': is_company,
                'eq_firstname': firstname,
                'eq_house_no': self.eq_house_no,
                'eq_birthday': self.birthdate,
                'eq_citypart': self.eq_citypart,
                'type': 'contact'
            }
        return self.env['res.partner'].create(values)

    @api.multi
    def _create_lead_partner(self):
        """ Create a partner from lead data
            :returns res.partner record
        """
        firstname = self.firstname
        lastname = self.lastname
        if not firstname or firstname is None:
            firstname = ''
        if not lastname or lastname is None:
            lastname = ''
        self.contact_name = firstname + ' ' + lastname
        contact_name = self.contact_name
        if not contact_name:
            contact_name = self.env['res.partner']._parse_partner_name(self.email_from)[0] if self.email_from else False
        if self.partner_name:
            first_name = ''
            partner_company = self._create_lead_partner_data(first_name, self.partner_name, True)
        elif self.partner_id:
            partner_company = self.partner_id
        else:
            partner_company = None
        if contact_name:
            return self._create_lead_partner_data(firstname, lastname, False, partner_company.id if partner_company else False)
        if partner_company:
            return partner_company
        return self._create_lead_partner_data(self.name, False)
