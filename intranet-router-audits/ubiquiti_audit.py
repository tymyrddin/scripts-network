# ubiquiti_audit.py
import paramiko

def audit_ubiquiti(ip, user, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=user, password=passwd)

    # Check default credentials
    stdin, stdout, stderr = ssh.exec_command("show configuration users")
    if "admin" in stdout.read().decode():
        print("[!] WARNING: Default 'admin' user still exists.")

    # Check firewall
    stdin, stdout, stderr = ssh.exec_command("show firewall name WAN_IN")
    if "drop" not in stdout.read().decode():
        print("[!] WARNING: WAN_IN firewall may allow unwanted traffic.")

    ssh.close()

audit_ubiquiti("192.168.1.1", "ubnt", "ubnt")