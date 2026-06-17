# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class HostelRoom(models.Model):

    _name = 'hostel.room'
    _description = "Information about hostel Room"

    name = fields.Char(string="Hostel Name", required=True)
    room_no = fields.Char(string="Room Number", required=True)
    other_info = fields.Text("Other Information",
                             help="Enter more information")
    description = fields.Html('Description')
    room_rating = fields.Float('Hostel Average Rating', digits=(14, 4))
    member_ids = fields.Many2many('hostel.room.member', string='Members')
    previous_room_id = fields.Many2one('hostel.room', string='Previous Room')
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")
    remarks = fields.Text('Remarks')
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        user = self.env.user
        if not user.has_groups('my_hostel.group_hostel_manager'):
            vals_list.get('remarks')
            if vals_list.get('remarks'):
                raise UserError(
                    'You are not allowed to modify remarks'
                )
        return super(HostelRoom, self).create(vals_list)

    def write(self, values):
        user = self.env.user
        if not user.has_groups('my_hostel.group_hostel_manager'):
            if values.get('remarks'):
                raise UserError(
                    'You are not allowed to modify '
                    'remarks'
                )
        return super(HostelRoom, self).write(values)

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'closed'),
                   ('closed', 'draft')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _('Moving from %s to %s is not allowed') % (room.state, new_state)
                raise UserError(message)

    def make_available(self):
        self.change_state('available')

    def make_closed(self):
        self.change_state('closed')

    @api.depends('room_no', 'name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.room_no} - {record.name}" if record.name and record.room_no else ""

    @api.model
    def _search_display_name(self, operator, value):
        domain = ['|', ('name', operator, value), ('room_no', operator, value)]
        return domain

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        domain = [] if domain is None else domain.copy()
        if not(name == '' and operator == 'ilike'):
            domain += ['|', '|',
                ('name', operator, name),
                ('room_no', operator, name),
                ('member_ids.name', operator, name)
            ]
        return super().name_search(name ,domain,operator,limit)


class HostelRoomMember(models.Model):

    _name = 'hostel.room.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Room member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade' ,required=True)
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    member_code = fields.Integer()
    date_of_birth = fields.Date('Date of birth')

