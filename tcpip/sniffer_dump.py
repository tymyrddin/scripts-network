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

And replace network card device with parameter -i.
"""

import sys
import getopt
import pcapy
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacketimport IP , TCP , UDP

# Default network card device interface
dev = "enp1s0"

# Using EthDecoder instead of ArpDecoder, because it allows users
# to specify filter with the -f parameter
decoder = EthDecoder()

# Files (defaults)
input_file = None
output_file = "sniffer.pcap"


def write_packet(hdr , data):
    print(decoder.decode(data))
    dumper.dump(hdr, data)


def read_packet(hdr, data):
    ether = decoder.decode(data)
    if ether.get_ether_type() == IP.ethertype:
        iphdr = ether.child()
        transhdr = iphdr.child()

        # Output all data of a packet by using the
        # __str__ method of Ethernet in ImpactPacket

        if iphdr.get_ip_p() == TCP.protocol:
            print(iphdr.get_ip_src() + ":" + \
                  str(transhdr.get_th_sport()) + \
                  " -> " + iphdr.get_ip_dst() + ":" + \
                  str(transhdr.get_th_dport()))
        elif iphdr.get_ip_p() == UDP.protocol:
            print(iphdr.get_ip_src() + ":" + \
                  str(transhdr.get_uh_sport()) + \
                  " -> " + iphdr.get_ip_dst() + ":" + \
                  str(transhdr.get_uh_dport()))
        else:
            print(iphdr.get_ip_src() + \
                  " -> " + iphdr.get_ip_dst() + ": " + \
                  str(transhdr))



def usage ():
    print(sys.argv[0] + """
    -i <dev>
    -r <input_file>
    -w <output_file>""")
    sys.exit(1)

# Parse parameters
try:
    cmd_opts = "i:r:w:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-w":
        output_file = opt[1]
    elif opt[0] == "-i":
        dev = opt[1]
    elif opt[0] == "-r":
        input_file = opt[1]
    else:
        usage()


if input_file == None:
    # Sniff and write packet to a pcap dump file
    pcap = pcapy.open_live(dev, 1500, 0 ,100)
    dumper = pcap.dump_open (output_file)
    pcap.loop(0, write_packet)

else:
    # Read pcap dump file and print it
    pcap = pcapy.open_offline(input_file)
    pcap.loop(0, read_packet)