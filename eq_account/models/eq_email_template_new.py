# -*- coding: utf-8 -*-

import logging
from odoo import models

_logger = logging.getLogger(__name__)


class EqInstallFunc(models.Model):
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
        delete_default_template = self.env['mail.template'].sudo().search([('name', '=', 'Invoicing: Invoice email')])
        delete_template_3 = self.env['mail.template'].sudo().search(
            [('eq_email_template_version', '=', 0), ('name', '=', 'Rechnung')])
        for delf_default_record in delete_default_template:
            delf_default_record.unlink()
        for del_3_record in delete_template_3:
            del_3_record.unlink()
