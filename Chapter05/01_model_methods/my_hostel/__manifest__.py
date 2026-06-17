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
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hostel_room.xml',
    ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}