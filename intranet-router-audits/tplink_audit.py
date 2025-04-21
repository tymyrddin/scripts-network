# tplink_audit.py
from pysnmp.hlapi import *


def audit_tplink(ip):
    # Check SNMP defaults (public/private)
    for community in ['public', 'private']:  # Test common default communities
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData(community, mpModel=0),
                   UdpTransportTarget((ip, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
        )

        if not errorIndication and not errorStatus:
            print(f"[!] CRITICAL: Default SNMP community '{community}' is enabled")
            for varBind in varBinds:
                print(f"[+] System Info: {varBind.prettyPrint()}")
        else:
            print(f"[+] SNMP community '{community}' not accessible (good)")

    # Additional checks (HTTP admin interface, open ports)
    print("\n[+] Running supplemental checks:")
    try:
        import requests
        # Check if web interface uses default credentials
        login_url = f"http://{ip}/userRpm/LoginRpm.htm?Save=Save"
        response = requests.get(login_url, auth=('admin', 'admin'), timeout=3)
        if "password" not in response.text.lower():
            print("[!] WARNING: Default admin credentials may work")
    except ImportError:
        print("[-] Install 'requests' library for HTTP checks: pip install requests")
    except Exception as e:
        print(f"[-] Web interface check failed: {str(e)}")


if __name__ == "__main__":
    audit_tplink("192.168.1.1")  # Replace with your router IP

