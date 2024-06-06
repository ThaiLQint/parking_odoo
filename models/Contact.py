import logging
from odoo import api, fields, models, http
import uuid
import json
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)

class Contact(models.Model):
    _inherit = 'res.partner'
    _sql_constraints = [
        ('vat_unique',
         'unique(vat)',
         'CMND/CCCD ĐÃ TỒN TẠI!!'),
        ('ma_dinh_danh_unique',
         'unique(ma_dinh_danh)',
         'MÃ ĐỊNH DANH ĐÃ TỒN TẠI!')
    ]
    type = fields.Selection(
        [('contact', 'Address'),
         ('invoice', 'Invoice Address'),
         ('delivery', 'Delivery Address'),
         ('other', 'Other Address'),
        ], string='Address Type',
        default='contact',
        help="- Contact: Use this to organize the contact details of employees of a given company (e.g. CEO, CFO, ...).\n"
             "- Invoice Address: Preferred address for all invoices. Selected by default when you invoice an order that belongs to this company.\n"
             "- Delivery Address: Preferred address for all deliveries. Selected by default when you deliver an order that belongs to this company.\n"
             "- Other: Other address for the company (e.g. subsidiary, ...)")
    display_name = fields.Char(string="Họ tên", required=False)
    name = fields.Char(string="Họ tên ")
    vat = fields.Char(string="Số CMND/CCCD", required=True)
    phone = fields.Char(string="Số điện thoại", required=True)  
    barcode = fields.Char(string="Mật khẩu",readonly=False)
    ref = fields.Char(string="Mã thẻ",readonly=False)
    employee = fields.Boolean(string="Cấp thẻ", default=False)
    ma_dinh_danh = fields.Char(string="ID nhân viên", required=False, store=True)
    # job_position = fields.Char(string="Job Position", required=True)
<<<<<<< HEAD
    zalo = fields.Char(string="Zalo", required=True, store=True)
    viper = fields.Char(string="Viper" )
    what_app = fields.Char(string="What's App")
    radio_zalo = fields.Boolean(string="Zalo", default=True)
    radio_viper = fields.Boolean(string="Viper", default=False)
    radio_what_app = fields.Boolean(string="What's App", default=False)
    date_expiration = fields.Datetime(string="Ngày hết hạn")
    
    product_ids_public = fields.Many2many("product.template", relation="product_template_res_partner_rel", column1="res_partner_id", column2="product_template_id", string="D/S xe dùng chung",
                                        readonly=True)
    product_ids_private = fields.One2many("product.template", "contact_id", string="D/S xe chính chủ",
                                        readonly=True)

    partner_id = fields.Many2one("res.partner", string="Liên hệ",store=True)
=======
    zalo = fields.Char(string="Zalo")
    viper = fields.Char(string="Viber")
    what_app = fields.Char(string="What's App")
    zalo_2 = fields.Char(string="Zalo", readonly=True)
    viper_2 = fields.Char(string="Viber", readonly=True)
    what_app_2 = fields.Char(string="What's App", readonly=True)
    radio_zalo = fields.Boolean(string="Zalo", default=True)
    radio_viper = fields.Boolean(string="Viber", default=False)
    radio_what_app = fields.Boolean(string="What's App", default=False)
    date_expiration = fields.Datetime(string="Ngày hết hạn", required=True)
    
    product_ids_public = fields.Many2many("product.template", relation="product_template_res_partner_rel", column1="res_partner_id", column2="product_template_id", string="D/S xe dùng chung",
                                        readonly=True)
        
    product_ids_private = fields.One2many("product.template", "contact_id", string="D/S xe chính chủ",
                                        readonly=True)

    partner_id = fields.Many2one("res.partner", string="Liên hệ")
>>>>>>> 7bc57abf3be0637b987b128c965cd2898e393e12
    partner_ids = fields.Many2many(
    'res.partner', 
    'contact_partner_rel', 
    'contact_id', 
    'partner_id', 
    string='Danh sách liên hệ',
<<<<<<< HEAD
    domain="[('id', '!=', id)]", store=True
    )
    
    vehicle = fields.Many2one("res.partner", string="Vehicle", store=True)

    vehicles = fields.One2many('res.partner', 'vehicle', string='Phương Tiện', store=True)
=======
    domain="[('id', '!=', id)]",
    )
    
    vehicle = fields.Many2one("res.partner", string="Vehicle")

    vehicles = fields.One2many('res.partner', 'vehicle', string='Phương Tiện')
