from odoo import http, modules
import pytz
import logging
import base64
import json
import math

from datetime import datetime
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class Webhoook(http.Controller):
    @http.route('/api/init/device', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def register(self, **kw):
        if kw["code"] == "parking":
            result = request.env['base.automation'].sudo().search(
                [('name', '=', kw["webhookName"])], limit=1)
            for actionServer in result.action_server_ids:
                if actionServer.webhook_url == kw['webhookUrl']:
                    idDevice = self.initDevice(kw)
                    return Response(json.dumps({"message": "Tạo thành công", "id": idDevice, }),
                                    content_type='application/json;charset=utf-8', status=201)
            branchId = request.env['setting.nsp.branch'].sudo().browse(
                kw['branchId'])
            if not branchId:
                return Response(json.dumps({"message": "Chi nhánh không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)

            parkingId = request.env['setting.nsp.parking'].sudo().browse(
                kw['parkingId'])
            if not parkingId:
                return Response(json.dumps({"message": "Bãi xe không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)

            officeId = request.env['setting.nsp.office'].sudo().browse(
                kw['officeId'])
            if not officeId:
                return Response(json.dumps({"message": "Văn phòng không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)

            webhook_field_ids = []
            if kw['name'] == "screen" or kw['name'] == "screenSecurity" or kw['name'] == "screenAlert":
                resultFields = request.env['ir.model.fields'].sudo().search(
                    [('model_id', '=', result.model_id.id), '|', ('name', '=', 'contact_id_in_out'), ('name', '=', 'picking_code')], limit=2)
                for resultField in resultFields:
                    webhook_field_ids.append((4, resultField.id))
            laneIn = True
            if kw['laneIn'] == '1':
                laneInId = request.env['setting.nsp.lane.in'].sudo().browse(
                    kw['laneId'])
                if not laneInId:
                    return Response(json.dumps({"message": "Cổng vào không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)
            else:
                laneIn = False
                laneOutId = request.env['setting.nsp.lane.out'].sudo().browse(
                    kw['laneId'])
                if not laneOutId:
                    return Response(json.dumps({"message": "Cổng ra không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)
            if laneIn:
                tempVals = {
                    "binding_model_id": False,
                    "name": "Send Webhook Nhân",
                    "state": "webhook",
                    "model_id": result.model_id.id,
                    "groups_id": [],
                    "evaluation_type": "value",
                    "update_path": False,
                    "update_field_id": False,
                    "value_field_to_show": "value",
                    "update_field_type": False,
                    "update_m2m_operation": "add",
                    "value": False,
                    "resource_ref": False,
                    "selection_value": False,
                    "update_boolean_value": "true",
                    "type": "ir.actions.server",
                    "crud_model_id": False,
                    "link_field_id": False,
                    "sms_template_id": False,
                    "sms_method": False,
                    "partner_ids": [],
                    "template_id": False,
                    "mail_post_method": False,
                    "mail_post_autofollow": False,
                    "webhook_url": kw['webhookUrl'],
                    "webhook_field_ids": webhook_field_ids,
                    "activity_type_id": False,
                    "activity_summary": False,
                    "activity_date_deadline_range": 0,
                    "activity_date_deadline_range_type": False,
                    "activity_user_type": False,
                    "activity_user_field_name": False,
                    "activity_user_id": False,
                    "activity_note": False,
                    "child_ids": [],
                    "sequence": 7,
                    "base_automation_id": result.id
                }
                result.write(
                    {'action_server_ids': [(0, 'virtual_17', tempVals)]})
                idDevice = self.initDevice(kw)
                return Response(json.dumps({
                    "message": "Tạo thành công",
                    "id": idDevice,
                }), content_type='application/json;charset=utf-8', status=201)
        return Response(json.dumps({"message": "Đăng ký dịch vụ không họp lệ!"}), content_type='application/json;charset=utf-8', status=400)

    def initDevice(self, kw):
        if kw['laneIn'] == '1':
            module = 'setting.nsp.device.in'
        else:
            module = 'setting.nsp.device.out'

        resultSetting = request.env[module].sudo().search(
            [('id', '=', kw["id"])], limit=1)
        if resultSetting:
            resultSetting.write({
                'name': kw['name'],
                'webhook_url': kw['webhookUrl'],
                'webhook_name': kw['webhookName'],
                'lane_id':kw['laneId']
            })
        else:
            resultSetting = request.env[module].sudo().create({
                'name': kw['name'],
                'webhook_url': kw['webhookUrl'],
                'webhook_name': kw['webhookName']
            })
        return resultSetting.idDevice
