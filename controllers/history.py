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
    @http.route('/api/history/validate', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def validate(self, **kw):
        if kw["code"] == "parking":
            return self._parkingHistoryHandle(kw)

    @http.route('/api/history/getbyid', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def getById(self, **kw):
        moveHistory = self._find_by_key("stock.move.line", "id", kw["id"])
        if not moveHistory:
            return json.dumps({"code": 400, "message": "Lịch sử di chuyển không tìm thấy"})
        partner = moveHistory.contact_id
        product = moveHistory.product_id
        return json.dumps({
            "nameNg": partner.name,
            "nameXe": product.name,
            "tidNg": partner.ref[8:],
            "tidXe": product.default_code[8:],
            "typeXe": product.categ_id.complete_name,
            "imgXe": product.image_1920.decode(),
            "imgNg": partner.image_1920.decode(),
            "imgPath1": moveHistory.image_1920_camera_truoc.decode(),
            "imgPath2": moveHistory.image_1920_camera_sau.decode(),
            "imgBienSo": product.image_1920_bien_so.decode(),
            "createDateTime": self._changeDate(moveHistory.create_date),
            "pickingCode": product.picking_code,
        })

    def _changeDate(self, date_in):
        user_tz = pytz.timezone(str(http.request.env.user.tz or pytz.utc))
        _logger.info(date_in)
        # Convert the date to a Python `datetime` object
        python_date = date_in.strptime(
            str(date_in), "%Y-%m-%d %H:%M:%S.%f")
        timezone = pytz.utc.localize(python_date).astimezone(user_tz)
        # if (timezone.date() == today):

        display_date_result = timezone.strftime("%d/%m/%Y %H:%M:%S")
        return display_date_result

    def _parkingHistoryHandle(self, kw):
        tid = kw.get("tid", None)
        checkProduct = False
        # Tìm kiếm sản phẩm theo default_code
        product = self._find_by_key("product.template", "default_code", tid)
        port = kw["port"]
        picking_code = "outgoing"
        if product:
            if not self._defferentTime(product.write_date): # timer chờ 5s
                return json.dumps({"code": 400, "message": "Chờ 5s"})
            product.write({"write_date": datetime.now()})

            if product.picking_code == "outgoing" and port == "Cổng Vào": # Nếu phát hiện thẻ xe trong database và đã ra bãi
                picking_code = "incoming"
                checkProduct = True
            elif product.picking_code == "incoming" and port == "Cổng Ra":
                picking_code = "outgoing"
            else:
                if port == "Cổng Ra":
                    message = "đã RA"
                elif port == "Cổng Vào":
                    message = "đã VÀO"
                else:
                    message = "không hợp lệ!!"
                return json.dumps({"code": 400, "message": "Xe " + message})

            result = self._handle_product_found(tid) # Lưu cặp giá trị thẻ <key, value>
            if picking_code == "outgoing":
                return result
        if picking_code == "outgoing":
            # Tìm kiếm đối tác theo ref
            partner = self._find_by_key("res.partner", "ref", tid)
            if not partner:
                return json.dumps({"code": 400, "message": "Không tìm thấy thẻ"})

            # Kiểm tra danh sách sản phẩm riêng tư
            tid = self._check_product_list(partner.product_ids_private)
            if tid != "None":
                checkProduct = True
            # Kiểm tra danh sách sản phẩm công cộng
            if checkProduct == False:
                tid = self._check_product_list(partner.product_ids_public)
                if tid != "None":
                    checkProduct = True

            if checkProduct:
                product = self._find_by_key(
                    "product.template", "default_code", my_dict[tid])

                if product.picking_code == "incoming" and port == "Cổng Ra":
                    picking_code = "outgoing"
                else:
                    if port == "Cổng Ra":
                        message = "đã RA"
                    elif port == "Cổng Vào":
                        message = "đã VÀO"
                    else:
                        message = "không hợp lệ!!"
                    return json.dumps({"code": 400, "message": "Xe " + message})

        if checkProduct:  # Xe vào + thẻ người thẻ xe lối ra hợp lệ
            my_dict.pop(tid, "None")
            product.write({"picking_code": picking_code})
            imgTruoc, imgSau = self._imgTruocSauCamera(
                kw["imgTruoc"], kw["imgSau"])
            id = 0
            if picking_code == "incoming":
                id = product.contact_id.id
            elif picking_code == "outgoing":
                id = partner.id

            idHistory = self._handle_history(
                id, product.id, port, product.move_history_id["id"], picking_code, imgTruoc, imgSau)
            product.write({"move_history_id": idHistory})
            if picking_code == "incoming":
                message = "VÀO họp lệ"
            elif picking_code == "outgoing":
                message = "RA họp lệ"
            else:
                message = "không hợp lệ!!"
            return json.dumps({"code": 200, "message": "Xe " + message})
        else:
            return json.dumps({"code": 400, "message": "Xe không hợp lệ!!"})

    def _imgTruocSauCamera(self, imgTruoc, imgSau):
        if imgTruoc != "None":
            file = imgTruoc
            img_attachment = file.read()
            imgTruoc = base64.b64encode(img_attachment)
        else:
            imgTruoc = None
        if imgSau != "None":
            file = imgSau
            img_attachment = file.read()
            imgSau = base64.b64encode(img_attachment)
        else:
            imgSau = None
        return imgTruoc, imgSau

    def _find_by_key(self, module, key, value):
        """Tìm kiếm sản phẩm theo default_code."""
        return request.env[module].sudo().search([(key, '=', value)], limit=1)

    def _handle_product_found(self, tid):
        """Xử lý khi tìm thấy sản phẩm."""
        my_dict.setdefault(tid, tid)
        return json.dumps({"code": 200, "message": "Tìm thấy thẻ xe"})

    def _handle_history(self, idPartner, idProduct, port, move_history_id, picking_code, imgTruoc, imgSau):
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
            'image_1920_camera_sau': imgSau,
            'image_1920_camera_truoc': imgTruoc,
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