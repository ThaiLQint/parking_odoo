from odoo import api, fields, models, http, exceptions
import uuid


def create_product_move_history(state, product_id, location_id, location_dest_id, epc):
    stock_move_history = http.request.env["stock.move.line"].sudo().create(
        {'reference': state,
            'product_id': product_id,
            'reserved_uom_qty': 1.0,
            'lot_name': epc,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'qty_done': 1.0,
            'company_id': 1})


def check_bien_so_xe(bien_so):
    xe = http.request.env['product.template'].sudo().search(
        domain=[('name', '=', bien_so)],
        limit=1)
    return xe


def check_exist_xe(bien_so, ma_dinh_danh):
    xe = http.request.env['product.product'].sudo().search(
        domain=['|', ('default_code', '=', ma_dinh_danh),
                ("name", "=", bien_so)],
        limit=1)
    if not xe:
        return 1
    if (xe.default_code == ma_dinh_danh):
        return -1
    if (xe.name == bien_so):
        return -2


def check_epc_xe(ma_dinh_danh):
    xe = http.request.env['product.template'].sudo().search(
        domain=[('default_code', '=', ma_dinh_danh)],
        limit=1)
    return xe


class Product_template(models.Model):
    _inherit = 'product.template'
    _sql_constraints = [
        ('field_unique',
         'unique(name)',
         'BIỂN SỐ ĐÃ TỒN TẠI!!')
    ]
    name = fields.Char(string="Biển số")

    contact_id = fields.Many2one(
        'res.partner', string='Chủ sở hữu', required=True)
    barcode = fields.Char(string="Mật khẩu", readonly=False)
    default_code = fields.Char(string="Mã thẻ")
    user_ids = fields.Many2many(
        'res.partner', string="Danh sách người dùng")
    check_doi_the = fields.Boolean(string="Đã đổi thẻ", default=False)
    activity_summary = fields.Char(string="Hãng xe", store=True)
    image_1920 = fields.Image(
        string="Ảnh xe", max_width=1920, max_height=1920)
    image_1920_bien_so = fields.Image(
        string="Ảnh biển số xe", max_width=1920, max_height=1920)
    image_1920_cavet_sau = fields.Image(
        string="Mặt trước cà vẹt xe", max_width=1920, max_height=1920)
    image_1920_cavet_truoc = fields.Image(
        string="Mặt sau cà vẹt xe", max_width=1920, max_height=1920)

    @api.model
    def create(self, vals):
        vals["tracking"] = "serial"
        new_record = super(Product_template, self).create(vals)
        # result = check_exist_xe(vals['name'], "123")
        # if result == -1:
        #     raise exceptions.UserError("THẺ ĐÃ TỒN TẠI!")
        # if result == -2:
        #     raise exceptions.UserError("BIỂN SỐ ĐÃ TỒN TẠI!")
        # hex_arr = uuid.uuid4().hex
        # if check_epc_xe("0" + hex_arr[1:24]):
        #     raise exceptions.UserError(
        #         "Không thể tạo được UUID liên hệ nhà phát triển để sử lý")
        # new_record = super(Product_template, self).create({
        #     'name':  vals['name'],
        #     'image_1920': vals['image_1920'],
        #     'default_code': "1" + hex_arr[1:24],
        #     'contact_id': vals['contact_id'],
        #     'barcode': hex_arr[24:],
        #     'user_ids': [(4, vals['contact_id'])],
        #     'detailed_type': 'product'
        # })
        new_record.product_variant_id.write({
            'name':  vals['name'],
            'responsible_id': vals['contact_id'],
        })
        # create_product_move_history(
        #     "BX/OUT", new_record.product_variant_id.id, 4, 5, "123")
        return new_record

    def createUUID(self):
        hex_arr = uuid.uuid4().hex
        if check_epc_xe("1" + hex_arr[1:24]):
            return "LỖI: KHÔNG THỂ TẠO UUID LIÊN HỆ NHÀ SẢN XUẤT ĐỂ KHẮC PHỤC!!"
        message = "ghi the|"+"1" + hex_arr[1:24] + "|"+hex_arr[24:]
        return message
