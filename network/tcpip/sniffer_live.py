#!/usr/bin/python3

"""
Extremely simple sniffer.

To run this script install impacket and pcapy. Pcapy is a
a Python extension module that enables software written in 
Python to access the routines from the pcap packet capture 
library. If not already available, you need to install 
that library first.

$ sudo apt install libpcap-dev

Then in the venv:

(venv) $ pip install impacket pcapy
"""

import sys
import getopt
import pcapy
from impacket.ImpactDecoder import EthDecoder

# Default network card device
dev = "enp1s0"

# Using EthDecoder instead of ArpDecoder, because it allows users
# to specify filter with the -f parameter
decoder = EthDecoder()

# Set a PCAP filter expression
filter = "arp"

# Print packet
def handle_packet(hdr, data):
    print(decoder.decode(data))

def usage():
    print(sys.argv[0] + " -i <dev> -f <pcap_filter>")
    sys.exit(1)

# Parse parameters
try:
    cmd_opts = "f:i:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-f":
        filter = opt[1]
    elif opt[0] == "-i":
        dev = opt[1]
    else:
        usage()


# Open device in promiscuous mode:
# open_live() opens a network interface for reading packets
pcap = pcapy.open_live(dev ,1500 ,0 ,100)

# Set pcap filter
pcap.setfilter (filter)

# Sniff: Read packets from the network card in an endless loop.
pcap.loop(0, handle_packet)
