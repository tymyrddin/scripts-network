#! /usr/bin/env python

import netfilterqueue
import scapy.all as scapy


def process_packet(packet):
    print(packet)
    packet.accept()


# Create netfilterqueue instance
queue = netfilterqueue.NetfilterQueue()
# Bind queue number 0 (queue zero in iptables)
queue.bind(0, process_packet)
# Run the queue
queue.run()
