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
        "views/hostel.xml",
    ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}
