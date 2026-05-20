import odoorpc

db_name = 'odoo-test'
user_name = 'admin'
password = 'admin'

# Prepare the connection to the server
odoo = odoorpc.ODOO('localhost', port=8069)
odoo.login(db_name, user_name, password)  # login

rooms_info = odoo.execute('hostel.room', 'search_read',
    [['name', 'ilike', 'Standard']])
print(rooms_info)
