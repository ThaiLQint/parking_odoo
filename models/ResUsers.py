from odoo import api, fields, models, http
import uuid
import json
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'
    @api.model
    def create(self, vals):
        users = super(ResUsers, self).create(vals)
        _logger.info(vals)
        return users
