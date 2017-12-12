# -*- coding: utf-8 -*-

from odoo import http


class CookieNotice(http.Controller):
    @http.route("/eq_website_cookie_notice/ok", auth="public", website=True, type='json', methods=['POST'])
    def accept_cookies(self):
        """Stop spamming with cookie banner."""
        http.request.session["accepted_cookies"] = True
        http.request.env['ir.ui.view'].search([
            ('type', '=', 'qweb')
            ]).clear_caches()
        return {'result': 'ok'}
