{
    'name': 'Generic Payment Gateway Integration',
    "version": "19.0.1.0.0",
    "summary": "Payment Gateway",  # Module subtitle phrase
    "description": """Efficiently manage the 
    entire payment process in website
    """,
    "category": "Tools",
    "website": "http://www.serpentcs.com",
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_provider.xml',
        'views/payment_templates.xml',
        'data/payment_provider_data.xml'
    ],
    "installable": True,
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "license": "AGPL-3",
}
