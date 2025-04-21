# mikrotik_audit.py
from routeros_api import RouterOsApi

connection = RouterOsApi(
    host='192.168.1.1',
    username='admin',
    password='',
    plaintext_login=True
)

# Check for default password
users = connection.get_resource('/user')
if any(user['name'] == 'admin' for user in users.get()):
    print("[!] WARNING: Default 'admin' user exists.")

# Check for open ports
ip_services = connection.get_resource('/ip/service')
for service in ip_services.get():
    if service['disabled'] == 'false':
        print(f"[+] Service {service['name']} is enabled (port {service['port']}).")
