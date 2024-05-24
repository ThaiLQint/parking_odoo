from odoo import api, fields, models

<<<<<<< HEAD
# COLOR_CHOICES = [
#     ('white', 'White'),
#     ('black', 'Black'),
#     ('red', 'Red'),
#     ('blue', 'Blue'),
#     ],
=======
>>>>>>> 28d7efaacc4993e575e361c03fefee412a40d6fd

class Product_product(models.Model):
    _inherit = 'product.product'
    name = fields.Char(string="Biển số")
    responsible_id = fields.Many2one('res.partner', string="Chủ sở hữu")
    barcode = fields.Char(string="Mật khẩu")
    default_code = fields.Char(string="Mã định danh")
    check_doi_the = fields.Boolean(string="Đã đổi thẻ", default=False)
    activity_summary = fields.Char(string="Hãng xe", store=True)

<<<<<<< HEAD
    so_khung = fields.Char(string="Số khung", store=True)
    # default_color = fields.Integer(string="Màu xe")

    so_loai = fields.Char(string="Mã kiểu loại", readonly=False)
    so_may = fields.Char(string="Số máy", readonly=False)
    so_dang_ky = fields.Char(string="Số đăng ký", readonly=False)

    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        return 0  
=======
    @api.constrains('barcode')
    def _check_barcode_uniqueness(self):
        return 0
>>>>>>> 28d7efaacc4993e575e361c03fefee412a40d6fd
