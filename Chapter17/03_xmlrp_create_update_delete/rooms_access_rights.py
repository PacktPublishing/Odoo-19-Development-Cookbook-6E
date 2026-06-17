from xmlrpc import client

server_url = 'http://localhost:1919'
db_name = 'cookbook_19'
username = 'admin'
password = 'admin'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    has_access = models.execute_kw(db_name, user_id, password,
        'hostel.room', 'check_access_rights',
        ['create'], {'raise_exception': False})
    print('Has create access on room:', has_access)
else:
    print('Wrong credentials')
