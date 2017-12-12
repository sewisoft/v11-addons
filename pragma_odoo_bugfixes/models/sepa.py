# -*- coding: utf-8 -*-

from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def process_reconciliation(self, counterpart_aml_dicts=None, payment_aml_rec=None, new_aml_dicts=None):
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ "
        orig = self.name
        clean = ''.join(c for c in orig if c in valid_chars)
        self.name = clean[:140]
        super(AccountBankStatementLine, self).process_reconciliation(counterpart_aml_dicts=counterpart_aml_dicts,
                                                                     payment_aml_rec=payment_aml_rec,
                                                                     new_aml_dicts=new_aml_dicts)

    @api.multi
    def process_reconciliations(self, data):
        valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/-?:().,'+ "
        if type(data) == list:
            for elem in data:
                if type(elem) == dict and 'new_aml_dicts' in elem:
                    for entry in elem['new_aml_dicts']:
                        if 'name' in entry and entry['name']:
                            clean = ''.join(c for c in entry['name'] if c in valid_chars)
                            entry['name'] = clean[:140]
        super(AccountBankStatementLine, self).process_reconciliations(data)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.one
    @api.constrains('payment_method_id', 'communication')
    def _check_communication_sepa(self):
        if self.payment_method_id == self.env.ref('account_sepa.account_payment_method_sepa_ct'):
            if len(self.communication) > 140:
                self.communication = self.communication[:140]
        super(AccountPayment, self)._check_communication_sepa()
