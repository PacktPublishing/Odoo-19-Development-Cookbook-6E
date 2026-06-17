from odoo import models, fields
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_razorpay import const


class PaymentProviderGeneric(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('generic', 'Generic Gateway')], ondelete={'generic': 'set default'})
    generic_api_key = fields.Char('API Key')
    generic_api_secret = fields.Char('API Secret')

    def _get_default_payment_method_codes(self):
        return ['generic']

    def _get_supported_operations(self):
        return ['online_redirect']  # This is critical

    def _get_redirect_form_view(self, is_validation=False):
        return self.env.ref('payment_gateway_generic.payment_generic_redirect_form')

    def _create_payment_request(self, tx, **kwargs):
        """Return the dict structure expected by frontend JS"""
        if self.code != 'generic':
            return super()._create_payment_request(tx, **kwargs)

        if not tx:
            raise ValidationError("Missing transaction.")

        base_url = self.get_base_url()
        return {
            'type': 'form',
            'url': f'{base_url}/payment/generic/redirect',
            'params': {
                'reference': tx.reference,
                'amount': tx.amount,
                'currency': tx.currency_id.name,
            }
        }


class PaymentTransactionGeneric(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of `payment` to return generic-specific processing values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the
                                       transaction.
        :return: The provider-specific processing values.
        :rtype: dict
        """
        if self.provider_code != 'generic':
            return super()._get_specific_processing_values(processing_values)

        if self.operation in ('online_token', 'offline'):
            return {}
        processing_values.update({
            'form_action': '/payment/generic/redirect'  # This is the controller
        })
        return processing_values

    def _extract_amount_data(self, payment_data):
        """Override of payment to extract the amount and currency from the payment data."""
        if self.provider_code != 'generic':
            return super()._extract_amount_data(payment_data)

        # Amount and currency are not sent in notification data for REDIRECT_PAYMENT_METHOD_CODES.
        if self.payment_method_id.code in const.REDIRECT_PAYMENT_METHOD_CODES:
            return
        

        return {
            'amount': payment_data.get('amount', 0),
            'currency_code': payment_data.get('currency'),
        }
