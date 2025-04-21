#!/bin/bash
# nokia_audit.sh
# Check for IKEv1 Aggressive Mode
ike-scan -A 192.168.1.1 | grep -q "Aggressive Mode" && \
  echo "[!] CRITICAL: IPsec using insecure IKEv1"

# Verify GPON credentials (requires SSH access)
ssh admin@192.168.1.1 "show running-config | include username"