#!/bin/bash
# zyxel_audit.sh
IP="192.168.1.1"
curl -s "http://$IP/rom-0" | grep -q "admin:password" && \
  echo "[!] WARNING: Firmware exposes default credentials in ROM"
