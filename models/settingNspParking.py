from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class SettingNspParking(models.Model):
    _name = 'setting.nsp.parking'
    _description = 'Setting Parking Name'
    name = fields.Char(string="Tên", required=True)
    branch_id  = fields.Many2one(
        "setting.nsp.branch", string="Chi nhánh")
    office_ids = fields.One2many('setting.nsp.office', 'parking_id', string="Văn phòng")