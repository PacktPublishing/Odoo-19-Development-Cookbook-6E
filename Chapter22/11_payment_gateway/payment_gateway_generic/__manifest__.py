# -*- coding: utf-8 -*-
{
    'name': 'Generic Payment Gateway',
    'version': '19.0.1.0.0',
    'summary': 'Custom payment gateway integration skeleton for Odoo 19',
    'description': """
Generic Payment Gateway
=======================
A clean, fully-correct skeleton for integrating a custom/third-party
payment gateway into Odoo 19. Implements the standard Odoo 19 payment
provider framework:
  - payment.provider  extension (credentials, redirect form view)
  - payment.transaction extension (_get_specific_rendering_values,
    _extract_reference, _extract_amount_data, _apply_updates)
  - HTTP controller for redirect, return, webhook, and verify routes
""",
    'category': 'Accounting/Payment Providers',
    'website': 'http://www.serpentcs.com',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'license': 'AGPL-3',
    'depends': ['account_payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_templates.xml',
        'data/payment_provider_data.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'installable': True,
}
