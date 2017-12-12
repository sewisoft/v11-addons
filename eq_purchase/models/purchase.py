# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as OE_DFORMAT


class EqPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    eq_head_text = fields.Html('Head Text')
    notes = fields.Html('Terms and conditions')
    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user)
    # Report
    show_planned_date = fields.Boolean(string='Show Planned Date')
    use_calendar_week = fields.Boolean('Use Calendar Week for Planned Date [eq_purchase]')
    eq_use_page_break_after_header = fields.Boolean(string='Page break after header text')
    eq_use_page_break_before_footer = fields.Boolean(string='Page break before footer text')

    @api.multi
    def action_rfq_send(self):
        """
        This function opens a window to compose an email, with the edi purchase template message loaded by default
        """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            if self.env.context.get('send_rfq', False):
                template_id = ir_model_data.get_object_reference('eq_purchase', 'email_template_edi_purchase_new')[1]
            else:
                template_id = ir_model_data.get_object_reference('eq_purchase', 'email_template_edi_purchase_done_new')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'purchase.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    @api.depends('order_line.date_planned')
    def _compute_date_planned(self):
        for order in self:
            min_date = False
            for line in order.order_line:
                if not min_date or line.date_planned < min_date:
                    min_date = line.date_planned
            if min_date:
                order.date_planned = min_date
            else:
                order.date_planned = order.date_order

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """
        Override für Wechsel der Partner_ID: Übernahme der custom-Felder
        :return:
        """
        super(EqPurchaseOrder, self).onchange_partner_id()
        partner = self.partner_id
        if partner:
            self.partner_ref = partner.eq_foreign_ref_purchase


class EqPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def _get_planned_date(self):
        """
        Hilfsfunktion für Report für Ermittlung des Lieferdatums
        Aktuell wird Feld show_delivery_date der purchase_order nicht gesetzt -> Rückgabe immer false
        :return:
        """
        result = {}
        for purchase_line in self:
            if purchase_line.order_id.show_planned_date and purchase_line.date_planned:
                planned_date = datetime.strptime(purchase_line.date_planned, OE_DFORMAT)
                if purchase_line.order_id.partner_id.eq_planned_date_type_purchase:
                    if purchase_line.order_id.partner_id.eq_planned_date_type_purchase == 'cw':
                        result[purchase_line.id] = 'KW ' + planned_date.strftime('%V/%Y')
                    elif purchase_line.order_id.partner_id.eq_planned_date_type_purchase == 'date':
                        result[purchase_line.id] = planned_date.strftime('%d.%m.%Y')
                else:
                    if purchase_line.order_id.use_calendar_week:
                        result[purchase_line.id] = 'KW ' + planned_date.strftime('%V/%Y')
                    else:
                        result[purchase_line.id] = planned_date.strftime('%d.%m.%Y')
            else:
                result[purchase_line.id] = False
        return result

    get_planned_date = fields.Char(compute="_get_planned_date", string="Planned Date", methode=True, store=False)

    # existierende Felder überschrieben für andere Angabe der Dezimalstellen
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Purchase Unit of Measure [eq_purchase]'),
                               required=True)
    price_unit = fields.Float(string='Unit Price', required=True,
                              digits=dp.get_precision('Purchase Product Price [eq_purchase]'))


class EqPurchaseConfigurationAddress(models.TransientModel):
    _inherit = 'res.config.settings'

    def set_values(self):
        super(EqPurchaseConfigurationAddress, self).set_values()
        ir_default = self.env['ir.default']
        ir_default.set('purchase.order', 'show_planned_date', self.default_show_planned_date)
        ir_default.set('purchase.order', 'use_calendar_week', self.default_use_calendar_week)

    def get_values(self):
        res = super(EqPurchaseConfigurationAddress, self).get_values()
        ir_default = self.env['ir.default']
        show_planned_date = ir_default.get('purchase.order', 'show_planned_date')
        use_calendar_week = ir_default.get('purchase.order', 'use_calendar_week')
        res.update(
            default_show_planned_date=show_planned_date,
            default_use_calendar_week=use_calendar_week,
        )
        return res

    default_show_planned_date = fields.Boolean(string='Show the Planned Date on the Purchase Order [eq_purchase]',
                                               help='The planned date will be shown in the Purchase Order',
                                               default_model='purchase.order')
    default_use_calendar_week = fields.Boolean('Show Calendar Week for Planned Date [eq_purchase]',
                                               help='The planned date will be shown as a calendar week',
                                               default_model='purchase.order')
