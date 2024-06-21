import requests
from odoo import http, _, fields
import pytz
import logging
import base64
import json
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from odoo.http import request, Response
import threading
import time
_logger = logging.getLogger(__name__)

class History(http.Controller):
    def __init__(self):
        self.my_dict = {}  # Khởi tạo dictionary rỗng
        url = 'http://localhost:8069'
        db = 'demo'
        username = 'ad'
        password = '1'

        session_url = f'{url}/web/session/authenticate'
        data = {
            'params': {
                'db': db,
                'login': username,
                'password': password,
            }
        }
        session_response = requests.post(session_url, json=data)
        session_data = session_response.json()
        if session_data.get('result') and session_response.cookies.get('session_id'):
            self.session_id = session_response.cookies['session_id']
        else:
            _logger.error(
                f'Error: Failed to authenticate - {session_data.get("error")}')
            return None

        self.lock = threading.Lock()
        threaded = threading.Thread(
            target=self.threadCheckAlert
        )
        threaded.start()

    def _defferentTime(self, datetime, second):
        difference = datetime.now() - datetime
        # Lấy tổng số giây
        total_seconds = difference.total_seconds()
        if (total_seconds < second):
            return False
        return True

    def run_Webhook(self, id):
        try:
            # 'send and forget' strategy, and avoid locking the user if the webhook
            # is slow or non-functional (we still allow for a 1s timeout so that
            # if we get a proper error response code like 400, 404 or 500 we can log)
            json_values = {
                'params': {
                    'productId': id,
                    'tag': 'Người',
                    'code': 'parking',
                    'codeAlert': 1
                }
            }
            response = requests.post("http://localhost:8069/api/history/alert/tag", json=json_values, headers={
                                     'Content-Type': 'application/json',
                                     'Cookie': f"session_id={self.session_id}",
                                     }, timeout=0.1)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            _logger.warning("Webhook call timed out after 1s - it may or may not have failed. "
                            "If this happens often, it may be a sign that the system you're "
                            "trying to reach is slow or non-functional.")
        except requests.exceptions.RequestException as e:
            _logger.warning("Webhook call failed: %s", e)
        except Exception as e:  # noqa: BLE001
            raise UserError(
                _("Wow, your webhook call failed with a really unusual error: %s", e)) from e

    def threadCheckAlert(self):
        while True:
            for key in self.my_dict:
                value = self.my_dict[key]
                if self._defferentTime(value["datetime"], 4):
                    try:
                        self.run_Webhook(value["id"])
                    except Exception as e:
                        _logger.error(str(e))
                    self.my_dict.pop(key)
                    if not self.my_dict:
                        break
            time.sleep(1)

    @http.route('/api/history/validate', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def validate(self, **kw):
        if kw["code"] == "parking":
            return self._parkingHistoryHandle(kw)

    @http.route('/api/history/alert/tag', type='json', auth='public', methods=['POST'],  website=False, csrf=False)
    def alert_tag(self, **kw):
        if kw["code"] == "parking":
            return self.create_alert_tag(kw)
        
    def create_alert_tag(self, kw):
        code = kw["codeAlert"]
        if code == 1:
            name = "Thiếu thẻ người"
        if code == 2:
            name = "Sai mật khẩu thẻ " + kw["tag"]
        result = request.env["alert.tag"].sudo().create({
            "code": code,
            "name": name,
            "product_id": kw["productId"]
        })
        result.unlink()
        return Response(json.dumps({"message": "Tạo thành công"}), content_type='application/json;charset=utf-8', status=201)

    @http.route('/api/history/alert/product', type='http', auth='public', methods=['POST'],  website=False, csrf=False)
    def alert_get_product(self, **kw):
        product = self._find_by_key('product.template', 'id', kw['productId'])
        partner = product.contact_id
        return Response(json.dumps({
            "productId": product.id,
            "nameNg": partner.name,
            "nameXe": product.name,
            "tidNg": partner.ref[8:],
            "tidXe": product.default_code[8:],
            "typeXe": product.categ_id.complete_name,
            "imgXe": product.image_1920.decode(),
            "imgNg": partner.image_1920.decode(),
            "imgPath1": "None",
            "imgPath2": "None",
            "imgBienSo": product.image_1920_bien_so.decode(),
            "createDateTime": "None",
            "pickingCode": product.picking_code,
        }), content_type='application/json;charset=utf-8', status=200)

    @http.route('/api/history/getbyid', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def getById(self, **kw):
        product = self._find_by_key("product.template", "id", kw["productId"])
        if not product:
            return Response(json.dumps({"message": "Xe không tìm thấy [" + kw["productId"]+"]"}), content_type='application/json;charset=utf-8', status=400)
        partner = self._find_by_key("res.partner", "id", kw["contactId"])
        if not partner:
            return Response(json.dumps({"message": "Liên hệ không tìm thấy [" + kw["contactId"]+"]"}), content_type='application/json;charset=utf-8', status=400)
        if product.image_1920 == False:
            product_image_1920 = "None"
        else:
            product_image_1920 = product.image_1920.decode()

        if product.image_1920_bien_so == False:
            product_image_1920_bien_so = "None"
        else:
            product_image_1920_bien_so = product.image_1920_bien_so.decode()
        return Response(json.dumps({
            "productId": product.id,
            "nameNg": partner.name,
            "nameXe": product.name,
            "tidNg": partner.ref[8:],
            "tidXe": product.default_code[8:],
            "typeXe": product.categ_id.complete_name,
            "imgXe": product_image_1920,
            "imgBienSo": product_image_1920_bien_so,
            "pickingCode": product.picking_code,
        }), content_type='application/json;charset=utf-8', status=200)

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
            if not self._defferentTime(product.write_date, 5):  # timer chờ 5s
                return Response(json.dumps({"message": "Chờ 5s"}), content_type='application/json;charset=utf-8', status=400)
            product.write({"write_date": datetime.now()})
            # Nếu phát hiện thẻ xe trong database và đã ra bãi
            if product.picking_code == "outgoing" and port == "Cổng Vào":
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

                return Response(json.dumps({"message": "Xe " + message}), content_type='application/json;charset=utf-8', status=400)
            # Lưu cặp giá trị thẻ <key, value>
            result = self._handle_product_found(tid, product.id)
            if picking_code == "outgoing":
                return result
        if picking_code == "outgoing":
            # Tìm kiếm đối tác theo ref
            partner = self._find_by_key("res.partner", "ref", tid)
            if not partner:
                return Response(json.dumps({"message": "Không tìm thấy thẻ"}), content_type='application/json;charset=utf-8', status=400)
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
                    "product.template", "default_code", self.my_dict[tid]['tid'])
                if product.picking_code == "incoming" and port == "Cổng Ra":
                    picking_code = "outgoing"
                else:
                    if port == "Cổng Ra":
                        message = "đã RA"
                    elif port == "Cổng Vào":
                        message = "đã VÀO"
                    else:
                        message = "không hợp lệ!!"

                    return Response(json.dumps({"message": "Xe " + message}), content_type='application/json;charset=utf-8', status=400)

        if checkProduct:  # Xe vào + thẻ người thẻ xe lối ra hợp lệ
            self.lock.acquire()
            self.my_dict.pop(tid, "None")
            self.lock.release()
            id = 0
            if picking_code == "incoming":
                id = product.contact_id.id
            elif picking_code == "outgoing":
                id = partner.id
            contact_id_in_out = id
            product.write({"picking_code": picking_code, 'contact_id_in_out': contact_id_in_out}) 
            imgTruoc, imgSau = self._imgTruocSauCamera(
                kw["imgTruoc"], kw["imgSau"])
            idHistory = self._handle_history(
                id, product.id, port, product.move_history_id["id"], picking_code, imgTruoc, imgSau)
            if picking_code == "incoming":
                message = "VÀO họp lệ"
            elif picking_code == "outgoing":
                message = "RA họp lệ"
            else:
                message = "không hợp lệ!!"
            product.write({"move_history_id": idHistory})
            return Response(json.dumps({"id": idHistory, "message": "Xe " + message}), content_type='application/json;charset=utf-8', status=200)
        else:
            return Response(json.dumps({"message": "Xe không hợp lệ!!"}), content_type='application/json;charset=utf-8', status=400)

    def _imgTruocSauCamera(self, imgTruoc, imgSau):
        img_attachment = imgTruoc.read()
        if not img_attachment:
            imgTruoc = None
        else:
            imgTruoc = base64.b64encode(img_attachment)

        img_attachment = imgSau.read()
        if not img_attachment:
            imgSau = None
        else:
            imgSau = base64.b64encode(img_attachment)
        return imgTruoc, imgSau

    def _find_by_key(self, module, key, value):
        """Tìm kiếm sản phẩm theo default_code."""
        return request.env[module].sudo().search([(key, '=', value)], limit=1)

    def _handle_product_found(self, tid, id):
        """Xử lý khi tìm thấy sản phẩm."""
        self.my_dict.setdefault(
            tid, {"tid": tid, "datetime": datetime.now(), 'id': id})

        return Response(json.dumps({"message": "Tìm thấy thẻ xe"}), content_type='application/json;charset=utf-8', status=200)

    def _handle_history(self, idPartner, idProduct, port, move_history_id, picking_code, imgTruoc, imgSau):
        """Tìm kiếm sản phẩm theo default_code."""
        location = request.env['stock.location'].sudo().search(
            [("complete_name", "=", "WH/Stock")], limit=1)
        move_history = request.env['stock.move.line'].sudo().create({
            'move_history_id_before': move_history_id,
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

        result = request.env['stock.move.line'].sudo().search(
            [('product_id', '=', idProduct)], limit=1000, order="create_date desc")
        if len(result) > 999:
            result[999].unlink()
        return move_history.id

    def _check_product_list(self, product_list):
        """Kiểm tra danh sách sản phẩm."""
        for product in product_list:
            if self.my_dict.get(product["default_code"], "None") != "None":
                return product["default_code"]
        return "None"
