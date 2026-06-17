from xmlrpc import client

server_url = 'http://localhost:1919'

common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
version_info = common.version()

print(version_info)
