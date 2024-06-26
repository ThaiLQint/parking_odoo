from odoo import fields, models, api
import logging
import uuid
from datetime import datetime
_logger = logging.getLogger(__name__)

configurationCode = "0001"


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

    def generate_truncated_uuid_4bytes(self):
        # Generate a full UUID
        full_uuid = uuid.uuid4()

        # Convert the full UUID to an integer
        full_uuid_int = int(full_uuid.hex, 16)

        # Truncate the integer to the first 4 bytes (32 bits)
        truncated_uuid_int = full_uuid_int & 0xFFFFFFFF

        return truncated_uuid_int

    @api.model
    def create(self, vals):
        now = datetime.now()
        # Format the date and time as a string
        formatted_now = now.strftime("%d%m%Y")
        id_device = "0000"
        if vals['name'] == 'screenSecurity':
            id_device = "0001"
        elif vals['name'] == 'screenIn':
            id_device = "0002"
        elif vals['name'] == 'screenOut':
            id_device = "0003"
        elif vals['name'] == 'screenAlert':
            id_device = "0004"
        uidBCD = str(self.generate_truncated_uuid_4bytes())
        vals['id_device'] = formatted_now + '-' + \
            id_device + '-' + configurationCode+'-' + uidBCD
        new_record = super(SettingNspDeviceIn, self).create(vals)
        return new_record
