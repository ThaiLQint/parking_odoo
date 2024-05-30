from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)

class  AlertTag(models.Model):
    _name = 'alert.tag'
    _description = 'Alert Tag'

    sequence = fields.Integer('Sequence', default=0)
    product_id = fields.Many2one(
        "product.template", string="Xe")
    name = fields.Char(string = "Thông điệp")
    code = fields.Integer(string = "Code")
    @api.model
    def create(self, vals):
        _logger.info(vals)
        new_record = super(AlertTag, self).create(vals)
        return new_record