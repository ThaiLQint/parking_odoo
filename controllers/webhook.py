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
    @http.route('/api/webhook/register', type='json', auth='public', methods=['POST'], website=False, csrf=False)
    def register(self, **kw):
        if kw["code"] == "parking":
            result = request.env['base.automation'].sudo().search(
                [('name', '=', kw["name"])], limit=1)
            for actionServer in result.action_server_ids:
                if actionServer.webhook_url == kw['webhook_url']:
                    return {"code": 200}
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
                "webhook_url": kw['webhook_url'],
                "webhook_field_ids": [],
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
            result.write({'action_server_ids': [(0, 'virtual_17', tempVals)]})
            return Response(json.dumps({"message": "Tạo thành công"}), content_type='application/json;charset=utf-8', status=201)
        return Response(json.dumps({"message": "Đăng ký dịch vụ không họp lệ!"}), content_type='application/json;charset=utf-8', status=400)

