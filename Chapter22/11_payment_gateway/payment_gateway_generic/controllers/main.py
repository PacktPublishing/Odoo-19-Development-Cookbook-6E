# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class GenericPaymentController(http.Controller):
    """HTTP controller for the Generic payment gateway.

    Defines four routes that cover the complete redirect-based payment lifecycle:

    /payment/generic/redirect  – The user is POST-redirected here from the
                                  Odoo checkout page.  In a real integration
                                  you would forward the user on to the actual
                                  gateway URL.  Here we simulate payment inline.

    /payment/generic/return    – The gateway redirects the user back here after
                                  the payment attempt.  We hand the POST data to
                                  _process() and then send the user to the
                                  standard Odoo payment status page.

    /payment/generic/webhook   – Asynchronous server-to-server notification.
                                  The gateway calls this endpoint independently
                                  of the user browser redirect, so it should
                                  work even if the user closes the tab.

    /payment/generic/verify    – Optional JSON-RPC endpoint for frontend-
                                  initiated server-side verification.
    """

    # ------------------------------------------------------------------
    # 1.  Redirect endpoint  (user leaves Odoo → gateway)
    # ------------------------------------------------------------------

    @http.route(
        '/payment/generic/redirect',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False,
    )
    def generic_redirect(self, **post):
        """Receive the payment form submission and redirect the user to the
        external gateway.

        In production, replace the simulated response below with:
          1. An API call to your gateway to create a payment order/session.
          2. A redirect to the gateway-supplied checkout URL.
        """
        _logger.info(
            "Generic Gateway: redirect route called with data:\n%s",
            pprint.pformat(post),
        )

        # ---------------------------------------------------------------
        # Simulate a successful payment locally (remove in production).
        # Build the payment_data dict the same way the real gateway
        # would POST it to /payment/generic/return.
        # ---------------------------------------------------------------
        payment_data = {
            'reference': post.get('reference'),
            'transaction_id': post.get('reference'),   # gateway's own ID
            'status': 'success',
            'message': 'Payment simulated successfully',
        }

        # Hand off to the return route logic (keeps the state machine in
        # one place and avoids duplication).
        try:
            request.env['payment.transaction'].sudo()._process('generic', payment_data)
        except ValidationError as e:
            _logger.exception("Generic Gateway: validation error in redirect: %s", e)

        return request.redirect('/payment/status')

    # ------------------------------------------------------------------
    # 2.  Return / callback endpoint  (gateway → user browser)
    # ------------------------------------------------------------------

    @http.route(
        '/payment/generic/return',
        type='http',
        auth='public',
        methods=['GET', 'POST'],
        csrf=False,
        save_session=False,
    )
    def generic_return(self, **post):
        """Handle the browser redirect back from the gateway after the user
        completes (or abandons) payment.

        The gateway is expected to supply at least 'reference' and 'status'
        in the query-string or POST body.  Adjust the field names to match
        your gateway's actual callback parameters.
        """
        _logger.info(
            "Generic Gateway: return route called with data:\n%s",
            pprint.pformat(post),
        )

        try:
            request.env['payment.transaction'].sudo()._process('generic', post)
        except ValidationError as e:
            _logger.exception("Generic Gateway: validation error in return: %s", e)

        return request.redirect('/payment/status')

    # ------------------------------------------------------------------
    # 3.  Webhook / IPN endpoint  (gateway → server, no browser)
    # ------------------------------------------------------------------

    @http.route(
        '/payment/generic/webhook',
        type='http',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False,
    )
    def generic_webhook(self, **post):
        """Receive asynchronous payment notifications from the gateway.

        This endpoint is called server-to-server and must return a 200 OK
        quickly.  In production you should:
          1. Verify the webhook signature using your gateway's HMAC/shared
             secret before trusting the data.
          2. Call _process() to update the transaction.
        """
        _logger.info(
            "Generic Gateway: webhook received:\n%s",
            pprint.pformat(post),
        )

        # TODO (production): verify HMAC signature here before proceeding.
        # Example:
        #   signature = request.httprequest.headers.get('X-Generic-Signature')
        #   provider = request.env['payment.provider'].sudo().search(
        #       [('code', '=', 'generic'), ('state', '!=', 'disabled')], limit=1)
        #   if not _verify_signature(post, signature, provider.generic_api_secret):
        #       return request.make_response('Forbidden', status=403)

        try:
            request.env['payment.transaction'].sudo()._process('generic', post)
        except ValidationError as e:
            _logger.exception("Generic Gateway: validation error in webhook: %s", e)
            # Return 200 even on validation error so the gateway does not
            # keep retrying a permanently-invalid payload.
        return request.make_response('OK', headers=[('Content-Type', 'text/plain')])

    # ------------------------------------------------------------------
    # 4.  Server-side verify endpoint  (optional, JSON-RPC)
    # ------------------------------------------------------------------

    @http.route(
        '/payment/generic/verify',
        type='jsonrpc',
        auth='public',
        methods=['POST'],
        csrf=False,
        save_session=False,
    )
    def generic_verify(self, reference=None, **kwargs):
        """Optional JSON-RPC endpoint for the frontend to trigger a
        server-side verification call against the gateway's API.

        The frontend should call this after receiving a payment token from
        the gateway's JavaScript SDK.  This endpoint then makes a server-side
        API call to confirm the payment is genuine before marking it done.

        :param str reference: The Odoo transaction reference.
        :return: dict with 'success' True/False and optional 'message'.
        :rtype: dict
        """
        _logger.info("Generic Gateway: verify called for reference %s", reference)

        if not reference:
            return {'success': False, 'message': 'Missing reference'}

        tx_sudo = request.env['payment.transaction'].sudo().search(
            [('reference', '=', reference), ('provider_code', '=', 'generic')],
            limit=1,
        )
        if not tx_sudo:
            return {'success': False, 'message': f'Transaction not found: {reference}'}

        # TODO (production): make a real API call to your gateway here to
        # confirm the payment amount and status.  Example:
        #   gateway_response = _call_gateway_verify_api(
        #       tx_sudo.provider_reference,
        #       tx_sudo.provider_id.generic_api_secret,
        #   )
        #   status = gateway_response.get('status')

        # Simulated: treat every verify call as confirmed.
        payment_data = {
            'reference': reference,
            'transaction_id': reference,
            'status': 'success',
            'message': 'Verified via server-side check',
        }

        try:
            tx_sudo._process('generic', payment_data)
        except ValidationError as e:
            return {'success': False, 'message': str(e)}

        return {'success': True}
