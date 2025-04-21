#!/bin/bash
# cisco_asr_audit.sh
# Validate NetFlow exports
ssh admin@asr-router "show running-config | include flow exporter" | grep -v "10.10.10.1" && \
  echo "[!] WARNING: NetFlow sent to unauthorized IPs"

# Check BGP route-maps
ssh admin@asr-router "show route-map BGP-FILTER" | grep -q "deny 65535" || \
  echo "[!] CRITICAL: Missing BGP route-map"
