from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class ParkingResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Alert Tag'

    navbar_background_color = fields.Char(
        string="Navigationbar Background Color")
    navbar_text_color = fields.Char(string="Navigationbar Text Color")
    navbar_text_color = fields.Char(string="Navigationbar Text Color")
    dropdown_item_color = fields.Char(string="Dropdown Items Color")
    button_color = fields.Char(string="Button Primary Color")
    website_title = fields.Char(string="Website Title")
    website_logo = fields.Image(string="Website Logo 1080", max_width=1080, max_height=1080)
    website_logo_main = fields.Image("Website Logo ", related="website_logo", max_width=40, max_height=40, store=True)
    app_logo = fields.Image(string="App Logo 1080", max_width=1080, max_height=1080)
    app_logo_main = fields.Image("App Logo ", related="app_logo", max_width=40, max_height=40, store=True)

    @api.model
    def get_values(self):
        res = super(ParkingResConfigSettings, self).get_values()
        IPC = self.env['ir.config_parameter'].sudo()

        navbar_background_color = IPC.get_param(
            'change_odoo_theme_header_color.navbar_background_color')
        navbar_text_color = IPC.get_param(
            'change_odoo_theme_header_color.navbar_text_color')
        dropdown_item_color = IPC.get_param(
            'change_odoo_theme_header_color.dropdown_item_color')
        button_color = IPC.get_param(
            'change_odoo_theme_header_color.button_color')
        website_title = IPC.get_param(
            'change_odoo_theme_header_color.website_title')
        website_logo = IPC.get_param(
            'change_odoo_theme_header_color.website_logo')
        app_logo = IPC.get_param(
            'change_odoo_theme_header_color.app_logo')
        app_logo_main = IPC.get_param(
            'change_odoo_theme_header_color.app_logo_main')
        website_logo_main = IPC.get_param(
            'change_odoo_theme_header_color.website_logo_main')
        res.update(
            navbar_background_color=navbar_background_color,
            navbar_text_color=navbar_text_color,
            dropdown_item_color=dropdown_item_color,
            button_color=button_color,
            website_title=website_title,
            website_logo=website_logo,
            app_logo=app_logo,
            app_logo_main=website_logo_main,
            website_logo_main=app_logo_main
        )
        return res

    def set_values(self):
        super(ParkingResConfigSettings, self).set_values()
        IPC = self.env['ir.config_parameter'].sudo()
        IPC.set_param('change_odoo_theme_header_color.navbar_background_color',
                      self.navbar_background_color)
        IPC.set_param(
            'change_odoo_theme_header_color.navbar_text_color', self.navbar_text_color)
        IPC.set_param(
            'change_odoo_theme_header_color.dropdown_item_color', self.dropdown_item_color)
        IPC.set_param(
            'change_odoo_theme_header_color.button_color', self.button_color)
        IPC.set_param(
            'change_odoo_theme_header_color.website_title', self.website_title)
        IPC.set_param(
            'change_odoo_theme_header_color.website_logo', self.website_logo)
        IPC.set_param(
            'change_odoo_theme_header_color.app_logo', self.app_logo)
        IPC.set_param(
            'change_odoo_theme_header_color.app_logo_main', self.app_logo_main)
        IPC.set_param(
            'change_odoo_theme_header_color.website_logo_main', self.website_logo_main)
        
