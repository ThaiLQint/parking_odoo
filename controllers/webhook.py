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

    @http.route('/api/update/state/device', type='http', auth='user', methods=['POST'], website=False, csrf=False)
    def update_state_webhook_device(self, **kw):
        if kw['code'] != "parking":
            return Response(json.dumps({"message": "Dịch vụ không hỗ trợ!"}), content_type='application/json;charset=utf-8', status=400)
        actionServerDevice = request.env['setting.nsp.device'].sudo().search(
            [('id_device', '=', kw['idDevice'])])
        if not actionServerDevice:
            return Response(json.dumps({"message": "Thiết bị không tìm thấy"}), content_type='application/json;charset=utf-8', status=400)
        boolean = actionServerDevice.write(
            {"isConnected": True if kw['isConnected'] == "1" else False,
             "isConnected2": not actionServerDevice.isConnected2}
        )
        return Response(json.dumps({"message": "Success"}), content_type='application/json;charset=utf-8', status=200)

    @http.route('/api/remove/webhook/device', type='http', auth='user', methods=['POST'], website=False, csrf=False)
    def remove_webhook_device(self, **kw):
        if kw['code'] != "parking":
            return Response(json.dumps({"message": "Dịch vụ không hỗ trợ!"}), content_type='application/json;charset=utf-8', status=400)
        actionServerDevice = request.env['ir.actions.server'].sudo().search(
            [('id_device', '=', kw['idDevice'])])
        if not actionServerDevice:
            return Response(json.dumps({"message": "Thiết bị không tìm thấy"}), content_type='application/json;charset=utf-8', status=400)
        for action in actionServerDevice:
            action.unlink()
        return Response(json.dumps({"message": "Success"}), content_type='application/json;charset=utf-8', status=200)

    @http.route('/api/load/nsp/config/view', type='json', auth='user', methods=['POST'], website=False, csrf=False)
    def load_config_view(self, **kw):
        if kw.get("code") != "parking":
            return {"message": "Dịch vụ không hỗ trợ!"}
        branches = request.env['setting.nsp.branch'].sudo().search([])
        if not branches:
            return {"message": "Chi nhánh không tìm thấy"}
        branch_data = [self._prepare_branch_data(
            branch) for branch in branches]
        return {"message": "Success", "records": branch_data}

    @ http.route('/api/load/nsp/config', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def load_config(self, **kw):
        if kw.get("code") != "parking":
            return Response(json.dumps({"message": "Dịch vụ không hỗ trợ!"}), content_type='application/json;charset=utf-8', status=400)
        device = request.env['setting.nsp.device'].sudo().search([
            ("id_device", "=", kw['idDevice'])
        ], limit=1)

        if not device:
            return Response(json.dumps({"message": "Thiết bị không tìm thấy!"}), content_type='application/json;charset=utf-8', status=400)
        lane = device.lane_id
        office = lane.office_id_in if lane and lane.laneInOut == "in" else (
            lane.office_id_out if lane else device.office_id)
        parking = office.parking_id
        branch = parking.branch_id

        config = self.build_config(branch, parking, office, lane, device)
        return Response(json.dumps(config), content_type='application/json;charset=utf-8', status=200)

    def build_config(self, branch, parking, office, lane=None, device=None):
        config = {
            "id": branch.id,
            "name": branch.name,
            "parking": {
                "id": parking.id,
                "name": parking.name,
                "office": {
                    "id": office.id,
                    "name": office.name
                }
            }
        }

        if lane:
            config["parking"]["office"]["lane"] = {
                "id": lane.id,
                "name": lane.name,
                "laneInOut": lane.laneInOut,
                "device": {
                    "id": device.id_device,
                    "name": device.name
                }
            }
        else:
            config["parking"]["office"].update({
                "device": {
                    "id": device.id_device,
                    "name": device.name
                },
                "listLaneIn": self._prepare_lane_data(office.lane_in_ids),
                "listLaneOut": self._prepare_lane_data(office.lane_out_ids)
            })

        return config

    def _prepare_branch_data(self, branch):
        parking_data = [self._prepare_parking_data(
            parking) for parking in branch.parking_ids]
        return {
            "id": branch.id,
            "name": branch.name,
            "listParking": parking_data
        }

    def _prepare_parking_data(self, parking):
        office_data = [self._prepare_office_data(
            office) for office in parking.office_ids]
        return {
            "id": parking.id,
            "name": parking.name,
            "listOffice": office_data
        }

    def _prepare_office_data(self, office):
        lane_in_data = [{"id": lane_in.id, "name": lane_in.name, "listDevice": self._prepare_device_data(lane_in)}
                        for lane_in in office.lane_in_ids]
        lane_out_data = [{"id": lane_out.id, "name": lane_out.name, "listDevice": self._prepare_device_data(lane_out)}
                         for lane_out in office.lane_out_ids]
        return {
            "id": office.id,
            "name": office.name,
            "listLaneIn": lane_in_data,
            "listLaneOut": lane_out_data
        }

    def _prepare_device_data(self, lane):
        device_data = [{"id": device.id, "name": device.name}
                       for device in lane.device_ids]
        return device_data

    def _prepare_lane_data(self, lanes):
        return [{"id": lane.id, "name": lane.name, "listDevice": self._prepare_device_data(lane)}
                for lane in lanes]

    @http.route('/api/register/device', type='http', auth='public', methods=['POST'], website=False, csrf=False)
    def register_device(self, **kw):
        if kw.get("code") != "parking":
            return self.create_response("Dịch vụ không họp lệ!", 400)

        result = self.find_automation(kw["webhookName"])
        if not result:
            return self.create_response("Không tìm thấy webhook", 400)

        for action_server in result.action_server_ids:
            if action_server.id_device == kw["idDevice"]:
                return self.update_existing_device(action_server, kw['webhookUrl'])

        return self.create_new_device(result, kw)

    def find_automation(self, webhook_name):
        return request.env['base.automation'].sudo().search([('name', '=', webhook_name)], limit=1)

    def update_existing_device(self, action_server, webhook_url):
        if action_server.webhook_url != webhook_url:
            action_server.write({"webhook_url": webhook_url})
        return self.create_response("Tạo thành công", 201)

    def create_new_device(self, result, kw):
        webhook_field_ids = self.get_webhook_field_ids(result, kw)
        new_device_vals = self.create_device_vals(
            kw, result, webhook_field_ids)
        result.write(
            {'action_server_ids': [(0, 'virtual_17', new_device_vals)]})
        return self.create_response("Tạo thành công", 201)

    def get_webhook_field_ids(self, result, kw):
        webhook_field_ids = []
        device_type = kw.get('deviceType')
        webhook_name = kw.get('webhookName')

        if not device_type or not webhook_name:
            return webhook_field_ids

        if device_type in ["screenIn", "screenOut", "screenSecurity"] and webhook_name not in ["alertOut", "alertIn"]:
            domain, limit = self.get_screen_domain_and_limit(result, device_type, webhook_name)
        elif webhook_name == "notifyDeviceStatus" and device_type == "reader":
            domain = [
                ('model_id', '=', result.model_id.id),
                '|', ('name', '=', 'isConnected'), ('name', '=', 'id_device')
            ]
            limit = 2
        elif webhook_name in ["alertIn", "alertOut"]:
            domain = [
                ('model_id', '=', result.model_id.id),
                '|', ('name', '=', 'product_id'), ('name', '=', 'code')
            ]
            limit = 2
        else:
            return webhook_field_ids

        try:
            fields = request.env['ir.model.fields'].sudo().search(domain, limit=limit)
            webhook_field_ids = [(4, field.id) for field in fields]
        except Exception as e:
            _logger.error(f"Error while searching fields: {e}")
            _logger.error(f"Domain: {domain}, Limit: {limit}")

        return webhook_field_ids

    def get_screen_domain_and_limit(self, result, device_type, webhook_name):
        model_condition = ('model_id', '=', result.model_id.id)
        common_fields = ['contact_id', 'product_id', 'picking_code', 'create_date']

        base_domain = [model_condition]

        if device_type in ["screenSecurity", "screenOut"]:
            domain = base_domain + [
                '|', ('name', 'in', common_fields),
                '|', ('name', '=', 'image_1920_camera_truoc'),
                    ('name', '=', 'image_1920_camera_sau')
            ]
            limit = 6
        elif device_type == "screenIn":
            domain = base_domain + [
                '|', ('name', '=', 'picking_code'),
                '|', ('name', '=', 'contact_id'),
                    ('name', '=', 'product_id')
            ]
            limit = 3
        else:
            domain = base_domain
            limit = 0

        return domain, limit

    def create_device_vals(self, kw, result, webhook_field_ids):
        return {
            "binding_model_id": False,
            "name": kw['name'],
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
            "base_automation_id": result.id,
            "id_device": kw["idDevice"]
        }

    def create_response(self, message, status):
        return Response(
            json.dumps({"message": message}),
            content_type='application/json;charset=utf-8',
            status=status
        )
