# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class GeneratorSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_auto_create = fields.Boolean(_('Autogenerate'), help=_('Autogenerate accounts for Persons'),
                                         default_model='res.partner')
    default_auto_customer_ref = fields.Boolean(_('Autogenerate Customer Reference'),
                                               help=_('Autogenerate customer numbers'), default_model='res.partner')
    auto_customer_ref_by_account = fields.Boolean(_('Create Customer Reference from Debitor Account'),
                                                  help=_('Create Customer Reference from Debitor Account'),
                                                  default_model='res.partner')
    default_auto_supplier_ref = fields.Boolean(_('Autogenerate Supplier Reference'),
                                               help=_('Autogenerate supplier numbers'), default_model='res.partner')
    auto_supplier_ref_by_account = fields.Boolean(_('Create Supplier Reference from Creditor Account'),
                                                  help=_('Create Supplier Reference from Creditor Account'),
                                                  default_model='res.partner')
    receivable_parent_id = fields.Many2one('account.account', _('Parent'), help=_('Parent account'))
    payable_parent_id = fields.Many2one('account.account', _('Parent'), help=_('Parent account'))

    @api.model
    def set_values(self):
        super(GeneratorSettings, self).set_values()
        ir_default = self.env['ir.default'].sudo()
        ir_default.set('res.partner', 'receivable_parent_id', self.receivable_parent_id and
                       self.receivable_parent_id.id or False)
        ir_default.set('res.partner', 'payable_parent_id', self.payable_parent_id and
                       self.payable_parent_id.id or False)
        ir_default.set('res.partner', 'default_auto_customer_ref', self.default_auto_customer_ref or False)
        ir_default.set('res.partner', 'default_auto_supplier_ref', self.default_auto_supplier_ref or False)
        ir_default.set('res.partner', 'auto_customer_ref_by_account', self.auto_customer_ref_by_account or False)
        ir_default.set('res.partner', 'auto_supplier_ref_by_account', self.auto_supplier_ref_by_account or False)

    @api.model
    def get_values(self):
        res = super(GeneratorSettings, self).get_values()
        ir_default = self.env['ir.default'].sudo()
        receivable = ir_default.get('res.partner', 'receivable_parent_id')
        payable = ir_default.get('res.partner', 'payable_parent_id')
        default_customer_ref = ir_default.get('res.partner', 'default_auto_customer_ref')
        default_supplier_ref = ir_default.get('res.partner', 'default_auto_supplier_ref')
        customer_ref_by_account = ir_default.get('res.partner', 'auto_customer_ref_by_account')
        supplier_ref_by_account = ir_default.get('res.partner', 'auto_supplier_ref_by_account')
        res.update(
            receivable_parent_id=receivable,
            payable_parent_id=payable,
            default_auto_customer_ref=default_customer_ref,
            default_auto_supplier_ref=default_supplier_ref,
            auto_customer_ref_by_account=customer_ref_by_account,
            auto_supplier_ref_by_account=supplier_ref_by_account,
        )
        return res
