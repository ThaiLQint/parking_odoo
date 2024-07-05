from odoo import fields, models, api
import logging
import uuid
from datetime import datetime
_logger = logging.getLogger(__name__)

configurationCode = "0001"


class SettingNspDevice(models.Model):
    _name = 'setting.nsp.device'
    _description = 'Setting Parking Device'
    isConnected = fields.Boolean(string="Reader Status", default=False)
    isConnected2 = fields.Boolean(
        string="Reader Status Trigger", default=False)
    id_device = fields.Char(string="ID thiết bị")
    name = fields.Selection([('reader', 'Đầu đọc thẻ'),
                             ('screenSecurity', "Màn hình bảo vệ"),
                             ('screenIn', "Màn hình vào"),
                             ('screenOut', "Màn hình ra"),
                             ], string="Loại thiết bị")
    name2 = fields.Selection([('screenSecurity', "Màn hình bảo vệ"),
                              ], string="Loại thiết bị")
    name3 = fields.Selection([('reader', 'Đầu đọc thẻ'),
                             ('screenIn', "Màn hình vào"),
                             ('screenOut', "Màn hình ra"),
                              ], string="Loại thiết bị")
    lane_id = fields.Many2one(
        "setting.nsp.lane", string="Cổng",  ondelete='cascade')
    office_id = fields.Many2one(
        "setting.nsp.office", string="Văn phòng",  ondelete='cascade')

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
        if vals['name2'] == 'screenSecurity':
            vals['name'] = vals['name2']
            id_device = "0001"
        elif vals['name3'] == 'screenIn':
            vals['name'] = vals['name3']
            id_device = "0002"
        elif vals['name3'] == 'screenOut':
            vals['name'] = vals['name3']
            id_device = "0003"
        else:
            vals['name'] = vals['name3']
        uidBCD = str(self.generate_truncated_uuid_4bytes())
        vals['id_device'] = formatted_now + '-' + \
            id_device + '-' + configurationCode+'-' + uidBCD
        new_record = super(SettingNspDevice, self).create(vals)
        return new_record
