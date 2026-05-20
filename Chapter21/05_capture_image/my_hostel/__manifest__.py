
{
    # Module information
    'name': 'My Hostel',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'LGPL-3',
    'summary': """
        Odoo19 Book
    """,

    # Author
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'https://www.serpentcs.com',

    # Dependancies
    'depends': ['base', 'quality_iot'],

    # Views
    'data': [
        "security/hostel_security.xml",
        "security/ir.model.access.csv",
        "views/hostel.xml",
        "views/hostel_room.xml",
        "views/hostel_student.xml",
    ],

    # Technical
    'installable': True,
    'auto_install': False,
}

