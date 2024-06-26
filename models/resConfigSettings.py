from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class ParkingResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Alert Tag'

    navbar_background_color = fields.Char(string = "Navigationbar Background Color")
    navbar_text_color = fields.Char(string = "Navigationbar Text Color")

    @api.model
    def get_values(self):
        res = super(ParkingResConfigSettings,self).get_values()
        IPC = self.env['ir.config_parameter'].sudo()
        
        navbar_background_color = IPC.get_param('change_odoo_theme_header_color.navbar_background_color')
        navbar_text_color = IPC.get_param('change_odoo_theme_header_color.navbar_text_color')
        res.update(
            navbar_background_color = navbar_background_color,
            navbar_text_color = navbar_text_color,
        )
        return res
    
    def set_values(self):
        super(ParkingResConfigSettings, self).set_values()
        IPC = self.env['ir.config_parameter'].sudo()
        IPC.set_param('change_odoo_theme_header_color.navbar_background_color', self.navbar_background_color)
        IPC.set_param('change_odoo_theme_header_color.navbar_text_color', self.navbar_text_color)
