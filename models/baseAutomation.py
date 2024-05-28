import logging
from odoo import api, fields, models, http
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class BaseAutomation(models.Model):
    _inherit = 'base.automation'
    def write(self, vals):
        """ Create a contextual action for each server action. """
        result = super(BaseAutomation, self).write(vals)
        return result