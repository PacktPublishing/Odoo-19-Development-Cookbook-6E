import logging

from odoo import fields, models, api, _
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    _description = 'Base Archive'

    active = fields.Boolean(default=True)


    def do_archive(self):
        for record in self:
            record.active = not record.active

class HostelRoom(models.Model):

    _name = "hostel.room"
    _description = "Hostel Room Information"
    _rec_name = "room_no"

    @api.depends("student_per_room", "student_ids")
    def _compute_check_availability(self):
        """Method to check room availability"""
        for rec in self:
            rec.availability = rec.student_per_room - len(rec.student_ids.ids)

    name = fields.Char(string="Room Name", required=True)
    room_no = fields.Char("Room No.", required=True)
    floor_no = fields.Integer("Floor No.", default=1, help="Floor Number")
    currency_id = fields.Many2one('res.currency', string='Currency')
    rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month") # optional attribute: currency_field='currency_id' incase currency field have another name then 'currency_id'
    hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")
    student_ids = fields.One2many("hostel.student", "room_id",
        string="Students", help="Enter students")
    hostel_amenities_ids = fields.Many2many("hostel.amenities",
        "hostel_room_amenities_rel", "room_id", "amenitiy_id",
        string="Amenities", domain="[('active', '=', True)]",
        help="Select hostel room amenities")
    student_per_room = fields.Integer("Student Per Room", required=True,
        help="Students allocated per room")
    availability = fields.Float(compute="_compute_check_availability",
        store=True, string="Availability", help="Room availability in hostel")
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('closed', 'Closed')],
        'State', default="draft")

    _room_no_uniq = models.Constraint(
        'UNIQUE(room_no)',
        'Room number must be unique!',
    )

    @api.constrains("rent_amount")
    def _check_rent_amount(self):
        """Constraint on negative rent amount"""
        if self.rent_amount < 0:
            raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

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

    def log_all_room_students(self):
        hostel_student_obj = self.env['hostel.student']  # This is an empty recordset of model hostel.room.member
        all_students = hostel_student_obj.search([])
        print ("*all_members---",all_students)
        return True

    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be created in hostel.room.category model
        record = self.env['hostel.category'].create(parent_category_val)
        return True

    def update_room_no(self):
        self.ensure_one()
        self.room_no = "RM002"

    def find_room(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'Room Name'),
                     ('hostel_id.category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'Second Room Name'),
                     ('hostel_id.category_id.name', '=', 'Second Category Name')
        ]
        Rooms = self.search(domain)
        _logger.info('Room found: %s', Rooms)
        return True

    @api.model
    def rooms_with_multiple_students(self, all_rooms):
        def predicate(room):
            if len(room.student_ids) > 1:
                return True
        return all_rooms.filtered(predicate)

    # Filter recordset
    def filter_students(self):
        all_rooms = self.search([])
        filtered_rooms = self.rooms_with_multiple_students(all_rooms)
        _logger.info('Filtered Rooms: %s', filtered_rooms)

