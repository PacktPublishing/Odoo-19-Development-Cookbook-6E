# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from werkzeug import urls

from odoo import _, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransactionGeneric(models.Model):
    """Extend payment.transaction with provider-specific hooks that the
    Odoo 19 payment framework requires for a redirect-based integration:

    1. _get_specific_rendering_values – build the dict that is rendered into
       the redirect form HTML template.
    2. _extract_reference – extract the Odoo transaction reference from the
       payment data that the gateway sends back.
    3. _extract_amount_data – extract amount/currency for framework validation.
    4. _apply_updates – update the transaction state from the gateway data.

    None of these methods should be called directly by application code; they
    are called internally by the framework through _get_processing_values()
    and _process().
    """

    _inherit = 'payment.transaction'

    # ======================================================================
    # 1.  Rendering values  (called during the checkout redirect)
    # ======================================================================

    def _get_specific_rendering_values(self, processing_values):
        """Override to return the values needed to render the redirect form
        template defined in views/payment_templates.xml.

        The dict returned here is merged with the generic processing values
        already computed by the framework and passed verbatim as template
        variables when Odoo renders the QWeb form.

        :param dict processing_values: Generic processing values already
            computed by :meth:`payment.transaction._get_processing_values`.
        :return: A dict of provider-specific values to render the redirect form.
        :rtype: dict
        """
        self.ensure_one()

        # Let the base implementation handle every other provider.
        if self.provider_code != 'generic':
            return super()._get_specific_rendering_values(processing_values)

        # Build the absolute URL the gateway should POST back to.
        base_url = self.provider_id.get_base_url()
        return_url = urls.url_join(base_url, '/payment/generic/return')

        # These values become QWeb template variables in
        # payment_generic_redirect_form (see views/payment_templates.xml).
        return {
            'form_action': urls.url_join(base_url, '/payment/generic/redirect'),
            'reference': self.reference,
            'amount': self.amount,
            'currency_code': self.currency_id.name,
            'partner_id': self.partner_id.id,
            'return_url': return_url,
        }

    # ======================================================================
    # 2.  Extract transaction lookup and amount validation data
    # ======================================================================

    def _extract_reference(self, provider_code, payment_data):
        """Override to extract the transaction reference from payment data.

        Odoo 19 calls this method from :meth:`payment.transaction._process` when
        the controller invokes the method on an empty transaction recordset.
        """
        if provider_code != 'generic':
            return super()._extract_reference(provider_code, payment_data)

        reference = payment_data.get('reference')
        if not reference:
            raise ValidationError(
                "Generic Gateway: "
                + _("No reference found in the payment data.")
            )
        return reference

    def _extract_amount_data(self, payment_data):
        """Override to provide amount data for Odoo's standard validation."""
        if self.provider_code != 'generic':
            return super()._extract_amount_data(payment_data)

        amount = payment_data.get('amount')
        currency_code = payment_data.get('currency') or payment_data.get('currency_code')
        if amount is None or not currency_code:
            return None

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValidationError(
                "Generic Gateway: "
                + _("Invalid payment amount received: %s", amount)
            )

        return {
            'amount': amount,
            'currency_code': currency_code,
        }

    # ======================================================================
    # 3.  Process the payment data and update the transaction state
    # ======================================================================

    def _apply_updates(self, payment_data):
        """Override to update the transaction state based on gateway data.

        This method is called by :meth:`payment.transaction._process` after the
        transaction has been located and the amount/currency have been
        validated. It must not be called directly by application code.

        :param dict payment_data: The payment data sent by the provider.
        :return: None
        """
        self.ensure_one()

        # Delegate to the base class for every other provider.
        if self.provider_code != 'generic':
            return super()._apply_updates(payment_data)

        # -----------------------------------------------------------------
        # Store the provider's own transaction reference (if supplied).
        # 'provider_reference' is the Odoo field for the gateway-side ID.
        # -----------------------------------------------------------------
        provider_reference = payment_data.get('transaction_id') or self.reference
        self.provider_reference = provider_reference

        # -----------------------------------------------------------------
        # Map gateway status codes to Odoo transaction states.
        #
        # Replace this mapping with the actual status values your gateway
        # sends (e.g. 'CAPTURED', 'FAILED', 'PENDING', …).
        # -----------------------------------------------------------------
        status = payment_data.get('status', '').lower()
        state_message = payment_data.get('message') or None

        if status == 'success':
            self._set_done(state_message=state_message)
        elif status == 'pending':
            self._set_pending(state_message=state_message)
        elif status in ('cancelled', 'cancel'):
            self._set_canceled(state_message=state_message)
        else:
            _logger.warning(
                "Generic Gateway: unknown payment status '%s' for transaction %s",
                status,
                self.reference,
            )
            self._set_error(
                "Generic Gateway: "
                + _("Received an unrecognised payment status: %s", status)
            )

    def _create_payment(self, **extra_create_values):
        """Override to ensure the Generic provider has an accounting method line."""
        self.ensure_one()
        if self.provider_code != 'generic':
            return super()._create_payment(**extra_create_values)

        provider = self.provider_id
        if hasattr(provider, '_setup_payment_method'):
            provider._setup_payment_method('generic')
        if not provider.journal_id:
            provider.journal_id = self.env['account.journal'].search([
                ('company_id', '=', provider.company_id.id),
                ('type', '=', 'bank'),
            ], limit=1)
        if hasattr(provider, '_ensure_payment_method_line'):
            provider._ensure_payment_method_line()

        if not provider.journal_id:
            raise ValidationError(
                "Generic Gateway: "
                + _("Please configure a bank journal on the payment provider.")
            )

        payment_method_line = provider.journal_id.inbound_payment_method_line_ids.filtered(
            lambda line: line.payment_provider_id == provider
        )[:1]
        if not payment_method_line:
            raise ValidationError(
                "Generic Gateway: "
                + _("No payment method line is configured on the provider payment journal.")
            )

        return super()._create_payment(
            payment_method_line_id=payment_method_line.id,
            **extra_create_values
        )
