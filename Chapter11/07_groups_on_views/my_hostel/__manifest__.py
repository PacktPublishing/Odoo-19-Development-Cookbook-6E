{
    "name": "Hostel Management",  # Module title
    "version": "19.0.1.0.0",
    "summary": "Manage Hostel easily",  # Module subtitle phrase
    "description": """
Manage Hostel
==============
Efficiently manage the entire residential facility in the school
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "category": "Hostel",
    "website": "http://www.serpentcs.com",
    "depends": ["base_setup"],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/hostel_room.xml',
        'views/hostel_room_category.xml',
        'views/res_config_settings.xml',
    ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}