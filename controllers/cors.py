from odoo import http
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class CORS(http.Controller):
    @http.route(['/web/session/authenticate', '/api/*'], type='http', auth="none", methods=['OPTIONS'])
    def cors_handler(self):
        _logger.info("hello")
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true',
        }
        return request.make_response('', headers=headers)