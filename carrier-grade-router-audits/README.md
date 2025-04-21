# Carrier-Grade Routers

Legal Considerations: Always obtain written permission before testing Carrier Grade equipment

## Scripts

----

[Juniper MX Series](juniper_audit.py) checks BGP hijacking risks, default SNMP

Metadata:

* Device Type: Core router
* Typical Deployment: Internet backbones, IXPs
* Protocols Audited: BGP
* Critical Risks: Route leaks/hijacks
* Script Purpose: Enforce RPKI and peer validation
* Impact: Prevents global outages

Install dependencies:

```commandline
pip install jnpr.junos
```

Run: `python3 juniper_audit.py`

----

[Nokia ISAM (DSLAM)](nokia_audit.sh) checks IKEv1 PSK weaknesses

* Device Type: DSLAM/OLT
* Typical Deployment: ISP last-mile aggregation
* Protocols Audited: IPsec, GPON
* Critical Risks: Mobile backhaul interception
* Script Purpose: Detect weak VPN configurations
* Impact: Prevents subscriber data theft

Install dependencies:

```commandline
brew install ike-scan dns-sd
sudo apt install ike-scan avahi-utils
```

Run: `chmod +x nokia_audit.sh && ./nokia_audit.sh`

----

[Cisco ASR 9000 (Carrier Core)](cisco_asr_audit.sh) checks NetFlow data leakage, BGP hijack prepend

Metadata:

* Device Type: Edge router
* Typical Deployment: ISP peering points
* Protocols Audited: BGP, NetFlow
* Critical Risks: Traffic interception
* Script Purpose: Enforce traffic logging policies
* Impact: Prevents ISP espionage

Run: `chmod +x cisco_asr_audit.sh && ./cisco_asr_audit.sh`

----