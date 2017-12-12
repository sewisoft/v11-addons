# -*- coding: utf-8 -*-

from odoo import models
import logging

_logger = logging.getLogger(__name__)


class EqInstallFunc(models.Model):
    """ Hilfsklasse mit Funktionen, die wir bei der Installation des Modules ausführen wollen..z.B.
    Defalt Email-Vorlagen löschen"""
    _name = "eq_install_func"

    def _eq_delete_default_templates(self):
        """
        Wir löschen hier Default E-Mail Vorlage für die Bestellbestätigung, die wir durch unsere Version ersetzen
        """
        _logger.info("** Deleting default email templates **")
        email_templates = self.env['mail.template'].sudo().search([('name', '=', 'Sales Order - Send by Email')])
        for record in email_templates:
            record.unlink()
