from odoo import api, fields, models, _
import uuid
import json
import logging
_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'
    # is_admin_or_manager = fields.Boolean(
    #     compute='_compute_is_admin_or_manager',
    #     store=True
    # )

    @api.model
    def create(self, vals):
        _logger.info(vals)
        vals['email'] = vals['login']
        vals['isUserCreateCheck'] = True
        users = super(ResUsers, self).create(vals)
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