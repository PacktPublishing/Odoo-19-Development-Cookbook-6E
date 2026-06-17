# -*- coding: utf-8 -*-
{
    "name": "Hostel Management",  # Module title
    "summary": "Manage Hostel Easily",  # Module subtitle phrase
    "description": """
Manage Hostel
==============
Efficiently manage the entire residential facility in the school
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "version": "19.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "category": "Tools",
    "website": "https://www.serpentcs.com",
    "license": "AGPL-3",
    "depends": ["base"],
    "data": [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel.xml",
        "views/hostel_room.xml",
        "views/hostel_amenities.xml",
        "views/hostel_student.xml",
        "views/hostel_categ.xml",
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    'application': True,
    'auto_install': False,
}
