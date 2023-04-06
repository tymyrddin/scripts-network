#!/usr/bin/python3

from scapy.all import Ether, Dot1Q, IP, ICMP

packet = Ether(dst="MAC address") / \
         Dot1Q(vlan=1) / \
         Dot1Q(vlan=2) / \
         IP(dst="IP address") / \
         ICMP()

sendp(packet)
