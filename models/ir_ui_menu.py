import logging
from odoo import fields, models,api
MENU_ITEM_SEPARATOR = "/"

_logger = logging.getLogger(__name__)

class IR_UI_MENU(models.Model):
    _inherit = 'ir.ui.menu'
    _allow_sudo_commands = True

    parent_id = fields.Many2one('ir.ui.menu', string='Parent Menu', index=True, ondelete="restrict")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for menu in self:
            menu.complete_name = menu._get_full_name()

    def _get_full_name(self, level=6):
        """ Return the full name of ``self`` (up to a certain level). """
        if level <= 0:
            return '...'
        if self.parent_id:
            return self.parent_id._get_full_name(level - 1) + MENU_ITEM_SEPARATOR + (self.name or "")
        else:
            return self.name