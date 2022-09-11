#!/usr/bin/python3

import os
from scapy.layers.dot11 import Dot11
from scapy.sendrecv import sniff

# Define the interface name that we will be sniffing from, you can
# change this if needed.
iface = "wlan0mon"
iwconfig_cmd = "/usr/sbin/iwconfig"

os.system(iwconfig_cmd + " " + iface + " mode monitor")


# Dump packets that are not beacons, probe request / responses
def dump_packet(pkt):
    if not pkt.haslayer(Dot11Beacon) and \
       not pkt.haslayer(Dot11ProbeReq) and \
       not pkt.haslayer(Dot11ProbeResp):
        print(pkt.summary())

        if pkt.haslayer(Raw):
            print(hexdump(pkt.load))
        print("\n")


while True:
    for channel in range(1, 14):
        os.system(iwconfig_cmd + " " + iface +
                  " channel " + str(channel))
        print("Sniffing on channel " + str(channel))

        sniff(iface=iface,
              prn=dump_packet,
              count=10,
              timeout=3,
              store=0)
