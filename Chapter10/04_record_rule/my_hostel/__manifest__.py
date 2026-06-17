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
    "depends": ["base"],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
    ],
    # This demo data files will be loaded if db initialize with demo data (commented because file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}
