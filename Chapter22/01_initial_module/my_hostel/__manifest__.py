# -*- coding: utf-8 -*-
{
    'name': "My Hostel",
    "version": "19.0.1.0.0",
    "summary": "Manage Hostel easily",  # Module subtitle phrase
    "description": """
Manage Hostel
==============
Efficiently manage the entire residential facility in the school
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "category": "Tools",
    "website": "http://www.serpentcs.com",
    'data': [
        # load views and templates here...
    ],
    'assets': {
        'web.assets_frontend': [
            'my_hostel/static/src/scss/hostel.scss',
            'my_hostel/static/src/js/hostel.js',
        ],
    },
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}
