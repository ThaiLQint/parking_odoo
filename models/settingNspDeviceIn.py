from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SettingNspDeviceIn(models.Model):
    _name = 'setting.nsp.device.in'
    _description = 'Setting Parking Device'
    name = fields.Selection([('reader', 'Đầu đọc vào'),
                             ('screenSecurity', "Màn hình bảo vệ"),
                             ('screen', "Màn hình vào"),
                            ('screenAlert', "Màn hình cảnh báo")], string="Loại thiết bị")
    webhook_url = fields.Char(string="Webhook URL")
    webhook_name = fields.Char(string="Webhook Name")
    lane_id = fields.Many2one(
        "setting.nsp.lane.in", string="Cổng vào",  ondelete='cascade')
