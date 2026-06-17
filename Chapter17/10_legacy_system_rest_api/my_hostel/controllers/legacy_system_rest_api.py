from odoo import http
from odoo.http import request, Response
import xmlrpc.client
import logging
import json

_logger = logging.getLogger(__name__)

class LegacyIntegrationController(http.Controller):

    @http.route('/api/legacy/create_data', type='http', auth='public', methods=['POST'], csrf=False)
    def create_data_from_legacy(self, **kwargs):
        """
        REST API endpoint to receive hostel data from a legacy system.
        Validates the caller using Odoo username and password before creating records.
        """
        try:
            # Extract credentials from the incoming payload
            
            raw_body = request.httprequest.data
            body     = json.loads(raw_body)        
            params   = body.get('params', {})
            db       = params.get('db')
            username = params.get('username')
            password = params.get('password')
            data     = params.get('data', {})
            credential = {'login': username, 'password': password,'type': 'password'}
            
            uid = request.session.authenticate(request.env, credential)
            user_id = uid.get("uid")
            if not uid:
                return Response(
                    json.dumps({'error': 'Authentication failed', 'status': 401}),
                    content_type='application/json',
                    status=401
                )

            hostel_obj  = request.env['hostel.room'].sudo().with_user(user_id)
            room = hostel_obj.create({
                'name':        data.get('name'),
                'room_no':     data.get('room_no'),
                'description': data.get('description'),
            })
            request.env.cr.commit()
            result = {
                'status':  200,
                'message': 'Room created successfully',
                'room_id': room.id,
                'data': {
                    'name':        room.name,
                    'room_no':     room.room_no,
                    'description': room.description,
                }
            }

            return Response(
                json.dumps(result),
                content_type='application/json',
                status=200
            )

        except json.JSONDecodeError:
            return Response(
                json.dumps({'error': 'Invalid JSON body', 'status': 400}),
                content_type='application/json',
                status=400
            )
        except Exception as e:
            return Response(
                json.dumps({'error': str(e), 'status': 500}),
                content_type='application/json',
                status=500
            )