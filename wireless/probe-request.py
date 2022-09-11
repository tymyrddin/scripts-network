#!/usr/bin/python3

from datetime import datetime
from scapy.layers.dot11 import Dot11
from scapy.sendrecv import sniff

# Define the interface name that we will be sniffing from, you can
# change this if needed.
iface = "wlan0mon"
iwconfig_cmd = "/usr/sbin/iwconfig"


# Print ssid and source address of probe requests
def handle_packet(packet):
    if packet.haslayer(Dot11ProbeResp):
        print(str(datetime.now()) + " " + packet[Dot11].addr2 +
              " searches for " + packet.info)


# Set device into monitor mode
os.system(iwconfig_cmd + " " + iface + " mode monitor")

# Start sniffing
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)
