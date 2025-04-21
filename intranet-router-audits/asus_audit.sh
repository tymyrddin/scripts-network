#!/bin/bash
# asus_audit.sh
IP="192.168.1.1"
USER="admin"
PASS="yourpassword"

sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no $USER@$IP <<EOF
    # Check remote management
    nvram get http_wan && echo "[!] WARNING: WAN HTTP access enabled."

    # Check Wi-Fi encryption
    nvram get wl0_auth_mode | grep -q "psk2" || echo "[!] WARNING: Weak Wi-Fi security (use WPA2/WPA3)."

    # Check firmware
    nvram get buildno
EOF