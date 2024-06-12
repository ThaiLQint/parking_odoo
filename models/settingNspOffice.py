from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class SettingNspOffice(models.Model):
    _name = 'setting.nsp.office'
    _description = 'Setting Parking Office'
    name = fields.Char(string="Tên", required=True)
    parking_id  = fields.Many2one(
        "setting.nsp.parking", string="Bãi xe")
    lane_in_ids = fields.One2many('setting.nsp.lane.in', 'office_id',string="Cổng vào")
    lane_out_ids = fields.One2many('setting.nsp.lane.out', 'office_id', string="Cổng ra")
    
