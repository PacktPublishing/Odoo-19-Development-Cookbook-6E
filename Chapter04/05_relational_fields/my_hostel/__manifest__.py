{
    "name": "Hostel Management",  # Module title
    "version": "19.0.1.0.0",
    "summary": "Manage Hostel easily",  # Module subtitle phrase
    "description": """
Manage Hostel
==============
Efficiently manage the entire residential facility in the school
    """,  # Supports reStructuredText(RST) format (description is Deprecated)
    "category": "Tools",
    "website": "http://www.serpentcs.com",
    "depends": ["base"],
    "data": [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "views/hostel.xml",
        "views/hostel_room.xml",
        "views/hostel_amenities.xml",
        "views/hostel_student.xml",
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}
