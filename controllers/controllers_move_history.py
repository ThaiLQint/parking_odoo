# -*- coding: utf-8 -*-
from odoo import http
from odoo import fields
class ControllerMoveHistory(http.Controller):
   

    @http.route('/parking/get/move_history/get_all/epc', website=False,csrf=False, type='json', methods=['POST'], auth='public')
    def get_all_move_history(self, **kw):
        move_histories = http.request.env['stock.move.line'].sudo().search_read(
            domain=[('lot_name', '=', kw['sEPC']), ('create_date','=',fields.Date.today())],
            fields=['date','lot_name', 'reference','location_id','location_dest_id'],
        )
        return move_histories

   
