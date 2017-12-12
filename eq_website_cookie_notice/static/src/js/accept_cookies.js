odoo.define('eq_website_cookie_notice.cookie_notice', function (require) {
"use strict";

var ajax = require('web.ajax');
var base = require('web_editor.base');

    base.ready().done(function() {
        $(".cc-cookies .btn-primary").click(function(e) {
            e.preventDefault();
            ajax.jsonRpc('/eq_website_cookie_notice/ok', 'call').then(function (data) {
                if (data.result == 'ok') {
                    $("#eq_website_cookie_notice").detach();
                }
            });
        });
    });

});
