from odoo import fields, models, api
import logging
import uuid
_logger = logging.getLogger(__name__)


class SettingNspDeviceIn(models.Model):
    _name = 'setting.nsp.device'
    _description = 'Setting Parking Device'
    id_device = fields.Char(string="ID thiết bị")
    name = fields.Selection([('reader', 'Đầu đọc thẻ'),
                             ('screenSecurity', "Màn hình bảo vệ"),
                             ('screenIn', "Màn hình vào"),  
                             ('screenOut', "Màn hình ra"),
                            ('screenAlert', "Màn hình cảnh báo")], string="Loại thiết bị")
  
    lane_id = fields.Many2one(
        "setting.nsp.lane", string="Cổng",  ondelete='cascade')

    @api.model
    def create(self, vals):
        new_record = super(SettingNspDeviceIn, self).create(vals)
        new_record.write({"id_device": str(uuid.uuid4())[
                         :15] + ',' + str(new_record.id)})
        return new_record
