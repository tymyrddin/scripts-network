#! /usr/bin/env python

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # DNS Resource Record
    if scapy_packet.haslayer(scapy.DNSRR):
        print(scapy_packet.show())
    packet.accept()


# Create netfilterqueue instance
queue = netfilterqueue.NetfilterQueue()
# Bind queue number 0 (queue zero in iptables)
queue.bind(0, process_packet)
# Run the queue
queue.run()
