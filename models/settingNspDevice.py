from odoo import fields, models, api
import logging
import uuid
_logger = logging.getLogger(__name__)


class SettingNspDeviceIn(models.Model):
    _name = 'setting.nsp.device'
    _description = 'Setting Parking Device'
    id_device = fields.Char(string="ID thiết bị")
    name = fields.Selection([('SYC_R16', 'Đầu đọc SYC_R16'),
                             ('ZTX_G20', 'Đầu đọc ZTX_G20'),
                            ('CF_RU6403', 'Đầu đọc CF_RU6403'),
                             ('screenSecurity', "Màn hình bảo vệ"),
                             ('screenIn', "Màn hình vào"),  
                             ('screenOut', "Màn hình ra"),
                            ('screenAlert', "Màn hình cảnh báo")], string="Loại thiết bị")
    antIn1 = fields.Boolean(string="ATN1", default=False)
    antIn2 = fields.Boolean(string="ATN2", default=False)
    antIn3 = fields.Boolean(string="ATN3", default=False)
    antIn4 = fields.Boolean(string="ATN4", default=False)

    antOut1 = fields.Boolean(string="ATN1", default=False)
    antOut2 = fields.Boolean(string="ATN2", default=False)
    antOut3 = fields.Boolean(string="ATN3", default=False)
    antOut4 = fields.Boolean(string="ATN4", default=False)
    lane_id = fields.Many2one(
        "setting.nsp.lane", string="Cổng",  ondelete='cascade')

    @api.model
    def create(self, vals):
        new_record = super(SettingNspDeviceIn, self).create(vals)
        new_record.write({"id_device": str(uuid.uuid4())[
                         :15] + ',' + str(new_record.id)})
        return new_record
