# ISP-Grade Routers

Legal Considerations:

* Always obtain written permission before testing ISP equipment
* Use dedicated VLANs for audits (avoid production traffic)

## Relatively small routers (can also be used for intranet)

[Huawei HG8245H (ISP)](huawei_audit.py) checks TR-069 exposure, default credentials, and TLS weaknesses

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
Run: `bash zyxel_audit.sh`

----

[FiberHome AN5506 (Asian ISPs)](fiberhome_audit.py) checks for HTTP header injection, ONU cloning 

Install dependencies:

```commandline
pip install requests beautifulsoup4
```

Run: `python3 huawei_audit.py`