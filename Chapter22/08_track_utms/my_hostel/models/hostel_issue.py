from odoo import models, fields


class HostelIssue(models.Model):
    _name = 'hostel.issue'
    _inherit = ['utm.mixin']

    student_id = fields.Many2one('res.partner', string="Student")
    room_id = fields.Many2one('hostel.room', string="Room")
    issue_description = fields.Text()