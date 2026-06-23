# post-migration.py

from odoo import api, SUPERUSER_ID
from datetime import datetime

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    students = env['hostel.student'].search([
        ('admission_date_old', '!=', False)
    ])

    for student in students:
        date_str = student.admission_date_old
        parsed_date = False

        # Try multiple formats (important for real data)
        for fmt in ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']:
            try:
                parsed_date = datetime.strptime(date_str, fmt).date()
                break
            except Exception:
                continue

        if parsed_date:
            student.admission_date = parsed_date
        else:
            # Optional: log invalid data
            _logger = env['ir.logging']
            _logger.create({
                'name': 'Migration',
                'type': 'server',
                'level': 'WARNING',
                'message': f"Invalid date format: {date_str}",
                'path': 'migration',
                'line': '0',
                'func': 'post-migration',
            })