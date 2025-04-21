# fiberhome_audit.py
import requests


def audit_fiberhome(ip="192.168.1.254"):
    try:
        # Test HTTP header injection
        headers = {"X-Forwarded-For": "127.0.0.1\r\nInjected: true"}
        r = requests.get(f"http://{ip}/index.html", headers=headers)
        if "Injected" in r.headers:
            print("[!] CRITICAL: HTTP header injection vulnerable")

        # Check default creds
        login_url = f"http://{ip}/login.cgi"
        resp = requests.post(login_url, data={"username": "admin", "password": "admin"})
        if "logout" in resp.text.lower():
            print("[!] WARNING: Default credentials (admin/admin) active")
    except Exception as e:
        print(f"Error: {e}")


audit_fiberhome()
