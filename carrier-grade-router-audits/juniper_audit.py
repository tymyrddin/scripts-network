# juniper_audit.py
from jnpr.junos import Device


def audit_juniper(host, user, passwd):
    with Device(host=host, user=user, password=passwd) as dev:
        # Check EOL firmware
        if dev.facts["version"].startswith("15"):
            print("[!] WARNING: Running EOL Junos 15 (no patches)")

        # Validate BGP peerings
        bgp = dev.rpc.get_bgp_summary()
        if bgp.xpath("//bgp-peer[local-as=external-as]"):
            print("[!] CRITICAL: BGP ASN misconfiguration")


audit_juniper("10.0.0.1", "admin", "password")

