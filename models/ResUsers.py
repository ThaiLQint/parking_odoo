from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.http import request, DEFAULT_LANG
import uuid
import json
import logging
import pytz
from odoo.exceptions import AccessDenied, UserError
from odoo.addons.auth_signup.models.res_users import SignupError
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'
    # is_admin_or_manager = fields.Boolean(
    #     compute='_compute_is_admin_or_manager',
    #     store=True
    # )
    @classmethod
    def _login(cls, db, login, password, user_agent_env):
        if not password:
            raise AccessDenied()
        ip = request.httprequest.environ['REMOTE_ADDR'] if request else 'n/a'
        try:
            with cls.pool.cursor() as cr:
                self = api.Environment(cr, SUPERUSER_ID, {})[cls._name]
                with self._assert_can_auth(user=login):
                    user = self.search(self._get_login_domain(login), order=self._get_login_order(), limit=1)
                    if not user:
                        raise AccessDenied()
                    user = user.with_user(user)
                    user._check_credentials(password, user_agent_env)
                    tz = request.httprequest.cookies.get('tz') if request else None
                    if tz in pytz.all_timezones and (not user.tz or not user.login_date):
                        # first login or missing tz -> set tz to browser tz
                        user.tz = tz
                    user._update_last_login()
        except AccessDenied:
            _logger.info("Login failed for db:%s login:%s from %s", db, login, ip)
            raise

        _logger.info("Login successful for db:%s login:%s from %s", db, login, ip)
        _logger.info("ĐÂY LÀ LOGIN METHOD")
        return user.id

    @api.model
    def create(self, vals):
        vals['email'] = vals['login']
        vals['isUserCreateCheck'] = True
        id_roles = self.env["res.groups"].search([
        '|',
            '|',
                ('full_name', '=', "Technical / Mail Template Editor"),
                ('full_name', '=', 'Extra Rights / Contact Creation'),
            '|',
                ('full_name', '=', 'Technical / Access to export feature'),
                ('full_name', '=', 'Extra Rights / Technical Features'),
        ], limit=6)
        data_write = {"company_ids": [(4,1)],
            "company_id": 1,
            "sel_groups_1_10_11": 1,
            "active":True}
        for role in id_roles:
            data_write['in_group_' + str(role.id)] = True
                
        _logger.info(data_write)
        users = super(ResUsers, self).create(vals)
        users.write(data_write)
        return users
    def write(self, vals):
        # Code before write: 'self' has the old values
        _logger.info(vals)
        record = super(ResUsers, self).write(vals)
        # Code after write: can use 'self' with the updated
        # values
        return record
    
    def _action_show2(self):
        _logger.info(self)
        users = self.env['res.users'].sudo().search([])
        view_id = self.env.ref('base.view_users_form').id
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'context': {'create': False},
        }
        if len(users) > 1:
            action.update({
                'name': _('Users'),
                'view_mode': 'list,form',
                'views': [[False, 'kanban'], [False, 'list'], [view_id, 'form']],
                'domain': [('id', 'in', users.ids)],
                'context': {'create': True},
            })
        else:
            action.update({
                'view_mode': 'form',
                'views': [[view_id, 'form']],
                'res_id': users.id,
                'context': {'create': True},
            })
        return action