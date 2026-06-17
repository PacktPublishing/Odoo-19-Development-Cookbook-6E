from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class LegacyIntegrationController(http.Controller):

    @http.route('/api/legacy/order', type='json', auth='public', methods=['POST'], csrf=False)
    def create_order_from_legacy(self, **kwargs):
        """
        REST API endpoint to receive hostel data from a legacy system.
        """
        try:
            data = kwargs
            _logger.info("Received legacy order data: %s", data)
            hostel_room = request.env['hostel.room'].sudo().create(data)
            _logger.info("Hostel Room %s for Legacy System", hostel_room.name)
            return {'status': 'success', 'order_name': hostel_room.name}
        except Exception as e:
            _logger.exception("Error processing legacy order: %s", e)
            return {'status': 'error', 'message': str(e)}
