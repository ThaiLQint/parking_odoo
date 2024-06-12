from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class SettingNspBranch(models.Model):
    _name = 'setting.nsp.branch'
    _description = 'Setting Parking'
    name = fields.Char(string="Chi Nhánh", required=True)
    parking_ids = fields.One2many(
        'setting.nsp.parking', 'branch_id', string="Bãi xe")

