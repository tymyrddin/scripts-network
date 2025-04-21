#!/bin/bash
# zte_audit.sh
IP="192.168.1.1"

# Check for TR-069 RCE (CVE-2020-29557)
curl -s "http://$IP/getpage.gch?pid=101&nextpage=manager_dev_config_t.gch" | grep -q "enable" && \
  echo "[!] CRITICAL: TR-069 config page exposed"

# Extract PPPoE credentials
strings /dev/mtdblock5 | grep -E 'ppp.*@|password' | head -n 5
