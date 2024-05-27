from odoo import http, modules
import pytz
import logging
import base64
import json
import math

from datetime import datetime
from odoo.http import request

_logger = logging.getLogger(__name__)


class SyncTag(http.Controller):
    @http.route('/api/sync/tag', type='json', auth='public', methods=['POST'], website=False, csrf=False)
    def register(self, **kw):
        pass
