# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging


import odoo
import odoo.modules.registry
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.service import security
from odoo.tools import ustr
from odoo.tools.translate import _

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi
from werkzeug.urls import iri_to_uri

from odoo.addons.web.controllers import (
    action, binary, database, dataset, export, home, report, session,
    utils, view, webclient,
)
# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang', 'signup_email'}
LOGIN_SUCCESSFUL_PARAMS = set()
_logger = logging.getLogger(__name__)


class WebLogin(http.Controller):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        utils.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # simulate hybrid auth=user/auth=public, despite using auth=none to be able
        # to redirect users when no db is selected - cfr ensure_db()
        if request.env.uid is None:
            if request.session.uid is None:
                # no user -> auth=public with specific website public user
                request.env["ir.http"]._auth_method_public()
            else:
                # auth=user
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items()
                  if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                uid = request.session.authenticate(
                    request.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _(
                    'Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    def user_internal(self, uid):
        user = request.env['res.users'].browse(uid)
        result = request.env['ir.ui.menu'].sudo().search(
            [("name", "=", "NSP")])
        menuId = False
        for menu in result.child_id:
            if menu.name == "Contact" and menu.parent_id.id == result.id:
                menuId = menu.id
                break
        return [user._is_internal(), user.partner_id.id, menuId]

    def _login_redirect(self, uid, redirect=None):
        _logger.info("aaaa")
        if request.session.uid:  # fully logged
            result = self.user_internal(request.session.uid)
            return redirect or ('/web#id='+str(result[1])+'&model=res.partner&view_type=form&menu_id='+str(result[2]) if result[0]
                                else '/web/login_successful')
        # partial session (MFA)
        url = request.env(user=uid)['res.users'].browse(uid)._mfa_url()
        if not redirect:
            return url

        parsed = werkzeug.urls.url_parse(url)
        qs = parsed.decode_query()
        qs['redirect'] = redirect
        return parsed.replace(query=werkzeug.urls.url_encode(qs)).to_url()
