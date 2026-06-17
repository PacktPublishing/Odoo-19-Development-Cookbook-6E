from odoo import http
from odoo.http import request

class GenericPaymentController(http.Controller):

    @http.route(['/payment/generic/redirect'], type='http', auth='public', csrf=False)
    def generic_redirect(self, **post):
        reference = post.get('reference')
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)
    
        if not tx:
            return request.not_found()
    
        # Simulate successful payment
        tx._set_done()
        post.update({'reference': tx.reference,
            'amount': float(tx.amount or 0),
            'currency': tx.currency_id.name,            # not ID
            'partner_id': tx.partner_id.id,
            'transaction_id': tx.reference,             # not recordset
            'acquirer_reference': tx.reference,         # optional but helps
            'status': 'success',
            'message': 'Payment simulated'
        })
        # Trigger post-processing
        tx._process('generic', post)
        # Redirect the user to the status page.
        return request.redirect('/payment/status')


    @http.route('/payment/generic/return', type='http', auth='public', csrf=False)
    def generic_return(self, **post):
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', post.get('order_id'))])
        if tx:
            tx._handle_feedback_data(post, tx.provider_id)
        return request.redirect('/shop/confirmation')

    @http.route('/payment/generic/verify', type='jsonrpc', auth='public', csrf=False)
    def generic_verify(self, **post):
        reference = post.get('reference')
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if tx:
            tx._handle_feedback_data({'status': 'success'}, tx.acquirer_id)
        return {'status': 'ok'}

    @http.route('/payment/generic/webhook', type='jsonrpc', auth='public', csrf=False)
    def generic_webhook(self, **post):
        reference = post.get('order_id')
        status = post.get('payment_status')
        tx = request.env['payment.transaction'].sudo().search([('reference', '=', reference)])
        if tx:
            tx._handle_feedback_data({'status': status}, tx.provider_id)
        return {'status': 'received'}
