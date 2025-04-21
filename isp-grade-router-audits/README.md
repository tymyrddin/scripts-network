# ISP-Grade Routers

Legal Considerations: Always obtain written permission before testing ISP equipment, and if possible, avoid production traffic

## Relatively small routers (can also be used for intranet)

[Huawei HG8245H (ONT)](huawei_audit.py) checks TR-069 exposure, default credentials, and TLS weaknesses

Metadata:

* Device Type: Fiber ONT
* Typical Deployment: FTTH customer premises
* Protocols Audited: TR-069, HTTP
* Critical Risks: Mass CPE compromise (botnets)
* Script Purpose: Detect default creds and ISP backdoors
* Impact: Prevents ISP-wide device hijacking

Install dependencies:

```commandline
pip install requests beautifulsoup4
```

Run: `python3 huawei_audit.py`

Critical findings:

* Default credentials → Change immediately
* TR-069/UPnP exposure → Disable in admin UI

----

[Zyxel VMG1312 (Vodafone/ISP)](zyxel_audit.sh) checks PPPoE credentials, and WPS vulns

* Device Type: VDSL2 Gateway
* Typical Deployment:
    * Vodafone, Deutsche Telekom, and other EU ISPs
    * Used for DSL-to-Ethernet conversion
    * Often branded as ISP "home gateways"
* Why It Matters:
    * ROM-0 Credential Leak: Firmware exposes admin:password in memory.
    * TR-069 RCE (CVE-2020-29557): Remote code execution via CWMP.
    * PPPoE Credential Exposure: Plaintext credentials in NVRAM.

Run: `chmod +x zyxel_audit.sh && ./zyxel_audit.sh`

----

[FiberHome AN5506 (Asian ISPs)](fiberhome_audit.py) checks for HTTP header injection, ONU cloning 

Metadata:

* Device Type: Fiber Optic Network Terminal (ONT)
* Typical Deployment: FTTH (Fiber-to-the-Home) in China/SE Asia, ISP-managed CPE (Customer Premises Equipment); Often deployed by China Telecom, Singtel, AIS
* Why It Matters:
    * HTTP Header Injection (CVE-2022-36367) allows bypassing authentication.
    * ONU Cloning risks (MAC/SN spoofing for free internet).
    * TR-069 Remote Management exposes devices to ISP attacks.

Impact if Vulnerable:

* ISP-Wide Compromise: Attackers can hijack all AN5506 devices in a region.
* Free Internet: Cloned ONUs bypass ISP billing.

Install dependencies:

```commandline
pip install requests
```

Run: `python3 fiberhome_audit.py`

----

[Netgear Nighthawk (Consumer Router)](netgear_audit.py)

Metadata:

* Device Type: Consumer Wi-Fi router
* Typical Deployment: Home/SOHO networks
* Protocols Audited: HTTP, CGI
* Critical Risks: Unauthenticated remote code execution
* Script Purpose: Detect known exploits
* Impact: Full device takeover

Run: `python3 netgear_audit.py`

----

[ZTE ZXHN F670 (Gateway)](zte_audit.sh)

Metadata:

* Device Type: Fiber gateway
* Typical Deployment: Mass-market consumer installs
* Protocols Audited: TR-069, PPPoE
* Critical Risks: Credential leakage, remote code execution
* Script Purpose: Find unprotected management interfaces
* Impact: Prevents ISP account theft

Run: `chmod +x zte_audit.sh && ./zte_audit.sh`

----
