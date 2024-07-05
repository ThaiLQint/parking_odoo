from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SettingNspOffice(models.Model):
    _name = 'setting.nsp.office'
    _description = 'Setting Parking Office'
    name = fields.Char(string="Tên", required=True)
    parking_id = fields.Many2one(
        "setting.nsp.parking", string="Bãi xe",  ondelete='cascade')
   
    device_ids = fields.One2many(
        'setting.nsp.device', 'office_id', string="Thiết bị")
    
    lane_in_ids = fields.One2many(
        'setting.nsp.lane', 'office_id_in', string="Cổng vào")

    lane_out_ids = fields.One2many(
        'setting.nsp.lane', 'office_id_out', string="Cổng ra")
