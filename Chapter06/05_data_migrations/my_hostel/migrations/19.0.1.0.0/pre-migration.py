# pre-migration.py

from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Add temporary column if not exists
    cr.execute("""
        ALTER TABLE hostel_student
        ADD COLUMN IF NOT EXISTS admission_date_old VARCHAR;
    """)

    # Copy existing data
    cr.execute("""
        UPDATE hostel_student
        SET admission_date_old = admission_date
        WHERE admission_date IS NOT NULL;
    """)