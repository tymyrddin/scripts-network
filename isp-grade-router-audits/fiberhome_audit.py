# fiberhome_audit.py
import requests

def check_header_injection(ip):
    headers = {"X-Forwarded-For": "127.0.0.1\r\nInjected: true"}
    r = requests.get(f"http://{ip}/index.html", headers=headers)
    if "Injected" in r.headers:
        print("[!] CRITICAL: HTTP header injection vulnerability")

check_header_injection("192.168.1.254")

