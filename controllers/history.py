from odoo import http, modules
import pytz
import logging
import base64
import json
import math

from datetime import datetime, timedelta
from odoo.http import request
import threading
_logger = logging.getLogger(__name__)
my_dict = {}


class History(http.Controller):

    # kw["tid"]
    # kw["isIn"]
    @http.route('/api/history/validate', type='json', auth='public', methods=['POST'], website=False, csrf=False)
    def validate(self, **kw):
        tid = kw.get("tid", None)
        checkProduct = False
        # Tìm kiếm sản phẩm theo default_code
        product = self._find_product_by_tid(tid)
        port = kw["port"]
        picking_code = "outgoing"
        if product:
            if not self._defferentTime(product.write_date):
                return {"code": 400, "message": "Chờ 5s"}
            product.write({"write_date": datetime.now()})

            if product.picking_code == "outgoing" and port == "Cổng Vào":
                picking_code = "incoming"
            elif product.picking_code == "incoming" and port == "Cổng Ra":
                picking_code = "outgoing"
            else:
                return {"code": 400, "message": "Xe đã RA" if port == "Cổng Ra" else "Xe đã VÀO"}

            return self._handle_product_found(tid)

        # Tìm kiếm đối tác theo ref
        partner = self._find_partner_by_tid(tid)
        if not partner:
            return {"code": 400, "message": "Không tìm thấy thẻ"}

        # Kiểm tra danh sách sản phẩm riêng tư
        productTID = self._check_product_list(partner.product_ids_private)
        if productTID != "None":
            checkProduct = True
        # Kiểm tra danh sách sản phẩm công cộng
        if checkProduct == False:
            productTID = self._check_product_list(partner.product_ids_public)
            if productTID != "None":
                checkProduct = True
        if checkProduct:
            product = self._find_product_by_tid(my_dict[productTID])
            my_dict.pop(productTID, "None")
            if product.picking_code == "outgoing" and port == "Cổng Vào":
                picking_code = "incoming"
            elif product.picking_code == "incoming" and port == "Cổng Ra":
                picking_code = "outgoing"
            else:
                return {"code": 400, "message": "Xe đã " + "RA" if port == "Cổng Ra" else "VÀO"}
            product.write({"picking_code": picking_code})
            idHistory = self._handle_history(
                partner.id, product.id, port, product.move_history_id["id"], picking_code)
            product.write({"move_history_id": idHistory})

            return {"code": 200, "message": "Xe VÀO họp lệ" if picking_code == "incoming" else "Xe RA họp lệ"}
        return {"code": 400, "message": "Xe không hợp lệ"}

    def _find_product_by_tid(self, tid):
        """Tìm kiếm sản phẩm theo default_code."""
        return request.env['product.template'].sudo().search([('default_code', '=', tid)], limit=1)

    def _find_partner_by_tid(self, tid):
        """Tìm kiếm đối tác theo ref."""
        return request.env['res.partner'].sudo().search([('ref', '=', tid)], limit=1)

    def _handle_product_found(self, tid):
        """Xử lý khi tìm thấy sản phẩm."""
        my_dict.setdefault(tid, tid)
        return {"code": 200, "message": "Tìm thấy thẻ xe"}

    def _handle_history(self, idPartner, idProduct, port, move_history_id, picking_code):
        """Tìm kiếm sản phẩm theo default_code."""
        location = request.env['stock.location'].sudo().search(
            [("complete_name", "=", "WH/Stock")], limit=1)
        move_history = request.env['stock.move.line'].sudo().create({
            'move_history_id_before': move_history_id,
            'bien_so_realtime': "default",
            'product_id': idProduct,
            'picking_code': picking_code,
            'contact_id': idPartner,
            'location_id': location.id,
            'port': port,
            'location_dest_id': location.id,
            'company_id': 1,
            #  'image_1920_camera_sau': image_1920_camera_sau,
            #  'image_1920_bs_camera': image_1920_bs_camera,
        })
        return move_history.id

    def _check_product_list(self, product_list):
        """Kiểm tra danh sách sản phẩm."""
        for product in product_list:
            if my_dict.get(product["default_code"], "None") != "None":
                return product["default_code"]
        return "None"

    def _defferentTime(self, datetime):
        difference = datetime.now() - datetime
        # Lấy tổng số giây
        total_seconds = difference.total_seconds()
        if (total_seconds < 5):
            return False
        return True
