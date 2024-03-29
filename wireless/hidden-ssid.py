#!/usr/bin/python3

import os
from scapy.layers.dot11 import Dot11
from scapy.sendrecv import sniff

# Define the interface name that we will be sniffing from, you can
# change this if needed.
iface = "wlan0mon"
iwconfig_cmd = "/usr/sbin/iwconfig"


# Print ssid of probe requests, probe response
# or association request
def handle_packet(packet):
    if packet.haslayer(Dot11ProbeReq) or \
            packet.haslayer(Dot11ProbeResp) or \
            packet.haslayer(Dot11AssoReq):
        print("Found SSID " + packet.info)


# Set device into monitor mode
os.system(iwconfig_cmd + " " + iface + " mode monitor")

# Start sniffing
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)
