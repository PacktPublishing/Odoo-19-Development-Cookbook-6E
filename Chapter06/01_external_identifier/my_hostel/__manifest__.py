# -*- coding: utf-8 -*-
{
    'name': "My Hostel",  # Module title
    "version": "19.0.1.0.0",
    'summary': "Manage Hostel easily",  # Module subtitle phrase
    'description': """
Manage Library
==============
Description related to Hostel.
    """,  # Supports reStructuredText(RST) format
    "category": "Tools",
    "website": "http://www.serpentcs.com",
    "depends": ['base'],
    'data': [
        'data/data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hostel_room.xml',
        'views/hostel_room_category_view.xml',
        'views/hostel_room_member_view.xml'
    ],
    'installable': True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",

}
