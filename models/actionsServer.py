import logging
from odoo import api, fields, models, http
import uuid
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ActionsServer(models.Model):
    _inherit = 'ir.actions.server'
    def create(self, vals):
        """ Create a contextual action for each server action. """
        new_record = super(ActionsServer, self).create(vals)
        return new_record