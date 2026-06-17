# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('m2m_group', 'M2m Group')])

    def _get_view_info(self):
        return {'m2m_group': {'icon': 'fa fa-id-card-o o_m2m_group_icon'}} | super()._get_view_info()
