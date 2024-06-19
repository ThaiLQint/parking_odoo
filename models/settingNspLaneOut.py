from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SettingNspLaneOut(models.Model):
    _name = 'setting.nsp.lane.out'
    _description = 'Setting Parking Lane Out'
    name = fields.Char(string="Tên", required=True)
    office_id = fields.Many2one(
        "setting.nsp.office", string="Văn phòng", ondelete='cascade')
    device_ids = fields.One2many(
        'setting.nsp.device.out', 'lane_id', string="Thiết bị")
