# Intranet router audits

Note: For home users, I recommend running this monthly. Enterprises should integrate it with tools like LibreNMS for 
continuous monitoring.

## How to use these scripts

1. Install dependencies:

```
pip3 install netmiko paramiko routeros-api pysnmp sshpass requests
```

2. Replace IPs/credentials in the scripts.
3. Run weekly via cron (enterprise) or manually (home).

### Output Interpretation

`[!] WARNING`: Immediate action required.

`[+]`: Informational (review if needed).

## @Home routers

[ASUSWRT (Home) Audit (Bash + SSH)](asus_audit.sh) checks WAN access, firmware, Wi-Fi security.
Run: `chmod +x asus_audit.sh && ./asus_audit.sh`

[TP-Link (Home) Audit (Python + SNMP)](tplink_audit.py) checks for default credentials, open ports, and admin access.
Run: `python3 tplink_audit.py`

[OpenWRT (Home) Audit (Bash)](openwrt_audit.sh) checks for open ports, stale packages, firewall.
Run: `chmod +x openwrt_audit.sh && ./openwrt_audit.sh`

## Small organisation routers

[Cisco IOS Audit (Bash + Netmiko)](cisco_audit.py) checks OSPF/EIGRP auth, SSH-only access, rogue neighbors.
Run: `python3 cisco_audit.py`

[Ubiquiti EdgeRouter Audit (Python + Paramiko)](ubiquiti_audit.py) checks for default credentials, firewall rules, VPN config.
Run: `python3 ubiquiti_audit.py`

[MikroTik RouterOS Audit (Python + API)](mikrotik_audit.py) checks for default passwords, unused services, IPsec leaks.
Run: `python3 mikrotik_audit.py`
