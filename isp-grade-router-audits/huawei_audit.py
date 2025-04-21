# huawei_audit.py
import requests
from bs4 import BeautifulSoup


def audit_huawei(ip="192.168.100.1"):
    try:
        # Check web interface for default creds
        session = requests.Session()
        login_url = f"http://{ip}/html/login.html"
        resp = session.post(login_url, data={"username": "admin", "password": "admin"})

        if "logout" in resp.text.lower():
            print("[!] CRITICAL: Default credentials (admin/admin) work")

        # Check TR-069 remote management
        config_url = f"http://{ip}/html/tr69config.html"
        tr69 = session.get(config_url)
        if "Enable" in tr69.text:
            print("[!] WARNING: TR-069 remote management enabled (ISP control)")

    except Exception as e:
        print(f"Error: {e}")


audit_huawei()

