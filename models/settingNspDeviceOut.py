from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SettingNspDeviceOut(models.Model):
    _name = 'setting.nsp.device.out'
    _description = 'Setting Parking Device'
    name = fields.Selection([('reader', 'Đầu đọc ra'),
                             ('screenSecurity', "Màn hình bảo vệ"),
                            ('screen', "Màn hình ra"),
                             ('screenAlert', "Màn hình cảnh báo")], string="Tên kết nối")
    webhook_url = fields.Char(string="Webhook URL")
    webhook_name = fields.Char(string="Webhook Name")
    lane_id = fields.Many2one(
        "setting.nsp.lane.out", string="Cổng Ra",  ondelete='cascade')
