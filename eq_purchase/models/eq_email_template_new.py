# -*- coding: utf-8 -*-

import logging
from odoo import models

_logger = logging.getLogger(__name__)


class EqInstallFunction(models.Model):
    """
        Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B.
        Defalt Email-Vorlagen löschen
    """
    _name = "eq_install_func"

    def _eq_delete_default_templates(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Bestellbestätigung, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),
                                                                   ('name', '=', ' Purchase Order - Send by Email')])
        for record in email_templates:
            record.unlink()
        email_templates = self.env['mail.template'].sudo().search([('eq_email_template_version', '=', False),
                                                                   ('name', '=', 'RFQ - Send by Email')])
        for record in email_templates:
            record.unlink()
        po_email_templates = self.env['mail.template'].sudo().search([('name', '=', 'Purchase Order - Send by Email')])
        for po_record in po_email_templates:
            po_record.unlink()
        rfq_email_templates = self.env['mail.template'].sudo().search([('name', '=', 'RFQ - Send by Email')])
        for rfq_record in rfq_email_templates:
            rfq_record.unlink()
