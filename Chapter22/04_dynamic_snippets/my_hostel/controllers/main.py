from odoo import http
from odoo.http import request


class HostelController(http.Controller):

    @http.route('/hostels', type='http', auth="user", website=True)
    def get_hostels(self):
        hostels = request.env['hostel.hostel'].search([])
        return request.render(
            'my_hostel.hostel_list', {
                'hostels': hostels,
            })

    @http.route('/hostel/<model("hostel.hostel"):hostel>', type='http', auth="user", website=True)
    def hostel_room_detail(self, hostel):
        return request.render(
            'my_hostel.hostel_detail', {
                'hostel': hostel,
            })

    @http.route(['/hostel_hostel/search_read'], type='jsonrpc', auth='user', methods=['POST'], website=True)
    def hostel_hostel_search_read(self, fields):
        return request.env['hostel.hostel'].search_read([], fields)
