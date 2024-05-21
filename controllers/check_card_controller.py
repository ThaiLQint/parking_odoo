from odoo import http, modules
import pytz
import logging 
import base64
import json
import math

from datetime import datetime
from odoo.http import request

_logger = logging.getLogger(__name__)

class CheckCardController(http.Controller):

    @http.route('/api/product/check_card', type='http', auth='public', methods=['POST'], csrf=False)
    def check_card_and_push_data(self, **kw):
        default_code = kw.get('tid_xe')
        bien_so_realtime = kw.get('bien_so_realtime')
        gate = kw.get('gate')
        entry_type = kw.get('entry_type')  # "ra" hoặc "vao"

        # tidXe = "123"
        # tidNg = "234"
        # inOut = 1/0
        # imgCamTruoc = File
        # imgCamSau = File
        
        # tim Xe dua tidXe => chủ sở hữu của xe vừa tìm được => so sánh mã thẻ của chủ sở hữu với tidNg=>
        # Dung het nhu data thi :
        # Luu vao lich su di chuyen

        if not default_code:
            return {
                'success': False,
                'message': 'default_code is required'
            }
        
        # Kiểm tra mã thẻ xe trong model 'product.template'
        product = http.request.env['product.template'].sudo().search([('tid_xe', '=', default_code)], limit=1)
        # check + .mÃ THẺ BARDCODE
        # get 2: .partner_ids và contact_id
        if product:
            contact_id = product.contact_id.id
            contact = http.request.env['res.partner'].sudo().search([('id', '=', contact_id)], limit=1)
            
            if not contact:
                return {
                    'success': False,
                    'message': 'Contact not found'
                }
            
            # Kiểm tra mã thẻ của chủ sở hữu
            if contact.ref != default_code:
                return {
                    'success': False,
                    'message': 'Owner card code does not match'
                }
            
            # Đẩy thông tin dữ liệu lên tab 'Lịch sử di chuyển'
            history_data = {
                'create_date': datetime.now(),
                'entry_type': entry_type,
                'contact_name': contact.name,
                'product_id': product.id,
                'bien_so_dang_ky': product.image_1920,  # Assuming 'image_1920' field is used for 'Biển số đã đăng ký'
                'bien_so_realtime': bien_so_realtime,
                'gate': gate,
            }
            
            # Tạo bản ghi lịch sử di chuyển 
            http.request.env['stock.move.line'].sudo().create(history_data)
            
            return {
                'success': True,
                'message': 'Data pushed successfully',
                'data': history_data
            }
        else:
            return {
                'success': False,
                'message': 'Chưa có mã thẻ xe'
            }