>>>>>>> 7bc57abf3be0637b987b128c965cd2898e393e12
    
    image_1920 = fields.Image(string="Ảnh đại diện", max_width=1024, max_height=768)
    image_1920_cmnd_cccd_truoc = fields.Image(
        string="Ảnh mặt trước CMND/CCCD", max_width=1920, max_height=1920)
    image_1920_cmnd_cccd_sau = fields.Image(
        string="Ảnh mặt sau CMND/CCCD", max_width=1920, max_height=1920)
    
    contact_id = fields.Many2one('res.partner', string='Chủ sở hữu')
    bien_so_realtime = fields.Char(string="Biển số xe")
    car_status = fields.Char(string="Trạng Thái")
    
    def delete_button(seft):
        seft.partner_id.partner_ids = [(3, seft.id)]
        _logger.info(seft.product_ids_public)
        

    def delete_button_user_ids(self):
        # Lấy id_product từ context
        _logger.info(self.env.context['id'])
        id_product = self.env.context['id']

        # id_product = self.env.context.get('id')
        _logger.info(f"Product ID from context: {id_product}")

        if id_product:
            product = self.env['product.template'].browse(id_product)
            _logger.info(f"Product browsed: {product}")
            # Kiểm tra sản phẩm có tồn tại không
            if product.exists():
                _logger.info(f"Product exists: {product.name}")
                # Kiểm tra user id có trong product user_ids không
                if self.id in product.user_ids.ids:
                    product.write({'user_ids': [(3, self.id)]})
                    _logger.info(f"User ID {self.id} removed from product {product.id}")
                else:
                    _logger.warning(f"User ID {self.id} not in product user_ids")
            else:
                _logger.error(f"Product ID {id_product} does not exist")
        else:
            _logger.error("No product ID found in context")
    
    # def delete_button_user_ids(self):
    #     _logger.info(self.env.context.get("id_product"))
    #     id_product = self.env.context.get("id_product")
    #     if id_product:
    #         product = self.env['product.template'].browse(id_product)
    #         if product.exists() and self.id in product.user_ids.ids:
    #             product.write({'user_ids': [(3, self.id)]})
    
    @api.model
   
    def create(self, vals):
        vals['date_expiration'] = fields.Datetime.now() + \
            relativedelta(months=1)
        new_record = super(Contact, self).create(vals)
<<<<<<< HEAD
        self.env["res.users"].create({'image_1920': vals['image_1920'], 'name': vals['name'], 'email': vals['email'],
                                     'login': vals['email'], 'company_id': 1, 'sel_groups_1_10_11': 11, 'active': True, 'partner_id': new_record.id})
=======
        # self.env["res.users"].create({'image_1920': vals['image_1920'], 'name': vals['name'], 'email': vals['email'],
        #                              'login': vals['email'], 'company_id': 1, 'sel_groups_1_10_11': 11, 'active': True, 'partner_id': new_record.id, 'password': vals['phone']})
>>>>>>> 7bc57abf3be0637b987b128c965cd2898e393e12
        return new_record
    
    @api.constrains('barcode')
    def _check_barcode_unicity(self):
        return 0

    def write(self, vals):
        # Code before write: 'self' has the old values

        record = super(Contact, self).write(vals)
        # Code after write: can use 'self' with the updated
        # values
        return record

    def createUUID(self):
        hex_arr = uuid.uuid4().hex
        check_epc_user = self.search(
            domain=[('ref', '=', "0" + hex_arr[1:24])],
            limit=1)
        if check_epc_user:
            return "LỖI: KHÔNG THỂ TẠO UUID DO BỊ ĐÃ TỒN TẠI [0" + hex_arr[1:24]+"]!!"
        message = "ghi epc|"+"0" + hex_arr[1:24] + "|"+hex_arr[24:]
        return message
<<<<<<< HEAD
=======
    
    @api.onchange('radio_zalo')
    def onchange_radio_zalo(self):
        if self.radio_zalo:
            self.radio_viper = False
            self.radio_what_app = False

    @api.onchange('radio_viper')
    def onchange_radio_viper(self):
        if self.radio_viper:
            self.radio_zalo = False
            self.radio_what_app = False

    @api.onchange('radio_what_app')
    def onchange_radio_what_app(self):
        if self.radio_what_app:
            self.radio_zalo = False
            self.radio_viper = False
        
    @api.model
    def create(self, vals):
        if 'zalo' in vals:
            vals['zalo_2'] = vals['zalo']
        if 'viper' in vals:
            vals['viper_2'] = vals['viper']
        if 'what_app' in vals:
            vals['what_app_2'] = vals['what_app']
        return super(Contact, self).create(vals)

    def write(self, vals):
        if 'zalo' in vals:
            vals['zalo_2'] = vals['zalo']
        if 'viper' in vals:
            vals['viper_2'] = vals['viper']
        if 'what_app' in vals:
            vals['what_app_2'] = vals['what_app']
        _logger.info(vals)
        return super(Contact, self).write(vals)

    @api.onchange('zalo')
    def _onchange_zalo(self):
        self.zalo_2 = self.zalo

    @api.onchange('viper')
    def _onchange_viper(self):
        self.viper_2 = self.viper

    @api.onchange('what_app')
    def _onchange_what_app(self):
        self.what_app_2 = self.what_app
>>>>>>> 7bc57abf3be0637b987b128c965cd2898e393e12
