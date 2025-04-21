# Carrier-Grade Routers

Legal Considerations:

* Always obtain written permission before testing ISP equipment
* Use dedicated VLANs for audits (avoid production traffic)

## How to use these scripts

Install dependencies:

```commandline
pip install jnpr.junos
brew install ike-scan dns-sd  # macOS
sudo apt install ike-scan avahi-utils  # Linux
```

Run scripts:

```commandline
python3 huawei_audit.py
bash zyxel_audit.sh
```

## Critical findings

BGP misconfig → Contact ISP
IKE misconfig → Implement RPKI for BGP and Batfish (config audit)

## Scripts

[Juniper MX Series](juniper_audit.py) checks BGP hijacking risks, default SNMP

[Nokia/Alcatel-Lucent](nokia_audit.sh) checks IKEv1 PSK weaknesses

Cisco ASR 9000 (Carrier Core) checks: NetFlow data leakage, BGP hijack prepend