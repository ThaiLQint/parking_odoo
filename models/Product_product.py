from odoo import api, fields, models

# COLOR_CHOICES = [
#     ('white', 'White'),
#     ('black', 'Black'),
#     ('red', 'Red'),
#     ('blue', 'Blue'),
#     ],

class Product_product(models.Model):
    _inherit = 'product.product'
    name = fields.Char(string="Biển số")
    responsible_id = fields.Many2one('res.partner', string="Chủ sở hữu")
    barcode = fields.Char(string="Mật khẩu")
    default_code = fields.Char(string="Mã định danh")
    check_doi_the = fields.Boolean(string="Đã đổi thẻ", default=False)
    activity_summary = fields.Char(string="Hãng xe", store=True)

    so_khung = fields.Char(string="Số khung", store=True)
    # default_color = fields.Integer(string="Màu xe")

    so_loai = fields.Char(string="Mã kiểu loại", readonly=False)
    so_may = fields.Char(string="Số máy", readonly=False)
    so_dang_ky = fields.Char(string="Số đăng ký", readonly=False)

    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        return 0  
