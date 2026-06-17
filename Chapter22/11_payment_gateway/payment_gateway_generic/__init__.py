from . import controllers
from . import models

from odoo.addons.payment import reset_payment_provider, setup_provider


def post_init_hook(env):
    setup_provider(env, 'generic')
    for provider in env['payment.provider'].search([('code', '=', 'generic')]):
        if hasattr(provider, '_ensure_payment_method_line'):
            provider._ensure_payment_method_line()


def uninstall_hook(env):
    reset_payment_provider(env, 'generic')
