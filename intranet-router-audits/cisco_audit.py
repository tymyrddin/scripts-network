# cisco_audit.py (Python3 + Netmiko)
from netmiko import ConnectHandler

device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.1',
    'username': 'admin',
    'password': 'yourpassword',
}


def audit_cisco(conn):
    # Check SSH-only access
    output = conn.send_command("show running-config | include line vty")
    if "transport input ssh" not in output:
        print("[!] WARNING: Telnet is enabled (use SSH only).")

    # Check OSPF authentication
    ospf_auth = conn.send_command("show running-config | section router ospf")
    if "authentication" not in ospf_auth.lower():
        print("[!] WARNING: OSPF authentication missing (enable MD5/SHA).")

    # Check firmware
    firmware = conn.send_command("show version | include Version")
    print(f"[+] Firmware: {firmware}")

with ConnectHandler(**device) as conn:
    audit_cisco(conn)