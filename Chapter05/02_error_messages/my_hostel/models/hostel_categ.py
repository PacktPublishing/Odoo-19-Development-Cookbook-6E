from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class HostelCategory(models.Model):
    _name = "hostel.category"
    _description = "Hostel Categories"
    # _parent_store = True
    # _parent_name = "parent_id" # optional if field is 'parent_id'

    name = fields.Char('Category')
    parent_id = fields.Many2one(
        'hostel.category',
        string='Parent Category',
        ondelete='restrict',
        index=True)
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many(
        'hostel.category', 'parent_id',
        string='Child Categories')

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if self._has_cycle():
            raise ValidationError(_('Error! You cannot create recursive categories.'))