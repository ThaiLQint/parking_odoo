from odoo import http, modules
import pytz
import logging 
import base64
import json
import math
from odoo.http import request

_logger = logging.getLogger(__name__)
class ParkingHistoryController(http.Controller):
    @http.route('/api/parking/history/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_parking_history(self, **kw):
        _logger.info('Request Data: %s', kw)

        # kw['picking_code']
        # Lấy dữ liệu từ yêu cầu
        bardcode = kw.get('picking_code')
        contact_id = kw.get('contact_id')
        product_id = kw.get('product_id')
        bien_so_realtime = kw.get('bien_so_realtime')
        location_id = kw.get('location_id')

        # Tạo bản ghi mới trong model parking.history
        try:
            new_record = request.env['parking.history'].sudo().create({
                'picking_code': picking_code,
                'contact_id': contact_id,
                'product_id': product_id,
                'bien_so_realtime': bien_so_realtime,
                'location_id': location_id
            })
            response_data = {
                'success': True,
                'message': 'Record created successfully',
                'data': {
                    'id': new_record.id,
                    'create_date': new_record.create_date,
                    'picking_code': new_record.picking_code,
                    'contact_id': new_record.contact_id.id,
                    'product_id': new_record.product_id.id,
                    'bien_so_realtime': new_record.bien_so_realtime,
                    'location_id': new_record.location_id.id
                }
            }
            _logger.info('New Record Created: %s', response_data)
            return response_data
        except Exception as e:
            _logger.error('Error creating record: %s', str(e))
            return {'success': False, 'message': 'Error creating record', 'error': str(e)}