#!/bin/bash
# nokia_audit.sh
ike-scan -A 192.168.1.1 | grep -q "Aggressive Mode" && \
  echo "[!] CRITICAL: IPsec using insecure IKEv1 Aggressive Mode"
