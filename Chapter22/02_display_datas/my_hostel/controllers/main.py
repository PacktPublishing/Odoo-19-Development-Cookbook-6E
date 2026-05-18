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
