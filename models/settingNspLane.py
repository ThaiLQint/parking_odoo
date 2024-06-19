from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class SettingNspLaneIn(models.Model):
    _name = 'setting.nsp.lane'
    _description = 'Setting Parking Lane'
    name = fields.Char(string="Tên", required=True)
    office_id_in  = fields.Many2one(
        "setting.nsp.office", string="Văn phòng",  ondelete='cascade')
    office_id_out  = fields.Many2one(
        "setting.nsp.office", string="Văn phòng",  ondelete='cascade')
    laneInOut = fields.Selection([('in', 'Làn vào'),
                                  ('out', 'Làn ra'),
                                  ], default="in", string="Cổng vào hay ra")
    device_ids = fields.One2many('setting.nsp.device', 'lane_id',string="Thiết bị")
    
