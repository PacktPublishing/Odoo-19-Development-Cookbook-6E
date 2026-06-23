from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HostelCategory(models.Model):
    _name = "hostel.category"
    _description = "Hostel Categories"

    name = fields.Char('Category')
    parent_id = fields.Many2one(
        'hostel.category',
        string='Parent Category',
        ondelete='restrict',
        index=True)
    child_ids = fields.One2many(
        'hostel.category', 'parent_id',
        string='Child Categories')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')