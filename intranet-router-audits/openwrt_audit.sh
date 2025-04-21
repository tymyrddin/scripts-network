#!/bin/bash
# openwrt_audit.sh
ssh root@192.168.1.1 <<EOF
    # Check open ports
    netstat -tuln | grep -E '0.0.0.0|:::' | grep -vE "::1|127.0.0.1"

    # Check for updates
    opkg list-upgradable

    # Check firewall defaults
    uci show firewall | grep -q "forwarding.*REJECT" || echo "[!] WARNING: Firewall may allow forwarding."
EOF