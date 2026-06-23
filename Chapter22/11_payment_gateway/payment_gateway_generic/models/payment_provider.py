# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, fields, models

_logger = logging.getLogger(__name__)


class PaymentProviderGeneric(models.Model):
    """Extend payment.provider to add the 'generic' provider code and its
    credential fields.  Every other provider-level behaviour (state machine,
    company handling, published flag …) is inherited unchanged from the base
    payment.provider model.
    """

    _inherit = 'payment.provider'

    # ------------------------------------------------------------------
    # Selection extension – adds 'generic' as a valid provider code.
    # ondelete='set default' resets the code to the default value when
    # this module is uninstalled, preventing database integrity errors.
    # ------------------------------------------------------------------
    code = fields.Selection(
        selection_add=[('generic', 'Generic Gateway')],
        ondelete={'generic': 'set default'},
    )

    # ------------------------------------------------------------------
    # Provider-specific credential fields.
    # In a real integration replace these with the actual field names
    # required by the third-party gateway (e.g. publishable_key / secret_key
    # for Stripe, merchant_id / secret_key for Razorpay, …).
    # ------------------------------------------------------------------
    generic_api_key = fields.Char(
        string='API Key',
        help='Public/publishable key supplied by the payment gateway.',
    )
    generic_api_secret = fields.Char(
        string='API Secret',
        help='Secret key supplied by the payment gateway. Keep this private.',
    )

    # ------------------------------------------------------------------
    # Override: tell the framework which QWeb template to use when
    # rendering the redirect form for this provider.
    # _get_redirect_form_view is called by payment/controllers/portal.py
    # inside _get_specific_rendering_values; it must return an ir.ui.view
    # record.
    # ------------------------------------------------------------------
    def _get_redirect_form_view(self, is_validation=False):
        """Return the redirect form view for the Generic provider.

        :param bool is_validation: Whether the operation is a validation.
        :return: The view of the redirect form template.
        :rtype: record of `ir.ui.view`
        """
        self.ensure_one()
        if self.code != 'generic':
            return super()._get_redirect_form_view(is_validation=is_validation)
        return self.env.ref('payment_gateway_generic.payment_generic_redirect_form')

    def _get_default_payment_method_codes(self):
        """Return the default payment method codes for the Generic provider."""
        self.ensure_one()
        if self.code != 'generic':
            return super()._get_default_payment_method_codes()
        return {'card'}

    # ------------------------------------------------------------------
    # Override: return provider-level removal values when the module is
    # uninstalled.  This resets the code field so the record is not left
    # referencing a now-missing selection value.
    # ------------------------------------------------------------------
    def _get_removal_values(self):
        """Return the removal values to update the provider with when its
        module is uninstalled.
        """
        res = super()._get_removal_values()
        if self.code == 'generic':
            res.update({'code': 'none'})
        return res
