# juniper_audit.py
from jnpr.junos import Device

with Device(host="isp-router") as dev:
    if dev.facts["version"].startswith("15"):
        print("[!] WARNING: Running EOL Junos 15 (no security patches)")
    bgp = dev.rpc.get_bgp_summary()
    if bgp.xpath("//bgp-peer[local-as=external-as]"):
        print("[!] CRITICAL: BGP ASN misconfiguration (potential hijack)")
