from xmlrpc import client

server_url = 'http://localhost:8069'
db_name = 'odoo-test'
username = 'admin'
password = 'admin'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    has_access = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'has_access',
        [[]], {'operation': 'create'})  # ✅ correct args for has_access
    print('Has create access on room:', has_access)
else:
    print('Wrong credentials')
